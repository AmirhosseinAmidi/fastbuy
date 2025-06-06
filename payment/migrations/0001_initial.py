# Generated by Django 5.2.1 on 2025-05-26 14:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ShippingAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=250)),
                ('email', models.CharField(max_length=300)),
                ('phone', models.CharField(max_length=20)),
                ('address1', models.CharField(blank=True, max_length=250, null=True)),
                ('address2', models.CharField(blank=True, max_length=250, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('state', models.CharField(blank=True, max_length=100)),
                ('zipcode', models.CharField(blank=True, max_length=30)),
                ('country', models.CharField(default='IRAN', max_length=100)),
                ('old_cart', models.CharField(blank=True, max_length=100, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
