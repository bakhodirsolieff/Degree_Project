from django.urls import path
from customer import views

app_name = "customer"

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("orders/", views.orders, name="orders"),
    path("order_detail/<order_id>/", views.order_detail, name="order_detail"),
    path("order_item_detail/<order_id>/<item_id>/", views.order_item_detail, name="order_item_detail"),
    path("wishlist/", views.wishlist, name="wishlist"),
    path("remove_from_wishlist/<id>/", views.remove_from_wishlist, name="remove_from_wishlist"),
    path("add_to_wishlist/<id>/", views.add_to_wishlist, name="add_to_wishlist"),
    path("notis/", views.notis, name="notis"),
    path("mark_noti_seen/<id>/", views.mark_noti_seen, name="mark_noti_seen"),
]