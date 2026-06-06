from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cart.models import Cart
from .forms import RegisterForm, LoginForm, ProfileForm


def register_view(request):
    """Регистрация"""
    if request.user.is_authenticated:
        return redirect('core:home')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            return redirect('core:home')
    else:
        form = RegisterForm()
    
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """Вход"""
    if request.user.is_authenticated:
        return redirect('core:home')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'С возвращением, {user.username}!')
            
            # Перенаправление после входа
            next_url = request.GET.get('next', 'core:home')
            return redirect(next_url)
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """Выход"""
    logout(request)
    messages.info(request, 'Вы вышли из аккаунта')
    return redirect('core:home')


@login_required
def profile_view(request):
    # Получаем или создаём корзину пользователя
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related('product').all()

    return render(request, 'accounts/profile.html', {
        'cart': cart,
        'cart_items': items,
    })


@login_required
def profile_edit_view(request):
    """Редактирование профиля"""
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль обновлён!')
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=request.user)
    
    return render(request, 'accounts/profile_edit.html', {'form': form})