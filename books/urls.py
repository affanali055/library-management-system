from django.urls import path
from django.shortcuts import redirect
from .views import (
    BookListAPIView, add_book, book_list, edit_book, register, 
    login_view, delete_book, borrow_book, return_book,
    dashboard_view, users_list, settings_view, logout_view
)

urlpatterns = [
    # Redirect base index route to dashboard
    path("", lambda request: redirect('dashboard') if request.user.is_authenticated else redirect('login'), name="index"),
    path("dashboard/", dashboard_view, name="dashboard"),
    path("books/", book_list, name="book-list"),
    path("users/", users_list, name="users"),
    path("settings/", settings_view, name="settings"),
    path("logout/", logout_view, name="logout"),
    
    # API and other pages
    path("api/", BookListAPIView.as_view(), name="book-list-api"),
    path("add/", add_book, name="add-book"),
    path("edit/<int:id>/", edit_book, name="edit-book"),
    path("register/", register, name="register"),
    path("login/", login_view, name="login"),
    path("delete/<int:id>/", delete_book, name="delete-book"),
    path("borrow/<int:id>/", borrow_book, name="borrow-book"),
    path("return/<int:id>/", return_book, name="return-book"), 
]
