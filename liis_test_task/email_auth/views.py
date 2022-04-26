from django.contrib.auth import get_user_model
from rest_framework import viewsets

from .permissions import IsSuperUser
from .serializers import UserSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """Read-only view for non-superusers"""

    queryset = User.objects.filter(is_active=True, is_superuser=False)
    serializer_class = UserSerializer
    permission_classes = [IsSuperUser]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.filter(is_active=True)
        else:
            return self.queryset
