import django.db
from django.contrib.contenttypes.models import ContentType
from rest_framework import permissions

from .models import Article

try:
    app_label = ContentType.objects.get_for_model(Article).app_label
except django.db.DatabaseError:
    # Initial migration is not applied yet so let's set default app_label,
    # although it could be overridden by custom app config,
    # it doesn't matter when import due to initial migration.
    app_label = "articles"

VIEW_NOT_PUBLIC = f"{app_label}.view_not_public_article"
DO_EVERYTHING = f"{app_label}.do_anything"


class IsPublicContentReader(permissions.DjangoModelPermissionsOrAnonReadOnly):
    """Can only view a public obj."""

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS and obj.is_public


# Protect against accidentally granting edit permission to the subscriber group
class IsSubscriber(permissions.DjangoModelPermissions):
    """Can view both public and not public obj."""

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS and (
                obj.is_public or request.user.has_perm(VIEW_NOT_PUBLIC))


class InAuthorGroupAndIsAuthorOf(permissions.DjangoModelPermissions):
    """
    Can always view their own obj.
    Can edit their own obj until he is not excluded from the author group.
    Can only view someone's else not public obj if he is given such privilege.

    Note that DRF browsable API always shows delete button
    (see ``rest_framework.renderers.BrowsableAPIRenderer.get_rendered_html_form()``)
    if a user has ``delete_permission`` on model,
    but actual deleting will be denied if the user is not an author of an obj.
    """

    def has_object_permission(self, request, view, obj):
        # A user is not allowed to edit even if he is an author of an obj
        # but has no more edit permission (excluded from the author group).
        # Can edit and view their own obj
        if obj.author == request.user:
            return True
        # Can view not public obj only if the author group given such privilege
        elif request.method in permissions.SAFE_METHODS and (obj.is_public or request.user.has_perm(VIEW_NOT_PUBLIC)):
            return True
        return False


class IsAdmin(permissions.DjangoModelPermissions):
    """Can do anything with obj"""

    # A user is considered as admin if he is staff and has a special privilege.
    # If he is not staff anymore, but still has the privilege
    # then he cannot edit an obj but can view not public obj
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS or request.user.is_staff
                ) and request.user.has_perm(DO_EVERYTHING)

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
