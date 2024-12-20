from django.urls import path
from . import views
from .views import MessageListView

urlpatterns = [
    path('', views.admin_login, name='admin_login'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('logout/', views.admin_logout, name='admin_logout'),
    path('edit_user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('view_user_messages/<int:user_id>/', views.view_user_messages, name='view_user_messages'),
    path('send_message/<int:user_id>/', views.send_message, name='send_message'),
    path('api/messages/', MessageListView.as_view(), name='message_list'),
     path('home/', views.home, name='home'),
]


