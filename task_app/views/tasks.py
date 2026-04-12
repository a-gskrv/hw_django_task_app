from datetime import datetime

from django.db.models import Count
from django.db.models.functions import ExtractIsoWeekDay
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from task_app.models import Task
from task_app.serializers.task import TaskCreateSerializer, TaskSerializer


@api_view(['POST'])
def task_create(request: Request) -> Response:
    try:
        serializer = TaskCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def task_get_by_id(request: Request, pk: int) -> Response:
    try:
        obj: Task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = TaskCreateSerializer(obj)
    return Response(
        data=serializer.data,
        status=status.HTTP_200_OK,
    )


@api_view(['GET'])
def task_get_all(request: Request) -> Response:
    qs = Task.objects.all().order_by('id')

    serializer = TaskSerializer(qs, many=True)
    return Response(
        data=serializer.data,
        status=status.HTTP_200_OK,
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


class TaskListView(APIView):

    def get(self,request,*args,**kwargs):
        objs = Task.objects.all()

        weekday = request.query_params.get('weekday')
        if weekday is not None:
            try:
                weekday = int(weekday)
                objs = objs.annotate(
                    weekday=ExtractIsoWeekDay('deadline')
                ).filter(weekday=weekday)
            except ValueError:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST
                )

            objs = objs.order_by('id')

            serializer = TaskSerializer(objs, many=True)
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK,
            )


        serializer = TaskSerializer(objs, many=True)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )