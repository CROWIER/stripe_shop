from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .services.item_service import ItemService
from .services.order_service import OrderService


def item_detail(request, id):
    item_service = ItemService()
    item = item_service.get_item(id)

    context = {
        'item': item,
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY
    }
    return render(request, 'payments/item_detail.html', context)


@csrf_exempt
def buy_item(request, id):
    item_service = ItemService()
    result = item_service.create_payment_session(id, request)

    if 'error' in result:
        return JsonResponse(result, status=400)
    return JsonResponse(result)


def order_detail(request, id):
    order_service = OrderService()
    order = order_service.get_order(id)
    order_items = order_service.get_order_items(order)

    context = {
        'order': order,
        'order_items': order_items,
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY
    }
    return render(request, 'payments/order_detail.html', context)


@csrf_exempt
def buy_order(request, id):
    order_service = OrderService()
    result = order_service.create_payment_session(id, request)

    if 'error' in result:
        return JsonResponse(result, status=400)
    return JsonResponse(result)


def success_view(request):
    return render(request, 'payments/success.html')


from django.shortcuts import render
