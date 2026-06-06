from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'updated_at', 'total_quantity', 'total_price')
    search_fields = ('user__username', 'user__email')
    inlines = [CartItemInline]


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'product_name', 'price', 'quantity', 'subtotal')

    def subtotal(self, obj):
        return obj.subtotal
    subtotal.short_description = 'Сумма'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'full_name',
        'phone',
        'email',
        'total_price',
        'status',
        'created_at'
    )
    list_filter = ('status', 'created_at')
    search_fields = (
        'full_name',
        'phone',
        'email',
        'address',
        'user__username',
        'user__email'
    )
    list_editable = ('status',)
    readonly_fields = ('created_at',)
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product_name', 'price', 'quantity', 'subtotal')
    search_fields = ('product_name', 'order__full_name', 'order__user__username')

    def subtotal(self, obj):
        return obj.subtotal
    subtotal.short_description = 'Сумма'