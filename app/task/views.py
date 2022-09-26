"""
Views for task API.
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Task
from task import serializers


class TaskViewSet(viewsets.ModelViewSet):
    """
    View for manage task APIs.
    """
    serializer_class = serializers.TaskDetailSerializer
    queryset = Task.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve tasks for authenticated user."""
        self.queryset = self.queryset.filter(user=self.request.user).order_by('date_due')

        query_params = self.request.query_params.dict()
        print(query_params)

        # Filter by 'is_completed'.
        if 'is_completed' in query_params:
            if query_params['is_completed'].lower() == 'true':
                self.queryset = self.queryset.filter(is_completed=True)
            if query_params['is_completed'].lower() == 'false':
                self.queryset = self.queryset.filter(is_completed=False)

        # Filter by 'due_date'.
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        if start_date and end_date:
            self.queryset = self.queryset.filter(date_due__range=[start_date, end_date])

        return self.queryset

    def get_serializer_class(self):
        """Return the serializer class for request."""
        # Use a different serializer for the list view.
        if self.action == 'list':
            return serializers.TaskSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new task."""
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
