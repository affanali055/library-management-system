# books/forms.py
from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'price', 'published_year', 'available']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter book title'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter author name'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter price', 'step': '0.01'}),
            'published_year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter publication year'}),
            'available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
