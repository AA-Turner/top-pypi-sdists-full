from django.conf import settings

TASK_JITTER = getattr(settings, 'AA_CONTACTS_TASK_JITTER', 300)
