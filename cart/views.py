from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST

from catalog.models import Product
from .models import Cart, CartItem


def get_user_cart(user):
    """Получить или создать корзину пользователя"""
    cart, created = Cart.objects.get_or_create(user=user)
    return cart


@login_required
def cart_view(request):
    """Отдельная страница корзины"""
    cart = get_user_cart(request.user)
    items = cart.items.select_related('product').all()

    return render(request, 'cart/cart.html', {
        'cart': cart,
        'items': items,
    })


@login_required
@require_POST
def add_to_cart(request, product_id):
    """Добавить товар в корзину"""
    product = get_object_or_404(Product, id=product_id, in_stock=True)
    cart = get_user_cart(request.user)

    quantity = int(request.POST.get('quantity', 1))
    if quantity < 1:
        quantity = 1

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )

    if not created:
        item.quantity += quantity
        item.save()

    messages.success(request, f'«{product.name}» добавлен в корзину')

    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER')
    return redirect(next_url or 'cart:cart')


@login_required
@require_POST
def remove_from_cart(request, item_id):
    """Удалить товар из корзины"""
    cart = get_user_cart(request.user)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)

    product_name = item.product.name
    item.delete()

    messages.info(request, f'«{product_name}» удалён из корзины')
    return redirect('accounts:profile')


@login_required
@require_POST
def update_cart(request, item_id):
    """Обновить количество товара"""
    cart = get_user_cart(request.user)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)

    quantity = int(request.POST.get('quantity', 1))

    if quantity < 1:
        item.delete()
        messages.info(request, f'«{item.product.name}» удалён из корзины')
    else:
        item.quantity = quantity
        item.save()
        messages.success(request, 'Количество обновлено')

    return redirect('accounts:profile')


@login_required
def checkout(request):
    """Оформление заказа"""
    return render(request, 'cart/checkout.html')


@login_required
def order_success(request, order_id):
    """Успешный заказ"""
    return render(request, 'cart/order_success.html', {'order_id': order_id})