from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from books.models import Book
from .serializers import BookSerializer
from utils.summariser import get_book_summary

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

@api_view(['GET'])
def book_summary_api(request, pk):
    book = get_object_or_404(Book, pk=pk)
    
    if book.summary:
        summary = book.summary
    else:
        summary = get_book_summary(book.description) if book.description else "No description available"
    
    return Response({
        'book_id': book.id,
        'title': book.title,
        'summary': summary
    })