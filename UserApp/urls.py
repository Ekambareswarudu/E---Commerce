from django.urls import path
from UserApp import views
urlpatterns = [

    path('login', views.login),
    path('register', views.register),
    path('regaction', views.regaction),
    path('loginaction', views.loginaction),
    path('UserHome', views.UserHome),
    path('Profile', views.Profile),
    path('Search', views.Search),
    path('SearchProduct', views.SearchProduct),
    path('BuyProduct', views.BuyProduct),
    path('BuyAction', views.BuyAction),
    path('viewImage', views.viewImage),
    path('ViewBookedProducts', views.ViewBookedProducts),


]
