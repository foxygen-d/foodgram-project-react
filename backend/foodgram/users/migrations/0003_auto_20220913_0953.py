# Generated by Django 3.1.7 on 2022-09-13 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_user_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_subcribed',
            field=models.BooleanField(default=False, help_text='Отметьте для подписки на автора', verbose_name='Подписка на автора'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(db_index=True, help_text='Адрес электронной почты', max_length=50, unique=True, verbose_name='Электронная почта'),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=128, verbose_name='password'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(db_index=True, help_text='Логин пользователя', max_length=50, unique=True, verbose_name='Логин'),
        ),
    ]
