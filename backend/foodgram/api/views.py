import io

from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from posts.models import Ingredient, Recipe, ShoppingList, Subscription, Tag
from .mixins import CreateDeleteMixin
from .permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from .serializers import (IngredientSerializer, PasswordSerializer,
                          RecipePostSerializer, RecipeSerializer,
                          SubscriptionSerializer, TagSerializer,
                          UserSerializer)

FILENAME = 'my_shopping_list.pdf'

User = get_user_model()


class CreateUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = LimitOffsetPagination
    http_method_name = (
        'get',
        'post',
        'put',
        'patch',
        'delete',
    )

    @action(
        detail=False,
        url_path='set_password',
        methods=['POST'],
        permission_classes=(IsAuthenticated,),
    )
    def set_password(self, request):
        user = request.user
        context = {'request': request}
        serializer = PasswordSerializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({'status': 'Пароль установлен!'})

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=(IsAuthenticated,),
    )
    def me(self, request, pk=None):
        if request.method == ['GET']:
            serializer = self.get_serializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        permission_classes=(IsAuthenticated,),
    )
    def subscriptions(self, request):
        queryset = User.objects.filter(following__user=request.user)
        obj = self.paginate_queryset(queryset)
        serializer = SubscriptionSerializer(
            obj, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=(IsAuthenticated,),
    )
    def subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, id=id)
        if request.method == 'POST':
            if user == author:
                return Response(
                    data={'detail': 'Нельзя подписываться на себя!'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if Subscription.objects.filter(user=user, author=author).exists():
                return Response(
                    data={'detail': 'Вы уже подписаны на этого автора!'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            Subscription.objects.create(user=user, author=author)
            serializer = self.get_serializer(author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            subscribe = Subscription.objects.filter(user=user, author=author)
            if not subscribe.exists():
                return Response(
                    data={'detail': 'Вы не подписаны на этого автора!'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            subscribe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return False


class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = LimitOffsetPagination


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = LimitOffsetPagination


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeSerializer
        else:
            return RecipePostSerializer

    @action(
        url_path='download_shopping_cart',
        detail=False,
        permission_classes=(IsAuthenticated,),
    )
    def download_shopping_cart(self, request):
        buffer = io.BytesIO()
        page = canvas.Canvas(buffer)
        pdfmetrics.registerFont(TTFont('List', 'data/List.ttf'))
        x_position, y_position = 50, 800
        shopping_cart = (
            ShoppingList.objects.filter(user=request.user)
            .values(
                'recipe__ingredients__name',
                'recipe__ingredients__measurement_unit',
            )
            .annotate(amount=Sum('recipe__recipesingredients__amount'))
            .order_by()
        )
        page.setFont('List', 14)
        if shopping_cart:
            indent = 20
            page.drawString(x_position, y_position, 'Cписок покупок:')
            for index, recipe in enumerate(shopping_cart, start=1):
                page.drawString(
                    x_position,
                    y_position - indent,
                    f'{index}. {recipe["recipe__ingredients__name"]} - '
                    f'{recipe["amount"]} '
                    f'{recipe["recipe__ingredients__measurement_unit"]}.',
                )
                y_position -= 15
                if y_position <= 50:
                    page.showPage()
                    y_position = 800
            page.save()
            buffer.seek(0)
            return FileResponse(buffer, as_attachment=True, filename=FILENAME)
        page.setFont('List', 24)
        page.drawString(x_position, y_position, 'Cписок покупок пуст!')
        page.save()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename=FILENAME)


class FavouriteRecipeViewSet(viewsets.ModelViewSet, CreateDeleteMixin):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = LimitOffsetPagination


class ShoppingListViewSet(viewsets.ModelViewSet, CreateDeleteMixin):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (
        IsAdminOrReadOnly,
        IsAuthorOrReadOnly,
        IsAuthenticated,
    )
    pagination_class = LimitOffsetPagination
