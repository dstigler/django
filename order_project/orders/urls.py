from django.urls import path
from .views import OrderListView, OrderDetailView, OrderCreateView, OrderUpdateView, OrderDeleteView, CustomerOrderListView, UserOrderListView
from . import views

urlpatterns = [
    path('', OrderListView.as_view(), name='orders-home'),
    path('user/<str:username>', UserOrderListView.as_view(), name='user-orders'),
    path('order/customer/<int:pk>', CustomerOrderListView.as_view(), name='customer-orders'),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('order/<int:pk>/update', OrderUpdateView.as_view(), name='order-update'),
    path('order/<int:pk>/delete', OrderDeleteView.as_view(), name='order-delete'),
    path('order/new/', OrderCreateView.as_view(), name='order-create'),

    # path('ajax/get-orders/', ajax_get_orders, name='ajax_get_orders'),
]