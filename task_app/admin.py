from django.contrib import admin

from task_app.models import Task, SubTask, Category


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'status',
        'deadline',
        'created_at',
    ]

    list_filter = [
        'status',
        'deadline',
    ]

    search_fields = [
        'title',
        'description',
    ]

    list_editable = ('status', 'deadline')

    list_per_page = 25


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'task',
        'status',
        'deadline',
        'created_at',
    ]

    list_filter = [
        'task',
        'status',
        'deadline',
    ]

    search_fields = [
        'title',
        'description',
    ]

    list_editable = ('status', 'deadline')

    list_per_page = 25


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'name',
    ]

    search_fields = [
        'name',
    ]

    list_per_page = 25
