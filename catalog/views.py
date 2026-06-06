from django.shortcuts import render, redirect, get_object_or_404
from .models import RoomType, Style, Category, Product


def catalog(request):
    """Страница каталога"""
    products = Product.objects.filter(in_stock=True)
    return render(request, 'catalog/catalog.html', {'products': products})


def product_detail(request, slug):
    """Страница товара"""
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'catalog/product_detail.html', {'product': product})


# ============ УМНЫЙ ПОДБОР ============

def smart_select_start(request):
    """Шаг 1: Выбор комнаты"""
    request.session['smart_select'] = {}
    rooms = RoomType.objects.all()
    return render(request, 'catalog/smart_select/step1_room.html', {
        'rooms': rooms,
        'step': 1,
        'total_steps': 4
    })


def smart_select_style(request, room_slug):
    """Шаг 2: Выбор стиля"""
    room = get_object_or_404(RoomType, slug=room_slug)

    request.session['smart_select'] = {'room': room_slug}
    request.session.modified = True

    styles = Style.objects.all()
    return render(request, 'catalog/smart_select/step2_style.html', {
        'room': room,
        'styles': styles,
        'step': 2,
        'total_steps': 4
    })


def smart_select_budget(request, room_slug, style_slug):
    """Шаг 3: Выбор бюджета"""
    room = get_object_or_404(RoomType, slug=room_slug)
    style = get_object_or_404(Style, slug=style_slug)

    request.session['smart_select'] = {
        'room': room_slug,
        'style': style_slug
    }
    request.session.modified = True

    budgets = [
        {'key': 'economy', 'name': 'Эконом', 'range': 'до 15 000 ₽', 'icon': '💰'},
        {'key': 'standard', 'name': 'Стандарт', 'range': '15 000 - 50 000 ₽', 'icon': '💎'},
        {'key': 'premium', 'name': 'Премиум', 'range': '50 000 - 100 000 ₽', 'icon': '👑'},
        {'key': 'luxury', 'name': 'Люкс', 'range': 'от 100 000 ₽', 'icon': '🏆'},
    ]

    return render(request, 'catalog/smart_select/step3_budget.html', {
        'room': room,
        'style': style,
        'budgets': budgets,
        'step': 3,
        'total_steps': 4
    })


def smart_select_category(request, room_slug, style_slug, budget):
    """Шаг 4: Выбор типа мебели"""
    room = get_object_or_404(RoomType, slug=room_slug)
    style = get_object_or_404(Style, slug=style_slug)

    request.session['smart_select'] = {
        'room': room_slug,
        'style': style_slug,
        'budget': budget
    }
    request.session.modified = True

    categories = Category.objects.all()

    budget_names = {
        'economy': 'Эконом',
        'standard': 'Стандарт',
        'premium': 'Премиум',
        'luxury': 'Люкс'
    }

    return render(request, 'catalog/smart_select/step4_category.html', {
        'room': room,
        'style': style,
        'budget': budget,
        'budget_name': budget_names.get(budget, budget),
        'categories': categories,
        'step': 4,
        'total_steps': 4
    })


def smart_select_results(request, room_slug, style_slug, budget, category_slug):
    """Результаты подбора"""
    room = get_object_or_404(RoomType, slug=room_slug)
    style = get_object_or_404(Style, slug=style_slug)
    category = get_object_or_404(Category, slug=category_slug)

    products = Product.objects.filter(
        room_types=room,
        styles=style,
        categories=category,
        budget_category=budget,
        in_stock=True
    ).distinct()

    similar_products = Product.objects.filter(
        styles=style,
        budget_category=budget,
        categories=category,
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
        'category': category,
        'budget': budget,
        'budget_name': budget_names.get(budget, budget),
        'products': products,
        'similar_products': similar_products,
        'total_found': products.count()
    })