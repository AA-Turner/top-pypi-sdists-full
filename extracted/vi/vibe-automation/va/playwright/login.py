"""
Login-related functionality for Page class.

This module contains login handling functions extracted from page.py
to improve code organization and maintainability.
"""

import asyncio
import contextvars
import logging
from functools import wraps

log = logging.getLogger("va.playwright")

# Context variable to track if we're currently inside a login handler
_in_login_handler: contextvars.ContextVar[bool] = contextvars.ContextVar(
    "in_login_handler", default=False
)


async def _wait_for_login_if_needed_async(page_instance):
    """
    Async login waiting logic shared by both decorator and wrapper.
    """
    # Skip waiting if we're inside a login handler to prevent deadlock
    if _in_login_handler.get(False):
        return

    # For async methods, always wait
    if page_instance._current_login_task:
        await page_instance._wait_for_login_task()


def _wait_for_login_if_needed(page_instance, method_name):
    """
    Synchronous login waiting logic shared by both decorator and wrapper.
    """
    # Skip waiting if we're inside a login handler to prevent deadlock
    if _in_login_handler.get(False):
        return

    if page_instance._current_login_task:
        try:
            asyncio.get_running_loop()
            # In async context with pending login task
            log.warning(
                f"Sync method {method_name} called while in async context with pending login task - proceeding without waiting"
            )
        except RuntimeError:
            # No event loop running, we can create one to wait
            asyncio.run(page_instance._wait_for_login_task())


def _wait_for_login_wrapper(page_instance, attr, func_name=None):
    """
    Creates a wrapper for a method that waits for login to complete before executing the method.
    """
    method_name = func_name or getattr(attr, "__name__", "unknown_method")

    if asyncio.iscoroutinefunction(attr):
        # Async method wrapper
        async def async_wrapper(*args, **kwargs):
            await _wait_for_login_if_needed_async(page_instance)
            return await attr(*args, **kwargs)

        return async_wrapper
    else:
        # Sync method wrapper
        def sync_wrapper(*args, **kwargs):
            _wait_for_login_if_needed(page_instance, method_name)
            return attr(*args, **kwargs)

        return sync_wrapper


def wait_for_login(func):
    """
    Decorator that ensures any pending login task completes before executing the method.

    Uses shared login waiting logic for consistency.
    """
    if asyncio.iscoroutinefunction(func):
        # Async method decorator
        @wraps(func)
        async def async_decorator_wrapper(self, *args, **kwargs):
            await _wait_for_login_if_needed_async(self)
            return await func(self, *args, **kwargs)

        return async_decorator_wrapper
    else:
        # Sync method decorator
        @wraps(func)
        def sync_decorator_wrapper(self, *args, **kwargs):
            _wait_for_login_if_needed(self, func.__name__)
            return func(self, *args, **kwargs)

        return sync_decorator_wrapper
