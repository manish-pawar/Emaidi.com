# Generated by Django 3.0.7 on 2020-07-24 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eb', '0002_auto_20200724_1651'),
    ]

    operations = [
        migrations.RenameField(
            model_name='worker',
            old_name='location',
            new_name='city',
        ),
        migrations.AddField(
            model_name='worker',
            name='village',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
