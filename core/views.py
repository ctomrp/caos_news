from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def news_gallery(request):
    return render(request, 'news_gallery.html')

def pictures_gallery(request):
    return render(request, 'pictures_gallery.html')

def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

def contact(request):
    return render(request, 'contact.html')

def create_news(request):
    return render(request, 'create_news.html')

def news_detail(request):
    return render(request, 'news_detail.html')

def news_state(request):
    return render(request, 'news_state.html')

def news_feedback(request):
    return render(request, 'news_feedback.html')

def journalist(request):
    return render(request, 'journalist.html')

def recover_password(request):
    return render(request, 'recover_password.html')
