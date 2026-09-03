from django.contrib import admin
from django.utils.html import format_html

from .dish_images import get_dish_image_url
from .models import Dish


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
        image_url = get_dish_image_url(obj)
        if image_url:
            return format_html(
                '<img src="{}" alt="{}" style="width:56px;height:42px;object-fit:cover;border-radius:6px;">',
                image_url,
                obj.name,
            )
        return '—'
