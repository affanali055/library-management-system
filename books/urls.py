# pyrefly: ignore [missing-import]
from django.urls import path
from .views import BookListAPIView, add_book, book_list, edit_book, register, login_view, delete_book,borrow_book,return_book 


urlpatterns = [
    path("", book_list, name="book-list"),
    path("api/", BookListAPIView.as_view(), name="book-list-api"),
    path("add/", add_book, name="add-book"),
    path("edit/<int:id>/", edit_book, name="edit-book"),
    path("register/", register, name="register"),
    path("login/", login_view, name="login"),
    path("delete/<int:id>/", delete_book, name="delete-book"),
    path("borrow/<int:id>/", borrow_book, name="borrow-book"),
    path("return/<int:id>/", return_book, name="return-book"), 

] 