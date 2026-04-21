from rest_framework import serializers

from task_app.models import SubTask, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'name',
        ]


class CategoryCreateSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Category
        fields = '__all__'

        def create(self, validated_data):
            category_name = validated_data['name']
            category_exists = Category.objects.filter(
                name__iexact=category_name
            ).exists()
            if category_exists:
                raise serializers.ValidationError(
                    f'Категория {category_name} уже существует в БД.'
                )
            return Category.objects.create(**validated_data)

        def update(self, instance, validated_data):
            category_name = validated_data['name']
            category_exists = Category.objects.filter(
                name__iexact=category_name
            ).exclude(
                id=instance.id
            ).exists()

            if category_exists:
                raise serializers.ValidationError(
                    f'Категория {category_name} уже существует в БД.'
                )

            for key, value in validated_data.items():
                setattr(instance, key, value)

            instance.save()

            return instance
