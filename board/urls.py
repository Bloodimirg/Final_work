from django.urls import path, include
from rest_framework.routers import DefaultRouter

from board.views import AdViewSet, ReviewViewSet

router = DefaultRouter()
router.register(r"ad", AdViewSet, basename="ad")  # Маршрут для объявлений
router.register(r"review", ReviewViewSet, basename="review")  # Маршрут для комментариев

app_name = "board"
urlpatterns = [
    path("", include(router.urls)),
]
