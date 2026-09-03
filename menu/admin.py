from django.contrib import admin
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
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'phone', 'status', 'total_price', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('id', 'user__username', 'full_name', 'phone', 'address')
    list_editable = ('status',)
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
    inlines = (OrderItemInline,)
