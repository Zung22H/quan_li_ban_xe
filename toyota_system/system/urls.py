from django.urls import path
from . import views
from .models import *


urlpatterns = [
    path('', views.index, name='index'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_item/', views.updateItem, name='update_item'),
    path('register/', views.register, name='register'),
    path('login/', views.sign_in, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('category/', views.category, name='category'),
    path('search/', views.search_feature, name='search-box'),
    path('detail/', views.detail, name='detail'),
    path('infomation/', views.infomation, name='infomation'),
]