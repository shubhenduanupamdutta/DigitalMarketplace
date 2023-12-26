from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('products/<int:id>/', views.detail, name='detail'),
    path('success/', views.payment_success_view, name='success'),
    path('failed/', views.payment_failed_view, name='failed'),
    path('api/checkout-session/<int:id>/', views.create_checkout_session, name='stripe_checkout'),
    path('create-product/', views.create_product, name='create_product'),
    path('edit-product/<int:id>/', views.edit_product, name='edit_product'),
    path('delete/<int:id>/', views.delete_product, name='delete_product'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name="myapp/login.html"), name='login'),
    path('logout/',
         auth_views.LogoutView.as_view(template_name="myapp/logout.html"), name='logout'),
    path('invalid/', views.invalid, name='invalid'),
    path('purchases/', views.my_purchases, name='purchases'),
    path('sales/', views.sales, name='sales'),
]
