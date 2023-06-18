from django.contrib import admin
from .models import *


admin.site.register(NewsCategory)
admin.site.register(NewsState)

admin.site.register(News)
admin.site.register(ContactForm)
admin.site.register(Picture)