from django.urls import path
from .views import CustomerListView , CustomerDetailView, CustomerCreateView, CustomerUpdateView, CustomerDeleteView, ajax_get_customer
from . import views

urlpatterns = [
    path('', CustomerListView.as_view(), name='customers-home'),
    # path('user/<str:username>', UserOrderListView.as_view(), name='user-orders'),
    path('customer/<int:pk>/', CustomerDetailView.as_view(), name='customer-details'),
    path('customer/<int:pk>/update', CustomerUpdateView.as_view(), name='customer-update'),
    path('customer/<int:pk>/delete', CustomerDeleteView.as_view(), name='customer-delete'),
    path('customer/new/', CustomerCreateView.as_view(), name='customer-create'),

    path('ajax/get-customer/<int:pk>/', ajax_get_customer, name='ajax_get_customer'),
]