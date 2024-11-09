import pytest
from django.utils import timezone
from board.models import Ad, Review
from users.models import User


@pytest.fixture
def user():
    """Создание пользователя для тестов"""
    return User.objects.create_user(
        email='test@example.com',
        password='testpassword',
        first_name='Test',
        last_name='User'
    )


@pytest.fixture
def ad(user):
    """Создание объявления для тестов"""
    return Ad.objects.create(
        title="Тестовое объявление",
        price=1000,
        description="Тестовое объявление",
        author=user
    )


@pytest.fixture
def review(user, ad):
    """Создание комментария для тестов"""
    return Review.objects.create(
        author=user,
        ad=ad,
        text="Test review text"
    )


@pytest.mark.django_db
class TestAdModel:
    """Тесты объявлений"""
    def test_ad_creation(self, ad):
        """Проверка создания объявления"""
        assert ad.title == "Тестовое объявление"
        assert ad.price == 1000
        assert ad.description == "Тестовое объявление"
        assert ad.author.email == "test@example.com"
        assert isinstance(ad.created_at, timezone.datetime)

    def test_ad_str_method(self, ad):
        """Проверка корректности метода __str__ объявления"""
        assert str(ad) == ad.title

    def test_ad_author_field(self, ad, user):
        """Проверка поля автора"""
        assert ad.author == user

    def test_ad_ordering(self, ad, user):
        """Проверка порядка сортировки объявлений по дате создания"""
        old_ad = Ad.objects.create(
            title="Old Ad",
            price=500,
            description="This is an old ad",
            author=user
        )
        ad.refresh_from_db()  # Обновить объект ad

        # Проверяем, что новое объявление идет первым
        ads = Ad.objects.all()
        assert ads[1] == ad  # Новое объявление на первом месте
        assert ads[0] == old_ad  # Старое об


@pytest.mark.django_db
class TestReviewModel:
    """Тесты комментариев"""

    def test_review_str_method(self, review):
        """Проверка корректности метода __str__ комментария"""
        assert str(review) == "Review by test@example.com on Тестовое объявление"
