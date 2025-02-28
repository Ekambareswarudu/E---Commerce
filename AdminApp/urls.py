from django.urls import path
from AdminApp import views
urlpatterns = [

    path('', views.index),
    path('login', views.login),
    path('loginaction', views.loginaction),
    path('AdminHome', views.AdminHome),
    path('AddCategory', views.AddCategory),
    path('categoryAction', views.categoryAction),
    path('UploadProducts', views.UploadProducts),
    path('productAction', views.productAction),
    path('ViewProducts', views.ViewProducts),
    path('viewImage', views.viewImage),
]
