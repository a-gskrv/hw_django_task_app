from datetime import datetime

from django.db.models import Count
from django.db.models.functions import ExtractIsoWeekDay
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response

from task_app.models import Task
from task_app.serializers import (
    TaskCreateSerializer,
    TaskSerializer,
    TaskDetailSerializer
)


@api_view(['GET'])
def tasks_stat(request: Request) -> Response:
    qs = Task.objects.all()
    tasks_count = qs.count()
    tasks_by_status = qs.values('status').annotate(count=Count('id')).order_by('status')
    tasks_overdue_count = qs.filter(deadline__lte=datetime.now()).exclude(status=50).count()
    data = {
        'tasks_count': tasks_count,
        'tasks_by_status': {tasks_status['status']: tasks_status['count'] for tasks_status in tasks_by_status},
        'tasks_overdue_count': tasks_overdue_count,
    }
    return Response(
        data=data,
        status=status.HTTP_200_OK,
    )


class TaskPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100


class TaskListCreateAPIView(ListCreateAPIView):
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter
    ]
    """
    Реализуйте фильтрацию по полям status и deadline.
    Реализуйте поиск по полям title и description.
    Добавьте сортировку по полю created_at.
    """
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']

    # pagination_class = TaskPagination

    def get_queryset(self):
        qs = Task.objects.all()

        weekday = self.request.query_params.get('weekday')
        if weekday is not None:
            try:
                weekday = int(weekday)
                qs = qs.annotate(
                    weekday=ExtractIsoWeekDay('deadline')
                ).filter(weekday=weekday)
            except ValueError:
                raise ValidationError('Invalid weekday')

        qs = qs.order_by('id')

        return qs

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TaskCreateSerializer
        return TaskSerializer

    # def get(self, request: Request) -> Response:
    #     qs = self.get_queryset()
    #
    #     qs = self.filter_queryset(qs)
    #
    #     serializer = self.get_serializer(qs, many=True)
    #     return Response(
    #         data=serializer.data,
    #         status=status.HTTP_200_OK,
    #     )


class TaskDetailUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskDetailSerializer