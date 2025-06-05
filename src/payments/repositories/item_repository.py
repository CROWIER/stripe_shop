from typing import List

from django.shortcuts import get_object_or_404

from ..models.item import Item


class ItemRepository:
    def __init__(self):
        self.model = Item

    def get_by_id(self, item_id: int) -> Item:
        return get_object_or_404(self.model, id=item_id)

    def get_all(self) -> List[Item]:
        return self.model.objects.all()

    def create(self, name: str, description: str, price: float) -> Item:
        return self.model.objects.create(
            name=name,
            description=description,
            price=price
        )
