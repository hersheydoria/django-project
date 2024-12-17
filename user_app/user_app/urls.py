from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('messaging.urls')),  # Include messaging app URLs directly
]
