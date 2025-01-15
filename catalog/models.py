from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    cover_image = models.ImageField(upload_to='images')
    count = models.IntegerField(default=0)
    pdf_file = models.FileField(upload_to='book_pdfs/', blank=True, null=True)
    def __str__(self):
        return self.title

class UserBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_date = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField(default=timezone.now() + timezone.timedelta(days=10))

    def __str__(self):
        return f"{self.user.username} borrowed {self.book.title}"
