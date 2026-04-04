import os


import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from task_app.models import Task, SubTask, Category
from datetime import timedelta
from django.utils import timezone


def get_task_by_title(title):
    return Task.objects.filter(title__iexact=title.lower()).first()

def get_sub_task_by_title(title):
    return SubTask.objects.filter(title__iexact=title.lower()).first()


def task_01():
    print('task_01', '*' * 25)
    task_1 = Task.objects.create(
        title="Prepare presentation",
        description="Prepare materials and slides for the presentation",
        status=10,
        deadline=timezone.now() + timedelta(days=3),
    )
    # task_1.categories.set(Category.objects.all())

    subtask_1 = SubTask.objects.create(
        title="Gather information",
        description="Find necessary information for the presentation",
        task=task_1,
        status=10,
        deadline=timezone.now() + timedelta(days=2),
    )

    subtask_2 = SubTask.objects.create(
        title="Create slides",
        description="Create presentation slides",
        task=task_1,
        status=1,
        deadline=timezone.now() + timedelta(days=1),
    )

    print('Task: ', task_1)
    print('SubTask: ', subtask_1)
    print('Task: ', subtask_2)



def task_02():
    print('task_02', '*' * 25)
    all_tasks_status_new = Task.objects.filter(status=10)
    print(all_tasks_status_new)

    expired_done_subtasks = SubTask.objects.filter(
        status=50,
        deadline__lt=timezone.now(),
    )
    print(expired_done_subtasks)

def task_03():
    print('task_03', '*' * 25)
    task_search = get_task_by_title("Prepare presentation")
    if task_search:
        print('v.1:', task_search, task_search.status)
        task_search.status = 20
        task_search.save()
        print('v.2: ', task_search, task_search.status)

    task_search = get_sub_task_by_title("Gather information")
    if task_search:
        print('v.1:', task_search, task_search.deadline)
        task_search.deadline -= timedelta(days=2)
        task_search.save()
        print('v.2: ', task_search, task_search.deadline)


    task_search = get_sub_task_by_title("Create slides")
    if task_search:
        print('v.1:', task_search, task_search.description)
        task_search.description = 'Create and format presentation slides'
        task_search.save()
        print('v.2: ', task_search, task_search.description)



def task_04():
    print('task_04', '*' * 25)
    task_search = get_task_by_title("Prepare presentation")
    if task_search:
        sub_tasks_search = SubTask.objects.filter(task=task_search)
        if sub_tasks_search:
            for sub_task in sub_tasks_search:
                print('Delete SubTask: ', sub_task)
                sub_task.delete()

        print('Delete Task: ', task_search)
        task_search.delete()



task_01()
task_02()
task_03()
task_04()