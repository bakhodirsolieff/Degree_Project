from django.urls import path, include
from store import views
print(dir(views))
app_name = 'vendor'
urlpatterns = [
    path("", views.index, name = "index"),
    path("detail/<slug>/", views.product_detail, name = "product_detail"),
]
