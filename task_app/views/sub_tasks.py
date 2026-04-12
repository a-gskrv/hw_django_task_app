from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from task_app.models import SubTask
from task_app.serializers import (
    SubTaskSerializer,
    SubTaskCreateSerializer,
)


class SubTaskListCreateView(APIView, PageNumberPagination):
    page_size = 5

    def get_page_size(self, request):

        page_size = request.query_params.get('page_size')
        if page_size and page_size.isdigit():
            return int(page_size)
        return self.page_size

    def get(self, request, *args, **kwargs):
        subtasks = SubTask.objects.all().order_by('-created_at')

        task_title = request.query_params.get('task_title')
        status = request.query_params.get('status')

        if task_title:
            subtasks = subtasks.filter(task__title__iexact=task_title)

        if status:
            subtasks = subtasks.filter(status=status)

        page_size = self.get_page_size(request)
        self.page_size = page_size

        results = self.paginate_queryset(subtasks, request, view=self)

        if results is not None:
            serializer = SubTaskSerializer(results, many=True)

            return self.get_paginated_response(serializer.data)

        else:
            return Response(
                data={},
                status=status.HTTP_400_BAD_REQUEST
            )

    def post(self, request, *args, **kwargs):
        serializer = SubTaskCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class SubTaskDetailUpdateDeleteView(APIView):

    def get_obj(self):
        subtask_id = self.kwargs['pk']
        try:
            subtask = SubTask.objects.get(id=subtask_id)
            return subtask

        except SubTask.DoesNotExist:
            raise NotFound(f'SubTask with id {subtask_id} not found')

    def get(self, request, *args, **kwargs):
        subtask = self.get_obj()

        serializer = SubTaskSerializer(subtask)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

    def put(self, request, *args, **kwargs):
        subtask = self.get_obj()
        serializer = SubTaskSerializer(subtask, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK
            )
        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, *args, **kwargs):
        subtask = self.get_obj()
        subtask.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
