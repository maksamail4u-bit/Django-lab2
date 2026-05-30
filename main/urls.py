from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.CartListView.as_view(), name='cart_list'),
]