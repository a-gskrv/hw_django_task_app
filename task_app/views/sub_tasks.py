from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from task_app.models import SubTask
from task_app.serializers import (
    SubTaskSerializer,
    SubTaskCreateSerializer,
)



class SubTaskListCreateView(APIView):
    def get(self,request,*args,**kwargs):
        subtasks = SubTask.objects.all()
        serializer = SubTaskSerializer(subtasks, many=True)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

    def post(self,request,*args,**kwargs):
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



    def get(self,request,*args,**kwargs):
        subtask = self.get_obj()

        serializer = SubTaskSerializer(subtask)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

    def put(self,request,*args,**kwargs):
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


    def delete(self,request,*args,**kwargs):
        subtask = self.get_obj()
        subtask.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )