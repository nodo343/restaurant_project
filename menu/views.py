from urllib.parse import quote

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST

from .cart import Cart
from .forms import CheckoutForm, LoginForm, RegisterForm
from .models import Dish, Order, OrderItem


def dish_list(request):
    dishes = Dish.objects.all()
    search_query = request.GET.get('q', '').strip()

    if search_query:
        dishes = dishes.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))

    # --- კატეგორიის ფილტრი (შეიძლება რამდენიმეს არჩევა) ---
    selected_categories = request.GET.getlist('category')
    if selected_categories:
        dishes = dishes.filter(category__in=selected_categories)

    # --- სიცხარის ფილტრი (ზუსტად არჩეული მაჩვენებელი 0-4) ---
    max_spice = request.GET.get('max_spice')
    if max_spice not in (None, ''):
        try:
            max_spice = int(max_spice)
            if 0 <= max_spice <= 4:
                dishes = dishes.filter(spice_level=max_spice)
            else:
                max_spice = None
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

    paginator = Paginator(dishes, 8)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'dishes': page_obj,
        'page_obj': page_obj,
        'search_query': search_query,
        'categories': Dish.Category.choices,
        'selected_categories': selected_categories,
        'max_spice': max_spice if max_spice not in (None, '') else '',
        'walnuts': walnuts or '',
        'vegetarian': vegetarian or '',
        'spice_levels': Dish.SPICE_LEVEL_CHOICES,
        'spice_slots': range(1, 5),
        'cart_count': len(Cart(request)),
    }
    return render(request, 'menu/dish_list.html', context)


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'რეგისტრაცია წარმატებით დასრულდა.')
            return redirect('dish_list')
    else:
        form = RegisterForm()

    context = {
        'form': form,
        'cart_count': len(Cart(request)),
    }
    return render(request, 'menu/register.html', context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dish_list')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, 'წარმატებით შეხვედით ანგარიშში.')
            return redirect(request.GET.get('next') or 'dish_list')
    else:
        form = LoginForm()

    context = {
        'form': form,
        'cart_count': len(Cart(request)),
    }
    return render(request, 'menu/login.html', context)


@require_POST
def logout_view(request):
    logout(request)
    messages.success(request, 'ანგარიშიდან გამოხვედით.')
    return redirect('dish_list')


@require_POST
def add_to_cart(request, dish_id):
    if not request.user.is_authenticated:
        messages.warning(request, 'კალათაში დამატებისთვის ჯერ გაიარეთ რეგისტრაცია ან შედით ანგარიშში.')
        next_url = request.META.get('HTTP_REFERER') or reverse('dish_list')
        return redirect(f"{reverse('login')}?next={quote(next_url)}")

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


@login_required
def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.warning(request, 'კალათა ცარიელია.')
        return redirect('cart_detail')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            cart_items = list(cart)
            with transaction.atomic():
                order = Order.objects.create(
                    user=request.user,
                    full_name=form.cleaned_data['full_name'],
                    phone=form.cleaned_data['phone'],
                    address=form.cleaned_data['address'],
                    note=form.cleaned_data['note'],
                    payment_method=form.cleaned_data['payment_method'],
                    payment_status=(
                        Order.PaymentStatus.PAID
                        if form.cleaned_data['payment_method'] == Order.PaymentMethod.CARD
                        else Order.PaymentStatus.PENDING
                    ),
                    total_price=cart.get_total_price(),
                )
                OrderItem.objects.bulk_create([
                    OrderItem(
                        order=order,
                        dish=item['dish'],
                        dish_name=item['dish'].name,
                        unit_price=item['dish'].price,
                        quantity=item['quantity'],
                        total_price=item['total_price'],
                    )
                    for item in cart_items
                ])
                cart.clear()

            messages.success(request, f'შეკვეთა #{order.id} მიღებულია. გადახდის სტატუსი: {order.get_payment_status_display()}.')
            return redirect('my_orders')
    else:
        initial = {
            'full_name': request.user.get_full_name() or request.user.username,
        }
        form = CheckoutForm(initial=initial)

    context = {
        'form': form,
        'cart': cart,
        'cart_count': len(cart),
    }
    return render(request, 'menu/checkout.html', context)


@login_required
def my_orders(request):
    orders = request.user.orders.prefetch_related('items')
    context = {
        'orders': orders,
        'cart_count': len(Cart(request)),
    }
    return render(request, 'menu/my_orders.html', context)


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

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        dish_total = '0.00'
        for item in cart:
            if item['dish'].id == dish_id:
                dish_total = f"{item['total_price']:.2f}"
                break
        return JsonResponse({
            'cart_count': len(cart),
            'cart_total': f"{cart.get_total_price():.2f}",
            'item_total': dish_total,
        })

    return redirect('cart_detail')
