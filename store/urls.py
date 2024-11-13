from django.urls import path, include
from store import views
app_name = 'vendor'
urlpatterns = [
    path("", views.index, name = "index")
    
]
