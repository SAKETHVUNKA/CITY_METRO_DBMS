# from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import *
from .models import CustomUser
from .utils import *
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User

# Create your views here.
def home(request):
    logout(request)
    return render(request, 'home.html')

def card(request):
    user_id = request.user.username
    cardDetes = fetch_card_details_by_user_id(user_id)
    lastTrip = get_most_recent_ticket(user_id)
    return render(request, 'card.html', {'cardDetes': cardDetes,'lastTrip':lastTrip})

def home_admin(request):
    return render(request, 'home-admin.html')

def home_user(request):
    return render(request, 'home-user.html')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                # User credentials are valid, log in the user
                login(request, user)
                return redirect('home_user')  # Redirect to a dashboard page on successful login
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Check if passwords match
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            if password1 == password2:
                username = form.cleaned_data['username']
                phone = form.cleaned_data['phone']

                user = User.objects.create_user(username=username, password=password1)

                user = authenticate(request, username=username, password=password1)

                if user is not None:
                    login(request, user)

                    insert_user_and_rider_card(username, password1, phone)

                    return redirect('home_user') 
                else:
                    print(f"Authentication failed for username: {username}")

    else:
        form = RegistrationForm()

    return render(request, 'signup.html', {'form': form})


def login_signin(request):
    return render(request, 'login-signin.html')

def parking(request):
    return render(request, 'parking.html')

def parking_add(request):
    return render(request, 'parking-add.html')

def parking_remove(request):
    return render(request, 'parking-remove.html')

def schedule(request):
    return render(request, 'schedule.html')

def schedule_show(request):
    return render(request, 'schedule-show.html')

def ticket_buy(request):
    return render(request, 'ticket-buy.html')

def ticket_counter(request):
    return render(request, 'ticket-counter.html')

def card_recharge(request):
    if request.method == 'POST':
        form = RechargeForm(request.POST)
        if form.is_valid():
            rechargeAmt = form.cleaned_data['amount']

            cardDetes = fetch_card_details_by_user_id(request.user.username)
            card_ID = cardDetes.Card_ID[0]

            increment_card_balance(card_ID, rechargeAmt)

            return redirect("/home_user")
    else:
        form = RechargeForm()

    return render(request, 'card-recharge.html', {'form': form})

def ticket_page(request):
    return render(request, 'ticket.html')

def ticket_use(request):
    return render(request, 'ticket-use.html')

def entrance_scan(request):
    return render(request, 'entrance-scan.html')

def exit_scan(request):
    return render(request, 'exit-scan.html')

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

            routeDetes = find_routes(entry_option, exit_option)
            routeDetes = routeDetes.to_dict(orient='records')

            return render(request, 'route-show-details.html', {'routeDetes': routeDetes})
    else:
        form = RouteForm()

    return render(request, 'route-show.html', {'form': form})