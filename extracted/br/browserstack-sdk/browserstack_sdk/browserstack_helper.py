"""
BrowserStack Helper Module for Multi-Driver Support
This module provides helper methods for managing multi-driver test execution,
specifically for scenarios requiring multiple browser/device sessions.
"""
import threading
from typing import Optional, List
from bstack_utils import logger_utils
logger = logger_utils.get_logger(__name__)
class BrowserStackHelper:
    """
    Helper class for multi-driver test execution.
    This class provides methods to explicitly control driver assignment
    to specific platforms when running tests with multiple drivers.
    Example usage:
        >>> from browserstack_sdk.browserstack_helper import BrowserStackHelper        >>> 
        >>> @pytest.fixture
        >>> def desktop_driver():
        >>>     BrowserStackHelper.set_driver_label("desktop")
        >>>     driver = webdriver.Remote(command_executor=hub_url, options=options)
        >>>     yield driver
        >>>     driver.quit()
        >>> 
        >>> @pytest.fixture
        >>> def mobile_driver():
        >>>     BrowserStackHelper.set_driver_label("mobile")
        >>>     driver = webdriver.Remote(command_executor=hub_url, options=options)
        >>>     yield driver
        >>>     driver.quit()
    """
    _thread_local = threading.local()
    @classmethod
    def set_driver_label(cls, label: str) -> None:
        """
        Set the platform label for the next driver initialization.
        This method should be called before creating a WebDriver instance
        to explicitly assign it to a specific platform configuration.
        The label should match one defined in the YAML configuration file.
        Args:
            label: Platform label (e.g., "desktop", "mobile", "driver#1")
        Example:
            >>> BrowserStackHelper.set_driver_label("desktop")
            >>> driver = webdriver.Remote(...)
        Note:
            This setting is thread-local, so it only affects driver creation
            in the current thread. The label is automatically cleared after
            the driver is initialized. No validation is performed when setting
            the label; validation occurs during driver initialization.
        """
        cls._thread_local.driver_label = label
    @classmethod
    def get_driver_label(cls) -> Optional[str]:
        """
        Get the current driver label for this thread.
        Returns:
            The driver label string if set, None otherwise
        Example:
            >>> BrowserStackHelper.set_driver_label("desktop")
            >>> label = BrowserStackHelper.get_driver_label()
            >>> print(label)  # Output: "desktop"
        """
        return getattr(cls._thread_local, 'driver_label', None)
    @classmethod
    def clear_driver_label(cls) -> None:
        """
        Clear the driver label for the current thread.
        This method can be called manually if you need to clear a label
        that was previously set with set_driver_label().
        """
        if hasattr(cls._thread_local, 'driver_label'):
            label = cls._thread_local.driver_label
            delattr(cls._thread_local, 'driver_label')
    @classmethod
    def validate_label(cls, label: str, available_labels: List[str]) -> bool:
        """
        Validate if a label exists in the available platform labels.
        Args:
            label: The label to validate
            available_labels: List of available platform labels
        Returns:
            True if label is valid
        Raises:
            ValueError: If label is invalid or no labels are configured
        """
        if not available_labels:
            raise ValueError(
                f"No platform labels configured. Please check your browserstack.yml configuration."
            )
        if label not in available_labels:
            available = "', '".join(available_labels)
            raise ValueError(
                f"Invalid driver label '{label}'. "
                f"Available labels: '{available}'. "
                f"Please ensure the label matches one defined in your browserstack.yml file."
            )
        return True
    @classmethod
    def reset(cls) -> None:
        """
        Reset the helper to its initial state.
        This is primarily used for testing purposes to clear
        all configuration and state.
        """
        if hasattr(cls._thread_local, 'driver_label'):
            delattr(cls._thread_local, 'driver_label')
