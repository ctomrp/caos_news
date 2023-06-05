from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('gallery/', gallery, name='gallery'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('contact/', contact, name='contact'),
]
