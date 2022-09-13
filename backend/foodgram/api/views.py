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

from posts.models import (FavouriteRecipe, Ingredient, Recipe, ShoppingList,
                          Subscription, Tag)
from .permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from .serializers import (IngredientSerializer, PasswordSerializer,
                          RecipePostSerializer, RecipeSerializer,
                          SubscriptionSerializer, TagSerializer,
                          UserSerializer)


FILENAME = 'my_shopping_cart.pdf'

User = get_user_model()


class CreateUserViewSet(UserViewSet):
    """Вьюсет для пользователя."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
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
        if serializer.is_valid():
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'status': 'Пароль установлен!'})
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

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


class SubscriptionViewSet(viewsets.ModelViewSet):
    """Представление для подписок пользователя."""
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = LimitOffsetPagination


class TagViewSet(viewsets.ModelViewSet):
    """Представление для тегов."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination


class IngredientViewSet(viewsets.ModelViewSet):
    """Представление для ингредиентов."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = LimitOffsetPagination


class RecipeViewSet(viewsets.ModelViewSet):
    """Представление для рецептов."""
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
        """Получение списка покупок в формате pdf."""
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


class FavouriteRecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def create(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        if FavouriteRecipe.objects.filter(user=request.user, recipe=recipe).exists():
            return Response(
                data={'detail': 'Этот рецепт уже есть в избранном!'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        FavouriteRecipe.objects.create(user=request.user, recipe=recipe)
        serializer = self.get_serializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, recipe_id):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        favorite = FavouriteRecipe.objects.filter(user=user, recipe=recipe)
        if not favorite.exists():
            return Response(
                data={'detail': 'Вы не подписаны на этот рецепт!'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        favorite.delete()
        return Response(
            f'Рецепт {favorite} удален из избранного у пользователя'
            f' {request.user}',
            status=status.HTTP_204_NO_CONTENT,
        )


class ShoppingListViewSet(viewsets.ModelViewSet):
    """Представление для списка покупок."""
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (
        IsAdminOrReadOnly,
        IsAuthorOrReadOnly,
        IsAuthenticated,
    )

    def create(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        if ShoppingList.objects.filter(
            user=request.user, recipe=recipe
        ).exists():
            return Response(
                data={'detail': 'Рецепт уже есть в списке покупок!'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        ShoppingList.objects.create(user=request.user, recipe=recipe)
        serializer = self.get_serializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, recipe_id):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        cart = ShoppingList.objects.filter(user=user, recipe=recipe)
        if not cart.exists():
            return Response(
                data={'detail': 'Рецепта еще нет в списке покупок!'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        cart.delete()
        return Response(
            f'Рецепт {cart} удален из списка покупок у пользователя'
            f' {request.user}',
            status=status.HTTP_204_NO_CONTENT,
        )
