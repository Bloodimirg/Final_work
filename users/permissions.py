from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Проверка на администратора"""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups.filter(name="admin").exists()


class IsAuthenticatedUser(permissions.BasePermission):
    """Проверка на аутентифицированного пользователя"""

    def has_permission(self, request, view):
        return request.user.is_authenticated and not request.user.groups.filter(name="admin").exists()
