from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('news_gallery/', news_gallery, name='news_gallery'),
    path('news_premium/', news_premium, name='news_premium'),
    path('contact/', contact, name='contact'),
    path('create_news/',create_news, name='create_news'),
    path('news_detail/<int:news_id>/', news_detail, name='news_detail'),
    path('edit_news/<int:news_id>/', edit_news, name='edit_news'),
    path('news_feedback/<int:news_id>/', news_feedback, name='news_feedback'),
    path('news_state/', news_state, name='news_state'),
    path('journalist/', journalist, name='journalist'),
    path('recover_password/', recover_password, name='recover_password'),
    path('auth_register/',auth_register,name='auth_register'),
    path('auth_login/',auth_login,name='auth_login'),
    path('logout/',exit,name='exit'),
    path('news_detail/<int:news_id>/', news_detail, name='news_detail'),
    path('pictures_gallery/<int:news_id>/', pictures_gallery, name='pictures_gallery'),
    path('edit_pictures/<int:news_id>/', edit_pictures, name='edit_pictures'),
    path('search/', buscar, name='buscar'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
