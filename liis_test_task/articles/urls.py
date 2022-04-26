from django.urls import include, path
from rest_framework import routers

from .views import ArticleViewSet, UserRegister

router = routers.SimpleRouter()
router.register('articles', ArticleViewSet)
router.register('register', UserRegister, basename="register")

urlpatterns = [path('', include(router.urls))]
