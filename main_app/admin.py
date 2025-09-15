from django.contrib import admin

# Register your models here.
from .models import Category,Watch

admin.site.register(Category)
admin.site.register(Watch)