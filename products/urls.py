from django.urls import path

from products.apps import ProductsConfig
from products.views import get_stripe_session_id, item_detail, order_payment, toggle_item, create_order

app_name = ProductsConfig.name

urlpatterns = [
    path('buy/<int:pk>/', get_stripe_session_id, name='buy-item'),
    path('order/create', create_order, name='create_order'),
    path('order/payment', order_payment, name='payment_order'),
    path('item/<int:pk>/', item_detail, name='item-page'),
    path('toggle_item/<int:item_pk>/', toggle_item, name='add_and_delete_item'),
]
