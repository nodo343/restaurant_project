from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models


class Dish(models.Model):
    SPICE_LEVEL_CHOICES = [
        (0, '0 - არ არის ცხარე'),
        (1, '1 - ოდნავ ცხარე'),
        (2, '2 - საშუალოდ ცხარე'),
        (3, '3 - ცხარე'),
        (4, '4 - ძალიან ცხარე'),
    ]

    class Category(models.TextChoices):
        SALADS = 'Salads', 'Salads'
        SOUPS = 'Soups', 'Soups'
        CHICKEN = 'Chicken-Dishes', 'Chicken-Dishes'
        BEEF = 'Beef-Dishes', 'Beef-Dishes'
        SEAFOOD = 'Seafood-Dishes', 'Seafood-Dishes'
        VEGETABLE = 'Vegetable-Dishes', 'Vegetable-Dishes'
        BITS_BITES = 'Bits&Bites', 'Bits&Bites'
        ON_THE_SIDE = 'On-The-Side', 'On-The-Side'

    name = models.CharField('დასახელება', max_length=150)
    category = models.CharField('კატეგორია', max_length=30, choices=Category.choices)
    image = models.ImageField('სურათი', upload_to='dishes/', blank=True, null=True)
    spice_level = models.PositiveSmallIntegerField(
        'სიცხარის მაჩვენებელი',
        choices=SPICE_LEVEL_CHOICES,
        validators=[MinValueValidator(0), MaxValueValidator(4)],
        default=0,
    )
    has_walnuts = models.BooleanField('ნიგვზიანია', default=False)
    is_vegetarian = models.BooleanField('ვეგეტარიანულია', default=False)
    price = models.DecimalField('ფასი', max_digits=6, decimal_places=2)
    description = models.TextField('აღწერა', blank=True)

    class Meta:
        verbose_name = 'კერძი'
        verbose_name_plural = 'კერძები'
        ordering = ['category', 'name']

    def __str__(self):
        return self.name


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'მიღებულია'
        PREPARING = 'preparing', 'მზადდება'
        ON_THE_WAY = 'on_the_way', 'გზაშია'
        DELIVERED = 'delivered', 'ჩაბარებულია'
        CANCELLED = 'cancelled', 'გაუქმებულია'

    class PaymentMethod(models.TextChoices):
        CASH = 'cash', 'ნაღდი ანგარიშსწორება'
        CARD = 'card', 'ბარათით გადახდა'

    class PaymentStatus(models.TextChoices):
        PENDING = 'pending', 'გადახდა მოლოდინშია'
        PAID = 'paid', 'გადახდილია'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    full_name = models.CharField('სახელი და გვარი', max_length=180)
    phone = models.CharField('ტელეფონი', max_length=30)
    address = models.CharField('მისამართი', max_length=255)
    note = models.TextField('შენიშვნა', blank=True)
    status = models.CharField('სტატუსი', max_length=20, choices=Status.choices, default=Status.PENDING)
    payment_method = models.CharField(
        'გადახდის მეთოდი',
        max_length=20,
        choices=PaymentMethod.choices,
        default=PaymentMethod.CASH,
    )
    payment_status = models.CharField(
        'გადახდის სტატუსი',
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
    )
    total_price = models.DecimalField('ჯამი', max_digits=8, decimal_places=2)
    created_at = models.DateTimeField('შექმნის დრო', auto_now_add=True)
    updated_at = models.DateTimeField('განახლების დრო', auto_now=True)

    class Meta:
        verbose_name = 'შეკვეთა'
        verbose_name_plural = 'შეკვეთები'
        ordering = ['-created_at']

    def __str__(self):
        return f'შეკვეთა #{self.id}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    dish = models.ForeignKey(Dish, on_delete=models.SET_NULL, blank=True, null=True, related_name='order_items')
    dish_name = models.CharField('კერძი', max_length=150)
    unit_price = models.DecimalField('ერთეულის ფასი', max_digits=6, decimal_places=2)
    quantity = models.PositiveIntegerField('რაოდენობა')
    total_price = models.DecimalField('ჯამი', max_digits=8, decimal_places=2)

    class Meta:
        verbose_name = 'შეკვეთის კერძი'
        verbose_name_plural = 'შეკვეთის კერძები'

    def __str__(self):
        return f'{self.dish_name} x{self.quantity}'
