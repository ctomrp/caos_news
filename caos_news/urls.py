from django.contrib import admin
from django.urls import path, include
from login import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('',views.index),

]
