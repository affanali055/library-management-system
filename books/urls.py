# books/urls.py
from django.urls import path

from .views import BookListAPIView, add_book, book_list,edit_book,register 

urlpatterns = [
    path("", book_list, name="book-list"),
    path("api/", BookListAPIView.as_view(), name="book-list-api"),
    path("add/", add_book, name="add-book"),
    path("edit/<int:id>/", edit_book, name="edit-book"),
    path("register/", register, name="register"),
    path("login/", login_view, name="login"),

]
