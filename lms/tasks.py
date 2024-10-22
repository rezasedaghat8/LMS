from celery import shared_task
from django.core.mail import send_mail
from .models import BorrowingTransaction

@shared_task
def send_due_date_reminder():
    transactions = BorrowingTransaction.objects.filter(return_date__isnull=True)
    for transaction in transactions:
        send_mail(
            'Reminder: Return your book',
            f"Dear {transaction.borrower.user.username}, please remember to return the book '{transaction.book.title}' on time.",
            'library@library.com',
            [transaction.borrower.user.email],
            fail_silently=False,
        )
        