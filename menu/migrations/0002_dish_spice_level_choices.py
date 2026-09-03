import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dish',
            name='spice_level',
            field=models.PositiveSmallIntegerField(
                choices=[
                    (0, '0 - არ არის ცხარე'),
                    (1, '1 - ოდნავ ცხარე'),
                    (2, '2 - საშუალოდ ცხარე'),
                    (3, '3 - ცხარე'),
                    (4, '4 - ძალიან ცხარე'),
                ],
                default=0,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(4),
                ],
                verbose_name='სიცხარის მაჩვენებელი',
            ),
        ),
    ]
