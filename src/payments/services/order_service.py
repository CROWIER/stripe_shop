from typing import Dict, Optional, List
from django.http import HttpRequest

from ..models.order import Order, OrderItem
from .stripe_service import StripeService
from ..repositories.item_repository import ItemRepository
from ..repositories.order_repository import OrderRepository


class OrderService:
    def __init__(self,
                 order_repository: Optional[OrderRepository] = None,
                 item_repository: Optional[ItemRepository] = None,
                 stripe_service: Optional[StripeService] = None):

        self.repository = order_repository or OrderRepository()
        self.item_repository = item_repository or ItemRepository()
        self.stripe_service = stripe_service or StripeService()

    def get_order(self, order_id: int) -> Order:
        return self.repository.get_by_id(order_id)

    def get_order_items(self, order: Order) -> List[OrderItem]:
        return self.repository.get_order_items(order)

    def create_payment_session(self, order_id: int, request: HttpRequest) -> Dict:
        order = self.repository.get_by_id(order_id)
        result = self.stripe_service.create_checkout_session_for_order(order, request)

        if 'session_id' in result:
            self.repository.update_session_id(order, result['session_id'])

        return result

    def create_order_with_items(self, items_data: list) -> Order:
        order = self.repository.create()

        for item_data in items_data:
            item = self.item_repository.get_by_id(item_data['item_id'])
            self.repository.add_item(
                order=order,
                item=item,
                quantity=item_data.get('quantity', 1)
            )

        return order
