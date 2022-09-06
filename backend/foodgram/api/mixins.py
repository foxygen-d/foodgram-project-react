from rest_framework import mixins, serializers, viewsets

from posts.models import Subscription
from django.contrib.auth import get_user_model


User = get_user_model()


# class SubscribeMixin(mixins.ListModelMixin, mixins.UpdateModelMixin,
#                      viewsets.GenericViewSet):
#     is_subscribed = serializers.SerializerMethodField()

#     def get_is_subscribed(self, obj):
#         user_id = obj.id if isinstance(obj, User) else obj.author.id
    
#         request_user = self.context.get('request').user.id
#         queryset = Subscription.objects.filter(author=user_id,
#                                                follower=request_user).exists()
#         return queryset
