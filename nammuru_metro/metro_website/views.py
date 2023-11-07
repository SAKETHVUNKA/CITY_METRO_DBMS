# from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import *
from .models import CustomUser
from .utils import *


from django.contrib.auth.hashers import check_password

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

def login(request):
    template = loader.get_template('login.html')
    return HttpResponse(template.render())

def register_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Check if passwords match
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            if password1 == password2:
                username = form.cleaned_data['username']
                phone = form.cleaned_data['phone']

                # Create the user and set the password
                user = CustomUser.objects.create_user(username=username, password=password1, phone=phone)

                # Additional logic, e.g., login the user or redirect to a dashboard page on successful registration
                # You can add a login session here if you want to automatically log in the user after registration.

                # Redirect to a success page or dashboard after registration
                return redirect('home_user')  # Adjust 'dashboard' to your actual URL name
            else:
                # Passwords don't match, handle the error
                form.add_error('password1', 'Passwords do not match')

    else:
        form = RegistrationForm()

    return render(request, 'signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                user = CustomUser.objects.get(username=username)
                # print(user)  # Debugging
            except CustomUser.DoesNotExist:
                user = None

            if user and check_password(password, user.password):
                # print("Passwords match!")  # Debugging
                # Passwords match, so log in the user
                request.session['user_id'] = user.id  # You can store the user's ID in the session
                return redirect('home_user')  # Redirect to a dashboard page on successful login
            else:
                print("Passwords don't match!")  # Debugging
                # Passwords don't match, you can handle this by adding an error message
                form.add_error(None, 'Invalid username or password')

    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

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
    if request.method == 'POST':
        form = LineForm(request.POST)
        if form.is_valid():
            selected_option = form.cleaned_data['from_choice']

            lineDetes, stationList = getLineInfo(selected_option)
            stationList = stationList['Station_Name'].tolist()

            return render(request, 'line-info-details.html', {'lineDetes': lineDetes, 'stationList':stationList})
    else:
        form = LineForm()

    return render(request, 'line-info.html', {'form': form})

def station_info(request):
    if request.method == 'POST':
        form = StationForm(request.POST)
        if form.is_valid():
            selected_option = form.cleaned_data['from_choice']
            print(selected_option)

            stationDetes = getStationInfo(selected_option)

            return render(request, 'station-info-details.html', {'stationDetes': stationDetes})
    else:
        form = StationForm()

    return render(request, 'station-info.html', {'form': form})

def show_routes(request):
    if request.method == 'POST':
        form = RouteForm(request.POST)
        if form.is_valid():
            entry_option = form.cleaned_data['entry_choice']
            exit_option = form.cleaned_data['exit_choice']
            
            print(entry_option, exit_option)

            routeDetes = find_routes(entry_option, exit_option)
            routeDetes = routeDetes.to_dict(orient='records')

            print(routeDetes)

            return render(request, 'route-show-details.html', {'routeDetes': routeDetes})
    else:
        form = RouteForm()

    return render(request, 'route-show.html', {'form': form})