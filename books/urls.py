# books/urls.py
from django.urls import path
from .views import BookListAPIView, add_book

urlpatterns = [
    path("", BookListAPIView.as_view(), name="book-list"),
    path("add/", add_book, name="add-book"),
]
