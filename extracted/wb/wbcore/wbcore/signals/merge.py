from django.db.models.signals import ModelSignal

# Signal fired before merged/obsolete object are deleted during a merge phase
pre_merge = ModelSignal(use_caching=False)
post_merge = ModelSignal(use_caching=False)
