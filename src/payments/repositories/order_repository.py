from typing import List

from django.shortcuts import get_object_or_404

from ..models.item import Item
from ..models.order import Order, OrderItem


class OrderRepository:
    def __init__(self):
        self.model = Order

    def get_by_id(self, order_id: int) -> Order:
        return get_object_or_404(self.model, id=order_id)

    def create(self) -> Order:
        return self.model.objects.create()

    def add_item(self, order: Order, item: Item, quantity: int = 1) -> OrderItem:
        return OrderItem.objects.create(
            order=order,
            item=item,
            quantity=quantity
        )

    def get_order_items(self, order: Order) -> List[OrderItem]:
        return list(order.orderitem_set.all())

    def update_session_id(self, order: Order, session_id: str):
        order.stripe_session_id = session_id
        order.save()
        return order
