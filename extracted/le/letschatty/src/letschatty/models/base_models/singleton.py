import threading
from abc import ABCMeta




import threading
from abc import ABCMeta
from typing import Dict, Any, Type
import logging

logger = logging.getLogger("Singleton")

class SingletonMeta(type):
    """
    Thread-safe implementation of the Singleton pattern with deadlock prevention.
    """
    _instances: Dict[Type, Any] = {}
    _init_locks: Dict[Type, threading.Lock] = {}
    _global_lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        # Fast path: check if instance exists (no lock)
        if cls in cls._instances:
            return cls._instances[cls]

        # Instance doesn't exist yet, create it with proper locking

        # Get or create a lock for this class
        if cls not in cls._init_locks:
            with cls._global_lock:  # Short lock to safely get/create the per-class lock
                if cls not in cls._init_locks:
                    cls._init_locks[cls] = threading.Lock()

        # Use the class-specific lock to create the instance
        with cls._init_locks[cls]:
            # Double-check pattern - instance might have been created while waiting for lock
            if cls not in cls._instances:
                cls._instances[cls] = super().__call__(*args, **kwargs)

        return cls._instances[cls]


class SingletonABCMeta(SingletonMeta, ABCMeta):
    """
    Metaclass that combines singleton behavior with ABC functionality.
    """
    pass
# class SingletonMeta(type):
#     _instances = {}
#     _lock: threading.Lock = threading.Lock()

#     def __call__(cls, *args, **kwargs):
#         if cls not in cls._instances:
#             with cls._lock:
#                 if cls not in cls._instances:
#                     instance = super().__call__(*args, **kwargs)
#                     cls._instances[cls] = instance
#         return cls._instances[cls]


# class SingletonABCMeta(SingletonMeta, ABCMeta):
#     """Metaclass that combines singleton behavior with ABC functionality"""
#     pass
