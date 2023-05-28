from django.contrib.auth.models import User
from django.forms import model_to_dict
from rest_framework import serializers

from advertisements.models import Advertisement


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', )

    def create(self, validated_data):
        """Метод для создания"""
        print(validated_data)
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""
        if self.context["request"].method == 'POST' or data.get('status') == 'OPEN':
            counter = Advertisement.objects.filter(
                creator=self.context["request"].user,
                status='OPEN'
            ).count()
            if counter >= 10:
                raise ValidationError(
                    'Невозможно создать новое объявление: у Вас уже есть 10 объявлений со статусом "Открыто".'
                )

        return data
