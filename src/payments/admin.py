from django.contrib import admin
from .models.item import Item
from .models.adds import Discount, Tax
from .models.order import Order, OrderItem

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'description']
    search_fields = ['name']
    list_filter = ['price']

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'get_total_price', 'stripe_session_id']
    inlines = [OrderItemInline]
    readonly_fields = ['created_at', 'stripe_session_id']
    list_filter = ['created_at']

@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ['name', 'percent', 'order']
    list_filter = ['percent']

@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ['name', 'percent', 'order']
    list_filter = ['percent']