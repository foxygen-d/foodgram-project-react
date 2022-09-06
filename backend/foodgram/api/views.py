from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import filters, permissions, viewsets
from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenViewBase

from posts.models import Tag, Ingredient, Recipe, Subscription
# from .mixins import SubscribeMixin
from .serializers import (TagSerializer, IngredientSerializer,
                          RecipeSerializer, UserSerializer,
                          SubscriptionSerializer,)


MAIL_SUBJECT = 'YAMDB: Your confirmation code'
MAIL_BODY = 'Hi {username}, here is your code: {code}'
User = get_user_model()


class UsersViewSet(viewsets.ModelViewSet):
    """Представление для пользователей."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination


class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    pagination_class = LimitOffsetPagination


class TagViewSet(viewsets.ModelViewSet):
    """Представление для тегов."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = LimitOffsetPagination


class IngredientViewSet(viewsets.ModelViewSet):
    """Представление для ингредиентов."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = LimitOffsetPagination

class RecipeViewSet(viewsets.ModelViewSet):
    """Представление для рецептов."""
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = LimitOffsetPagination
