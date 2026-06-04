from django.shortcuts import render
from catalog.models import Product, Category


def home(request):
    """Главная страница"""
    featured_products = Product.objects.filter(
        is_featured=True, 
        in_stock=True
    )[:8]
    
    new_products = Product.objects.filter(
        in_stock=True
    ).order_by('-created_at')[:4]
    
    categories = Category.objects.all()[:6]
    
    return render(request, 'core/home.html', {
        'featured_products': featured_products,
        'new_products': new_products,
        'categories': categories,
    })


def about(request):
    """Страница О нас"""
    return render(request, 'core/about.html')