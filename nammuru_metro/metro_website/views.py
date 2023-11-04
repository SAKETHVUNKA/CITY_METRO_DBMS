# from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.
def home(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render())

def card(request):
    template = loader.get_template('card.html')
    return HttpResponse(template.render())

def home_admin(request):
    template = loader.get_template('home-admin.html')
    return HttpResponse(template.render())

def home_user(request):
    template = loader.get_template('home-user.html')
    return HttpResponse(template.render())

def line_info_details(request):
    template = loader.get_template('line-info-details.html')
    return HttpResponse(template.render())

def login(request):
    template = loader.get_template('login.html')
    return HttpResponse(template.render())

def login_signin(request):
    template = loader.get_template('login-signin.html')
    return HttpResponse(template.render())

def parking(request):
    template = loader.get_template('parking.html')
    return HttpResponse(template.render())

def parking_add(request):
    template = loader.get_template('parking-add.html')
    return HttpResponse(template.render())

def parking_remove(request):
    template = loader.get_template('parking-remove.html')
    return HttpResponse(template.render())

def schedule(request):
    template = loader.get_template('schedule.html')
    return HttpResponse(template.render())

def schedule_show(request):
    template = loader.get_template('schedule-show.html')
    return HttpResponse(template.render())

def signin(request):
    template = loader.get_template('signin.html')
    return HttpResponse(template.render())

def station_info_details(request):
    template = loader.get_template('station-info-details.html')
    return HttpResponse(template.render())

def ticket_buy(request):
    template = loader.get_template('ticket-buy.html')
    return HttpResponse(template.render())

def ticket_counter(request):
    template = loader.get_template('ticket-counter.html')
    return HttpResponse(template.render())




def card_recharge(request):
    template = loader.get_template('card-recharge.html')
    return HttpResponse(template.render())

def ticket_page(request):
    template = loader.get_template('ticket.html')
    return HttpResponse(template.render())

def ticket_use(request):
    template = loader.get_template('ticket-use.html')
    return HttpResponse(template.render())

def entrance_scan(request):
    template = loader.get_template('entrance-scan.html')
    return HttpResponse(template.render())

def exit_scan(request):
    template = loader.get_template('exit-scan.html')
    return HttpResponse(template.render())

def line_info(request):
    template = loader.get_template('line-info.html')
    return HttpResponse(template.render())

def station_info(request):
    template = loader.get_template('station-info.html')
    return HttpResponse(template.render())

def show_routes(request):
    template = loader.get_template('route-show.html')
    return HttpResponse(template.render())

def show_routes_details(request):
    template = loader.get_template('route-show-details.html')
    return HttpResponse(template.render())