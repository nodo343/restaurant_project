from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Dish(models.Model):
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
