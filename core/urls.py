from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('gallery/', gallery, name='gallery'),
    path('login/', login, name='login'),
    #path('register/', register, name='register'),
    path('contact/', contact, name='contact'),
    path('create_news/', create_news, name='create_news'),
    path('news_detail/', news_detail, name='news_detail'),
    path('news_state/', news_state, name='news_state'),
    path('news_feedback/', news_feedback, name='news_feedback'),
    path('journalist/', journalist, name='journalist'),
    path('recover_password/', recover_password, name='recover_password'),
    path('auth_register/',auth_register,name='auth_register'),
]
