import json
from django.http import HttpResponse,JsonResponse
from django.template import loader
from .models import *
from .forms import SignUpForm, LoginForm
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.shortcuts import render, redirect



def detail(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer)
        items = order.orderdetail_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_items']
    id = request.GET.get('id','')
    car = Car.objects.filter(id=id)
    categories = Category.objects.filter(is_sub=False)
    active_category = request.GET.get('category', '')
    context = {"car": car,"active_category": active_category,"categories": categories,"items": items, "order": order, "cartItems": cartItems}
    template = loader.get_template('system/car_detail.html')
    return HttpResponse(template.render(context, request))

def search_feature(request):
    if request.method == 'POST':
        search_query = request.POST['search_query']
        posts = Car.objects.filter(nameCar__contains=search_query)
       

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer)
        items = order.orderdetail_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_items']
    categories = Category.objects.filter(is_sub = False)
    active_category = request.GET.get('category','')
    cars = Car.objects.all()
    context = {"active_category": active_category,"categories": categories,"cars": cars, "cartItems": cartItems,'search_query':search_query, 'posts':posts}
    return render(request, 'system/search_result.html',context)


def category(request):
    categories = Category.objects.filter(is_sub = False)
    active_category = request.GET.get('category','')
    if active_category:
        cars = Car.objects.filter(category__slug = active_category)
    else:
        cars = ''
    p = Car.objects.all()

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer)
        items = order.orderdetail_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_items']
    context = {'p':p,'categories': categories, 'cars':cars,'active_category':active_category, "cartItems": cartItems}
    return render(request,'system/category.html',context)


def sign_in(request):

    if request.method == 'GET':
        form = LoginForm()
        return render(request,'system/login.html', {'form': form})
    
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request,username=username,password=password)
            if user:
                login(request, user)
                messages.success(request,f'Hi {username.title()}, welcome back!')
                return redirect('/')
        
        # form is not valid or user is not authenticated
        messages.error(request,f'Invalid username or password')
        return render(request,'system/login.html',{'form': form})

def register(request):
    form = SignUpForm()

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/login/")

    context = {"form": form}
    template = loader.get_template('system/register.html')
    return HttpResponse(template.render(context,request))

def logout_view(request):
  logout(request)

  return redirect('login')

def index(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer)
        items = order.orderdetail_set.all()
        cartItems = order.get_cart_items

    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_items']

    cars = Car.objects.all()
    categories = Category.objects.filter(is_sub = False)
    active_category = request.GET.get('category','')
    context = {"active_category": active_category,"categories": categories,"cars": cars, "cartItems": cartItems}

    template = loader.get_template('system/index.html')
    return HttpResponse(template.render(context,request))


def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer)
        items = order.orderdetail_set.all()
        print(items)
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_items']
    categories = Category.objects.filter(is_sub=False)
    active_category = request.GET.get('category', '')
    context = {"active_category": active_category,"categories": categories,"items": items, "order": order, "cartItems": cartItems}
    template = loader.get_template('system/cart.html')
    return HttpResponse(template.render(context, request))


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer)
        items = order.orderdetail_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_items']

    categories = Category.objects.filter(is_sub=False)
    active_category = request.GET.get('category', '')
    context = {"active_category": active_category,"categories": categories,"items": items, "order": order, "cartItems": cartItems}
    template = loader.get_template('system/checkout.html')
    return HttpResponse(template.render(context, request))


def updateItem(request):
    data = json.loads(request.body)
    print(data)
    carId = data['productId']
    action = data['action']
    if not carId or not action:
            return JsonResponse({'error': 'Invalid data'}, status=400)
    customer = request.user
    car = Car.objects.get(id=carId)
    order, created = Order.objects.get_or_create(customer=customer)
    orderItem, created = OrderDetail.objects.get_or_create(order=order, car=car)
    if action == 'add':
        orderItem.quantity +=1
    elif action == 'remove':
        orderItem.quantity -=1
    orderItem.save()
    if orderItem.quantity <=0:
        orderItem.delete()
    return JsonResponse('added',safe=False)

def infomation(request):
    template = loader.get_template('system/infomation.html')
    info = request.user
    categories = Category.objects.filter(is_sub = False)
    active_category = request.GET.get('category','')
    context = {
        "info": info,
        'categories': categories,
        'active_category':active_category
    }
    return render(request, 'system/infomation.html', context)
