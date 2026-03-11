from django_celery_beat.models import IntervalSchedule, PeriodicTask
from django.db import DEFAULT_DB_ALIAS
from django.apps import apps as global_apps


def initialize_task(app_config, verbosity=2, interactive=True, using=DEFAULT_DB_ALIAS, apps=global_apps, **kwargs):
    PeriodicTask.objects.update_or_create(
        task="wbcore.contrib.notifications.management.tasks.orchestrate_aggregated_email_notification",
        defaults={
            "name": "Notification: aggregate and send email notifications",
            "interval": IntervalSchedule.objects.get_or_create(every=5, period=IntervalSchedule.MINUTES)[0],
            "crontab": None,
        },
    )
