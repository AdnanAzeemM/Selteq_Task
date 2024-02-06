from django.urls import path
from .views import UserRegistrationView, PostTaskView, GetTasksView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('post_tasks/', PostTaskView.as_view(), name='post-task'),
    path('get_tasks/', GetTasksView.as_view(), name='get-tasks'),
]
