from rest_framework import permissions


class IsStaffOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only staff users to update or delete objects,
    while allowing read-only access to anyone.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_staff

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_staff or obj.user == request.user
