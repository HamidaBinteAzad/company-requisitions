from django.urls import path
from . views import *

urlpatterns = [
    # path("catalog/", include('catalog.urls')),
    path('product_list', product_list, name='product_list'),
    path('detail<int:id>/', product_detail, name='product_detail'),
]
