import os

broker_url = os.getenv("CELERY_BROKER_URL") or 'redis://localhost:6379/0'
# result_backend = os.getenv("CELERY_BACKEND_URL") or 'redis://localhost:6379/1'

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'Asia/Shanghai'
enable_utc = False

imports = ["celery_tasks.tasks"]