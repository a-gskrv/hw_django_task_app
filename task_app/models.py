from datetime import datetime

from django.core.validators import MaxLengthValidator
from django.db import models

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
        on_delete=models.PROTECT, # CASCADE,
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


class Category(models.Model):
    name: str = models.CharField(
        max_length=25,
        unique=True,
        verbose_name='Category name',
    )
