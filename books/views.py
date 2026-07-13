# books/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User

from .models import Book
from .serializers import BookSerializer
from .forms import BookForm, UserRegisterForm

class BookListAPIView(APIView):
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Book saved successfully!")
            return redirect('book-list')
    else:
        form = BookForm()
    
    return render(request, 'books/add_book.html', {'form': form})

def book_list(request):
    books = Book.objects.all()
    return render(request, "books/book_list.html", {"books": books})

def edit_book(request, id):
    book = Book.objects.get(id=id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, "Book updated successfully!")
            return redirect('book-list')
    else:
        form = BookForm(instance=book)
    return render(request, 'books/edit_book.html', {'form': form, 'book': book})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data.get('full_name')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            
            name_parts = full_name.split(' ', 1)
            first_name = name_parts[0]
            last_name = name_parts[1] if len(name_parts) > 1 else ''
            
            # Create a secure user
            User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            
            messages.success(request, "Account created successfully!")
            return redirect('login')
    else:
        form = UserRegisterForm()
        
    return render(request, 'books/register.html', {'form': form})
