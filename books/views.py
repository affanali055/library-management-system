# books/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Book
from .serializers import BookSerializer
from .forms import BookForm

class BookListAPIView(APIView):

    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            # Save the new book to the database
            form.save()
            messages.success(request, "Book saved successfully!")
            # Redirect to the API book-list view (or any other listing page)
            return redirect('book-list')
    else:
        form = BookForm()
    
    return render(request, 'books/add_book.html', {'form': form})
def book_list(request):
    books = Book.objects.all()
    return render(request, "books/book_list.html", {"books": books})

# Add this at the bottom of books/views.py

def edit_book(request, id):
    # Fetch the specific book from the database
    book = Book.objects.get(id=id)
    
    if request.method == 'POST':
        # Bind the form to POST data and the existing book instance
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()  # Save database updates
            return redirect('book-list')  # Redirect back to Book List
    else:
        # Prepopulate the form with the current book details
        form = BookForm(instance=book)
        
    return render(request, 'books/edit_book.html', {'form': form, 'book': book})
