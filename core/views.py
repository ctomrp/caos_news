from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .forms import RegistrationForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse, HttpResponseRedirect

def index(request):
    return render(request, 'index.html')

def gallery(request):
    return render(request, 'gallery.html')

#def login(request):
#    return render(request, 'login.html')

#def register(request):
#    return render(request, 'register.html')

def contact(request):
    return render(request, 'contact.html')
@login_required
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
            return redirect('base_user.html')
        else:
            error='Correo o Contraseña incorrecta!'
            return render(request, 'login.html',{'error':error})
    else:
        return render(request,'login.html')
    
@login_required
def base_user(request):
    return(render(request,'layouts/base_user.html'))
