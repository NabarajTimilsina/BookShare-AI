from rest_framework import serializers
from books.models import Book, Review

class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'username', 'rating', 'comment', 'created_at']

class BookSerializer(serializers.ModelSerializer):
    uploaded_by = serializers.CharField(source='uploaded_by.username', read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    
    class Meta:
        model = Book
        fields = [
            'id', 'title', 'author', 'description', 
            'uploaded_by', 'upload_date', 'summary', 'reviews'
        ]