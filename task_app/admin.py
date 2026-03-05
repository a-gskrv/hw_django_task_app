from django.contrib import admin

from task_app.models import Task, SubTask, Category


@admin.register(Task)
class BorrowAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'categories',
        'status',
        'deadline',
        'created_at',
    ]

    list_filter = [
        'categories',
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
class BorrowAdmin(admin.ModelAdmin):
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
class BorrowAdmin(admin.ModelAdmin):
    list_display = [
        'name',
    ]

    search_fields = [
        'name',
    ]

    list_per_page = 25
