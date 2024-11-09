from django.contrib.auth.models import AbstractUser
from django.db import models
from users.managers import CustomUserManager

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    """Модель пользователя"""

    ROLE_CHOICES = (
        ("user", "User"),
        ("admin", "Admin"),
    )
    username = None
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    phone = models.CharField(max_length=50, **NULLABLE, verbose_name="Телефон")
    email = models.EmailField(
        unique=True, verbose_name="Почта", help_text="Укажите почту"
    )
    role = models.CharField(
        max_length=10, choices=ROLE_CHOICES, default="user", verbose_name="Роль"
    )
    image = models.ImageField(upload_to="media/image", **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()  # Для тестов кастомная модель

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
