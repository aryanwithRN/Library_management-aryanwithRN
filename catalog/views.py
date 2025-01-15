from django.shortcuts import render
from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth import logout
from django.contrib import messages
from .models import Book
# Create your views here.
def index(request):
    books = Book.objects.all()
    return render(request, 'index.html',{'books': books})


# About page 
def about(request):
    return render (request, 'about.html')

def signup_view(request):
    if request.method == "POST":
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password')  # Corrected 'request.Post' to 'request.POST'
        pass2 = request.POST.get('password1')  # Corrected 'password1' to match your form field name

        if pass1 != pass2:
            return HttpResponse("Passwords do not match")

        # Check if the user already exists
        if User.objects.filter(username=uname).exists():
            error_message = 'Username already exists. Please choose a different username.'
            return render(request, 'signup.html', {'error_message': error_message})

        # Create the user using the User model
        my_user = User.objects.create_user(username=uname, email=email, password=pass1)  # Corrected 'User.objects.create_user'
        my_user.save()

        return redirect('login')  # Assuming 'login' is the name of your login URL pattern

    return render(request, "signup.html")

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to home page after successful login
        else:
            error = 'Invalid credentials. Please try again.'
            return render(request, 'login.html', {'error': error})
    return render(request, 'login.html')

# for logout 


def logout_view(request):
    logout(request)
    return redirect('index')


# Home page 


# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Book, UserBook
from django.utils import timezone
from datetime import timedelta


@login_required
def home(request):
    books = Book.objects.all()
    return render(request, 'home.html', {'books': books})

# Borrow Book 
@login_required
def confirm_borrow(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    context = {
        'book': book,
        'borrowed_date': timezone.now(),
        'due_date': timezone.now() + timedelta(days=10),
    }
    return render(request, 'confirm_borrow.html', context)

@login_required
def borrow_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        borrowed_date = timezone.now()
        due_date = borrowed_date + timedelta(days=10)
        
        user_book = UserBook(
            user=request.user,
            book=book,
            borrowed_date=borrowed_date,
            due_date=due_date
        )
        user_book.save()
        
        book.count -= 1
        book.save()
        
        return redirect('account')
    
    return redirect('confirm_borrow', book_id=book.id)


# Account Page

from django.utils import timezone

@login_required
def account(request):
    user_books = UserBook.objects.filter(user=request.user)
    context = {
        'user_books': user_books,
        'now': timezone.now(),
    }
    return render(request, 'account.html', context)

# return book

@login_required
def return_book(request, user_book_id):
    user_book = get_object_or_404(UserBook, id=user_book_id, user=request.user)
    now = timezone.now()
    days_borrowed = (now.date() - user_book.borrowed_date.date()).days + 1  # Ensure at least 1 day
    days_overdue = max(0, (now.date() - user_book.due_date.date()).days)
    fine = 0 if days_overdue == 0 else days_overdue * 29

    if request.method == 'POST':
        book = user_book.book
        user_book.delete()
        book.count += 1
        book.save()
        
        if fine > 0:
            messages.warning(request, f'You have been fined {fine} rupees for returning the book late.')
        else:
            messages.success(request, 'Book returned successfully!')
        return redirect('account')

    context = {
        'user_book': user_book,
        'days_borrowed': days_borrowed,
        'days_overdue': days_overdue,
        'fine': fine,
        'now': now
    }
    return render(request, 'return_book.html', context)



# For search box 
def search_books(request):
    query = request.GET.get('q')
    if query:
        results = Book.objects.filter(title__icontains=query)
    else:
        results = None
    
    context = {
        'query': query,
        'results': results,
    }
    return render(request, 'search_results.html', context)


# For sorting A-Z / Z-A

def all_books(request):
    all_books = Book.objects.all()
    sort_key = request.GET.get('sort', 'az')  # Default to A-Z sorting if no sort parameter is provided

    if sort_key == 'az':
        all_books = all_books.order_by('title')  # Sort A-Z
    elif sort_key == 'za':
        all_books = all_books.order_by('-title')  # Sort Z-A

    context = {
        'books': all_books,
        'sort_key': sort_key,
    }
    return render(request, 'home.html', context)