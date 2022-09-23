from django.shortcuts import get_object_or_404
from rest_framework import mixins, serializers, status, viewsets
from rest_framework.response import Response

from posts.models import Recipe, Subscription


class SubscriptionMixin(serializers.Serializer):
    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        return (
            request.user.is_authenticated
            and Subscription.objects.filter(
                user=request.user, author=obj
            ).exists()
        )


class CreateDeleteMixin(mixins.CreateModelMixin, mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    def create(self, **kwargs):
        recipe = get_object_or_404(Recipe, pk=self.recipe_id)
        if self.objects.filter(user=self.request.user,
                               recipe=recipe).exists():
            return Response(
                data={'detail': 'Этот рецепт уже есть в списке!'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        self.objects.create(user=self.request.user, recipe=recipe)
        serializer = self.get_serializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, **kwargs):
        user = self.request.user
        recipe = get_object_or_404(Recipe, pk=self.recipe_id)
        favorite = self.objects.filter(user=user, recipe=recipe)
        if not favorite.exists():
            return Response(
                data={'detail': 'У вас нет этого рецепта!'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        favorite.delete()
        return Response(
            f'Рецепт {favorite} удален!'
            f' {self.request.user}',
            status=status.HTTP_204_NO_CONTENT,
        )
