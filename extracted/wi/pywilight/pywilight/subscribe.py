"""Module to listen for wilights events."""
import collections
import logging

class SubscriptionRegistry:
    """Class for subscribing to wilight events."""

    def __init__(self):
        """Create the subscription registry object."""
        self._callbacks = collections.defaultdict(list)

    def event(self, device, type_, value):
        """Execute the callback for a received event."""
        for type_filter, callback in self._callbacks.get(
                device.serial_number, ()):
            if type_filter is None or type_ == type_filter:
                callback(device, type_, value)

    # pylint: disable=invalid-name
    def on(self, device, type_filter, callback):
        """Add an event callback for a device."""
        self._callbacks[device.serial_number].append((type_filter, callback))
