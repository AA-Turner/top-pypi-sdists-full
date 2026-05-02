import os
import sys

PARENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PARENT_DIR)

from celery import Celery

app = Celery('ga_chgraph')
app.config_from_object("celery_tasks.celery_config")

