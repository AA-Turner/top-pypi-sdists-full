import os
import importlib

NOTIFICATIONS_MODULE = "cosmicfrog.frog_notifications"
CF_ACTIVITY_URL = os.getenv("CF_ACTIVITY_URL") or "https://white-bullfrog-c368f0-barking.azurewebsites.net/cosmicfrog/v0.2"

class ModelActivity:
    def __new__(cls, *args, **kwargs):
        # Dynamically import the module
        module = importlib.import_module(NOTIFICATIONS_MODULE)
        actual_class = getattr(module, "ModelActivity")
        instance = actual_class(*args, **kwargs)

        return instance

class AsyncFrogActivityHandler:
    def __new__(cls, *args, **kwargs):
        # Dynamically import the module
        module = importlib.import_module(NOTIFICATIONS_MODULE)
        actual_class = getattr(module, "AsyncFrogActivityHandler")
        instance = actual_class(*args, **kwargs)

        return instance
