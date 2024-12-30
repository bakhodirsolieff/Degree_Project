from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.db import models
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.db.models.functions import TruncMonth
from django.db.models import Count

import json

from plugin.paginate_queryset import paginate_queryset
from store import models as store_models
from vendor import models as vendor_models

def get_monthly_sales():
    monthly_sales = (
        store_models.OrderItem.objects
        .annotate(month=TruncMonth('date')) 
        .values('month') 
        .annotate(order_count=Count('id')) 
        .order_by('month')
    )
    return monthly_sales 

@login_required
def dashboard(request):
    products = store_models.Product.objects.filter(vendor=request.user)
    orders = store_models.Order.objects.filter(vendors=request.user, payment_status="Paid")
    revenue = store_models.OrderItem.objects.filter(vendor=request.user).aggregate(total = models.Sum("total"))['total']
    notis = vendor_models.Notifications.objects.filter(user=request.user, seen=False)
    reviews = store_models.Review.objects.filter(product__vendor=request.user)
    rating = store_models.Review.objects.filter(product__vendor=request.user).aggregate(avg = models.Avg("rating"))['avg']
    monthly_sales = get_monthly_sales()
 
    labels = [sale['month'].strftime('%B %Y') for sale in monthly_sales]   
    data = [sale['order_count'] for sale in monthly_sales]


    context = {
        "products": products,
        "orders": orders,
        "revenue": revenue,
        "notis": notis,
        "reviews": reviews,
        "rating": rating,
        "labels": json.dumps(labels),
        "data": json.dumps(data),
    }

    return render(request, "vendor/dashboard.html", context)

@login_required
def products(request):
    products_list = store_models.Product.objects.filter(vendor=request.user)
    products = paginate_queryset(request, products_list, 10)

    context = {
        "products": products,
        "products_list": products_list,
    }
    return render(request, "vendor/products.html", context)

@login_required
def orders(request):
    orders = store_models.Order.objects.filter(vendors=request.user, payment_status="Paid")
    
    #orders = paginate_queryset(request, orders_list, 10)

    context = {
        "orders": orders,
        #"orders_list": orders_list,
    }

    return render(request, "vendor/orders.html", context)

@login_required
def order_detail(request, order_id):
    order = store_models.Order.objects.get(vendors=request.user, order_id=order_id, payment_status="Paid")

    context = {
        "order": order,
    }

    return render(request, "vendor/order_detail.html", context)

@login_required
def order_item_detail(request, order_id, item_id):
    order = store_models.Order.objects.get(vendors=request.user, order_id=order_id, payment_status="Paid")
    item = store_models.OrderItem.objects.get(item_id=item_id, order=order)
    context = {
        "order": order,
        "item": item,
    }
    return render(request, "vendor/order_item_detail.html", context)

@login_required
def update_order_status(request, order_id):
    order = store_models.Order.objects.get(vendors=request.user, order_id=order_id, payment_status="Paid")
    
    if request.method == "POST":
        order_status = request.POST.get("order_status")
        order.order_status = order_status
        order.save()

        messages.success(request, "Order status updated")
        return redirect("vendor:order_detail", order.order_id)

    return redirect("vendor:order_detail", order.order_id)

@login_required
def update_order_item_status(request, order_id, item_id):
    order = store_models.Order.objects.get(vendors=request.user, order_id=order_id, payment_status="Paid")
    item = store_models.OrderItem.objects.get(item_id=item_id, order=order)
    
    if request.method == "POST":
        
        order_status = request.POST.get("order_status")
        shipping_service = request.POST.get("shipping_service")
        tracking_id = request.POST.get("tracking_id")
        
        item.order_status = order_status
        item.shipping_service = shipping_service
        item.tracking_id = tracking_id
        item.save()

        messages.success(request, "Item status updated")
        return redirect("vendor:order_item_detail", order.order_id, item.item_id)
    return redirect("vendor:order_item_detail", order.order_id, item.item_id)

@login_required
def coupons(request):
    coupons_list = store_models.Coupon.objects.filter(vendor=request.user)
    coupons = paginate_queryset(request, coupons_list, 10)

    context = {
        "coupons": coupons,
        "coupons_list": coupons_list,
    }
    return render(request, "vendor/coupons.html", context)

@login_required
def update_coupon(request, id):
    coupon = store_models.Coupon.objects.get(vendor=request.user, id=id)
    
    if request.method == "POST":
        code = request.POST.get("coupon_code")
        coupon.code = code
        coupon.save()

    messages.success(request, "Coupon updated")
    return redirect("vendor:coupons")


@login_required
def delete_coupon(request, id):
    coupon = store_models.Coupon.objects.get(vendor=request.user, id=id)
    coupon.delete()
    messages.success(request, "Coupon deleted")
    return redirect("vendor:coupons")


@login_required
def create_coupon(request):
    if request.method == "POST":
        code = request.POST.get("coupon_code")
        discount = request.POST.get("coupon_discount")
        store_models.Coupon.objects.create(vendor=request.user, code=code, discount=discount)

    messages.success(request, "Coupon created")
    return redirect("vendor:coupons")