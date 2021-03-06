# Generated by Django 3.0.7 on 2020-07-26 13:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eb', '0004_worker_salary'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='eb.Customer')),
                ('worker', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='eb.Worker')),
            ],
        ),
    ]
