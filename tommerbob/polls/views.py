from django.shortcuts import get_object_or_404, render, redirect
from django.template import loader
from django.http import Http404
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

import logging
logging.basicConfig(level=logging.INFO) # Here

from .models import *

# Create your views here.
from django.http import HttpResponse

# @login_required(login_url="login")
def index(request):
    beverage_list = Beverage.objects.all()
    context = {
        'beverage_list': beverage_list
    }

    return render(request, 'polls/index.html', context)

@login_required(login_url="/login")
def account(request):
    user = Bruger.objects.get(id=request.user.id)
    orders = Order.objects.filter(user=user.id)
    user_orders = orders.order_by('date')
    credit = user.account
    total_orders = len(orders)

    context = {
        'order_list': user_orders,
        'credit': credit,
        'total_orders': total_orders
    }

    return render(request, 'polls/orders.html', context)

@login_required(login_url="/login")
def beverage_details(request, beverage_id):
    try:
        beverage = Beverage.objects.get(pk=beverage_id)
    except Beverage.DoesNotExist:
        raise Http404("Beverage does not exist")
    return render(request, 'polls/detail.html', {'beverage': beverage})

def login_request(request, bruger_id):
    if request.method == "POST":
        logging.info("Got post request")
        username = Bruger.objects.get(pk=bruger_id).user_profile
        password = "password"
        user = authenticate(username=username, password=password)
        logging.info(user)
        if user is not None:
            login(request, user)
            logging.info(request, f"You are now logged in as {username}.")
            return redirect("/")
        else:
            logging.error(request,"Invalid username or password.")
    else:
        logging.error(request,"Invalid username or password.")

    return redirect("/")

def brugere(request):
    bruger_list = Bruger.objects.all()
    context = {
        'bruger_list': bruger_list
    }
    return render(request=request, template_name="polls/login.html", context=context)


def logout_view(request):
    logout(request)
    return redirect('/')

@login_required(login_url="/login")
def new_order(request, beverage_id):
    quantity = request.POST['amount']
    print(f"REQUEST USER ID: {request.user.id}")
    user = Bruger.objects.get(id=request.user.id)
    print(f"BRUGER OBJECT: {user.name}")
    ordered_bev = Beverage.objects.get(id=beverage_id)
    order = Order.objects.create(user=user, order = ordered_bev, 
            quantity=quantity, price=int(quantity)*ordered_bev.price)

    user.account = user.account - order.price
    user.save()

    order.save()

    return redirect("/")
