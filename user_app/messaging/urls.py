from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name='user_login'),
    path('register/', views.user_register, name='user_register'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('logout/', views.user_logout, name='user_logout'),
    path('send_message/', views.send_message, name='send_message'),
]
