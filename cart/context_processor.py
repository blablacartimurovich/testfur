def cart_context(request):
    """Контекст корзины для всех шаблонов"""
    cart_count = 0
    if request.user.is_authenticated:
        # Позже здесь будет реальный подсчёт
        cart_count = 0
    return {'cart_count': cart_count}