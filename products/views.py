import json

import stripe
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt

from config.settings import STRIPE_SECRET_KEY, STRIPE_PUBLIC_KEY
from products.forms import OrderForm
from products.models import Item, Order

stripe.api_key = STRIPE_SECRET_KEY


@csrf_exempt
def get_stripe_session_id(request, pk):
    item = get_object_or_404(Item, id=pk)
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': item.currency,
                    'product_data': {
                        'name': item.name,
                        'description': item.description,
                    },
                    'unit_amount': int(item.price * 100),
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='http://127.0.0.1:8000/',
            cancel_url='http://127.0.0.1:8000/',
        )
        return JsonResponse({'session_id': session.id})
    except Exception as e:
        return HttpResponseBadRequest(json.dumps({'error': str(e)}), content_type='application/json')


def item_detail(request, pk):
    item = get_object_or_404(Item, id=pk)
    context = {
        'item': item,
        'STRIPE_PUBLIC_KEY': STRIPE_PUBLIC_KEY
    }
    return render(request, 'products/item_detail.html', context)


@csrf_exempt
def create_order(request):
    try:
        order = Order.objects.first()
        if order is None:
            order = Order.objects.create()

        if request.method == 'POST':
            form = OrderForm(request.POST, instance=order)
            if form.is_valid():
                form.save()
                total_amount = order.calculate_total_amount()
                return JsonResponse({'total_amount': total_amount})
        else:
            form = OrderForm(instance=order)

        return render(request, 'products/create_order.html', {'form': form, 'order': order,
                                                              'products': Item.objects.all(),
                                                              'STRIPE_PUBLIC_KEY': STRIPE_PUBLIC_KEY})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
def order_payment(request):
    try:
        order = Order.objects.first()
        if order is None:
            order = Order.objects.create()

        total_amount = order.calculate_total_amount()

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': order.currency,
                    'product_data': {
                        'name': 'Order #{}'.format(order.id),
                        'description': 'Payment for order #{}'.format(order.id),
                    },
                    'unit_amount': int(total_amount * 100),
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='http://127.0.0.1:8000/',
            cancel_url='http://127.0.0.1:8000/',
            metadata={
                'tax_amount': order.tax,
                'discount_amount': order.discount,
            }
        )
        return JsonResponse({'session_id': session.id})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


def toggle_item(request, item_pk):
    try:
        order = Order.objects.first()
        item = Item.objects.get(pk=item_pk)

        if item in order.items.all():
            order.items.remove(item)
        else:
            order.items.add(item)

        total_amount = order.calculate_total_amount()

        return JsonResponse({'total_amount': total_amount})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
