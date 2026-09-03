from django.templatetags.static import static


DISH_IMAGE_FILES = {
    'Caesar Salad': 'caesar-salad.jpg',
    'Greek Salad': 'greek-salad.jpg',
    'Pkhali Salad': 'pkhali-salad.jpg',
    'Chicken Soup': 'chicken-soup.jpg',
    'Kharcho': 'kharcho.jpg',
    'Lentil Soup': 'lentil-soup.jpg',
    'Grilled Chicken Breast': 'grilled-chicken-breast.jpg',
    'Spicy Chicken Wings': 'spicy-chicken-wings.jpg',
    'Chicken Satsivi': 'chicken-satsivi.jpg',
    'Beef Steak': 'beef-steak.jpg',
    'Beef Burger': 'beef-burger.jpg',
    'Spicy Beef Chili': 'spicy-beef-chili.jpg',
    'Grilled Salmon': 'grilled-salmon.jpg',
    'Spicy Shrimp': 'spicy-shrimp.jpg',
    'Fish & Chips': 'fish-and-chips.jpg',
    'Grilled Vegetables': 'grilled-vegetables.jpg',
    'Spicy Eggplant': 'spicy-eggplant.jpg',
    'Vegetable Stew': 'vegetable-stew.jpg',
    'Cheese Sticks': 'cheese-sticks.jpg',
    'Spicy Nachos': 'spicy-nachos.jpg',
    'Chicken Nuggets': 'chicken-nuggets.jpg',
    'French Fries': 'french-fries.jpg',
    'Garlic Bread': 'garlic-bread.jpg',
    'Rice Pilaf': 'rice-pilaf.jpg',
}


def get_dish_image_url(dish):
    if dish.image:
        return dish.image.url

    image_file = DISH_IMAGE_FILES.get(dish.name)
    if not image_file:
        return ''

    return static(f'menu/img/dishes/{image_file}')
