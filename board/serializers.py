from rest_framework import serializers

from board.models import Ad, Review


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор комментария текущего пользователя"""

    class Meta:
        model = Review
        fields = "__all__"
        read_only_fields = ["author", "created_at"]

    def create(self, validated_data):
        request = self.context.get("request")  # Получаем текущий запрос
        ad = Review.objects.create(
            author=request.user, **validated_data
        )  # Устанавливаем автора комментария как владельца
        return ad


class AdSerializer(serializers.ModelSerializer):
    """Сериализатор объявления текущего пользователя"""

    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Ad
        fields = [
            "id",
            "title",
            "price",
            "description",
            "created_at",
            "author",
            "reviews",
        ]
        read_only_fields = ["author", "created_at", "reviews"]

    def create(self, validated_data):
        request = self.context.get("request")  # Получаем текущий запрос
        ad = Ad.objects.create(
            author=request.user, **validated_data
        )  # Устанавливаем автора объявления как владельца
        return ad
