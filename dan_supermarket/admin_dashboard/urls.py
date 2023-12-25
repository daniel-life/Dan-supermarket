from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="admin_dashboard"),
    path('add_item', views.add_item, name="add_item")
]