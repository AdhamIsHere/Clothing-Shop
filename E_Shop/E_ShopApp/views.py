from django.shortcuts import render, redirect
from django.contrib.auth import login , logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
import json
from django.contrib import messages
from .forms import UserRegisterForm

from .models import *

# Create your views here.
def home_view(request):
    products = Product.objects.all()
    return render(request, 'home.html',{'products':products})


def signup_view(request):
    error_msg=None
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully')
            return redirect('home')
        else:
            error_msg =form.errors
    else:
        form = UserRegisterForm()
    
    return render(request, 'signup.html', {'form': form, 'error': error_msg})

def login_view(request):
    error_msg=None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error_msg = 'Invalid credentials'
    return render(request, 'login.html',{'error': error_msg})

@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login') 
    return redirect('home')

def GetOrSetProductCache(id):
    cache_key = f'product:{id}'
    cached_product = cache.get(cache_key)
    if cached_product:
        print("Cache hit for product:", id)
        return cached_product
    else:
        print("Cache miss for product:", id)
        try:
            product = Product.objects.get(id=id)
            cache.set(cache_key, product, timeout=60*15)  # Cache for 15 minutes
            return product
        except Product.DoesNotExist:
            return None

def product_details_view(request, id):

    product = GetOrSetProductCache(id)
    return render(request, 'product_details.html',{'product':product})


def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Get the user profile information
    user = request.user
    
    # Get cart statistics
    cart = request.session.get('cart', {})
    cart_items_count = sum(cart.values()) if cart else 0
    
    # Calculate total spent from past orders
    profile = Profile.objects.filter(user=user).first()
    
    from decimal import Decimal
    total_spent = Decimal('0.00')
    orders_count = 0
    
    if profile:
        orders = Order.objects.filter(user=profile)
        orders_count = orders.count()
        
        # Calculate total spent from all orders
        for order in orders:
            for order_item in order.items.all():
                total_spent += order_item.product.price * order_item.quantity
    
    context = {
        'profile': profile,
        'cart_items': cart_items_count,
        'total_spent': f"{total_spent:.2f}",
        'orders_count': orders_count,
        'order_history': Order.objects.filter(user=profile) if profile else []
    }
    return render(request, 'profile.html', context)

@login_required
def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0

    for product_id, quantity in cart.items():
        try:
            product = GetOrSetProductCache(int(product_id))
            if product:
                cart_items.append({
                    'product': product,  
                    'quantity': quantity,
                    'item_total': product.price * quantity
                })
                total_price += product.price * quantity
        except (Product.DoesNotExist, ValueError):
            continue

    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})


def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id = str(product_id)  
    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1
    request.session['cart'] = cart
    request.session.modified = True
    product = GetOrSetProductCache(product_id)
    messages.success(request, f'{product.name} added to cart successfully')
    # stay on the same page after adding to cart
    return redirect(request.META.get('HTTP_REFERER', 'home'))


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id = str(product_id)
    product= GetOrSetProductCache(product_id)
    if product_id in cart:
        del cart[product_id]
        request.session['cart'] = cart
        request.session.modified = True
        messages.success(request, f'{product.name} removed from cart successfully')
    else:
        messages.error(request, f'{product.name} not found in cart')
    return redirect('cart')

def increase_quantity(request, product_id):
    cart = request.session.get('cart', {})
    product_key = str(product_id)
    
    if product_key in cart:
        cart[product_key] += 1
        request.session['cart'] = cart
        request.session.modified = True
        product = GetOrSetProductCache(product_id)
        messages.success(request, f'{product.name} quantity increased')
    
    return redirect('cart')

def decrease_quantity(request, product_id):
    cart = request.session.get('cart', {})
    product_key = str(product_id)
    product = GetOrSetProductCache(product_id)
    if product_key in cart:
        if cart[product_key] > 1:
            cart[product_key] -= 1
            messages.success(request, f'{product.name} quantity decreased')
        else:
            del cart[product_key]
            messages.success(request, f'{product.name} removed from cart')
        
        request.session['cart'] = cart
        request.session.modified = True
    
    return redirect('cart')

def checkout_view(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Please login to checkout')
        return redirect('login')
    
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, 'Your cart is empty')
        return redirect('cart')
    
    cart_items = []
    total_price = 0
    
    # Calculate cart items and total
    for product_id, quantity in cart.items():
        try:
            product = GetOrSetProductCache(int(product_id))
            if product:
                item_total = product.price * quantity
                cart_items.append({
                    'product': product,
                    'quantity': quantity,
                    'item_total': item_total
                })
                total_price += item_total
        except (Product.DoesNotExist, ValueError):
            continue
    
    # Get or create user profile
    profile = Profile.objects.filter(user=request.user).first()
    
    if request.method == 'POST':
        # Handle checkout form submission
        profile.phone = request.POST.get('phone', '')
        profile.country = request.POST.get('country', '')
        profile.city = request.POST.get('city', '')
        profile.address = request.POST.get('address', '')
        profile.save()
        
        # Here you would typically:
        # 1. Create an Order object
        order = Order.objects.create(user=profile, status='P')
        for item in cart_items:
            order_item = OrderItem.objects.create(product=item['product'], quantity=item['quantity'])
            order.items.add(order_item)
            
        order.save()
        # 2. Process payment
        # 3. Clear the cart
        # For now, we'll just clear the cart and show success
        
        request.session['cart'] = {}
        request.session.modified = True
        
        messages.success(request, 'Order placed successfully! Thank you for your purchase.')
        return redirect('home')
    
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'profile': profile,
    }
    return render(request, 'checkout.html', context)
   