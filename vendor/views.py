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