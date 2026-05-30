from django.contrib import admin
from django.utils.html import format_html
from .models import Customer, Product, Cart, CartItem

class CartItemInline(admin.TabularInline):
    """Inline для отображения товаров в корзине"""
    model = CartItem
    extra = 0
    readonly_fields = ['total_price']
    fields = ['product', 'quantity', 'total_price']

    def total_price(self, obj):
        if obj.pk:
            return f"{obj.total_price()} руб."
        return "-"
    total_price.short_description = "Стоимость"

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    search_fields = ['first_name', 'last_name', 'email']
    list_filter = ['created_at']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ['name', 'description', 'category']
    list_filter = ['category', 'created_at']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'customer_link', 'items_count', 'total_price_display', 
        'status_colored', 'created_at', 'updated_at'
    ]
    list_display_links = ['id']
    search_fields = [
        'customer__first_name', 'customer__last_name', 
        'customer__email', 'id'
    ]
    list_filter = ['status', 'created_at', 'updated_at']
    inlines = [CartItemInline]
    readonly_fields = ['created_at', 'updated_at', 'total_price_display']
    fieldsets = (
        ('Основная информация', {
            'fields': ('customer', 'status', 'created_at', 'updated_at')
        }),
        ('Товары в корзине', {
            'fields': (),
            'description': 'Товары добавляются через inline-форму ниже'
        }),
        ('Финансовая информация', {
            'fields': ('total_price_display',),
        }),
    )

    def customer_link(self, obj):
        url = f"/admin/{obj.customer._meta.app_label}/{obj.customer._meta.model_name}/{obj.customer.id}/change/"
        return format_html('<a href="{}">{}</a>', url, obj.customer)
    customer_link.short_description = "Покупатель"

    def items_count(self, obj):
        return obj.items_count()
    items_count.short_description = "Кол-во товаров"

    def total_price_display(self, obj):
        return f"{obj.total_price():.2f} руб."
    total_price_display.short_description = "Общая стоимость"

    def status_colored(self, obj):
        colors = {
            'active': 'orange',
            'completed': 'green',
            'cancelled': 'red'
        }
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            colors.get(obj.status, 'black'),
            obj.get_status_display()
        )
    status_colored.short_description = "Статус"




@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    search_fields = ['product__name', 'cart__id']