"""
Serializers for the user API view.
"""
from django.utils import timezone

from core.models import Task

from rest_framework import serializers


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for the tasks."""

    class Meta:
        model = Task
        fields = ['id', 'title', 'date_created', 'date_due', 'date_completed', 'is_completed']
        read_only_fields = ['id', 'date_created', 'date_completed']

    def update(self, instance, validated_data):
        """Update and return task."""
        is_completed = validated_data.pop('is_completed', instance.is_completed)
        if is_completed is True and instance.is_completed is False:
            instance.date_completed = timezone.now()
            instance.is_completed = True
        if is_completed is False and instance.is_completed is True:
            instance.date_completed = None
            instance.is_completed = False
        task = super().update(instance, validated_data)
        return task


class TaskDetailSerializer(TaskSerializer):
    """Serializer for task detail view."""

    class Meta(TaskSerializer.Meta):
        fields = TaskSerializer.Meta.fields + ['description', 'date_completed', 'is_completed']
        read_only_fields = TaskSerializer.Meta.read_only_fields + []
