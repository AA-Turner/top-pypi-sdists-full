from __future__ import annotations

from django import apps
from django.db import models


def get_model_classes() -> set[type[models.Model]]:
    """
    Return all the installed Django model classes.
    """
    model_classes: set[type[models.Model]] = set()
    for app in apps.apps.get_app_configs():
        model_classes |= set(app.get_models())
    return model_classes
