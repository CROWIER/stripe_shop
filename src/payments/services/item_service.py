from typing import Dict, Optional

from django.http import HttpRequest

from ..models.item import Item
from ..repositories.item_repository import ItemRepository
from ..services.stripe_service import StripeService


class ItemService:
    def __init__(self, stripe_service: Optional[StripeService] = None):
        self.repository = ItemRepository()
        self.stripe_service = stripe_service or StripeService()

    def get_item(self, item_id: int) -> Item:
        return self.repository.get_by_id(item_id)

    def create_payment_session(self, item_id: int, request: HttpRequest) -> Dict:
        item = self.repository.get_by_id(item_id)
        return self.stripe_service.create_checkout_session_for_item(item, request)
