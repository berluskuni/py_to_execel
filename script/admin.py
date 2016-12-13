from django.contrib import admin
from .models import Product

# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'number_catalog', 'name_detail', 'price', 'brand', 'time_shipping']

admin.site.register(Product, ProductAdmin)
