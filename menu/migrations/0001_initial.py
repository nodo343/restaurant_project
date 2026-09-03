import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='დასახელება')),
                ('category', models.CharField(choices=[
                    ('Salads', 'Salads'),
                    ('Soups', 'Soups'),
                    ('Chicken-Dishes', 'Chicken-Dishes'),
                    ('Beef-Dishes', 'Beef-Dishes'),
                    ('Seafood-Dishes', 'Seafood-Dishes'),
                    ('Vegetable-Dishes', 'Vegetable-Dishes'),
                    ('Bits&Bites', 'Bits&Bites'),
                    ('On-The-Side', 'On-The-Side'),
                ], max_length=30, verbose_name='კატეგორია')),
                ('image', models.ImageField(blank=True, null=True, upload_to='dishes/', verbose_name='სურათი')),
                ('spice_level', models.PositiveSmallIntegerField(default=0, validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(4),
                ], verbose_name='სიცხარის მაჩვენებელი')),
                ('has_walnuts', models.BooleanField(default=False, verbose_name='ნიგვზიანია')),
                ('is_vegetarian', models.BooleanField(default=False, verbose_name='ვეგეტარიანულია')),
                ('price', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='ფასი')),
                ('description', models.TextField(blank=True, verbose_name='აღწერა')),
            ],
            options={
                'verbose_name': 'კერძი',
                'verbose_name_plural': 'კერძები',
                'ordering': ['category', 'name'],
            },
        ),
    ]
