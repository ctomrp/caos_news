from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse, HttpResponseRedirect
from .models import NewsCategory,NewsState,News
import os 
from django.conf import settings

def index(request):
    print('qqeqq')
    return render(request, 'index.html')

def news_gallery(request):
    return render(request, 'news_gallery.html')

def pictures_gallery(request):
    return render(request, 'pictures_gallery.html')

#def login(request):
#    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

def contact(request):
    return render(request, 'contact.html')

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

# @login_required
# @user_passes_test(lambda u: u.groups.filter(name='Periodista').exists(), login_url='index.html') 
# def crear_noticia(request):
#     data = NewsCategory.objects.all()
#     if request.method == 'POST':
#         user_id = request.user.id
#         auto= User.objects.get(id=user_id)

#         form = crearNoticiaForm(request.POST,request.FILES)
        
#         if form.is_valid():
#             titulo = request.POST['title']
#             articulo = request.POST['article']
#             categoria = request.POST['category']
#             foto = request.FILES['photo']
#             ubicacion = request.POST['ubicacion']
#             # # Guardar la foto en la carpeta media
#             # photo_path = os.path.join(settings.MEDIA_ROOT, foto.name)
#             # with open(photo_path, 'wb') as file:
#             #     for chunk in foto.chunks():
#             #         file.write(chunk)
#              # Obtener una lista de archivos enviados
#             fotos = request.FILES.getlist('photo')
#             for foto in fotos:
#             # Guardar cada foto en la carpeta media
#                 photo_path = os.path.join(settings.MEDIA_ROOT, foto.name)
#                 with open(photo_path, 'wb') as file:
#                     for chunk in foto.chunks():
#                         file.write(chunk)        
#                 objCategory = NewsCategory.objects.get(id=categoria)
#                 objState = NewsState.objects.get(id=1) 
#                 objNews = News.objects.create(
#                     title=titulo,
#                     article=articulo,
#                     author=auto,
#                     category=objCategory,
#                     photo=foto,
#                     location=ubicacion,
#                     state=objState
#                 )
#             objNews.save()
#             return redirect('index')
#         else:
#             print(form.errors)
#     return render(request, 'create_news.html', {'data': data})

def guardar_foto(foto):
    # Guardar la foto en la carpeta media
    photo_path = os.path.join(settings.MEDIA_ROOT, foto.name)
    with open(photo_path, 'wb') as file:
        for chunk in foto.chunks():
            file.write(chunk)

def crear_noticia(request):
    data = NewsCategory.objects.all()
    if request.method == 'POST':
        user_id = request.user.id
        author = get_object_or_404(User, id=user_id)
        form = crearNoticiaForm(request.POST, request.FILES)
        if form.is_valid():
            titulo = form.cleaned_data['title']
            articulo = form.cleaned_data['article']
            categoria = request.POST['category']
            ubicacion = form.cleaned_data['ubicacion']
            # Obtener una lista de archivos enviados
            fotos = request.FILES.getlist('photo')
            for foto in fotos:
                guardar_foto(foto)
                objCategory = get_object_or_404(NewsCategory, id=categoria)
                objNews = News.objects.create(
                    title=titulo,
                    article=articulo,
                    author=author,
                    category=objCategory,
                    photo=foto,
                    location=ubicacion,
                )
            objNews.save()
            return redirect('index')
        else:
            print(form.errors)
    return render(request, 'create_news.html', {'data': data})