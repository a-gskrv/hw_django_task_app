from datetime import datetime

from django.core.validators import MaxLengthValidator
from django.db import models
from django.db.models.functions import Lower

STATUS_CHOICES = (
    ('10', 'New'),
    ('20', 'In Progress'),
    ('30', 'Pending'),
    ('40', 'Blocked'),
    ('50', 'Done'),
)


class Task(models.Model):
    title: str = models.CharField(
        max_length=100,
        verbose_name='Task title',
        unique_for_date='created_at',
    )

    description: str = models.TextField(
        verbose_name='Task description',
        blank=True,
        null=True,
        validators=[
            MaxLengthValidator(500),
        ]
    )

    categories = models.ManyToManyField(
        'Category',
        related_name='tasks',
        verbose_name='Task categories',
    )

    status: str = models.CharField(
        verbose_name='Task status',
        max_length=20,
        choices=STATUS_CHOICES,
        default="0"
    )

    deadline: datetime = models.DateTimeField(
        verbose_name='Task deadline'
    )

    created_at: datetime = models.DateTimeField(
        verbose_name='Task created at',
        auto_now_add=True
    )

    class Meta:
        db_table = 'task_manager_task'
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'

        ordering = ['-created_at']

        constraints = [
            models.UniqueConstraint(
                Lower("title"),
                name="unique_lower_title"
            )
        ]

    def __str__(self):
        if len(self.title) > 20:
            return self.title[:17] + '...'
        return self.title


class SubTask(models.Model):
    title: str = models.CharField(
        max_length=100,
        verbose_name='Subtask title',
    )

    description: str = models.TextField(
        verbose_name='Subtask description',
        blank=True,
        null=True,
        validators=[
            MaxLengthValidator(500),
        ]
    )

    task = models.ForeignKey(
        Task,
        on_delete=models.PROTECT,  # CASCADE,
        related_name='subtasks',
    )

    status: str = models.CharField(
        verbose_name='Subtask status',
        max_length=20,
        choices=STATUS_CHOICES,
        default="0"
    )

    deadline: datetime = models.DateTimeField(
        verbose_name='Task deadline'
    )

    created_at: datetime = models.DateTimeField(
        verbose_name='Task created at',
        auto_now_add=True
    )

    class Meta:
        db_table = 'task_manager_subtask'
        verbose_name = 'SubTask'
        verbose_name_plural = 'SubTasks'

        ordering = ['-created_at']

        constraints = [
            models.UniqueConstraint(
                Lower("title"),
                name="unique_lower_title"
            )
        ]

    def __str__(self):
        if len(self.title) > 20:
            return self.title[:17] + '...'
        return self.title


class Category(models.Model):
    name: str = models.CharField(
        max_length=25,
        unique=True,
        verbose_name='Category name',
    )

    class Meta:
        db_table = 'task_manager_category'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

        constraints = [
            models.UniqueConstraint(
                Lower("name"),
                name="unique_lower_category"
            )
        ]

    def __str__(self):
        if len(self.name) > 20:
            return self.name[:17] + '...'
        return self.name
