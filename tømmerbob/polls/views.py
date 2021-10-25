from django.shortcuts import get_object_or_404, render, redirect
from django.template import loader
from django.http import Http404
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

from .models import *

# Create your views here.
from django.http import HttpResponse

def home(request):
    return render(request, 'polls/home.html')

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

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("/")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="polls/login.html", context={"login_form":form})

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
