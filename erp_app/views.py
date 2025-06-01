from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.http import JsonResponse
from .models import *
import json


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    # Dashboard statistics
    total_products = Product.objects.count()
    low_stock_items = Product.objects.filter(status='low_stock').count()
    pending_orders = Order.objects.filter(status='pending').count()
    total_customers = Customer.objects.count()

    # Recent products
    recent_products = Product.objects.all()[:10]

    context = {
        'total_products': total_products,
        'low_stock_items': low_stock_items,
        'pending_orders': pending_orders,
        'total_customers': total_customers,
        'recent_products': recent_products,
        'page_title': 'Dashboard',
    }
    return render(request, 'dashboard.html', context)


@login_required
def products(request):
    products_list = Product.objects.all()
    search_query = request.GET.get('search', '')

    if search_query:
        products_list = products_list.filter(
            Q(name__icontains=search_query) |
            Q(sku__icontains=search_query)
        )

    context = {
        'products': products_list,
        'search_query': search_query,
        'page_title': 'Products',
    }
    return render(request, 'products.html', context)


@login_required
def customers(request):
    # Customer statistics
    total_customers = Customer.objects.count()
    new_customers = Customer.objects.filter(segment='new').count()
    vip_customers = Customer.objects.filter(segment='vip').count()
    total_revenue = Customer.objects.aggregate(Sum('total_spent'))['total_spent__sum'] or 0

    # Customer list
    customers_list = Customer.objects.all()
    search_query = request.GET.get('search', '')

    if search_query:
        customers_list = customers_list.filter(
            Q(name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(customer_id__icontains=search_query)
        )

    context = {
        'total_customers': total_customers,
        'new_customers': new_customers,
        'vip_customers': vip_customers,
        'total_revenue': total_revenue,
        'customers': customers_list,
        'search_query': search_query,
        'page_title': 'Customers',
    }
    return render(request, 'customers.html', context)


@login_required
def inventory(request):
    # Inventory statistics
    total_inventory_value = Product.objects.aggregate(
        total=Sum('price') * Sum('stock_quantity')
    )['total'] or 0
    low_stock_alerts = Product.objects.filter(status='low_stock').count()
    total_skus = Product.objects.count()

    # Inventory details
    inventory_items = Inventory.objects.all()

    context = {
        'total_inventory_value': total_inventory_value,
        'low_stock_alerts': low_stock_alerts,
        'total_skus': total_skus,
        'inventory_items': inventory_items,
        'page_title': 'Inventory Management',
    }
    return render(request, 'inventory.html', context)


@login_required
def orders(request):
    orders_list = Order.objects.all().order_by('-created_at')

    # Calculate order statistics
    total_orders = orders_list.count()
    pending_orders = orders_list.filter(status='pending').count()
    completed_orders = orders_list.filter(status='delivered').count()
    total_revenue = orders_list.aggregate(Sum('total_amount'))['total_amount__sum'] or 0

    context = {
        'orders': orders_list,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'completed_orders': completed_orders,
        'total_revenue': total_revenue,
        'page_title': 'Orders',
    }
    return render(request, 'orders.html', context)


@login_required
def users(request):
    # User statistics
    total_users = User.objects.count()
    administrators = UserProfile.objects.filter(role='admin').count()
    managers = UserProfile.objects.filter(role='manager').count()
    warehouse_staff = UserProfile.objects.filter(role='warehouse_staff').count()

    # User list
    users_list = User.objects.all()

    context = {
        'total_users': total_users,
        'administrators': administrators,
        'managers': managers,
        'warehouse_staff': warehouse_staff,
        'users': users_list,
        'page_title': 'User Management',
    }
    return render(request, 'users.html', context)


@login_required
def settings(request):
    context = {
        'page_title': 'Settings',
    }
    return render(request, 'settings.html', context)


@login_required
def notifications(request):
    notifications_list = Notification.objects.all()
    unread_count = notifications_list.filter(is_read=False).count()
    urgent_count = notifications_list.filter(priority='urgent').count()

    context = {
        'notifications': notifications_list,
        'unread_count': unread_count,
        'urgent_count': urgent_count,
        'page_title': 'Notifications',
    }
    return render(request, 'notifications.html', context)


@login_required
def analytics(request):
    # Analytics data
    total_revenue = Order.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    total_orders = Order.objects.count()
    products_sold = OrderItem.objects.aggregate(Sum('quantity'))['quantity__sum'] or 0
    active_customers = Customer.objects.filter(total_orders__gt=0).count()

    context = {
        'total_revenue': total_revenue,
        'total_orders': total_orders,
        'products_sold': products_sold,
        'active_customers': active_customers,
        'page_title': 'Analytics Dashboard',
    }
    return render(request, 'analytics.html', context)