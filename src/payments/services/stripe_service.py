import stripe
from typing import Dict, Optional
from django.conf import settings
from django.http import HttpRequest

from ..models.item import Item
from ..models.order import Order
from ..repositories.order_repository import OrderRepository


class StripeService:
    def __init__(self,
                 order_repository: Optional[OrderRepository] = None):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        self.stripe = stripe

        self.order_repository = order_repository or OrderRepository()

        self.default_currency = 'usd'

    def create_checkout_session_for_item(self,
                                         item: Item,
                                         request: HttpRequest,
                                         success_url: str = None,
                                         cancel_url: str = None) -> Dict:
        try:
            if not success_url:
                success_url = request.build_absolute_uri('/success/')
            if not cancel_url:
                cancel_url = request.build_absolute_uri(f'/item/{item.id}/')

            session = self.stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': self.default_currency,
                        'product_data': {
                            'name': item.name,
                            'description': item.description,
                        },
                        'unit_amount': int(item.price * 100),
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=success_url,
                cancel_url=cancel_url,
            )
            return {'session_id': session.id}
        except Exception as e:
            return {'error': str(e)}

    def create_checkout_session_for_order(self,
                                          order: Order,
                                          request: HttpRequest,
                                          success_url: str = None,
                                          cancel_url: str = None) -> Dict:
        try:
            if not success_url:
                success_url = request.build_absolute_uri('/success/')
            if not cancel_url:
                cancel_url = request.build_absolute_uri(f'/order/{order.id}/')

            order_items = self.order_repository.get_order_items(order)

            line_items = [{
                'price_data': {
                    'currency': self.default_currency,
                    'product_data': {
                        'name': f'Order #{order.id}',
                        'description': f'Order with {len(order_items)} items',
                    },
                    'unit_amount': int(order.get_total_price() * 100),  # Общая сумма
                },
                'quantity': 1,
            }]

            session_params = {
                'payment_method_types': ['card'],
                'line_items': line_items,
                'mode': 'payment',
                'success_url': success_url,
                'cancel_url': cancel_url,
            }

            session = self.stripe.checkout.Session.create(**session_params)

            self.order_repository.update_session_id(order, session.id)

            return {'session_id': session.id}
        except Exception as e:
            return {'error': str(e)}

    def create_coupon(self, discount) -> Optional[str]:
        try:
            coupon = self.stripe.Coupon.create(
                percent_off=float(discount.percent),
                duration='once',
                name=discount.name
            )
            return coupon.id
        except Exception:
            return None

    def get_session(self, session_id: str) -> Optional[Dict]:
        try:
            session = self.stripe.checkout.Session.retrieve(session_id)
            return session.to_dict()
        except Exception:
            return None

    def verify_webhook_signature(self, payload: bytes, signature: str) -> bool:
        try:
            webhook_secret = settings.STRIPE_WEBHOOK_SECRET
            self.stripe.Webhook.construct_event(payload, signature, webhook_secret)
            return True
        except Exception:
            return False
