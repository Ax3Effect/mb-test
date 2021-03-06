# Generated by Django 2.2.8 on 2019-12-17 19:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pizza', '0002_auto_20191216_2121'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='anonymouscustomer',
            options={'ordering': ['id'], 'verbose_name': 'Anonymous Customer', 'verbose_name_plural': 'Anonymous Customers'},
        ),
        migrations.AlterModelOptions(
            name='menuitem',
            options={'ordering': ['id'], 'verbose_name': 'Pizza on Menu', 'verbose_name_plural': 'Pizzas on Menu'},
        ),
        migrations.AlterModelOptions(
            name='menuitemsize',
            options={'verbose_name': 'Pizza Size', 'verbose_name_plural': 'Pizza Sizes'},
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'Order', 'verbose_name_plural': 'Orders'},
        ),
        migrations.AlterModelOptions(
            name='orderitem',
            options={'verbose_name': 'Pizza on Order', 'verbose_name_plural': 'Pizzas on Order'},
        ),
        migrations.AlterModelOptions(
            name='orderitemsize',
            options={'verbose_name': 'Pizza Size on Order', 'verbose_name_plural': 'Pizza Sizes on Order'},
        ),
    ]
