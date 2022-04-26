from rest_framework import permissions


class IsSuperUser(permissions.DjangoModelPermissions):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or request.user.is_superuser
