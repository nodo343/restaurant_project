from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST

from .models import Dish
from .cart import Cart


def dish_list(request):
    dishes = Dish.objects.all()

    # --- კატეგორიის ფილტრი (შეიძლება რამდენიმეს არჩევა) ---
    selected_categories = request.GET.getlist('category')
    if selected_categories:
        dishes = dishes.filter(category__in=selected_categories)

    # --- სიცხარის ფილტრი (მაქსიმალური მაჩვენებელი 0-4) ---
    max_spice = request.GET.get('max_spice')
    if max_spice not in (None, ''):
        try:
            max_spice = int(max_spice)
            dishes = dishes.filter(spice_level__lte=max_spice)
        except ValueError:
            max_spice = None

    # --- ნიგვზიანობის ფილტრი ---
    walnuts = request.GET.get('walnuts')  # 'yes' / 'no' / None (ყველა)
    if walnuts == 'yes':
        dishes = dishes.filter(has_walnuts=True)
    elif walnuts == 'no':
        dishes = dishes.filter(has_walnuts=False)

    # --- ვეგეტარიანულობის ფილტრი ---
    vegetarian = request.GET.get('vegetarian')  # 'yes' / 'no' / None (ყველა)
    if vegetarian == 'yes':
        dishes = dishes.filter(is_vegetarian=True)
    elif vegetarian == 'no':
        dishes = dishes.filter(is_vegetarian=False)

    context = {
        'dishes': dishes,
        'categories': Dish.Category.choices,
        'selected_categories': selected_categories,
        'max_spice': max_spice if max_spice not in (None, '') else '',
        'walnuts': walnuts or '',
        'vegetarian': vegetarian or '',
        'spice_range': range(0, 5),
        'cart_count': len(Cart(request)),
    }
    return render(request, 'menu/dish_list.html', context)


@require_POST
def add_to_cart(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    cart = Cart(request)
    cart.add(dish=dish, quantity=1)
    messages.success(request, f'"{dish.name}" დაემატა კალათაში.')
    # მომხმარებელს ვაბრუნებთ იმ გვერდზე, საიდანაც მოვიდა (ფილტრები არ იკარგება)
    redirect_to = request.META.get('HTTP_REFERER') or 'dish_list'
    return redirect(redirect_to)


def cart_detail(request):
    cart = Cart(request)
    context = {
        'cart': cart,
        'cart_count': len(cart),
    }
    return render(request, 'menu/cart.html', context)


@require_POST
def update_cart_item(request, dish_id):
    cart = Cart(request)
    action = request.POST.get('action')

    if action == 'remove':
        cart.remove(dish_id)
    else:
        try:
            quantity = int(request.POST.get('quantity', 1))
        except ValueError:
            quantity = 1
        cart.set_quantity(dish_id, quantity)

    return redirect('cart_detail')
