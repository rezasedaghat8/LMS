from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)
    biography = models.TextField()
    nationality = models.CharField(max_length=50)
    birth_date = models.DateField()
    
    books = models.ManyToManyField('Book', related_name='authors')
    
    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    isbn = models.CharField(max_length=13, unique=True)
    category = models.CharField(max_length=100)
    publication_date = models.DateField()
    available = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Borrower(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    borrowed_books = models.ManyToManyField(Book, through='BorrowingTransaction')
        
    def __str__(self):
        return self.username
    
    
class BorrowingTransaction(models.Model):
    borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)    
    
    
class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(Borrower, on_delete=models.CASCADE)
    rating = models.IntegerField()
    review_text = models.TextField()
    
    class Meta:
        unique_together = ['book', 'user'] 

    def __str__(self):
        return f"Review by {self.user.username} for {self.book.title}"

    