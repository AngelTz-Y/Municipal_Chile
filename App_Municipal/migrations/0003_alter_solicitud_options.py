# Generated by Django 5.0 on 2024-11-16 01:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App_Municipal', '0002_solicitud_delete_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='solicitud',
            options={'permissions': [('buscar_solicitud', 'Puede buscar solicitudes')]},
        ),
    ]
