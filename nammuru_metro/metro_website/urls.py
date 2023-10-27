from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('card/', views.card, name='card'),
    path('home_admin/', views.home_admin, name='home_admin'),
    path('home_user/', views.home_user, name='home_user'),
    path('line_info_details/', views.line_info_details, name='line_info_details'),
    path('login/', views.login, name='login'),
    path('login_signin/', views.login_signin, name='login_signin'),
    path('parking/', views.parking, name='parking'),
    path('parking_add/', views.parking_add, name='parking_add'),
    path('parking_remove/', views.parking_remove, name='parking_remove'),
    path('schedule/', views.schedule, name='schedule'),
    path('schedule_show/', views.schedule_show, name='schedule_show'),
    path('signin/', views.signin, name='signin'),
    path('station_info_details/', views.station_info_details, name='station_info_details'),
    path('ticket_buy/', views.ticket_buy, name='ticket_buy'),
    path('ticket_counter/', views.ticket_counter, name='ticket_counter'),
]