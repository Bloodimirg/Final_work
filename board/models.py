from django.db import models
from config.settings import AUTH_USER_MODEL

NULLABLE = {"blank": True, "null": True}


class Ad(models.Model):
    """Модель объявления"""

    title = models.CharField(max_length=100, verbose_name='Заголовок')
    price = models.IntegerField(verbose_name='Цена')
    description = models.TextField(max_length=255, verbose_name='Описание')
    author = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Автор')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Review(models.Model):
    """Модель отзыва"""
    text = models.TextField(max_length=255, verbose_name='Содержание')
    author = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews', verbose_name='Автор')
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='reviews', verbose_name='Объявление')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return f'Review by {self.author} on {self.ad}'
