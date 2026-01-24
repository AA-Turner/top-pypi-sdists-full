from datetime import date, timedelta

from celery import shared_task
from django.db import connection
from django.utils import timezone
from dynamic_preferences.registries import global_preferences_registry

from wbcore.workers import Queue


@shared_task(queue=Queue.BACKGROUND.value)
def clean_up_import_source(today: date | None = None):
    if not today:
        today = timezone.now()
    global_preferences = global_preferences_registry.manager()
    retention_period = global_preferences["io__import_source_retention_period"]
    retention_until = today - timedelta(days=retention_period)
    with connection.cursor() as cursor:
        cursor.execute(
            """
            UPDATE io_importsource
            SET data = '{}'::jsonb,
                log = ''
            WHERE created < %s;
        """,
            (retention_until,),
        )
