from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from .models import Book
from .serializers import BookSerializer
from .forms import BookForm, UserRegisterForm,LoginForm


class BookListAPIView(APIView):
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)


def book_list(request):
    books = Book.objects.all()
    return render(request, "books/book_list.html", {"books": books})


def add_book(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Book added successfully!")
            return redirect("book-list")
    else:
        form = BookForm()

    return render(request, "books/add_book.html", {"form": form})


def edit_book(request, id):
    book = Book.objects.get(id=id)

    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, "Book updated successfully!")
            return redirect("book-list")
    else:
        form = BookForm(instance=book)

    return render(request, "books/edit_book.html", {"form": form, "book": book})


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            full_name = form.cleaned_data["full_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            name_parts = full_name.split(" ", 1)
            first_name = name_parts[0]
            last_name = name_parts[1] if len(name_parts) > 1 else ""

            User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )

            messages.success(request, "Registration successful!")
            return redirect("book-list")

    else:
        form = UserRegisterForm()

    return render(request, "books/register.html", {"form": form})
def login_view(request):
    error_message = None
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            # Authenticate the user
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('book-list')
            else:
                error_message = "Invalid username or password."
    else:
        form = LoginForm()
        
    return render(request, 'books/login.html', {'form': form, 'error_message': error_message})
