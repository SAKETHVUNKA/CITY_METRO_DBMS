from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # path('home', views.home, name='home'),
    path('card/', views.card, name='card'),
    path('home_admin/', views.home_admin, name='home_admin'),
    path('home_user/', views.home_user, name='home_user'),
    path('line_info_details/', views.line_info_details, name='line_info_details'),
    path('register/', views.register_user, name='register_user'),
    path('login/', views.user_login, name='user_login'),
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
    path('card_recharge/', views.card_recharge, name='card_recharge'),
    path('ticket_page/', views.ticket_page, name='ticket_page'),
    path('ticket_use/', views.ticket_use, name='ticket_use'),
    path('entrance_scan/', views.entrance_scan, name='entrance_scan'),
    path('exit_scan/', views.exit_scan, name='exit_scan'),
    path('line_info/', views.line_info, name='line_info'),
    path('station_info/', views.station_info, name='station_info'),
    path('show_routes/', views.show_routes, name='show_routes'),
    path('show_routes_details/', views.show_routes_details, name='show_routes_details'),
]

LOGIN_URL = 'login'
LOGOUT_URL = 'logout'