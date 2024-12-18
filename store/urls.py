from django.urls import path, include
from store import views
app_name = 'store'
urlpatterns = [
    path("", views.index, name="index"),
    path("detail/<slug>/", views.product_detail, name="product_detail"),
    path("add_to_cart/", views.add_to_cart, name="add_to_cart"),
    path("cart/", views.cart, name="cart"),
    path("delete_cart_item/", views.delete_cart_item, name="delete_cart_item"),
    path("create_order/", views.create_order, name="create_order"),
    path("checkout/<order_id>/", views.checkout, name="checkout"),
    path("coupon_apply/<order_id>/", views.coupon_apply, name="coupon_apply") 
]
