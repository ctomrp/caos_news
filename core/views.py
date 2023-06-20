from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import User, Group
from django.db.models import Q
from .forms import *
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.urls import reverse

def index(request):
    data = News.objects.filter(headline=True, state_id=1)
    pictures = Picture.objects.filter(news__in=data, principal=True)
    return render(request, 'index.html', {'data': data, 'pictures': pictures})


def base_context(request):
    categories = NewsCategory.objects.all()
    return {'categories': categories}



##########################
#   news
##########################

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Periodista').exists(), login_url='index.html') 
def create_news(request):
    data = NewsCategory.objects.all()
    if request.method == 'POST':
        user_id = request.user.id
        auto = User.objects.get(id=user_id)

        form = crearNoticiaForm(request.POST, request.FILES)

        if form.is_valid():
            titulo = form.cleaned_data['title']
            articulo = form.cleaned_data['article']
            categoria = form.cleaned_data['category']
            ubicacion = form.cleaned_data['ubicacion']

            # Guardar la noticia en la base de datos
            objCategory = NewsCategory.objects.get(id=categoria.id)
            objState = NewsState.objects.get(id=2)
            objNews = News.objects.create(
                title=titulo,
                article=articulo,
                author=auto,
                category=objCategory,
                state=objState,
                location=ubicacion
            )

            # Obtener las imágenes del formulario
            fotos = request.FILES.getlist('photo')

            # Guardar cada imagen en la tabla Picture asociada a la noticia
            for foto in fotos:
                picture = Picture.objects.create(picture=foto, news=objNews)

            return redirect('index')
        else:
            print(form.errors)
    return render(request, 'create_news.html', {'data': data})


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

    for news_item in news:
        picture = Picture.objects.filter(news_id=news_item.id, principal=True).first()
        if picture:
            news_item.image = picture.picture.url
        else:
            news_item.image = 'images/default-image.png'  # Ruta a la imagen por defecto

    return render(request, 'news_gallery.html', {'news': news})


# def pictures_gallery(request, news_id):
#     pictures = Picture.objects.filter(news_id=news_id)
#     return render(request, 'pictures_gallery.html', {'pictures': pictures})

def pictures_gallery(request, news_id):
    pictures = Picture.objects.filter(news_id=news_id)
    news = get_object_or_404(News, id=news_id)
    news_detail_url = reverse('news_detail', args=[news_id])
    context = {
        'pictures': pictures,
        'news_id': news_id,
        'news': news,
        'news_detail_url': news_detail_url,
    }
    return render(request, 'pictures_gallery.html', context)

def news_detail(request, news_id):
    news = get_object_or_404(News, id=news_id)
    detail = News.objects.get(id = news.id)
    pictures = Picture.objects.filter(news_id=news.id)

    return render(request, 'news_detail.html', {'news': news, 'detail': detail, 'pictures': pictures})

def news_pictures(request, news_id):
    news = get_object_or_404(News, id=news_id)
    print(news.id)
    pictures = Picture.objects.filter(news_id=news.id)
    print(pictures)
    return render(request, 'news_detail.html', {'news': news, 'pictures': pictures})


def news_state(request):
    return render(request, 'news_state.html')

@login_required
def news_premium(request):
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

    for news_item in news:
        picture = Picture.objects.filter(news_id=news_item.id, principal=True).first()
        if picture:
            news_item.image = picture.picture.url
        else:
            news_item.image = 'images/default-image.png'  # Ruta a la imagen por defecto

    return render(request, 'news_premium.html', {'news': news})


def pictures_gallery(request, news_id):
    news = get_object_or_404(News, id=news_id)
    pictures = Picture.objects.filter(news_id=news.id)
    return render(request, 'pictures_gallery.html', {'news': news, 'pictures': pictures})


def register(request):
    return render(request, 'register.html')




def journalist(request):
    grupo_periodista = Group.objects.get(name='periodista')
    periodistas = grupo_periodista.user_set.all()
    return render(request, 'journalist.html', {'periodistas': periodistas})

def recover_password(request):
    return render(request, 'recover_password.html')

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

def exit(request):
    logout(request)
    return redirect('auth_login')

# def contact(request):
#     if request.method == 'POST':
#         form = cf(request.POST)
#         if form.is_valid():
#             name = request.POST['name']
#             last_name = request.POST['last_name']
#             email = request.POST['email']
#             email2 = request.POST['email2']
#             phone = request.POST['phone']
#             comment = request.POST['comment']
#             form = ContactForm.objects.create(
#                 name = name,
#                 last_name = last_name,
#                 email = email,
#                 email2 = email2,
#                 phone = phone,
#                 comment = comment,
#             )
#             form.save()
#             return redirect('index')  # Redirigir a una página de éxito o cualquier otra página
#     else:
#         form = cf()
#     return render(request, 'contact.html', {'form': form})

# def contact(request):
#     if request.method == 'POST':
#         form = ContactFormForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('index')
#     else:
#         form = ContactFormForm()
    
#     return render(request, 'contact.html', {'form': form})


def contact(request):
    if request.method == 'POST':
        form = Contacto(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            comment = form.cleaned_data['comment']
        
            form = ContactForm.objects.create(
                name = name,
                last_name = last_name,
                email = email,
                phone = phone,
                comment = comment
            )
            form.save
            return redirect('index')
        else:
            print(form.errors)
    return(render(request,'contact.html'))


def news_state(request):
    author_id = request.GET.get('author_id')

    news = News.objects.all()

    if author_id:
        news = news.filter(author__id=author_id)
        
    return render(request, 'news_state.html', {'news': news})

def editor_dash(request):
    return render(request, 'editor_dash.html')

def edit_news(request, news_id):
    news = get_object_or_404(News, id=news_id)
    detail = News.objects.get(id = news.id)
    pictures = Picture.objects.filter(news_id=news.id)
    states = NewsState.objects.all()

    return render(request, 'edit_news.html', {'news': news, 'detail': detail, 'pictures': pictures, 'states': states})

def news_feedback(request, news_id):
    news = get_object_or_404(News, id=news_id)
    detail = News.objects.get(id = news.id)
    pictures = Picture.objects.filter(news_id=news.id)
    states = NewsState.objects.all()
    category = NewsCategory.objects.all()

    return render(request, 'news_feedback.html', {'news': news, 'detail': detail, 'pictures': pictures, 'states': states, 'category': category})

def edit_pictures(request, news_id):
    pictures = Picture.objects.filter(news_id=news_id)
    news = get_object_or_404(News, id=news_id)
    news_detail_url = reverse('edit_news', args=[news_id])
    context = {
        'pictures': pictures,
        'news_id': news_id,
        'news': news,
        'news_detail_url': news_detail_url,
    }
    return render(request, 'edit_pictures.html', context)