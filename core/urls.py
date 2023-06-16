from django.urls import path, include
from .views import *

urlpatterns = [
    path('', index, name='index'),
    # path('', last, name='index'),
    # path('news_gallery/', news_gallery, name='news_gallery'),
    # path('news_gallery/<int:author_id>/', news_gallery, name='news_gallery'),
    path('news_gallery/', news_gallery, name='news_gallery'),
    path('news_premium/', news_premium, name='news_premium'),
    path('pictures_gallery/', pictures_gallery, name='pictures_gallery'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('contact/', contact, name='contact'),
    path('create_news/',crear_noticia, name='create_news'),
    # path('news_detail/', news_detail, name='news_detail'),
    path('news_detail/<int:news_id>/', news_detail, name='news_detail'),
    path('news_state/', news_state, name='news_state'),
    path('news_feedback/', news_feedback, name='news_feedback'),
    path('journalist/', journalist, name='journalist'),
    path('recover_password/', recover_password, name='recover_password'),
    path('auth_register/',auth_register,name='auth_register'),
    path('auth_login/',auth_login,name='auth_login'),
    path('logout/',exit,name='exit'),
]
