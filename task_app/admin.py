from django.contrib import admin

from task_app.models import Task, SubTask, Category



class SubTaskInline(admin.StackedInline):
    model = SubTask
    extra = 1
    max_num = 5
    # readonly_fields = ('created',)
    verbose_name = "Sub Task"
    verbose_name_plural = 'Sub Tasks'

    # fieldsets = (
    #     ("Task Details", {
    #         "fields": ("title", "task", "description"),
    #     })
    # )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = [
        # 'title',
        'short_title',
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

    inlines = (
        SubTaskInline,
    )

    @admin.display(description="Название", ordering="title")
    def short_title(self, obj):
        if len(obj.title) > 10:
            return obj.title[:10] + '...'
        return obj.title



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

    actions = [
        "mark_as_done"
    ]

    @admin.action(description="Mark as done")
    def mark_as_done(self, request, queryset):
        queryset.update(status=50)
        self.message_user(
            request,
            "Sub Task marked as done.",
        )

    # mark_as_done.short_description = "Mark Sub Task as done"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'name',
    ]

    search_fields = [
        'name',
    ]

    list_per_page = 25

