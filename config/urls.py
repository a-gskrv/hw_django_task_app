"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter

from task_app.views.categories import CategoryViewSet

from task_app.views.sub_tasks import (
    SubTaskListCreateAPIView,
    SubTaskDetailUpdateDeleteView
)

from task_app.views.tasks import (
    # task_create,
    # task_get_by_id,
    # task_get_all,
    tasks_stat,
    TaskListCreateAPIView,
    TaskDetailUpdateDeleteAPIView,
)


router = DefaultRouter()
router.register('categories', CategoryViewSet)

urlpatterns = [
    # path('', index),
    path('admin/', admin.site.urls),
    # path('task/', task_create),
    # path('task/<int:pk>', task_get_by_id),
    # path('tasks/', task_get_all),
    path('tasks_stat/', tasks_stat),
    path('subtasks/', SubTaskListCreateAPIView.as_view()),
    path('subtasks/<int:pk>/', SubTaskDetailUpdateDeleteView.as_view()),

    path('tasks/', TaskListCreateAPIView.as_view()),
    path('tasks/<int:pk>/', TaskDetailUpdateDeleteAPIView.as_view()),

]

urlpatterns += router.urls