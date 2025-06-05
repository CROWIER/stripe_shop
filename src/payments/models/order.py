from django.db import models

from .item import Item

class Order(models.Model):
    items = models.ManyToManyField(Item, through='OrderItem')
    created_at = models.DateTimeField(auto_now_add=True)
    stripe_session_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Order #{self.id}"

    def get_total_price(self):
        total = sum([order_item.get_total_price() for order_item in self.orderitem_set.all()])
        if hasattr(self, 'discount') and self.discount:
            total = total * (1 - self.discount.percent / 100)
        if hasattr(self, 'tax') and self.tax:
            total = total * (1 + self.tax.percent / 100)
        return round(total, 2)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_total_price(self):
        return self.item.price * self.quantity