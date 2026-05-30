from django.shortcuts import render
from django.views.generic import ListView
from .models import Cart


class CartListView(ListView):
    """Представление для отображения списка корзин"""
    model = Cart
    template_name = 'shop/cart_list.html'
    context_object_name = 'carts'
    paginate_by = 10

    def get_queryset(self):
        """Получаем корзины с связанными данными"""
        return Cart.objects.select_related('customer').prefetch_related(
            'items__product'
        ).all()

    def get_context_data(self, **kwargs):
        """Добавляем дополнительный контекст"""
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список корзин'
        return context