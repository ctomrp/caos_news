from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse, HttpResponseRedirect
from .models import NewsCategory,NewsState,News
from django.db.models import Max
from django.shortcuts import get_object_or_404
import os 
from django.conf import settings
from django.shortcuts import render, redirect
from .models import ContactForm
from .forms import ContactForm as cf

def index(request):
    data = News.objects.filter(headline=True)
    # last = News.objects.aggregate(date=Max('date'))
    # contexto = {'data': data, 'last_date': last['date']}
    return render(request, 'index.html', {'data': data})

def base_context(request):
    categories = NewsCategory.objects.all()
    return {'categories': categories}

# def news_gallery(request):
#     data = News.objects.all()
#     return render(request,'news_gallery.html', {'data':data})

# def news_by_author(request):
#     grupo_periodista = Group.objects.get(name='periodista')
#     periodistas = User.objects.filter(groups=grupo_periodista)
#     news = News.objects.filter(author__user__in=periodistas)    
#     return render(request, 'journalist.html', {'news': news})

def news_gallery(request):
    author_id = request.GET.get('author_id')
    category_id = request.GET.get('category_id')
    search_query = request.GET.get('search_query')

    news = News.objects.all()

    if author_id:
        news = news.filter(author__id=author_id)

    if category_id:
        news = news.filter(category_id=category_id)

    if search_query:
        news = news.filter(
            Q(title__icontains=search_query) |
            Q(article__icontains=search_query)
        )

    return render(request, 'news_gallery.html', {'news': news})

@login_required
def news_premium(request):
    news_premium = News.objects.filter(premium=1)
    return render(request, 'news_premium.html', {'news_premium': news_premium})


def pictures_gallery(request):
    data = News.objects.get()
    return render(request, 'pictures_gallery.html')

#def login(request):
#    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

def news_detail(request, news_id):
    news = get_object_or_404(News, id=news_id)
    detail = News.objects.get(id = news.id)
    print(detail.photo)
    return render(request, 'news_detail.html', {'detail': detail})

def news_state(request):
    return render(request, 'news_state.html')

def news_feedback(request):
    return render(request, 'news_feedback.html')

def journalist(request):
    grupo_periodista = Group.objects.get(name='periodista')
    periodistas = grupo_periodista.user_set.all()
    return render(request, 'journalist.html', {'periodistas': periodistas})

def recover_password(request):
    return render(request, 'recover_password.html')


# def registrarUsuario(request):
#     
#     if request.method == 'GET':
#         return render(request ,'register.html',{
#             'form': UserCreationForm
#         })
#     else:
#         if request.POST['password'] == request.POST['password2']:
#             try:     
#                 User.objects.create_user(first_name=request.POST['name'],last_name=request.POST['last_name'],password=request.POST['password'],email=request.POST['email'])
#                 User.save()
#                 return HttpResponse('Usuario Creado Correctamente')
#             except:
#                 return('Usuario ya existe')
#     return HttpResponse('Contraseñas no coinciden')   
# 

def auth_register(request):
    if request.method=='POST':
        form = RegistrationForm(request.POST)
        print(form)
        if form.is_valid():
            username = form.cleaned_data['username']
            name = form.cleaned_data['name']
            last_name = form.cleaned_data['last_name']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email'] 
            User.objects.create_user(username=username,first_name=name,last_name=last_name,password=password,email=email)
            messages.success(request,'Registro añadido correctamente')
            print('ola')
            return(render(request,'login.html'))
    elif request.method == 'GET':
        form = RegistrationForm()
        return render(request, 'register.html', {'form': form})    
    else:
        print('no funsiona')
        form = RegistrationForm()
    return(render(request,'register.html'))    

def auth_login(request):
    if request.method=='POST':
        email = request.POST['email']
        password= request.POST['password']
        user= authenticate(request,email=email,password=password)
        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            error='Correo o Contraseña incorrecta!'
            return render(request, 'login.html',{'error':error})
    else:
        return render(request,'login.html')
    
# @login_required
# def create_news(request):
#     es_periodista = request.User.groups.filter(name='Periodista').exists()
#     return render(request, 'create_news.html',{'es_periodista':es_periodista})

def exit(request):
    logout(request)
    return redirect('auth_login')

# def category_values(request):
#     data = NewsCategory.objects.all()
#     return render(request,'create_news.html', {'data':data})

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Periodista').exists(), login_url='index.html') 
def crear_noticia(request):
    data = NewsCategory.objects.all()
    if request.method == 'POST':
        user_id = request.user.id
        auto= User.objects.get(id=user_id)

        form = crearNoticiaForm(request.POST,request.FILES)
        
        if form.is_valid():
            titulo = request.POST['title']
            articulo = request.POST['article']
            categoria = request.POST['category']
            foto = request.FILES['photo']
            ubicacion = request.POST['ubicacion']
            # # Guardar la foto en la carpeta media
            # photo_path = os.path.join(settings.MEDIA_ROOT, foto.name)
            # with open(photo_path, 'wb') as file:
            #     for chunk in foto.chunks():
            #         file.write(chunk)
             # Obtener una lista de archivos enviados
            fotos = request.FILES.getlist('photo')
            for foto in fotos:
            # Guardar cada foto en la carpeta media
                photo_path = os.path.join(settings.MEDIA_ROOT, foto.name)
                with open(photo_path, 'wb') as file:
                    for chunk in foto.chunks():
                        file.write(chunk)        

                objCategory = NewsCategory.objects.get(id=categoria)
                objState = NewsState.objects.get(id=1) 
                objNews = News.objects.create(
                    title=titulo,
                    article=articulo,
                    author=auto,
                    category=objCategory,
                    photo=foto,
                    location=ubicacion,
                    state=objState
                )
            objNews.save()
            return redirect('index')
        else:
            print(form.errors)
    return render(request, 'create_news.html', {'data': data})


def contact(request):
    if request.method == 'POST':
        form = cf(request.POST)
        if form.is_valid():
            name = request.POST['name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            email2 = request.POST['email2']
            phone = request.POST['phone']
            comment = request.POST['comment']
            form = ContactForm.objects.create(
                name = name,
                last_name = last_name,
                email = email,
                email2 = email2,
                phone = phone,
                comment = comment,
            )
            form.save()
            return redirect('index')  # Redirigir a una página de éxito o cualquier otra página
    else:
        form = cf()
    return render(request, 'contact.html', {'form': form})