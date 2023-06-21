from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import User, Group
from django.db.models import Q
from .forms import RegistrationForm,crearNoticiaForm
from .models import NewsCategory,News,Picture,NewsState,Contacto
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

    news = News.objects.all()

    for news_item in news:
        picture = Picture.objects.filter(news_id=news_item.id, principal=True).first()
        if picture:
            news_item.image = picture.picture.url
        else:
            news_item.image = 'images/default-image.png'  # Ruta a la imagen por defecto

    return render(request, 'index.html', {'data': data, 'pictures': pictures, 'news': news})


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

def journalist(request):
    grupo_periodista = Group.objects.get(name='periodista')
    periodistas = grupo_periodista.user_set.all()
    return render(request, 'journalist.html', {'periodistas': periodistas})

def recover_password(request):
    return render(request, 'recover_password.html')

def auth_register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            name = form.cleaned_data['name']
            last_name = form.cleaned_data['last_name']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            User.objects.create_user(username=username, first_name=name, last_name=last_name, password=password, email=email)
            messages.success(request, 'Registro añadido correctamente')
            return redirect('auth_login')
        else:
            messages.error(request, 'Error en el registro. Por favor, corrija los campos resaltados.')
    else:  # GET request or any other method
        form = RegistrationForm()
    
    return render(request, 'auth_register.html', {'form': form})

def auth_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            error = 'Correo o Contraseña incorrecta!'
            return render(request, 'auth_login.html', {'error': error})
    else:
        return render(request, 'auth_login.html')

def exit(request):
    logout(request)
    return redirect('auth_login')


# def guardar_foto(foto):
#     # Guardar la foto en la carpeta media
#     photo_path = os.path.join(settings.MEDIA_ROOT, foto.name)
#     with open(photo_path, 'wb') as file:
#         for chunk in foto.chunks():
#             file.write(chunk)

def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        last_name = request.POST['lastname']
        email = request.POST['email']
        email2 = request.POST['email2']
        phone = request.POST['phone']
        comment = request.POST['comment']
        
        if email != email2:
            messages.error(request, 'Los correos no coinciden')
            return redirect('contact')

        Contacto.objects.create(
            name=name,
            last_name=last_name,
            email=email,
            phone=phone,
            comment=comment
        )
        messages.success(request, 'Registro añadido correctamente')
        return redirect('contact')
    else:
        return render(request, 'contact.html')
    
def buscar(request):
    queryset = request.GET.get("buscar")
    search = None
    if queryset:
        try:
            objCategoria = NewsCategory.objects.get(Q(category__icontains=queryset))
        except NewsCategory.DoesNotExist:
            objCategoria = None
        
        try:
            objUser = User.objects.get(username__icontains=queryset)
        except User.DoesNotExist:
            objUser = None
        
        try:
            objNews = News.objects.get(Q(title__icontains=queryset)|Q(location__icontains=queryset))
        except News.DoesNotExist:
            objNews = None
        
        if objUser:
            return redirect('journalist')
        elif objCategoria or objNews:
            return redirect('news_gallery')
    return(render(request,'index.html'))


def news_state(request):
    news = News.objects.all()
    author_id = request.GET.get('author_id')

    if author_id:
        news = news.filter(author__id=author_id)
        
    return render(request, 'news_state.html', {'news': news})


def edit_news(request, news_id):
    news = get_object_or_404(News, id=news_id)
    detail = News.objects.get(id=news.id)
    pictures = Picture.objects.filter(news_id=news.id)
    states = NewsState.objects.all()

    if request.method == 'POST':
        news.feedback = request.POST.get('feedback')

        valorTitular = request.POST.get('titularCheckbox')
        valorPremium = request.POST.get('premiumCheckbox')

        if valorTitular:
            news.headline = True
        else:
            news.headline = False

        if valorPremium:
            news.premium = True
        else:
            news.premium = False

        estado_id = request.POST.get('estadosNoticia')
        estado = NewsState.objects.get(id=estado_id)
        news.state = estado

        news.save()
        messages.success(request, 'Edición guardada correctamente')
        return redirect('news_state')
    else:
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

    if request.method == 'POST':
        selected_principal = request.POST.get('principal')
        for picture in pictures:
            if str(picture.id) == selected_principal:
                picture.principal = True
            else:
                picture.principal = False

            active = request.POST.get('active_{}'.format(picture.id), False)
            if active:
                picture.active = True
            else:
                picture.active = False

            picture.save()

        messages.success(request, 'Fotos seleccionadas guardadas con éxito')

    context = {
        'pictures': pictures,
        'news_id': news_id,
        'news': news,
        'news_detail_url': news_detail_url,
    }

    return render(request, 'edit_pictures.html', context)