from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    # Каталог
    path('', views.catalog, name='catalog'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    
    # Умный подбор
    path('smart/', views.smart_select_start, name='smart_select_start'),
    path('smart/<slug:room_slug>/', views.smart_select_style, name='smart_select_style'),
    path('smart/<slug:room_slug>/<slug:style_slug>/', views.smart_select_budget, name='smart_select_budget'),
    path('smart/<slug:room_slug>/<slug:style_slug>/<str:budget>/', views.smart_select_results, name='smart_select_results'),
]