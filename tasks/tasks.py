from celery import shared_task
from datetime import datetime


@shared_task
def print_task_name(task_name):
    print(f"Executing task: {task_name} at {datetime.now()}")
