from django.db.models import Q
from rest_framework import generics, permissions, viewsets
from rest_framework import status
from rest_framework.response import Response

from .models import Article
from .pagination import StandardResultsSetPagination
from .permissions import DO_EVERYTHING, InAuthorGroupAndIsAuthorOf, IsAdmin, IsPublicContentReader, IsSubscriber, \
    VIEW_NOT_PUBLIC
from .serializers import ArticleSerializerDetail, ArticleSerializerList, UserRegisterRequestSerializer, \
    UserRegisterResultSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.order_by("-added_at").all()
    serializer_class = ArticleSerializerDetail
    permission_classes = [IsPublicContentReader | IsSubscriber | InAuthorGroupAndIsAuthorOf | IsAdmin]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        user = self.request.user
        if self.action == "list":
            if user.has_perm(VIEW_NOT_PUBLIC) or user.has_perm(DO_EVERYTHING):
                return self.queryset
            elif user.is_authenticated:
                return self.queryset.filter(Q(is_public=True) | Q(author=user))
            else:
                return self.queryset.filter(is_public=True)
        return self.queryset

    def get_serializer_class(self):
        if self.action == "list":
            return ArticleSerializerList
        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


def do_something(*args, **kwargs):
    return True


class UserRegister(viewsets.ViewSetMixin, generics.CreateAPIView):
    """
    Register a new user, either subscriber or not.
    """
    permission_classes = [~permissions.IsAuthenticated]
    serializer_class = UserRegisterRequestSerializer

    def get_view_name(self):
        return "User Register"

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = UserRegisterRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data["is_subscription_requested"]:
            result = do_something(request)
            if not result:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.perform_create(serializer)
        output_serializer = UserRegisterResultSerializer(serializer.instance, context={'request': request})
        headers = self.get_success_headers(output_serializer.data)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
