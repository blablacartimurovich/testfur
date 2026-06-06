from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from cart.models import Cart, Order, OrderItem
from .forms import OrderForm


@login_required
def create_order_request(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.items.select_related('product').all()
    except Cart.DoesNotExist:
        cart = None
        cart_items = []

    if not cart_items:
        messages.error(request, 'Ваша корзина пуста.')
        return redirect('accounts:profile')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                user=request.user,
                full_name=form.cleaned_data['full_name'],
                phone=form.cleaned_data['phone'],
                email=form.cleaned_data['email'],
                address=form.cleaned_data['address'],
                comment=form.cleaned_data['comment'],
                total_price=0,
                status='new'
            )

            total = 0

            for item in cart_items:
                order_item = OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    product_name=item.product.name,
                    price=item.product.price,
                    quantity=item.quantity
                )
                total += order_item.subtotal

            order.total_price = total
            order.save()

            # очищаем корзину
            cart_items.delete()

            messages.success(
                request,
                'Анкета успешно заполнена. Вам обязательно перезвонят в течение рабочего времени.'
            )
            return redirect('accounts:profile')
    else:
        form = OrderForm(initial={
            'full_name': f'{request.user.first_name} {request.user.last_name}'.strip(),
            'phone': getattr(request.user, 'phone', ''),
            'email': request.user.email,
        })

    return render(request, 'orders/order_form.html', {
        'form': form,
        'cart': cart,
        'cart_items': cart_items,
    })