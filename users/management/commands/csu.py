from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):
    """Создание пользователей"""

    def handle(self, *args, **options):
        """Создание админа"""
        if not User.objects.filter(email="").exists():
            user = User.objects.create_superuser(email="", password="")
            user.save()
            self.stdout.write(
                self.style.SUCCESS(f"Суперпользователь {user.email} успешно создан")
            )
        else:
            self.stdout.write(
                self.style.WARNING("Пользователь с таким email уже существует")
            )
