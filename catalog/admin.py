from django.contrib import admin
from django.utils.html import format_html
from .models import RoomType, Style, Category, Product, ProductImage


@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ['icon_display', 'name', 'slug', 'products_count']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    
    def icon_display(self, obj):
        return format_html('<span style="font-size: 24px;">{}</span>', obj.icon)
    icon_display.short_description = 'Иконка'
    
    def products_count(self, obj):
        return obj.products.count()
    products_count.short_description = 'Товаров'


@admin.register(Style)
class StyleAdmin(admin.ModelAdmin):
    list_display = ['icon_display', 'name', 'slug', 'products_count']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    
    def icon_display(self, obj):
        return format_html('<span style="font-size: 24px;">{}</span>', obj.icon)
    icon_display.short_description = 'Иконка'
    
    def products_count(self, obj):
        return obj.products.count()
    products_count.short_description = 'Товаров'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['icon_display', 'name', 'slug', 'products_count']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    
    def icon_display(self, obj):
        return format_html('<span style="font-size: 24px;">{}</span>', obj.icon)
    icon_display.short_description = 'Иконка'
    
    def products_count(self, obj):
        return obj.products.count()
    products_count.short_description = 'Товаров'


class ProductImageInline(admin.TabularInline):
    """Инлайн для дополнительных фото товара"""
    model = ProductImage
    extra = 1
    fields = ['image', 'alt_text', 'order']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'image_preview', 
        'name', 
        'price_display', 
        'budget_category',
        'in_stock', 
        'is_featured',
        'is_new',
        'created_at'
    ]
    
    list_filter = [
        'categories', 
        'styles', 
        'room_types', 
        'budget_category', 
        'in_stock',
        'is_featured',
        'is_new'
    ]
    
    search_fields = ['name', 'description', 'material']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['in_stock', 'is_featured', 'is_new']
    
    filter_horizontal = ['categories', 'styles', 'room_types']  # Удобный виджет для ManyToMany
    
    inlines = [ProductImageInline]
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'slug', 'short_description', 'description')
        }),
        ('Изображение', {
            'fields': ('image',)
        }),
        ('Цена', {
            'fields': ('price', 'old_price', 'budget_category')
        }),
        ('Категоризация', {
            'fields': ('categories', 'styles', 'room_types'),
            'description': 'Можно выбрать несколько пунктов (Ctrl+клик или перетаскивание)'
        }),
        ('Характеристики', {
            'fields': ('material', 'dimensions', 'color', 'weight'),
            'classes': ('collapse',)  # Свёрнутый блок
        }),
        ('Статус', {
            'fields': ('in_stock', 'is_featured', 'is_new')
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 5px;"/>',
                obj.image.url
            )
        return "—"
    image_preview.short_description = 'Фото'
    
    def price_display(self, obj):
        if obj.old_price:
            return format_html(
                '<span style="text-decoration: line-through; color: #999;">{} ₽</span><br>'
                '<strong style="color: #e74c3c;">{} ₽</strong>',
                int(obj.old_price),
                int(obj.price)
            )
        return format_html('<strong>{} ₽</strong>', int(obj.price))
    price_display.short_description = 'Цена'


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'image_preview', 'order']
    list_filter = ['product']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 80px; height: 80px; object-fit: cover;"/>',
                obj.image.url
            )
        return "—"
    image_preview.short_description = 'Превью'