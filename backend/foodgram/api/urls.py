from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (UsersViewSet, TagViewSet, IngredientViewSet, RecipeViewSet, SubscriptionViewSet)


router = DefaultRouter()
router.register('users', UsersViewSet, basename='users')
router.register('tags', TagViewSet, basename='tags')
router.register('recipes', RecipeViewSet, basename='recipes')
# router.register(
#     r'recipes/(?P<recipes_id>\d+)/shopping_cart',
#     RecipeViewSet, basename='shopping_cart')
# router.register(
#     r'recipes/(?P<recipes_id>\d+)/favorite',
#     RecipeViewSet, basename='favorites')
router.register('users/subscriptions', SubscriptionViewSet, basename='subscriptions')
router.register('ingredients', IngredientViewSet, basename='ingredients')


urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
