from django.urls import path
from . import views

from django.conf.urls import url
# from django.contrib import admin

urlpatterns = [
    path('',views.homepage, name = 'home'),
    path('register/',views.register_page, name='register'),
    path('login/',views.login_page,name='login'),
    path('logout/',views.logoutUser,name='logout'),
    path('places/<str:name>/',views.iternary,name='iternary'),
    path('home/<str:tagname>/',views.tagPackage,name='tagPackage'),
    path('mytrips/',views.prevTrip,name='myTrips'),
    path('booknow/',views.bookNow,name='bookNow'),
    path('buycoins/',views.buyCoin,name='buyCoin'),
    path('paymentSucessful/',views.paymentSuccess,name='paymentSuccess'),
    path('buyextracoins/',views.buyExtraCoins,name = 'buyExtraCoins'),
    path('contact/',views.contact,name='contact'),
    path('tracking/',views.tracking,name='tracking'),
    path('leftovercoins/',views.leftovercoins,name='leftovercoins'),
    path('previousTrips/',views.previousTrips,name='previousTrips'),
    path('futureTrips/',views.futureTrips,name='futureTrips'),
    path('transaction/', views.transaction, name='transaction'),
    path('blockchain/', views.blockchain, name='blockchain'),

]