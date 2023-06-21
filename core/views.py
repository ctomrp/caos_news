from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import User, Group
from django.db.models import Q
from django.views.generic import ListView
from .forms import RegistrationForm,crearNoticiaForm
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db import connection

def index(request):
    data = News.objects.filter(headline=True, state_id=1)
    pictures = Picture.objects.filter(news__in=data, principal=True)

    news = News.objects.all()

    for news_item in news:
        picture = Picture.objects.filter(news_id=news_item.id, principal=True).first()
        if picture:
            news_item.image = picture.picture.url
        else:
            news_item.image = '../static/img/no_image.png'  # Ruta a la imagen por defecto

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
            messages.success(request, 'Noticia guardada correctamente')
            messages.get_messages(request).used = True
            return redirect('news_state')
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
            news_item.image = '../static/img/no_image.png'  # Ruta a la imagen por defecto

    return render(request, 'news_gallery.html', {'news': news})


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
            news_item.image = '../static/img/no_image.png'  # Ruta a la imagen por defecto

    return render(request, 'news_premium.html', {'news': news})


def pictures_gallery(request, news_id):
    news = get_object_or_404(News, id=news_id)
    pictures = Picture.objects.filter(news_id=news.id)
    return render(request, 'pictures_gallery.html', {'news': news, 'pictures': pictures})

def journalist(request):
    grupo_periodista = Group.objects.get(name='periodista')
    periodistas = grupo_periodista.user_set.all()

    cantidad = []
    for periodista in periodistas:
        raw_query = "SELECT COUNT(*) FROM core_news WHERE author_id = %s"
        with connection.cursor() as cursor:
            cursor.execute(raw_query, [periodista.id])
            resultado = cursor.fetchone()[0]
            cantidad.append(resultado)

    periodistas_cantidad = zip(periodistas, cantidad)

    return render(request, 'journalist.html', {'periodistas_cantidad': periodistas_cantidad})


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
            if User.objects.filter(username=username).exists():
                messages.error(request, 'El nombre de usuario ingresado ya existe')
                messages.get_messages(request).used = True
                return redirect('auth_register')
            if User.objects.filter(email=email).exists():
                messages.error(request, 'El correo ingresado ya existe')
                messages.get_messages(request).used = True
                return redirect('auth_register')
            User.objects.create_user(username=username, first_name=name, last_name=last_name, password=password, email=email)
            return redirect('auth_login')
        else:
            messages.error(request, 'Error en el registro. Por favor, corrija los campos resaltados.')
            messages.get_messages(request).used = True
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
            messages.get_messages(request).used = True
            return redirect('contact')

        Contacto.objects.create(
            name=name,
            last_name=last_name,
            email=email,
            phone=phone,
            comment=comment
        )
        messages.success(request, 'Registro añadido correctamente')
        messages.get_messages(request).used = True
        return redirect('contact')
    else:
        return render(request, 'contact.html')
    

class SearchResultsView(ListView):
    model = News
    template_name = 'search_results.html'
    context_object_name = 'results'

    def get_queryset(self):
        query = self.request.GET.get('search_query')
        print(query)
        if query:
            print(query)
            queryset = News.objects.filter(
                Q(title__icontains=query) |
                Q(article__icontains=query) |
                Q(location__icontains=query) |
                Q(author_id__username__icontains=query) |
                Q(author_id__first_name__icontains=query) |
                Q(author_id__last_name__icontains=query) |
                Q(category_id__category__icontains=query)
            )
            return queryset
        else:
            return News.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


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
        messages.get_messages(request).used = True
        return redirect('news_state')
    else:
        return render(request, 'edit_news.html', {'news': news, 'detail': detail, 'pictures': pictures, 'states': states})


def news_feedback(request, news_id):
    news = get_object_or_404(News, id=news_id)
    detail = News.objects.get(id = news.id)
    pictures = Picture.objects.filter(news_id=news.id)
    states = NewsState.objects.all()
    category = NewsCategory.objects.all()
    objState = NewsState.objects.get(id=2)

    if request.method == 'POST':
        titulo = request.POST.get('titleF')
        articulo = request.POST.get('articleF')
        categoria = request.POST.get('categoryF')
        ubicacion = request.POST.get('ubicacionF')
        fotos = request.FILES.getlist('photo')
        
        if categoria:
            objCategoria = NewsCategory.objects.get(id=categoria)
            #actualizacion de la tabla
            news.title = titulo
            news.article = articulo
            news.category = objCategoria
            news.location = ubicacion
            news.state = objState
            for foto in fotos:
                picture = Picture.objects.create(picture=foto, news=detail)
            news.save()
            messages.success(request, 'Noticia guardada exitosamente')
            messages.get_messages(request).used = True
            return redirect('news_state')
        else:
            messages.error(request,'Debe ingresar una categoria')
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
        messages.get_messages(request).used = True

    context = {
        'pictures': pictures,
        'news_id': news_id,
        'news': news,
        'news_detail_url': news_detail_url,
    }

    return render(request, 'edit_pictures.html', context)