from django.db.models.signals import post_save
from django.dispatch import receiver
from tasks.models import Task
from .tasks import print_task_name


@receiver(post_save, sender=Task)
def task_created(sender, instance, created, **kwargs):
    if created:
        print_task_name.delay(instance.name)
