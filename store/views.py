from django.shortcuts import render
from django.http import HttpResponse
from store import models as store_models

# Create your views here.
def index(request):
    products = store_models.Product.objects.filter(status="Published")
    for p in products:
        pass
    return render(request, "store/index.html", {"products":products})
