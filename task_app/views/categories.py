from django.db.models import Count
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from task_app.models import Category, Task
from task_app.serializers.category import CategorySerializer, CategoryCreateSerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return CategoryCreateSerializer
        return CategorySerializer

    @action(detail=False, methods=['GET'])
    def count_tasks(self, request, pk=None):
        queryset = self.get_queryset()
        queryset = queryset.annotate(task_count=Count('tasks'))
        data = [
            {
                'id': cat.id,
                'name': cat.name,
                'task_count': cat.task_count,
            }
            for cat in queryset
        ]
        return Response(
            data,
            status=status.HTTP_200_OK,
        )
