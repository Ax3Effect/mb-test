# Generated by Django 2.2.8 on 2019-12-14 19:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pizza', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitemsize',
            name='item',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='size', to='pizza.OrderItem'),
        ),
    ]