# Generated by Django 3.2.13 on 2022-10-06 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0007_auto_20221006_1240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(default=None, help_text='Фото блюда', upload_to='media', verbose_name='Картинка'),
        ),
    ]
