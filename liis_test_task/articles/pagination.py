from django.conf import settings
from rest_framework.pagination import LimitOffsetPagination


class StandardResultsSetPagination(LimitOffsetPagination):
    try:
        default_limit = settings.PAGINATION["StandardResultsSetPagination"]["default_limit"]
    except (AttributeError, KeyError):
        default_limit = 10
    try:
        max_limit = settings.PAGINATION["StandardResultsSetPagination"]["max_limit"]
    except (AttributeError, KeyError):
        max_limit = 50
