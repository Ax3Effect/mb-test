# Generated by Django 2.2.8 on 2019-12-14 19:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pizza', '0002_auto_20191214_1937'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitemsize',
            name='item',
        ),
        migrations.AddField(
            model_name='orderitem',
            name='size',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='pizza.OrderItemSize'),
            preserve_default=False,
        ),
    ]
