# Generated by Django 3.2.13 on 2022-10-06 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0009_alter_recipe_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(help_text='Фото блюда', upload_to='', verbose_name='Картинка'),
        ),
    ]