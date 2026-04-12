from django.utils import timezone
from rest_framework import serializers

from task_app.models import Task


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'title',
            'description',
            'categories',
            'status',
            'deadline',

        ]

        def validate_deadline(self, value):
            if value < timezone.now():
                raise serializers.ValidationError(
                    'Deadline cannot be in the future'
                )

            return value


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class TaskDetailSerializer(serializers.ModelSerializer):
    subtasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = '__all__'
