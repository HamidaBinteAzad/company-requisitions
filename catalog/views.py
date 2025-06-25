from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from django.db.models import Q

# Create your views here.



# 3rd update
def product_list(request):
    # Search
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')
    
    products = Product.objects.select_related('category').all()
    
    if search_query:
        products = products.filter(Q(name__icontains=search_query) | Q(sku__icontains=search_query) | Q(description__icontains=search_query))
    
    if category_filter:
        products = products.filter(category_id=category_filter)
    
    categories = Category.objects.all()
    
    context = {
        'products': products,
        'categories': categories,
        'search_query': search_query,
        'category_filter': int(category_filter) if category_filter else 0,
    }
    return render(request, 'catalog/product_list.html', context)

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'catalog/product_detail.html', context)

