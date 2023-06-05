from django.contrib import admin
from .models import *

admin.site.register(UserType)
admin.site.register(NewsCategory)
admin.site.register(NewsState)
admin.site.register(User)
admin.site.register(News)
admin.site.register(ContactForm)