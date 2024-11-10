import os

from django.core.mail import send_mail
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.tokens import RefreshToken, UntypedToken
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import User
from users.serializers import UserSerializer, CustomTokenObtainPairSerializer


class UserCreateApiView(CreateAPIView):
    """Создание пользователя"""

    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class CustomTokenObtainPairView(TokenObtainPairView):
    """Получение пары токенов access/refresh"""

    serializer_class = CustomTokenObtainPairSerializer


class PasswordResetRequestView(APIView):
    """Запрос восстановления пароля"""

    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        try:
            user = User.objects.get(email=email)
            refresh = RefreshToken.for_user(user)
            reset_token = str(refresh.access_token)

            # Отправка email с токеном для сброса пароля
            reset_link = (
                f"http://example.com/password-reset-confirm/?token={reset_token}"
            )
            send_mail(
                "Восстановление пароля",
                f"Перейдите по ссылке для восстановления пароля: {reset_link}",
                os.getenv("EMAIL_HOST_USER"),
                [email],
                fail_silently=False,
            )
            return Response(
                {"message": "Ссылка для восстановления пароля отправлена на почту."},
                status=status.HTTP_200_OK,
            )
        except User.DoesNotExist:
            return Response(
                {"error": "Пользователь с данным email отсутствует."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class PasswordResetConfirmView(APIView):
    """Подтверждение восстановления пароля"""

    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get("token")
        new_password = request.data.get("new_password")

        try:
            # Проверка токена
            UntypedToken(token)
            user_id = UntypedToken(token).get("user_id")
            user = User.objects.get(id=user_id)

            # Устанавка нового пароля
            user.set_password(new_password)
            user.save()

            return Response(
                {"message": "Пароль успешно изменен."}, status=status.HTTP_200_OK
            )

        except (TokenError, InvalidToken, User.DoesNotExist):
            return Response(
                {"error": "Ошибка токена или не найден пользователь."},
                status=status.HTTP_400_BAD_REQUEST,
            )
