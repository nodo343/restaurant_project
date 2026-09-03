from shutil import copyfile

from django.conf import settings
from django.core.management.base import BaseCommand

from menu.models import Dish


SAMPLE_DISHES = [
    # (name, category, spice, walnuts, vegetarian, price, image)
    ("Caesar Salad", Dish.Category.SALADS, 0, False, False, 14.50, "caesar-salad.jpg"),
    ("Greek Salad", Dish.Category.SALADS, 0, False, True, 12.00, "greek-salad.jpg"),
    ("Pkhali Salad", Dish.Category.SALADS, 1, True, True, 11.00, "pkhali-salad.jpg"),
    ("Chicken Soup", Dish.Category.SOUPS, 1, False, False, 9.50, "chicken-soup.jpg"),
    ("Kharcho", Dish.Category.SOUPS, 3, True, False, 10.50, "kharcho.jpg"),
    ("Lentil Soup", Dish.Category.SOUPS, 1, False, True, 8.50, "lentil-soup.jpg"),
    ("Grilled Chicken Breast", Dish.Category.CHICKEN, 1, False, False, 18.00, "grilled-chicken-breast.jpg"),
    ("Spicy Chicken Wings", Dish.Category.CHICKEN, 4, False, False, 15.00, "spicy-chicken-wings.jpg"),
    ("Chicken Satsivi", Dish.Category.CHICKEN, 1, True, False, 17.50, "chicken-satsivi.jpg"),
    ("Beef Steak", Dish.Category.BEEF, 2, False, False, 26.00, "beef-steak.jpg"),
    ("Beef Burger", Dish.Category.BEEF, 2, False, False, 16.50, "beef-burger.jpg"),
    ("Spicy Beef Chili", Dish.Category.BEEF, 4, False, False, 19.00, "spicy-beef-chili.jpg"),
    ("Grilled Salmon", Dish.Category.SEAFOOD, 0, False, False, 24.00, "grilled-salmon.jpg"),
    ("Spicy Shrimp", Dish.Category.SEAFOOD, 3, False, False, 22.00, "spicy-shrimp.jpg"),
    ("Fish & Chips", Dish.Category.SEAFOOD, 1, False, False, 18.50, "fish-and-chips.jpg"),
    ("Grilled Vegetables", Dish.Category.VEGETABLE, 0, False, True, 12.50, "grilled-vegetables.jpg"),
    ("Spicy Eggplant", Dish.Category.VEGETABLE, 3, True, True, 11.50, "spicy-eggplant.jpg"),
    ("Vegetable Stew", Dish.Category.VEGETABLE, 1, False, True, 13.00, "vegetable-stew.jpg"),
    ("Cheese Sticks", Dish.Category.BITS_BITES, 0, False, True, 8.00, "cheese-sticks.jpg"),
    ("Spicy Nachos", Dish.Category.BITS_BITES, 3, False, True, 9.00, "spicy-nachos.jpg"),
    ("Chicken Nuggets", Dish.Category.BITS_BITES, 1, False, False, 8.50, "chicken-nuggets.jpg"),
    ("French Fries", Dish.Category.ON_THE_SIDE, 0, False, True, 6.00, "french-fries.jpg"),
    ("Garlic Bread", Dish.Category.ON_THE_SIDE, 0, True, True, 5.50, "garlic-bread.jpg"),
    ("Rice Pilaf", Dish.Category.ON_THE_SIDE, 0, False, True, 6.50, "rice-pilaf.jpg"),
]


class Command(BaseCommand):
    help = "Seeds the database with sample restaurant dishes."

    def handle(self, *args, **options):
        created_count = 0
        updated_images = 0
        media_dishes_dir = settings.MEDIA_ROOT / 'dishes'
        media_dishes_dir.mkdir(parents=True, exist_ok=True)

        for name, category, spice, walnuts, vegetarian, price, image_file in SAMPLE_DISHES:
            source_image = settings.BASE_DIR / 'menu' / 'static' / 'menu' / 'img' / 'dishes' / image_file
            target_image = media_dishes_dir / image_file
            if source_image.exists() and not target_image.exists():
                copyfile(source_image, target_image)

            dish, created = Dish.objects.get_or_create(
                name=name,
                defaults={
                    'category': category,
                    'image': f'dishes/{image_file}',
                    'spice_level': spice,
                    'has_walnuts': walnuts,
                    'is_vegetarian': vegetarian,
                    'price': price,
                },
            )
            if created:
                created_count += 1
            elif not dish.image and target_image.exists():
                dish.image = f'dishes/{image_file}'
                dish.save(update_fields=['image'])
                updated_images += 1

        self.stdout.write(self.style.SUCCESS(
            f'დასრულდა. დაემატა {created_count} ახალი კერძი, '
            f'სურათი განახლდა {updated_images} კერძზე (სულ {Dish.objects.count()}).'
        ))
