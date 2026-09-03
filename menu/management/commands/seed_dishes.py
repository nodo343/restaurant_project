from django.core.management.base import BaseCommand
from menu.models import Dish


SAMPLE_DISHES = [
    # (name, category, spice, walnuts, vegetarian, price)
    ("Caesar Salad", Dish.Category.SALADS, 0, False, False, 14.50),
    ("Greek Salad", Dish.Category.SALADS, 0, False, True, 12.00),
    ("Pkhali Salad", Dish.Category.SALADS, 1, True, True, 11.00),
    ("Chicken Soup", Dish.Category.SOUPS, 1, False, False, 9.50),
    ("Kharcho", Dish.Category.SOUPS, 3, True, False, 10.50),
    ("Lentil Soup", Dish.Category.SOUPS, 1, False, True, 8.50),
    ("Grilled Chicken Breast", Dish.Category.CHICKEN, 1, False, False, 18.00),
    ("Spicy Chicken Wings", Dish.Category.CHICKEN, 4, False, False, 15.00),
    ("Chicken Satsivi", Dish.Category.CHICKEN, 1, True, False, 17.50),
    ("Beef Steak", Dish.Category.BEEF, 2, False, False, 26.00),
    ("Beef Burger", Dish.Category.BEEF, 2, False, False, 16.50),
    ("Spicy Beef Chili", Dish.Category.BEEF, 4, False, False, 19.00),
    ("Grilled Salmon", Dish.Category.SEAFOOD, 0, False, False, 24.00),
    ("Spicy Shrimp", Dish.Category.SEAFOOD, 3, False, False, 22.00),
    ("Fish & Chips", Dish.Category.SEAFOOD, 1, False, False, 18.50),
    ("Grilled Vegetables", Dish.Category.VEGETABLE, 0, False, True, 12.50),
    ("Spicy Eggplant", Dish.Category.VEGETABLE, 3, True, True, 11.50),
    ("Vegetable Stew", Dish.Category.VEGETABLE, 1, False, True, 13.00),
    ("Cheese Sticks", Dish.Category.BITS_BITES, 0, False, True, 8.00),
    ("Spicy Nachos", Dish.Category.BITS_BITES, 3, False, True, 9.00),
    ("Chicken Nuggets", Dish.Category.BITS_BITES, 1, False, False, 8.50),
    ("French Fries", Dish.Category.ON_THE_SIDE, 0, False, True, 6.00),
    ("Garlic Bread", Dish.Category.ON_THE_SIDE, 0, True, True, 5.50),
    ("Rice Pilaf", Dish.Category.ON_THE_SIDE, 0, False, True, 6.50),
]


class Command(BaseCommand):
    help = "Seeds the database with sample restaurant dishes."

    def handle(self, *args, **options):
        created_count = 0
        for name, category, spice, walnuts, vegetarian, price in SAMPLE_DISHES:
            _, created = Dish.objects.get_or_create(
                name=name,
                defaults={
                    'category': category,
                    'spice_level': spice,
                    'has_walnuts': walnuts,
                    'is_vegetarian': vegetarian,
                    'price': price,
                },
            )
            if created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(
            f'დასრულდა. დაემატა {created_count} ახალი კერძი (სულ {Dish.objects.count()}).'
        ))
