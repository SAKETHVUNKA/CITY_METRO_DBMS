# from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import *
from .models import *
from .utils import *
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
import math
import base64
from datetime import datetime

# Create your views here.
def home(request):
    logout(request)
    return render(request, 'home.html')

def card(request):
    user_id = request.user.username
    cardDetes = fetch_card_details_by_user_id(user_id)
    lastTrip = get_most_recent_ticket(user_id)

    lastRechargeTime = str(cardDetes.Last_Recharge_Time[0])
    lastRechargeTime = datetime.fromisoformat(lastRechargeTime)
    lastRechargeTime = lastRechargeTime.strftime("%B %d, %Y %I:%M %p")

    if lastTrip.empty:
        return render(request, 'card.html', {'cardDetes': cardDetes,'lastTrip':lastTrip, 'lastRechargeTime':lastRechargeTime, 'lastStart':None, 'lastEnd':None})
    
    return render(request, 'card.html', {'cardDetes': cardDetes,'lastTrip':lastTrip, 'lastRechargeTime':lastRechargeTime,'lastStart':stationReverseMappings[lastTrip.Start_Station[0]],'lastEnd':stationReverseMappings[lastTrip.End_Station[0]]})

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
    # insert_parking(' JYN', request.user.username, "KA 06", 99)
    parkingDf = fetch_parking_details(request.user.username)

    print(parkingDf)

    if parkingDf.empty or parkingDf.Status[0] == 0:
        return render(request, 'parking.html', {'parkingDf': None})
    
    parkingTime = str(parkingDf.TimeStamp[0])
    parkingTime = datetime.fromisoformat(parkingTime)
    parkingTime = parkingTime.strftime("%B %d, %Y %I:%M %p")

    qr_code_bytes = parkingDf.QR_Code[0]
    qr_code_base64 = base64.b64encode(qr_code_bytes).decode('utf-8')

    return render(request, 'parking.html', {'parkingDf':parkingDf, 'StationName':stationReverseMappings[parkingDf.Station_id[0]], 'qr_code_base64': qr_code_base64, 'parkingTime':parkingTime})

def parking_add(request):
    return render(request, 'parking-add.html')

def parking_remove(request):
    return render(request, 'parking-remove.html')

def schedule(request):
    return render(request, 'schedule.html')

def schedule_show(request):
    return render(request, 'schedule-show.html')

def ticket_buy(request):
    if request.method == 'POST':
        form = TicketBuyForm(request.POST)
        if form.is_valid():
            fromStation = form.cleaned_data['start_station']
            toStation = form.cleaned_data['end_station']

            routeDetes = find_routes(fromStation, toStation)
            ticketPrice = math.ceil(float(routeDetes.price[0]) * 0.95)

            cardDetes = fetch_card_details_by_user_id(request.user.username)
            card_ID = cardDetes.Card_ID[0]

            if check_balance(ticketPrice, card_ID):
                res = insert_ticket(ticketPrice, stationMappings[fromStation], stationMappings[toStation], "card", card_ID)
                print(res)
                return redirect("/home_user")
            else:
                form.add_error(None, 'Insufficient Balance')


    else:
        form = TicketBuyForm()
    return render(request, 'ticket-buy.html', {'form':form})

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
    ticket = get_most_recent_ticket(request.user.username)

    print(ticket.Exit_Time[0])

    if ticket.empty or ticket.Exit_Time[0]:
        return render(request, 'ticket-use.html', {'ticket':None})

    startStation = stationReverseMappings[ticket.Start_Station[0]]
    endStation = stationReverseMappings[ticket.End_Station[0]]

    qr_code_bytes = ticket.QR_Code[0]
    qr_code_base64 = base64.b64encode(qr_code_bytes).decode('utf-8')

    print(qr_code_bytes)
    return render(request, 'ticket-use.html', {'ticket':ticket, 'startStation':startStation, 'endStation':endStation, 'qr_code_base64': qr_code_base64})

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