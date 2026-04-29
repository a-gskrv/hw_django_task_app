from datetime import datetime

from django.utils import timezone
from rest_framework import serializers

from task_app.models import Task
from task_app.serializers.sub_task import SubTaskSerializer


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

        read_only_fields = ['owner',]

    def validate_deadline(self, value: datetime):
        # value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')

        if value < timezone.now():
            raise serializers.ValidationError(
                'Deadline cannot be in the past'
            )

        return value


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

        read_only_fields = (
            'id',
            'created_at',
            'owner',
        )


class TaskDetailSerializer(serializers.ModelSerializer):
    subtasks = SubTaskSerializer(many=True, read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Task
        # fields = '__all__'
        fields = [
            'id',
            'title',
            'description',
            'categories',
            'status',
            'deadline',
            'subtasks',
            'created_at',
            'owner',
        ]
        read_only_fields = (
            'id',
            'created_at',
            'owner',
        )

        validators = []

    def validate(self, attrs):
        title = attrs.get('title')
        created_at = self.instance.created_at

        if title is None:
            title = self.instance.title

        qs = Task.objects.filter(
            title__icontains=title,
            created_at=created_at,
        ).exclude(id=self.instance.pk)

        if qs.exists():
            raise serializers.ValidationError({
                'title': 'Task with this title already exists for this date',
            })

        return attrs
