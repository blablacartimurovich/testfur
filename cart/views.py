from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def cart_view(request):
    """Корзина"""
    return render(request, 'cart/cart.html')

@login_required
def add_to_cart(request, product_id):
    """Добавить в корзину"""
    return redirect('cart:cart')

@login_required
def remove_from_cart(request, item_id):
    """Удалить из корзины"""
    return redirect('cart:cart')

@login_required
def update_cart(request, item_id):
    """Обновить количество"""
    return redirect('cart:cart')

@login_required
def checkout(request):
    """Оформление заказа"""
    return render(request, 'cart/checkout.html')

@login_required
def order_success(request, order_id):
    """Успешный заказ"""
    return render(request, 'cart/order_success.html')