from django.db import models
from django.contrib.auth.models import AbstractUser,User
# #crear permisos
# from django.contrib.auth.models import Group, Permission
# from django.contrib.contenttypes.models import ContentType

# tablaNoticia = ContentType.objects.get(app_label='core',model='News')
# periodistaG = Group.objects.get(name='Periodista')
# permiso1 = Permission(name='crear_noticia',codename='crear_noticia',content_type=tablaNoticia)
# permiso1.save()
# periodistaG.permissions.add(permiso1)
# #end crear permisos

# class UserType(models.Model):
#     type = models.CharField(max_length=50, blank=False, null=False)

#     def __str__(self):
#         return str(self.type)

class NewsCategory(models.Model):
    category = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return str(self.category)

class NewsState(models.Model):
    state = models.CharField(max_length=50, blank=False, null=False)
    feedback = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return str(self.state)

# class User_modelo(models.Model):
#     name = models.CharField(max_length=50, blank=False, null=False)
#     last_name = models.CharField(max_length=50, blank=False, null=False)
#     email = models.EmailField(max_length=50, blank=False, unique=True, null=False)
#     password = models.CharField(max_length=50, blank=False, null=False)
#     type = models.ForeignKey('UserType',on_delete=models.CASCADE)

#     def __str__(self):
#         return str(self.name + ' ' + self.last_name + ' ' + str(self.type))
    
class News(models.Model):
    title = models.CharField(max_length=100, blank=False, null=False)
    article = models.TextField(blank=False, null=False)
    photo = models.ImageField(upload_to='fotos_noticias/')
    location = models.CharField(max_length=40,blank=False,null=False)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    category = models.ForeignKey('NewsCategory',on_delete=models.CASCADE)
    state = models.ForeignKey('NewsState', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.title)

class ContactForm(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    last_name = models.CharField(max_length=50, blank=False, null=False)
    email = models.EmailField(max_length=50, blank=False, null=False)
    phone = models.IntegerField()
    comment = models.TextField(blank=False, null=False)

    def __str__(self):
        return str(self.name)