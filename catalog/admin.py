from django.contrib import admin
from .models import Category, Product

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'category', 'unit_price', 'current_stock')
    list_filter = ('category',)
    search_fields = ('name', 'sku')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)