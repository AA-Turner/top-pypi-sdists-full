"""
Mixpanel tracking utilities for code-loader.
"""
import os
import sys
import getpass
import uuid
import logging
from enum import Enum
from typing import Optional, Dict, Any, Set, Union, TypedDict
import mixpanel  # type: ignore[import]

logger = logging.getLogger(__name__)

TRACKING_VERSION = '1'


class AnalyticsEvent(str, Enum):
    """Enumeration of all tracked analytics events."""
    CODE_LOADER_LOADED = "code_loader_loaded"
    LOAD_MODEL_INTEGRATION_TEST = "load_model_integration_test"
    PREPROCESS_INTEGRATION_TEST = "preprocess_integration_test"
    INPUT_ENCODER_INTEGRATION_TEST = "input_encoder_integration_test"
    GT_ENCODER_INTEGRATION_TEST = "gt_encoder_integration_test"


class CodeLoaderLoadedProps(TypedDict, total=False):
    """Properties for code_loader_loaded event."""
    event_type: str
    code_path: str
    code_entry_name: str


class LoadModelEventProps(TypedDict, total=False):
    """Properties for load_model_integration_test event."""
    prediction_types_count: int


class PreprocessEventProps(TypedDict, total=False):
    """Properties for preprocess_integration_test event."""
    preprocess_responses_count: int


class InputEncoderEventProps(TypedDict, total=False):
    """Properties for input_encoder_integration_test event."""
    encoder_name: str
    channel_dim: int


class GtEncoderEventProps(TypedDict, total=False):
    """Properties for gt_encoder_integration_test event."""
    encoder_name: str


class MixpanelTracker:
    """Handles Mixpanel event tracking for code-loader."""
    
    def __init__(self, token: str = "0c1710c9656bbfb1056bb46093e23ca1"):
        self.token = token
        self.mp = mixpanel.Mixpanel(token)
        self._user_id: Optional[str] = None
    
    def _get_whoami(self) -> str:
        """Get the current system username (whoami) for device identification.
        
        Returns:
            str: The system username, with fallbacks to environment variables or 'unknown'
        """
        if self._user_id is None:
            try:
                self._user_id = getpass.getuser()
            except Exception as e:
                logger.debug(f"Failed to get username via getpass: {e}")
                # Fallback to environment variables or default
                self._user_id = os.environ.get('USER', os.environ.get('USERNAME', 'unknown'))
        return self._user_id or 'unknown'
    
       
    def _get_tensorleap_user_id(self) -> Optional[str]:
        """Get the TensorLeap user ID from ~/.tensorleap/user_id if it exists."""
        try:
            user_id_path = os.path.expanduser("~/.tensorleap/user_id")
            if os.path.exists(user_id_path):
                with open(user_id_path, 'r') as f:
                    user_id = f.read().strip()
                    if user_id:
                        return user_id
        except Exception as e:
            logger.debug(f"Failed to read TensorLeap user ID: {e}")
        return None
    
    def _get_or_create_device_id(self) -> str:
        """Get or create a device ID from ~/.tensorleap/device_id file.
        
        If the file doesn't exist, creates it with a new UUID.
        
        Returns:
            str: The device ID (UUID string)
        """
        try:
            device_id_path = os.path.expanduser("~/.tensorleap/device_id")
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(device_id_path), exist_ok=True)
            
            if os.path.exists(device_id_path):
                with open(device_id_path, 'r') as f:
                    device_id = f.read().strip()
                    if device_id:
                        return device_id
            
            # Generate new device ID and save it
            device_id = str(uuid.uuid4())
            with open(device_id_path, 'w') as f:
                f.write(device_id)
            
            return device_id
        except Exception as e:
            logger.debug(f"Failed to read/write device ID file: {e}")
            # Fallback to generating a new UUID if file operations fail
            return str(uuid.uuid4())
    
    def _get_distinct_id(self) -> str:
        """Get the distinct ID for Mixpanel tracking.
        
        Priority order:
        1. TensorLeap user ID (from ~/.tensorleap/user_id)
        2. Device ID (from ~/.tensorleap/device_id, generated if not exists)
        """
        tensorleap_user_id = self._get_tensorleap_user_id()
        if tensorleap_user_id:
            return tensorleap_user_id
        
        return self._get_or_create_device_id()
    
    def _track_event(self, event_name: Union[str, AnalyticsEvent], event_properties: Optional[Dict[str, Any]] = None) -> None:
        """Internal method to track any event with device identification.
        
        Args:
            event_name: The name of the event to track (string or AnalyticsEvent enum)
            event_properties: Optional additional properties to include in the event
        """
        # Skip tracking if IS_TENSORLEAP_PLATFORM environment variable is set to 'true'
        if os.environ.get('IS_TENSORLEAP_PLATFORM') == 'true':
            return
            
        try:
            distinct_id = self._get_distinct_id()
            
            tensorleap_user_id = self._get_tensorleap_user_id()
            whoami = self._get_whoami()
            device_id = self._get_or_create_device_id()
            
            properties = {
                'tracking_version': TRACKING_VERSION,
                'service': 'code-loader',
                'whoami': whoami,
                '$device_id': device_id,  # Always use device_id for $device_id
                'python_version': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
                'platform': os.name,
            }
            
            if tensorleap_user_id:
                properties['user_id'] = tensorleap_user_id
            
            if event_properties:
                properties.update(event_properties)
            
            self.mp.track(distinct_id, str(event_name), properties)
        except Exception as e:
            logger.debug(f"Failed to track event '{event_name}': {e}")

    def track_code_loader_loaded(self, event_properties: Optional[Dict[str, Any]] = None) -> None:
        """Track code loader loaded event with device identification.
        
        Args:
            event_properties: Optional additional properties to include in the event
        """
        self._track_event(AnalyticsEvent.CODE_LOADER_LOADED, event_properties)

    def track_integration_test_event(self, event_name: Union[str, AnalyticsEvent], event_properties: Optional[Dict[str, Any]] = None) -> None:
        """Track an integration test event with device identification.
        
        Args:
            event_name: The name of the event to track (string or AnalyticsEvent enum)
            event_properties: Optional additional properties to include in the event
        """
        self._track_event(event_name, event_properties)


# Global tracker instance
_tracker = None


def get_tracker() -> MixpanelTracker:
    global _tracker
    if _tracker is None:
        _tracker = MixpanelTracker()
    return _tracker


def track_code_loader_loaded(event_properties: Optional[Dict[str, Any]] = None) -> None:
    get_tracker().track_code_loader_loaded(event_properties)


def track_integration_test_event(event_name: Union[str, AnalyticsEvent], event_properties: Optional[Dict[str, Any]] = None) -> None:
    get_tracker().track_integration_test_event(event_name, event_properties)


# Module-level set to track which integration test events have been emitted
_integration_events_emitted: Set[str] = set()


def emit_integration_event_once(event_name: Union[str, AnalyticsEvent], props: Dict[str, Any]) -> None:
    """Emit an integration test event only once per test run."""
    event_name_str = str(event_name)
    if event_name_str in _integration_events_emitted:
        return
    
    try:
        track_integration_test_event(event_name, props)
        _integration_events_emitted.add(event_name_str)
    except Exception as e:
        logger.debug(f"Failed to emit integration event once '{event_name}': {e}")


def clear_integration_events() -> None:
    """Clear the integration events set for a new test run."""
    global _integration_events_emitted
    _integration_events_emitted.clear()
