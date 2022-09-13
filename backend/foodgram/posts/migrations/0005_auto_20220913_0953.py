# Generated by Django 3.1.7 on 2022-09-13 09:53

from django.db import migrations, models
import django.db.models.expressions
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_auto_20220905_1444'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ('-pub_date',), 'verbose_name': 'Рецепт', 'verbose_name_plural': 'Рецепты'},
        ),
        migrations.RemoveConstraint(
            model_name='subscription',
            name='unique_follower',
        ),
        migrations.AddField(
            model_name='recipe',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, help_text='Введите дату создания рецепта', verbose_name='Дата создания рецепта'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(default=None, help_text='Фото блюда', upload_to='recipes/images/', verbose_name='Картинка'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(help_text='Ингредиенты для приготовления блюда', related_name='recipes', through='posts.IngredientAmount', to='posts.Ingredient', verbose_name='Ингредиенты'),
        ),
        migrations.AddConstraint(
            model_name='favouriterecipe',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique_recipe_in_favorite'),
        ),
        migrations.AddConstraint(
            model_name='ingredientamount',
            constraint=models.UniqueConstraint(fields=('recipe', 'ingredient'), name='unique_ingredient_in_recipe'),
        ),
        migrations.AddConstraint(
            model_name='shoppinglist',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique_shopping_cart'),
        ),
        migrations.AddConstraint(
            model_name='subscription',
            constraint=models.UniqueConstraint(fields=('user', 'author'), name='unique_relationships'),
        ),
        migrations.AddConstraint(
            model_name='subscription',
            constraint=models.CheckConstraint(check=models.Q(_negated=True, user=django.db.models.expressions.F('author')), name='prevent_self_follow'),
        ),
    ]
