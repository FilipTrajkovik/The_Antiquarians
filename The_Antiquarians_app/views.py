from django.core.paginator import Paginator
from django.db.models import Sum, F
from django.shortcuts import render, redirect, get_object_or_404

from .decorators import unauthenticated_user, allowed_users
from .forms import CreateUserForm
from .models import *
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import *


# Create your views here.

def home(request):
    context = {}

    return render(request, "home.html", context=context)

def user_manual(request):
    context = {}

    return render(request, "user_manual.html", context=context)

@unauthenticated_user
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.add_message(request, messages.ERROR, 'Погрешно внесено кориснико име или лозинка')

    context = {}

    return render(request, "login.html", context=context)


@login_required(login_url='login_page')
def logout_user(request):
    logout(request)
    return redirect('login_page')

@unauthenticated_user
def register_page(request):
    form = CreateUserForm()
    buyer = Buyer()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='buyer')
            user.groups.add(group)
            buyer.user = user
            buyer.username = user.username
            buyer.email = user.email
            buyer.save()

            messages.add_message(request, messages.SUCCESS, 'Успешно креирана корисничка сметка за  ' + user.username)
            return redirect('login_page')

    context = {'form': form}

    return render(request, "register.html", context=context)


def products(request):
    name_filter = request.GET.get('name_filter')
    category_filter = request.GET.get('category_filter')
    model_filter = request.GET.get('model_filter')
    year_filter = request.GET.get('year_filter')

    all_products = Product.objects.all()

    if name_filter:
        all_products = all_products.filter(name__icontains=name_filter)
    if category_filter:
        all_products = all_products.filter(category__icontains=category_filter)
    if model_filter:
        all_products = all_products.filter(model__icontains=model_filter)
    if year_filter:
        all_products = all_products.filter(year__icontains=year_filter)

    paginator = Paginator(all_products, 12)
    page_number = request.GET.get('page')
    all_products = paginator.get_page(page_number)

    categories = []
    for category in Product.CATEGORY:
        categories.append(category[1])

    context = {
        "products": all_products,
        "name_filter_value": name_filter,
        "category_filter_value": category_filter,
        "model_filter_value": model_filter,
        "year_filter_value": year_filter,
        "categories": categories
    }

    return render(request, "products.html", context=context)


def product_details(request, id=0):
    antique_item = Product.objects.get(pk=id)

    quantity = request.session.get('quantity', 0)

    if request.method == 'POST':
        if 'increase_quantity' in request.POST:
            if antique_item.quantity > 0:
                quantity += 1
                antique_item.quantity -= 1
        elif 'decrease_quantity' in request.POST:
            if quantity > 0:
                quantity -= 1
                antique_item.quantity += 1

        request.session['quantity'] = quantity
        antique_item.save()

    context = {
        'antique_item': antique_item,
        'quantity': quantity,
    }

    return render(request, 'product_details.html', context)


@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admin', 'buyer'])
def add_to_shopping_cart(request):
    if request.method == "POST":
        antique_item_id = request.POST.get('antique_item_id')
        quantity = request.session.get('quantity')
        buyer = request.user.buyer
        order, created = Order.objects.get_or_create(buyer=buyer)
        antique_item = get_object_or_404(Product, pk=antique_item_id)
        order_item_exists = order.orderitem_set.filter(product=antique_item).first()

        if order_item_exists:
            order_item = order_item_exists
            order_item.quantity += quantity
            order_item.save()
        else:
            order_item = OrderItem.objects.create(product=antique_item, order=order, quantity=quantity)
            order_item.quantity = quantity
            order_item.save()

        request.session['quantity'] = 0
        return redirect("shopping_cart")
    else:
        return redirect("products")


@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admin'])
def add_product(request, id=0):
    if request.method == "POST":
        if id == 0:
            form = ProductForm(request.POST, request.FILES)
        else:
            antique_item = Product.objects.get(pk=id)
            form = ProductForm(request.POST, request.FILES, instance=antique_item)
        if form.is_valid():
            form.save()
        return redirect("products")
    else:
        if id == 0:
            form = ProductForm()
        else:
            antique_item = Product.objects.get(pk=id)
            form = ProductForm(instance=antique_item)

    context = {"form": form}

    return render(request, "add_product.html", context=context)


@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admin'])
def delete_product(request, id=0):
    antique_item = Product.objects.get(pk=id)
    antique_item.delete()

    return redirect('products')


@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admin', 'buyer'])
def shopping_cart(request):
    if request.user.is_authenticated:
        buyer = request.user.buyer
        order, created = Order.objects.get_or_create(buyer=buyer)
        shopping_cart_items = order.orderitem_set.all()

        for item in shopping_cart_items:
            item.total_price = item.product.price * item.quantity

        shopping_cart_total = order.orderitem_set.aggregate(total=Sum(F('product__price') * F('quantity')))['total']

        if shopping_cart_total is None:
            shopping_cart_total = 0

    else:
        shopping_cart_items = []
        shopping_cart_total = 0
        order = {'get_cart_total': 0, 'get_cart_items': 0}

    context = {
        "shopping_cart_items": shopping_cart_items,
        "shopping_cart_total": shopping_cart_total,
        "order": order
    }
    return render(request, "shopping_cart.html", context=context)


@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admin', 'buyer'])
def delete_shopping_cart_item(request, id=0):
    order_item = OrderItem.objects.get(pk=id)
    order_item.delete()

    return redirect('shopping_cart')


@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admin', 'buyer'])
def delete_order(request, id=0):
    order = Order.objects.get(pk=id)
    order.delete()

    return redirect('products')


@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admin', 'buyer'])
def create_order(request, id=0):
    if request.method == "POST":
        order = Order(pk=id)
        order.delete()
        return redirect('order_done')
    else:
        order = Order(pk=id)

    context = {"order": order}

    return render(request, "create_order.html", context=context)


@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admin', 'buyer'])
def order_done(request):
    context = {}

    return render(request, "order_done.html", context=context)



