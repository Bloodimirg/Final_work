from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from board.models import Ad, Review
from board.paginations import AdPagination
from board.serializers import AdSerializer, ReviewSerializer
from rest_framework import permissions

from users.permissions import IsAuthenticatedOrReadOnly, IsOwnerOrAdmin


class AdViewSet(viewsets.ModelViewSet):
    """View set объявления"""

    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    pagination_class = AdPagination  # пагинация
    filter_backends = [DjangoFilterBackend]  # фильтрация
    filterset_fields = ["title"]  # фильтрация по названию board/ad/?title='user1'

    def get_permissions(self):
        if self.action == "list":

            # Анонимные могут только читать
            self.permission_classes = [IsAuthenticatedOrReadOnly]
        elif self.action == "create":

            # Создавать только авторизованные
            self.permission_classes = [permissions.IsAuthenticated]
        elif self.action in ["update", "partial_update"]:

            # Только автор или админ может редактировать
            self.permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
        elif self.action == "destroy":

            # Только автор или админ может удалять
            self.permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
        return super().get_permissions()


class ReviewViewSet(viewsets.ModelViewSet):
    """Представление комментария объявления"""

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.action == "list":

            # Анонимные могут только читать
            self.permission_classes = [IsAuthenticatedOrReadOnly]
        elif self.action == "create":

            # Только аутентифицированные могут создавать
            self.permission_classes = [permissions.IsAuthenticated]
        elif self.action in ["update", "partial_update"]:

            # Только автор или администратор может редактировать
            self.permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
        elif self.action == "destroy":

            # Только автор или администратор может удалять
            self.permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
        return super().get_permissions()
