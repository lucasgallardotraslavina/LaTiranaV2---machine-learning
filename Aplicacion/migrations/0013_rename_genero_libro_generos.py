# Generated by Django 3.2 on 2024-11-16 19:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Aplicacion', '0012_rename_generos_libro_genero'),
    ]

    operations = [
        migrations.RenameField(
            model_name='libro',
            old_name='genero',
            new_name='generos',
        ),
    ]
