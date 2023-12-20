from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('products/<int:id>', views.detail, name='detail'),
]
