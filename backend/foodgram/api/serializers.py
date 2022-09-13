import base64

import django.contrib.auth.password_validation as validators
import webcolors
from django.core.files.base import ContentFile
from django.forms import ValidationError
from posts.models import (Ingredient, IngredientAmount, Recipe, Subscription,
                          Tag)
from rest_framework import serializers
from users.models import User


class PasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(max_length=150)
    current_password = serializers.CharField(max_length=150)

    def validate_current_password(self, data):
        user = self.context['request'].user
        current_password = data
        if not user.check_password(current_password):
            raise ValidationError('Неверный пароль, попробуйте еще раз!')
        return current_password

    def validate(self, data):
        if data['current_password'] == data['new_password']:
            raise ValidationError('Пароли не должны совпадать!')
        return data


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name',
                  'last_name', 'is_subscribed',)

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save
        return user

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Subscription.objects.filter(
            user=request.user, author=obj
        ).exists()

    def validate_email(self, data):
        if User.objects.filter(email=data).exists():
            raise ValidationError('Пользователь с данной почтой существует!')
        return data

    def validate_password(self, password):
        validators.validate_password(password)
        return password


class SubscribeRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time',)


class SubscriptionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='author.id')
    email = serializers.EmailField(source='author.email')
    username = serializers.CharField(source='author.username')
    first_name = serializers.CharField(source='author.first_name')
    last_name = serializers.CharField(source='author.last_name')
    recipes = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()
    recipes_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Subscription
        fields = ('email', 'id', 'username', 'first_name', 'last_name',)

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        return (
            request.user.is_authenticated
            and Subscription.objects.filter(
                user=request.user, author=obj
            ).exists()
        )

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        recipes = (
            obj.author.recipe.all()[:int(limit)] if limit
            else obj.author.recipe.all())
        return SubscribeRecipeSerializer(
            recipes,
            many=True).data


class Hex2NameColor(serializers.Field):
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        try:
            data = webcolors.hex_to_name(data)
        except ValueError:
            raise serializers.ValidationError('Для этого цвета нет имени')
        return data


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для тегов."""
    color = Hex2NameColor()

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для ингредиентов."""
    class Meta:
        model = Ingredient
        fields = '__all__'


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для рецептов."""
    author = UserSerializer()
    image = Base64ImageField(required=False, allow_null=True)
    ingredients = IngredientSerializer(many=True)
    tags = TagSerializer(many=True)

    class Meta:
        model = Recipe
        fields = '__all__'

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)

        for ingredient in ingredients:
            current_ingredient, status = Ingredient.objects.get_or_create(
                **ingredient
            )
            IngredientAmount.objects.create(
                ingredient=current_ingredient, recipe=recipe
            )
        for tag in tags:
            current_tag, status = Tag.objects.get_or_create(
                **tag
            )
            Tag.objects.create(
                tag=current_tag, recipe=recipe
            )

        return recipe

    def update(self, instance, validated_data):
        instance.author = validated_data.get('author', instance.author)
        instance.name = validated_data.get('name', instance.name)
        instance.image = validated_data.get('image', instance.image)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get('cooking_time',
                                                   instance.cooking_time)

        if 'ingredients' in validated_data:
            ingredients_data = validated_data.pop('ingredients')
            lst = []
            for ingredient in ingredients_data:
                current_ingredient, status = Ingredient.objects.get_or_create(
                    **ingredient
                    )
                lst.append(current_ingredient)
            instance.ingredients.set(lst)

        if 'tags' in validated_data:
            tags_data = validated_data.pop('tags')
            lst = []
            for tag in tags_data:
                current_tag, status = Tag.objects.get_or_create(
                    **tag
                    )
                lst.append(current_tag)
            instance.tags.set(lst)

        instance.save()
        return instance


class AddToIngredientInRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления количества ингредиентов."""

    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField(write_only=True)

    class Meta:
        fields = ('id', 'amount')
        model = IngredientAmount


class RecipePostSerializer():
    author = UserSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
    ingredients = AddToIngredientInRecipeSerializer(
        source='recipesingredients', many=True
    )
    image = Base64ImageField(max_length=None, use_url=True)

    class Meta:
        fields = (
            'id',
            'author',
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time',
        )
        model = Recipe

    def validate_ingredients(self, ingredients):
        print(ingredients)
        if not ingredients:
            raise serializers.ValidationError(
                'Необходимо выбрать ингредиенты!'
            )

        for ingredient in ingredients:
            if ingredient['amount'] < 1:
                raise serializers.ValidationError(
                    'Количество не может быть меньше 1!'
                )
        ids = [ingredient['id'] for ingredient in ingredients]
        if len(ids) != len(set(ids)):
            raise serializers.ValidationError(
                'Данный ингредиент уже есть в рецепте!'
            )
        return ingredients

    def add_ingredients_and_tags(self, tags, ingredients, recipe):
        for tag in tags:
            recipe.tags.add(tag)
            recipe.save()
        instances = [
            IngredientAmount(
                recipe=recipe,
                ingredient=ingredient['id'],
                amount=ingredient['amount'],
            )
            for ingredient in ingredients
        ]
        IngredientAmount.objects.bulk_create(instances)
        return recipe
