from django.db import models
from django.contrib.auth.models import User

class NewsCategory(models.Model):
    category = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return str(self.category)

class NewsState(models.Model):
    state = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return str(self.state)
  
class News(models.Model):
    title = models.CharField(max_length=100, blank=False, null=False)
    article = models.TextField(blank=False, null=False)
    headline = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    feedback = models.TextField(blank=True, null=True)
    premium = models.BooleanField(default=False)
    location = models.CharField(max_length=40,blank=False,null=False)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    category = models.ForeignKey('NewsCategory',on_delete=models.CASCADE)
    state = models.ForeignKey('NewsState', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.title)
    
class Picture(models.Model):
    picture = models.ImageField(upload_to='')
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='images')
    principal = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

class Contacto(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    last_name = models.CharField(max_length=50, blank=False, null=False)
    email = models.EmailField(max_length=50, blank=False, null=False)
    phone = models.CharField(max_length=20, blank=False, null=False)
    comment = models.TextField(blank=False, null=False)

    def __str__(self):
        return str(self.name + ' ' + self.last_name)