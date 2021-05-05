from django.urls import include, path

from .views import dashboard_index, index

urlpatterns = [
    path('', index, name='index'),
    path('dashboard/', dashboard_index, name='dashboard_index'),
]
