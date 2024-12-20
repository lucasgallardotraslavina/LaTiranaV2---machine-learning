# Generated by Django 3.2 on 2024-11-15 23:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Aplicacion', '0008_editorial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Genero',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='libro',
            name='editorial',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Aplicacion.editorial'),
        ),
        migrations.AlterField(
            model_name='libro',
            name='genero',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Aplicacion.genero'),
        ),
    ]
