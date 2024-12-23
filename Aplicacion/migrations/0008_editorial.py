# Generated by Django 3.2 on 2024-11-15 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Aplicacion', '0007_auto_20241108_1643'),
    ]

    operations = [
        migrations.CreateModel(
            name='Editorial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('direccion', models.TextField()),
                ('telefono', models.CharField(max_length=15)),
                ('correo_electronico', models.EmailField(max_length=254, unique=True)),
                ('anio_fundacion', models.PositiveIntegerField()),
            ],
        ),
    ]
