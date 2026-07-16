from django.shortcuts import render, redirect, get_object_or_404 
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q, Count
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Book, BookLoan
from .serializers import BookSerializer
from .forms import BookForm, UserRegisterForm, LoginForm, UserSettingsForm
from datetime import timedelta


class BookListAPIView(APIView):
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

@login_required
def book_list(request):
    # Get search query from URL parameter 'q'
    query = request.GET.get('q')
    
    if query:
        # Filter books matching title OR author
        books = Book.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        )
    else:
        books = Book.objects.all()

    # Dashboard summary cards stats (overall library count)
    total_books = Book.objects.count()
    available_books = Book.objects.filter(available=True).count()
    issued_books = Book.objects.filter(available=False).count()
    total_members = User.objects.count()
    
    context = {
        "books": books,
        "total_books": total_books,
        "available_books": available_books,
        "issued_books": issued_books,
        "total_members": total_members,
        "active_tab": "books",
    }
    return render(request, "books/book_list.html", context)






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
    book = get_object_or_404(Book, id=id)

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


@require_POST
def delete_book(request, id):
    book = get_object_or_404(Book, id=id)
    book.delete()
    messages.success(request, "Book deleted successfully!")
    return redirect("book-list")
    # Replace lines 142 to 207 in books/views.py with this clean block:

@login_required
def borrow_book(request, id):
    book = get_object_or_404(Book, id=id)
    if book.available:
        book.available = False
        book.save()
        
        # Calculate due date (14 days from now)
        borrow_date = timezone.now()
        due_date = borrow_date.date() + timedelta(days=14)
        
        BookLoan.objects.create(
            book=book,
            user=request.user,
            borrowed_at=borrow_date,
            due_date=due_date
        )
        messages.success(request, f"You successfully borrowed '{book.title}'! Due date: {due_date.strftime('%B %d, %Y')}.")
    else:
        messages.error(request, "This book is already borrowed.")
    return redirect("book-list")

@login_required
def return_book(request, id):
    book = get_object_or_404(Book, id=id)
    # Find the active loan for this book
    loan = BookLoan.objects.filter(book=book, returned_at__isnull=True).first()
    if loan:
        loan.returned_at = timezone.now()
        loan.save()
        book.available = True
        book.save()
        messages.success(request, f"You successfully returned '{book.title}'!")
    else:
        messages.error(request, "No active borrow record found for this book.")
    return redirect("book-list")

   
@login_required
def dashboard_view(request):
    total_books = Book.objects.count()
    available_books = Book.objects.filter(available=True).count()
    issued_books = Book.objects.filter(available=False).count()
    total_members = User.objects.count()
    
    # Fetch 5 most recent borrow activities
    recent_loans = BookLoan.objects.all().order_by('-borrowed_at')[:5]
    
    context = {
        "total_books": total_books,
        "available_books": available_books,
        "issued_books": issued_books,
        "total_members": total_members,
        "recent_loans": recent_loans,
        "active_tab": "dashboard",
    }
    return render(request, "dashboard.html", context)

@login_required
def users_list(request):
    query = request.GET.get('q')
    users = User.objects.all().annotate(
        active_loans_count=Count('loans', filter=Q(loans__returned_at__isnull=True))
    )
    
    if query:
        users = users.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query)
        )
        
    context = {
        "users_list": users,
        "active_tab": "users",
    }
    return render(request, "books/user.html", context)

@login_required
def settings_view(request):
    if request.method == "POST":
        form = UserSettingsForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("settings")
    else:
        form = UserSettingsForm(instance=request.user)
        
    context = {
        "form": form,
        "active_tab": "settings",
    }
    return render(request, "books/setting.html", context)

def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect("login")

