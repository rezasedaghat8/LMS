from django.shortcuts import render
from rest_framework import viewsets, filters, status
from .models import *
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from django.db.models import Count
from rest_framework.decorators import action


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class BorrowerViewSet(viewsets.ModelViewSet):
    queryset = Borrower.objects.all()
    serializer_class = BorrowerSerializer


class BorrowingTransactionViewSet(viewsets.ModelViewSet):
    queryset = BorrowingTransaction.objects.all()
    serializer_class = BorrowingTransactionSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['title', 'author__name', 'category']
    filterset_fields = ['category', 'available']  

    @action(detail=False)
    def most_borrowed(self, request):
        books = Book.objects.annotate(num_borrows=Count('borrowingtransaction')).order_by('-num_borrows')[:10]
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)


class BorrowingTransactionViewSet(viewsets.ModelViewSet):
    queryset = BorrowingTransaction.objects.all()
    serializer_class = BorrowingTransactionSerializer

    def create(self, request, *args, **kwargs):
        borrower = request.user.borrower 
        if borrower.borrowed_books.count() >= 3: 
            return Response({"error": "You cannot borrow more than 3 books at once."}, status=status.HTTP_400_BAD_REQUEST)
        
        book_id = request.data.get('book')
        book = Book.objects.get(id=book_id)
        if not book.available:  
            return Response({"error": "This book is already reserved by another user."}, status=status.HTTP_400_BAD_REQUEST)
        
        return super().create(request, *args, **kwargs)
    
    
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    
    
