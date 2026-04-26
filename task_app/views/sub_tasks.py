from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination


from task_app.models import SubTask
from task_app.serializers import (
    SubTaskSerializer,
    SubTaskCreateSerializer,
)


class SubTaskPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100


class SubTaskListCreateAPIView(ListCreateAPIView):
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

    # pagination_class = SubTaskPagination

    queryset = SubTask.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SubTaskCreateSerializer
        return SubTaskSerializer

class SubTaskDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer
