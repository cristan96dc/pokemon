# Generated by Django 5.0 on 2024-03-24 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registro',
            name='fecha_presentacion',
            field=models.DateField(),
        ),
    ]