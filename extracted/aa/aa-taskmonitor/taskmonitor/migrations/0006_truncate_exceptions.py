"""Truncate exception field in preparation of changing it from text to char."""

from django.db import migrations


def forwards(apps, schema_editor):
    """Apply a forwards migration."""

    TaskLog = apps.get_model("taskmonitor", "TaskLog")

    for obj in TaskLog.objects.exclude(exception=""):
        parts = obj.exception.split("(")
        obj.exception = parts[0][:254]
        obj.save()


class Migration(migrations.Migration):
    dependencies = [
        ("taskmonitor", "0005_tasklog_current_queue_length_alter_tasklog_priority"),
    ]

    operations = [migrations.RunPython(forwards, migrations.RunPython.noop)]
