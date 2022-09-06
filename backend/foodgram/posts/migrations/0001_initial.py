# Generated by Django 2.2.16 on 2022-08-30 14:43

import colorfield.fields
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, help_text='Название ингредиента', max_length=50, verbose_name='Название')),
                ('measurement_unit', models.CharField(default='г', help_text='Единицы измерения', max_length=10, verbose_name='Единицы измерения')),
            ],
            options={
                'verbose_name': 'Ингредиент',
                'verbose_name_plural': 'Ингредиенты',
            },
        ),
        migrations.CreateModel(
            name='IngredientAmount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveSmallIntegerField(default=1, help_text='Количество', validators=[django.core.validators.MinValueValidator(1, 'Количество используемых в рецепте ингредиентов не может быть меньше 1!'), django.core.validators.MaxValueValidator(1000, 'Количество используемых в рецепте ингредиентов не может быть больше 1000!')], verbose_name='Количество')),
                ('ingredient', models.ForeignKey(help_text='Ингредиент', on_delete=django.db.models.deletion.CASCADE, to='posts.Ingredient', verbose_name='Ингредиент')),
            ],
            options={
                'verbose_name': 'Кол-во ингредиентов',
                'verbose_name_plural': 'Кол-во ингредиентов',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Название тега', max_length=20, unique=True, verbose_name='Название')),
                ('color', colorfield.fields.ColorField(default='#FF0000', help_text='Цветовой HEX-код', image_field=None, max_length=18, samples=None, verbose_name='Цветовой HEX-код')),
                ('slug', models.SlugField(help_text='Slug тега', max_length=20, unique=True, verbose_name='Slug')),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Название рецепта', max_length=100, verbose_name='Название')),
                ('image', models.ImageField(help_text='Фото блюда', upload_to='recipes/', verbose_name='Картинка')),
                ('text', models.TextField(help_text='Описание рецепта', verbose_name='Описание')),
                ('cooking_time', models.PositiveSmallIntegerField(default=1, help_text='Время приготовления в минутах', validators=[django.core.validators.MinValueValidator(1, 'Запрещено добавлять рецепты блюд, время приготовления которых менее 1 минуты!'), django.core.validators.MaxValueValidator(180, 'Запрещено добавлять рецепты блюд, время приготовления которых более 3 часов!')], verbose_name='Время приготовления')),
                ('author', models.ForeignKey(help_text='Автор рецепта', on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL, verbose_name='Автор публикации')),
                ('ingredients', models.ManyToManyField(help_text='Ингредиенты для приготовления блюда', through='posts.IngredientAmount', to='posts.Ingredient', verbose_name='Ингредиенты')),
                ('tags', models.ManyToManyField(help_text='Теги', to='posts.Tag', verbose_name='Тег')),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепты',
            },
        ),
        migrations.AddField(
            model_name='ingredientamount',
            name='recipe',
            field=models.ForeignKey(help_text='Рецепт', on_delete=django.db.models.deletion.CASCADE, to='posts.Recipe', verbose_name='Рецепт'),
        ),
    ]
