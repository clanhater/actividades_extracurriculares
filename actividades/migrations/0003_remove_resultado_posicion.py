# Generated by Django 5.0.3 on 2024-11-04 17:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('actividades', '0002_nombreactividad_tipoactividad_alter_actividad_nombre_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resultado',
            name='posicion',
        ),
    ]
