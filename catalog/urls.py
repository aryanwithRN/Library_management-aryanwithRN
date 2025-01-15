from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index,name='index'),
    path('about/', views.about, name ='about'),
    path('signup', views.signup_view,name='signup'),
    path('login', views.login_view,name='login'),
    path('home', views.home,name='home'),
    path('account', views.account,name='account'),

    path('borrow/<int:book_id>/', views.borrow_book, name='borrow_book'),
    path('confirm_borrow/<int:book_id>/', views.confirm_borrow, name='confirm_borrow'),
    path('return_book/<int:user_book_id>/', views.return_book, name='return_book'),
    path('search/', views.search_books, name='search_books'),



]+  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)