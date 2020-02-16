from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product
from django.contrib.auth.models import User, auth
from django.contrib.auth import login, logout
from .models import Contact, Orders, OderUpdate
from django.contrib import messages
from math import ceil
import json

# Create your views here.


def index(request):
    allProds = []
    catProds = Product.objects.values('category')
    cats = {item['category'] for item in catProds}

    for cat in cats:
        Prod = Product.objects.filter(category=cat)
        n = len(Prod)
        nOfSlides = n//4 + ceil((n/4)-n//4)
        allProds.append([Prod, range(1, nOfSlides), nOfSlides])

    params = {'allProds': allProds}

    return render(request, 'shop/index.html', params)


# Search Page Logic
def searchMatch(query,item):
    if (query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower()):
        return True
    else:
        return False

def search(request):

    allProds = []
    catProds = Product.objects.values('category')
    cats = {item['category'] for item in catProds}

    for cat in cats:
        query = request.GET.get('search')
        Prodtemp = Product.objects.filter(category=cat)
        Prod = [item for item in Prodtemp if searchMatch(query,item)]
        n = len(Prod)
        nOfSlides = n//4 + ceil((n/4)-n//4)
        if len(Prod) != 0:
            allProds.append([Prod, range(1, nOfSlides), nOfSlides])

    params = {'allProds': allProds}

    return render(request, 'shop/search.html/', params)



def about(request):
    return render(request, 'shop/about.html')

# Contact Page Logic


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contacts = Contact(name=name, email=email, phone=phone, desc=desc)
        contacts.save()
    return render(request, 'shop/contact.html')

# Tracker Page Logic


def tracker(request):

    if request.method == 'POST':
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')

        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order) > 0:
                update = OderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append( {'text': item.update_desc, 'time': item.timeStmp})
                    reponse = json.dumps({"status":"success","updates":updates,"itemJson":order[0].item_json} ,default=str)
                return HttpResponse(reponse)
            else:
                return HttpResponse('{"status":"No Item"}') 
        except Exception as e:
            return HttpResponse('{"status":"error"}')    
    return render(request, 'shop/tracker.html')


# Product Page Logic


def product(request, product_id):
    products = Product.objects.filter(product_id=product_id)
    return render(request, 'shop/product.html', {'Product': products[0]})


# Checkout Page Logic


def checkout(request):
    if request.method == 'POST':
        itemsJson = request.POST.get('itemsjson', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        adderss = request.POST.get('address', '') + \
            '' + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('state', '')

        order = Orders(item_json=itemsJson, name=name, email=email, address=adderss,
                       city=city, state=state, zip_code=zip_code)
        order.save()
        update = OderUpdate(order_id=order.order_id,
                            update_desc="Your Order hass Ben Placed")
        update.save()
        thank=True
        id = order.order_id
        return render(request, 'shop/checkout.html',{"thank":thank,'id':id})
    return render(request, 'shop/checkout.html')

# Login Page Logic

def getlogin(request):

    if request.user.is_authenticated:
        return redirect('/shop/userprofile/')
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['pass']

            user = auth.authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('/shop/userprofile/')
            else:
                messages.error(request, 'Invalid User')
                return redirect('/shop/login/')

        else:
            return render(request, 'shop/login.html')

# Register Page Logic


def register(request):
    if request.method == "POST":
        first_name = request.POST['name1']
        last_name = request.POST['name2']
        username = request.POST['username']
        password1 = request.POST['pass1']
        password2 = request.POST['pass2']
        email = request.POST['email']

        if password1 == password2:

            if User.objects.filter(email=email).exists():
                messages.error(request, "Email Already Exists")
                return redirect('/shop/register/')

            elif User.objects.filter(username=username).exists():
                messages.error(request, "This Already Exists")
                return redirect('/shop/register/')

            else:
                users = User.objects.create_user(
                    username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
                users.save()
                return redirect('/shop/login/')
        else:
            messages.error(request, "Use a Same Password")
            return redirect('/shop/register/')

    else:
        return render(request, 'shop/register.html')

# UserProfile Page Logic


def userprofile(request):
    return render(request, 'shop/profile.html')

# Logout Page Logic

def getlogout(request):
    logout(request)
    return redirect('/shop/')
