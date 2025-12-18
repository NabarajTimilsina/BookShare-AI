from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    path('upload/', views.upload_book, name='upload_book'),
    path('search/', views.search_books, name='search_books'),

    # NEW (for live recommendations)
    path('ajax/search/', views.ajax_search, name='ajax_search'),
]
