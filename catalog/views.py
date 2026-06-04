from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Product, Category, Style, RoomType


def catalog(request):
    """Страница каталога с фильтрами"""
    products = Product.objects.filter(in_stock=True)
    
    # Фильтры
    category_slug = request.GET.get('category')
    style_slug = request.GET.get('style')
    room_slug = request.GET.get('room')
    budget = request.GET.get('budget')
    search = request.GET.get('search')
    sort = request.GET.get('sort', 'newest')
    
    # Применяем фильтры
    if category_slug:
        products = products.filter(categories__slug=category_slug)
    if style_slug:
        products = products.filter(styles__slug=style_slug)
    if room_slug:
        products = products.filter(room_types__slug=room_slug)
    if budget:
        products = products.filter(budget_category=budget)
    if search:
        products = products.filter(
            Q(name__icontains=search) | 
            Q(description__icontains=search) |
            Q(material__icontains=search)
        )
    
    # Сортировка
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'name':
        products = products.order_by('name')
    else:  # newest
        products = products.order_by('-created_at')
    
    # Убираем дубликаты (из-за ManyToMany)
    products = products.distinct()
    
    # Пагинация
    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    products = paginator.get_page(page)
    
    # Данные для фильтров
    categories = Category.objects.all()
    styles = Style.objects.all()
    room_types = RoomType.objects.all()
    
    return render(request, 'catalog/catalog.html', {
        'products': products,
        'categories': categories,
        'styles': styles,
        'room_types': room_types,
        'current_category': category_slug,
        'current_style': style_slug,
        'current_room': room_slug,
        'current_budget': budget,
        'current_search': search,
        'current_sort': sort,
    })


def product_detail(request, slug):
    """Страница товара"""
    product = get_object_or_404(Product, slug=slug)
    
    # Похожие товары (из тех же категорий)
    similar_products = Product.objects.filter(
        categories__in=product.categories.all(),
        in_stock=True
    ).exclude(id=product.id).distinct()[:4]
    
    return render(request, 'catalog/product_detail.html', {
        'product': product,
        'similar_products': similar_products,
    })


def smart_select_start(request):
    """Шаг 1: Выбор комнаты"""
    rooms = RoomType.objects.all()
    return render(request, 'catalog/smart_select/step1_room.html', {
        'rooms': rooms
    })


def smart_select_style(request, room_slug):
    """Шаг 2: Выбор стиля"""
    room = get_object_or_404(RoomType, slug=room_slug)
    styles = Style.objects.all()
    return render(request, 'catalog/smart_select/step2_style.html', {
        'room': room,
        'styles': styles
    })


def smart_select_budget(request, room_slug, style_slug):
    """Шаг 3: Выбор бюджета"""
    room = get_object_or_404(RoomType, slug=room_slug)
    style = get_object_or_404(Style, slug=style_slug)
    
    budgets = [
        {'slug': 'economy', 'name': 'Эконом', 'range': 'до 15 000 ₽', 'icon': '💰'},
        {'slug': 'standard', 'name': 'Стандарт', 'range': '15 000 - 50 000 ₽', 'icon': '💵'},
        {'slug': 'premium', 'name': 'Премиум', 'range': '50 000 - 100 000 ₽', 'icon': '💎'},
        {'slug': 'luxury', 'name': 'Люкс', 'range': 'от 100 000 ₽', 'icon': '👑'},
    ]
    
    return render(request, 'catalog/smart_select/step3_budget.html', {
        'room': room,
        'style': style,
        'budgets': budgets
    })


def smart_select_results(request, room_slug, style_slug, budget):
    """Результаты подбора"""
    room = get_object_or_404(RoomType, slug=room_slug)
    style = get_object_or_404(Style, slug=style_slug)
    
    products = Product.objects.filter(
        room_types=room,
        styles=style,
        budget_category=budget,
        in_stock=True
    ).distinct()
    
    similar_products = Product.objects.filter(
        styles=style,
        budget_category=budget,
        in_stock=True
    ).exclude(room_types=room).distinct()[:4]
    
    budget_names = {
        'economy': 'Эконом',
        'standard': 'Стандарт',
        'premium': 'Премиум',
        'luxury': 'Люкс'
    }
    
    return render(request, 'catalog/smart_select/results.html', {
        'room': room,
        'style': style,
        'budget': budget,
        'budget_name': budget_names.get(budget, budget),
        'products': products,
        'similar_products': similar_products,
        'total_found': products.count()
    })