# Generated by Django 3.2 on 2024-11-16 19:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Aplicacion', '0011_auto_20241115_2136'),
    ]

    operations = [
        migrations.RenameField(
            model_name='libro',
            old_name='generos',
            new_name='genero',
        ),
    ]
