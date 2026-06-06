from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from catalog.models import Product


class Cart(models.Model):
    """Корзина пользователя"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name="Пользователь"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создана")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлена")

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

    def __str__(self):
        return f"Корзина {self.user.username}"

    @property
    def total_price(self):
        """Общая сумма корзины"""
        return sum(item.subtotal for item in self.items.all())

    @property
    def total_quantity(self):
        """Общее количество товаров"""
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    """Товар в корзине"""
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name="Корзина"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Товар"
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")
    added_at = models.DateTimeField(auto_now_add=True, verbose_name="Добавлен")

    class Meta:
        verbose_name = "Товар в корзине"
        verbose_name_plural = "Товары в корзине"
        unique_together = ('cart', 'product')  # один товар = одна строка

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    @property
    def subtotal(self):
        """Сумма по этой позиции"""
        return self.product.price * self.quantity


class Order(models.Model):
    """Заказ"""
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('processing', 'В обработке'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменён'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name="Пользователь"
    )
    # Контактные данные
    full_name = models.CharField(max_length=200, verbose_name="ФИО")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    email = models.EmailField(verbose_name="Email")
    address = models.TextField(verbose_name="Адрес доставки")
    comment = models.TextField(blank=True, verbose_name="Комментарий")

    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, verbose_name="Сумма заказа"
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Статус"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата заказа")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['-created_at']

    def __str__(self):
        return f"Заказ #{self.id} от {self.full_name}"


class OrderItem(models.Model):
    """Позиция заказа (фиксируем цену на момент покупки)"""
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name="Заказ"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Товар"
    )
    product_name = models.CharField(max_length=200, verbose_name="Название")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")

    class Meta:
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказа"

    def __str__(self):
        return f"{self.product_name} x {self.quantity}"

    @property
    def subtotal(self):
        return self.price * self.quantity