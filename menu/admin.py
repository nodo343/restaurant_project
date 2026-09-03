from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html

from .models import Dish, Order, OrderItem


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = (
        'image_preview',
        'name',
        'category',
        'spice_level',
        'has_walnuts',
        'is_vegetarian',
        'price',
    )
    list_display_links = ('image_preview', 'name')
    list_editable = ('category', 'spice_level', 'has_walnuts', 'is_vegetarian', 'price')
    list_filter = ('category', 'spice_level', 'has_walnuts', 'is_vegetarian')
    search_fields = ('name', 'description')
    ordering = ('category', 'name')
    readonly_fields = ('image_preview',)
    fieldsets = (
        ('ძირითადი ინფორმაცია', {
            'fields': ('name', 'category', 'description', 'price'),
        }),
        ('ფოტო', {
            'fields': ('image', 'image_preview'),
        }),
        ('თვისებები', {
            'fields': ('spice_level', 'has_walnuts', 'is_vegetarian'),
        }),
    )

    @admin.display(description='ფოტო')
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" alt="{}" style="width:56px;height:42px;object-fit:cover;border-radius:6px;">',
                obj.image.url,
                obj.name,
            )
        return '—'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('dish', 'dish_name', 'unit_price', 'quantity', 'total_price')
    fields = ('dish_name', 'dish', 'unit_price', 'quantity', 'total_price')
    can_delete = False
    show_change_link = True


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'full_name',
        'phone',
        'short_address',
        'items_count',
        'status',
        'total_price',
        'created_at',
    )
    list_filter = ('status', 'created_at')
    search_fields = ('id', 'user__username', 'full_name', 'phone', 'address')
    list_editable = ('status',)
    list_select_related = ('user',)
    date_hierarchy = 'created_at'
    readonly_fields = (
        'user',
        'full_name',
        'phone',
        'address',
        'note',
        'total_price',
        'created_at',
        'updated_at',
    )
    fieldsets = (
        ('დამკვეთი', {
            'fields': ('user', 'full_name', 'phone', 'address'),
        }),
        ('შეკვეთა', {
            'fields': ('status', 'total_price', 'note'),
        }),
        ('დრო', {
            'fields': ('created_at', 'updated_at'),
        }),
    )
    inlines = (OrderItemInline,)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(_items_count=Count('items'))

    @admin.display(description='მისამართი')
    def short_address(self, obj):
        if len(obj.address) <= 42:
            return obj.address
        return f'{obj.address[:39]}...'

    @admin.display(description='კერძები', ordering='_items_count')
    def items_count(self, obj):
        return obj._items_count


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'dish_name', 'quantity', 'unit_price', 'total_price')
    list_filter = ('order__status',)
    search_fields = ('dish_name', 'order__full_name', 'order__phone')
    list_select_related = ('order', 'dish')
    readonly_fields = ('order', 'dish', 'dish_name', 'unit_price', 'quantity', 'total_price')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
