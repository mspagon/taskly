"""
Serializers for the user API view.
"""
from core.models import Task

from rest_framework import serializers


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for the tasks."""

    class Meta:
        model = Task
        fields = ['id', 'title']
        read_only_fields = ['id']


class TaskDetailSerializer(TaskSerializer):
    """Serializer for task detail view."""

    class Meta(TaskSerializer.Meta):
        fields = TaskSerializer.Meta.fields + ['description', 'time_created', 'time_completed', 'is_completed']
        read_only_fields = ['time_created']
