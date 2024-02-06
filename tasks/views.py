from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer, TaskSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Task


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostTaskView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        task_name = request.data.get('name')
        if not task_name:
            return Response({"error": "Task name is required"}, status=400)

        task = Task.objects.create(name=task_name, user=request.user)
        return Response({"message": "Task created", "task": task.name})


class GetTasksView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        tasks = Task.objects.filter(user=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
