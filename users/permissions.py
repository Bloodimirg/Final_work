from rest_framework import permissions


class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """Проверка, что запрос анонимный (чтение) или пользователь авторизован"""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:  # Только чтение
            return True
        return (
            request.user and request.user.is_authenticated
        )  # Для изменений нужно быть аутентифицированным


# Разрешение для владельца (автора)
class IsOwnerOrAdmin(permissions.BasePermission):
    """Проверка на владельца или администратора"""

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:  # Админ может редактировать любые объекты
            return True
        return (
            obj.author == request.user
        )  # Только автор объекта может редактировать его
