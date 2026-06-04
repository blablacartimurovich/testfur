from django.db import models


class RoomType(models.Model):
    """Тип комнаты (гостиная, спальня, кухня, кабинет)"""
    name = models.CharField(max_length=100, verbose_name="Название")
    slug = models.SlugField(unique=True, verbose_name="URL")
    icon = models.CharField(max_length=50, default="🏠", verbose_name="Иконка")
    image = models.ImageField(upload_to='rooms/', blank=True, null=True, verbose_name="Изображение")
    description = models.TextField(blank=True, verbose_name="Описание")
    
    class Meta:
        verbose_name = "Тип комнаты"
        verbose_name_plural = "Типы комнат"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Style(models.Model):
    """Стиль мебели (лофт, классика, сканди)"""
    name = models.CharField(max_length=100, verbose_name="Название")
    slug = models.SlugField(unique=True, verbose_name="URL")
    icon = models.CharField(max_length=50, default="🎨", verbose_name="Иконка")
    description = models.TextField(blank=True, verbose_name="Описание")
    image = models.ImageField(upload_to='styles/', blank=True, null=True, verbose_name="Изображение")
    
    class Meta:
        verbose_name = "Стиль"
        verbose_name_plural = "Стили"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Category(models.Model):
    """Категория мебели (диваны, столы, шкафы)"""
    name = models.CharField(max_length=100, verbose_name="Название")
    slug = models.SlugField(unique=True, verbose_name="URL")
    icon = models.CharField(max_length=50, default="🪑", verbose_name="Иконка")
    description = models.TextField(blank=True, verbose_name="Описание")
    image = models.ImageField(upload_to='categories/', blank=True, null=True, verbose_name="Изображение")
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Product(models.Model):
    """Товар (мебель)"""
    
    BUDGET_CHOICES = [
        ('economy', 'Эконом (до 15 000 ₽)'),
        ('standard', 'Стандарт (15 000 - 50 000 ₽)'),
        ('premium', 'Премиум (50 000 - 100 000 ₽)'),
        ('luxury', 'Люкс (от 100 000 ₽)'),
    ]
    
    name = models.CharField(max_length=200, verbose_name="Название")
    slug = models.SlugField(unique=True, verbose_name="URL")
    description = models.TextField(verbose_name="Описание")
    short_description = models.CharField(max_length=300, blank=True, verbose_name="Краткое описание")
    
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    old_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Старая цена")
    
    image = models.ImageField(upload_to='products/', verbose_name="Главное изображение")
    
    # МНОЖЕСТВЕННЫЕ СВЯЗИ (ManyToMany)
    categories = models.ManyToManyField(
        Category, 
        related_name='products', 
        verbose_name="Категории"
    )
    styles = models.ManyToManyField(
        Style, 
        related_name='products', 
        verbose_name="Стили"
    )
    room_types = models.ManyToManyField(
        RoomType, 
        related_name='products', 
        verbose_name="Типы комнат"
    )
    
    budget_category = models.CharField(
        max_length=20, 
        choices=BUDGET_CHOICES, 
        verbose_name="Ценовая категория"
    )
    
    material = models.CharField(max_length=100, verbose_name="Материал")
    dimensions = models.CharField(max_length=100, blank=True, verbose_name="Размеры (ШxГxВ)")
    color = models.CharField(max_length=100, blank=True, verbose_name="Цвет")
    weight = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="Вес (кг)")
    
    in_stock = models.BooleanField(default=True, verbose_name="В наличии")
    is_featured = models.BooleanField(default=False, verbose_name="Рекомендуемый")
    is_new = models.BooleanField(default=False, verbose_name="Новинка")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    @property
    def discount_percent(self):
        """Вычисляет процент скидки"""
        if self.old_price and self.old_price > self.price:
            return int((1 - self.price / self.old_price) * 100)
        return 0
    
    def get_categories_display(self):
        """Возвращает список категорий через запятую"""
        return ", ".join([c.name for c in self.categories.all()])
    
    def get_styles_display(self):
        """Возвращает список стилей через запятую"""
        return ", ".join([s.name for s in self.styles.all()])
    
    def get_rooms_display(self):
        """Возвращает список комнат через запятую"""
        return ", ".join([r.name for r in self.room_types.all()])


class ProductImage(models.Model):
    """Дополнительные изображения товара"""
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name='images',
        verbose_name="Товар"
    )
    image = models.ImageField(upload_to='products/gallery/', verbose_name="Изображение")
    alt_text = models.CharField(max_length=200, blank=True, verbose_name="Alt текст")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    
    class Meta:
        verbose_name = "Изображение товара"
        verbose_name_plural = "Изображения товаров"
        ordering = ['order']
    
    def __str__(self):
        return f"Фото {self.order} - {self.product.name}"