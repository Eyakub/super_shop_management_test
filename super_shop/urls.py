from django.urls import include, path

from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('dashboard/', dashboard_index, name='dashboard_index'),
    path('dashboard/product-add', product_add, name='product_add'),
    path('dashboard/product-edit/<product_id>', product_edit, name='product_edit'),
    path('dashboard/product-delete/<product_id>', product_delete, name='product_delete'),
]
