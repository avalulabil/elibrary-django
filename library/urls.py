from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('', views.dashboard, name='dashboard'),
    path('books/', views.book_list, name='book_list'),
    path('books/<int:pk>/', views.book_detail, name='book_detail'),
    path('books/new/', views.book_create, name='book_create'),
    path('books/<int:pk>/edit/', views.book_update, name='book_update'),
    path('books/<int:pk>/delete/', views.book_delete, name='book_delete'),
    path('books/<int:pk>/preview/', views.pdf_preview, name='pdf_preview'),
    path("logout/", views.Logout, name="logout"),
    path('topics/', views.topic_modeling, name='topic_modeling'),
]
