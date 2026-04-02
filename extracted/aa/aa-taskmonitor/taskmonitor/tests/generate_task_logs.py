# flake8: noqa
"""Script for creating generated task logs for testing."""

import os
import sys
from pathlib import Path

myauth_dir = Path(__file__).parent.parent.parent.parent / "myauth"
sys.path.insert(0, str(myauth_dir))

import django

# init and setup django project
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myauth.settings.local")
django.setup()

"""MAIN"""
from taskmonitor.core import cached_reports
from taskmonitor.models import TaskLog
from taskmonitor.tests.factories import TaskLogFactory

MAX_ENTRIES = 500_000
MAX_BATCH = 10_000

assert MAX_BATCH <= MAX_ENTRIES
assert MAX_ENTRIES % MAX_BATCH == 0
print(f"Generating a total of {MAX_ENTRIES:,} task logs...")
max_runs = MAX_ENTRIES // MAX_BATCH
for run in range(max_runs):
    print(f"Generating {MAX_BATCH:,} logs - {run + 1:,} / {max_runs:,}")
    objs = TaskLogFactory.build_batch(size=MAX_BATCH)
    TaskLog.objects.bulk_create(objs, batch_size=500, ignore_conflicts=True)
cached_reports.refresh_cache()
print("DONE!")
