from django.contrib import admin
from .models import Dish


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'spice_level', 'has_walnuts', 'is_vegetarian', 'price')
    list_filter = ('category', 'spice_level', 'has_walnuts', 'is_vegetarian')
    search_fields = ('name',)
