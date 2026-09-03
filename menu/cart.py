from decimal import Decimal
from .models import Dish

CART_SESSION_KEY = 'cart'


class Cart:
    """
    მარტივი, სესიაზე დაფუძნებული საყიდლების კალათა.
    კალათა ინახავს ლექსიკონს {dish_id (str): quantity (int)}
    request.session-ში, ასე რომ არ სჭირდება ავტორიზაცია
    და მუშაობს ცალკეული ბრაუზერის სესიისთვის.
    """

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_KEY)
        if cart is None:
            cart = self.session[CART_SESSION_KEY] = {}
        self.cart = cart

    def add(self, dish, quantity=1):
        dish_id = str(dish.id)
        if dish_id in self.cart:
            self.cart[dish_id] += quantity
        else:
            self.cart[dish_id] = quantity
        if self.cart[dish_id] < 1:
            self.cart[dish_id] = 1
        self.save()

    def set_quantity(self, dish_id, quantity):
        dish_id = str(dish_id)
        if quantity <= 0:
            self.remove(dish_id)
            return
        if dish_id in self.cart:
            self.cart[dish_id] = quantity
            self.save()

    def remove(self, dish_id):
        dish_id = str(dish_id)
        if dish_id in self.cart:
            del self.cart[dish_id]
            self.save()

    def clear(self):
        self.session[CART_SESSION_KEY] = {}
        self.save()

    def save(self):
        self.session.modified = True

    def __iter__(self):
        dish_ids = self.cart.keys()
        dishes = Dish.objects.filter(id__in=dish_ids)
        dishes_by_id = {str(dish.id): dish for dish in dishes}
        for dish_id, quantity in self.cart.items():
            dish = dishes_by_id.get(dish_id)
            if not dish:
                continue
            total_price = dish.price * quantity
            yield {
                'dish': dish,
                'quantity': quantity,
                'total_price': total_price,
            }

    def __len__(self):
        return sum(self.cart.values())

    def get_total_price(self):
        total = Decimal('0.00')
        for item in self:
            total += item['total_price']
        return total
