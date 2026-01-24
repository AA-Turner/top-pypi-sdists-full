"""
CSSL Event System
Handles @event.* registrations and dispatching for CSSL scripts
"""

from enum import Enum, auto
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Any, Optional, Set
import threading
import time


class EventCategory(Enum):
    """Event categories for CSSL"""
    BOOT = "Boot"
    SYSTEM = "System"
    VSRAM = "VSRam"
    SERVICE = "Service"
    KERNEL = "Kernel"
    NETWORK = "Network"
    USER = "User"
    WHEEL = "Wheel"
    CUSTOM = "Custom"


class EventType(Enum):
    """All supported CSSL events"""
    # Boot Events
    BOOTING = ("Boot", "Booting")
    BOOTED = ("Boot", "Booted")
    EARLY_BOOT = ("Boot", "EarlyBoot")
    LATE_BOOT = ("Boot", "LateBoot")

    # System Events
    SHUTDOWN = ("System", "Shutdown")
    RESTART = ("System", "Restart")
    SUSPEND = ("System", "Suspend")
    RESUME = ("System", "Resume")
    ERROR = ("System", "Error")
    CRITICAL = ("System", "Critical")

    # VSRAM Events
    VSRAM_SWITCHED = ("VSRam", "Switched")
    VSRAM_FULL = ("VSRam", "Full")
    VSRAM_CRITICAL = ("VSRam", "Critical")
    VSRAM_SET = ("VSRam", "Set")
    VSRAM_GET = ("VSRam", "Get")
    VSRAM_DELETE = ("VSRam", "Delete")
    VSRAM_UPDATE = ("VSRam", "Update")

    # Service Events
    SERVICE_START = ("Service", "Start")
    SERVICE_STOP = ("Service", "Stop")
    SERVICE_ERROR = ("Service", "Error")
    SERVICE_COMPLETE = ("Service", "Complete")
    SERVICE_TIMEOUT = ("Service", "Timeout")

    # Kernel Events
    KERNEL_INIT = ("Kernel", "Init")
    KERNEL_READY = ("Kernel", "Ready")
    KERNEL_ERROR = ("Kernel", "Error")
    KERNEL_COMMAND = ("Kernel", "Command")

    # Network Events
    NETWORK_CONNECT = ("Network", "Connect")
    NETWORK_DISCONNECT = ("Network", "Disconnect")
    NETWORK_ERROR = ("Network", "Error")
    NETWORK_DATA = ("Network", "Data")
    NETWORK_UPDATE = ("Network", "Update")

    # User Events
    USER_LOGIN = ("User", "Login")
    USER_LOGOUT = ("User", "Logout")
    USER_CREATE = ("User", "Create")
    USER_DELETE = ("User", "Delete")
    USER_CHANGE = ("User", "Change")

    # Wheel Events
    WHEEL_CHANGE = ("Wheel", "Change")
    WHEEL_READ = ("Wheel", "Read")
    WHEEL_WRITE = ("Wheel", "Write")
    WHEEL_INIT = ("Wheel", "Init")

    def __init__(self, category: str, name: str):
        self._category = category
        self._event_name = name

    @property
    def category(self) -> str:
        return self._category

    @property
    def event_name(self) -> str:
        return self._event_name

    @property
    def full_name(self) -> str:
        return f"@event.{self._category}.{self._event_name}"

    @classmethod
    def from_string(cls, event_string: str) -> Optional['EventType']:
        """Parse event string like '@event.Boot.Booting' to EventType"""
        if not event_string.startswith('@event.'):
            return None

        parts = event_string[7:].split('.')
        if len(parts) == 1:
            # Short form: @event.Booting
            for event in cls:
                if event.event_name == parts[0]:
                    return event
        elif len(parts) == 2:
            # Full form: @event.Boot.Booting
            category, name = parts
            for event in cls:
                if event.category == category and event.event_name == name:
                    return event

        return None


@dataclass
class EventData:
    """Data passed to event handlers"""
    event_type: EventType
    timestamp: float = field(default_factory=time.time)
    source: str = ""
    data: Dict[str, Any] = field(default_factory=dict)
    cancelled: bool = False

    def cancel(self):
        """Cancel event propagation"""
        self.cancelled = True

    def get(self, key: str, default: Any = None) -> Any:
        """Get data value"""
        return self.data.get(key, default)

    def set(self, key: str, value: Any):
        """Set data value"""
        self.data[key] = value


@dataclass
class EventHandler:
    """Registered event handler"""
    callback: Callable[[EventData], Any]
    priority: int = 0
    once: bool = False
    filter_func: Optional[Callable[[EventData], bool]] = None
    service_name: str = ""
    handler_id: str = ""


class CSSLEventManager:
    """
    Central event manager for CSSL
    Handles registration, deregistration, and dispatching of events
    """

    def __init__(self):
        self._handlers: Dict[EventType, List[EventHandler]] = {}
        self._custom_handlers: Dict[str, List[EventHandler]] = {}
        self._lock = threading.RLock()
        self._handler_counter = 0
        self._event_history: List[EventData] = []
        self._max_history = 100
        self._enabled = True
        self._blocked_events: Set[EventType] = set()

    def _generate_handler_id(self) -> str:
        """Generate unique handler ID"""
        self._handler_counter += 1
        return f"handler_{self._handler_counter}_{time.time()}"

    def register(self,
                 event_type: EventType,
                 callback: Callable[[EventData], Any],
                 priority: int = 0,
                 once: bool = False,
                 filter_func: Optional[Callable[[EventData], bool]] = None,
                 service_name: str = "") -> str:
        """
        Register an event handler

        Args:
            event_type: The event type to listen for
            callback: Function to call when event fires
            priority: Higher priority handlers run first (default 0)
            once: If True, handler is removed after first execution
            filter_func: Optional filter function, handler only runs if filter returns True
            service_name: Name of the service registering this handler

        Returns:
            Handler ID for later deregistration
        """
        with self._lock:
            handler_id = self._generate_handler_id()
            handler = EventHandler(
                callback=callback,
                priority=priority,
                once=once,
                filter_func=filter_func,
                service_name=service_name,
                handler_id=handler_id
            )

            if event_type not in self._handlers:
                self._handlers[event_type] = []

            self._handlers[event_type].append(handler)
            # Sort by priority (higher first)
            self._handlers[event_type].sort(key=lambda h: -h.priority)

            return handler_id

    def register_custom(self,
                        event_name: str,
                        callback: Callable[[EventData], Any],
                        priority: int = 0,
                        once: bool = False,
                        service_name: str = "") -> str:
        """Register a custom event handler"""
        with self._lock:
            handler_id = self._generate_handler_id()
            handler = EventHandler(
                callback=callback,
                priority=priority,
                once=once,
                service_name=service_name,
                handler_id=handler_id
            )

            if event_name not in self._custom_handlers:
                self._custom_handlers[event_name] = []

            self._custom_handlers[event_name].append(handler)
            self._custom_handlers[event_name].sort(key=lambda h: -h.priority)

            return handler_id

    def unregister(self, handler_id: str) -> bool:
        """Remove a handler by ID"""
        with self._lock:
            # Check standard handlers
            for event_type in self._handlers:
                handlers = self._handlers[event_type]
                for i, handler in enumerate(handlers):
                    if handler.handler_id == handler_id:
                        handlers.pop(i)
                        return True

            # Check custom handlers
            for event_name in self._custom_handlers:
                handlers = self._custom_handlers[event_name]
                for i, handler in enumerate(handlers):
                    if handler.handler_id == handler_id:
                        handlers.pop(i)
                        return True

            return False

    def unregister_service(self, service_name: str) -> int:
        """Remove all handlers registered by a service"""
        count = 0
        with self._lock:
            for event_type in self._handlers:
                original_len = len(self._handlers[event_type])
                self._handlers[event_type] = [
                    h for h in self._handlers[event_type]
                    if h.service_name != service_name
                ]
                count += original_len - len(self._handlers[event_type])

            for event_name in self._custom_handlers:
                original_len = len(self._custom_handlers[event_name])
                self._custom_handlers[event_name] = [
                    h for h in self._custom_handlers[event_name]
                    if h.service_name != service_name
                ]
                count += original_len - len(self._custom_handlers[event_name])

        return count

    def emit(self,
             event_type: EventType,
             source: str = "",
             data: Optional[Dict[str, Any]] = None,
             sync: bool = True) -> EventData:
        """
        Emit an event

        Args:
            event_type: The event to emit
            source: Source identifier
            data: Event data dictionary
            sync: If True, run handlers synchronously

        Returns:
            EventData object with results
        """
        if not self._enabled:
            return EventData(event_type=event_type)

        if event_type in self._blocked_events:
            return EventData(event_type=event_type, cancelled=True)

        event_data = EventData(
            event_type=event_type,
            source=source,
            data=data or {}
        )

        if sync:
            self._dispatch(event_data)
        else:
            thread = threading.Thread(
                target=self._dispatch,
                args=(event_data,),
                daemon=True
            )
            thread.start()

        # Add to history
        with self._lock:
            self._event_history.append(event_data)
            if len(self._event_history) > self._max_history:
                self._event_history.pop(0)

        return event_data

    def emit_custom(self,
                    event_name: str,
                    source: str = "",
                    data: Optional[Dict[str, Any]] = None) -> bool:
        """Emit a custom event"""
        if not self._enabled or event_name not in self._custom_handlers:
            return False

        event_data = EventData(
            event_type=EventType.BOOTING,  # Placeholder for custom
            source=source,
            data=data or {}
        )
        event_data.data['_custom_event_name'] = event_name

        handlers_to_remove = []

        with self._lock:
            handlers = self._custom_handlers.get(event_name, [])[:]

        for handler in handlers:
            if event_data.cancelled:
                break

            try:
                handler.callback(event_data)
                if handler.once:
                    handlers_to_remove.append(handler.handler_id)
            except Exception as e:
                print(f"CSSL Event Handler Error [{event_name}]: {e}")

        for handler_id in handlers_to_remove:
            self.unregister(handler_id)

        return True

    def _dispatch(self, event_data: EventData):
        """Internal dispatch method"""
        handlers_to_remove = []

        with self._lock:
            handlers = self._handlers.get(event_data.event_type, [])[:]

        for handler in handlers:
            if event_data.cancelled:
                break

            # Check filter
            if handler.filter_func:
                try:
                    if not handler.filter_func(event_data):
                        continue
                except Exception:
                    continue

            try:
                handler.callback(event_data)
                if handler.once:
                    handlers_to_remove.append(handler.handler_id)
            except Exception as e:
                print(f"CSSL Event Handler Error [{event_data.event_type.full_name}]: {e}")

        for handler_id in handlers_to_remove:
            self.unregister(handler_id)

    def block_event(self, event_type: EventType):
        """Block an event from being emitted"""
        self._blocked_events.add(event_type)

    def unblock_event(self, event_type: EventType):
        """Unblock an event"""
        self._blocked_events.discard(event_type)

    def enable(self):
        """Enable event system"""
        self._enabled = True

    def disable(self):
        """Disable event system (no events will be dispatched)"""
        self._enabled = False

    def get_handlers(self, event_type: EventType) -> List[EventHandler]:
        """Get all handlers for an event type"""
        with self._lock:
            return self._handlers.get(event_type, [])[:]

    def get_history(self, count: int = 10) -> List[EventData]:
        """Get recent event history"""
        with self._lock:
            return self._event_history[-count:]

    def clear_history(self):
        """Clear event history"""
        with self._lock:
            self._event_history.clear()

    def get_stats(self) -> Dict[str, Any]:
        """Get event system statistics"""
        with self._lock:
            total_handlers = sum(len(h) for h in self._handlers.values())
            total_custom = sum(len(h) for h in self._custom_handlers.values())

            return {
                'enabled': self._enabled,
                'total_handlers': total_handlers,
                'custom_handlers': total_custom,
                'blocked_events': len(self._blocked_events),
                'history_size': len(self._event_history),
                'event_types_with_handlers': len(self._handlers),
                'custom_event_types': len(self._custom_handlers)
            }


class EventDecorators:
    """
    Decorator factory for CSSL event handlers
    Used to register class methods as event handlers
    """

    def __init__(self, event_manager: CSSLEventManager):
        self._manager = event_manager

    def on(self, event_type: EventType, priority: int = 0):
        """Decorator to register a method as an event handler"""
        def decorator(func):
            self._manager.register(
                event_type=event_type,
                callback=func,
                priority=priority
            )
            return func
        return decorator

    def once(self, event_type: EventType, priority: int = 0):
        """Decorator to register a one-time event handler"""
        def decorator(func):
            self._manager.register(
                event_type=event_type,
                callback=func,
                priority=priority,
                once=True
            )
            return func
        return decorator


# Global event manager instance
_global_event_manager: Optional[CSSLEventManager] = None


def get_event_manager() -> CSSLEventManager:
    """Get the global event manager instance"""
    global _global_event_manager
    if _global_event_manager is None:
        _global_event_manager = CSSLEventManager()
    return _global_event_manager


def set_event_manager(manager: CSSLEventManager):
    """Set the global event manager instance"""
    global _global_event_manager
    _global_event_manager = manager


# Convenience functions for common events
def emit_boot_event(event_name: str, data: Optional[Dict[str, Any]] = None) -> EventData:
    """Emit a boot event"""
    event_map = {
        'Booting': EventType.BOOTING,
        'Booted': EventType.BOOTED,
        'EarlyBoot': EventType.EARLY_BOOT,
        'LateBoot': EventType.LATE_BOOT
    }
    event_type = event_map.get(event_name)
    if event_type:
        return get_event_manager().emit(event_type, source="boot", data=data)
    return EventData(event_type=EventType.BOOTING)


def emit_system_event(event_name: str, data: Optional[Dict[str, Any]] = None) -> EventData:
    """Emit a system event"""
    event_map = {
        'Shutdown': EventType.SHUTDOWN,
        'Restart': EventType.RESTART,
        'Suspend': EventType.SUSPEND,
        'Resume': EventType.RESUME,
        'Error': EventType.ERROR,
        'Critical': EventType.CRITICAL
    }
    event_type = event_map.get(event_name)
    if event_type:
        return get_event_manager().emit(event_type, source="system", data=data)
    return EventData(event_type=EventType.SHUTDOWN)


def emit_vsram_event(event_name: str, data: Optional[Dict[str, Any]] = None) -> EventData:
    """Emit a VSRAM event"""
    event_map = {
        'Switched': EventType.VSRAM_SWITCHED,
        'Full': EventType.VSRAM_FULL,
        'Critical': EventType.VSRAM_CRITICAL,
        'Set': EventType.VSRAM_SET,
        'Get': EventType.VSRAM_GET,
        'Delete': EventType.VSRAM_DELETE,
        'Update': EventType.VSRAM_UPDATE
    }
    event_type = event_map.get(event_name)
    if event_type:
        return get_event_manager().emit(event_type, source="vsram", data=data)
    return EventData(event_type=EventType.VSRAM_SET)


def emit_service_event(event_name: str, service: str = "", data: Optional[Dict[str, Any]] = None) -> EventData:
    """Emit a service event"""
    event_map = {
        'Start': EventType.SERVICE_START,
        'Stop': EventType.SERVICE_STOP,
        'Error': EventType.SERVICE_ERROR,
        'Complete': EventType.SERVICE_COMPLETE,
        'Timeout': EventType.SERVICE_TIMEOUT
    }
    event_type = event_map.get(event_name)
    if event_type:
        event_data = data or {}
        event_data['service'] = service
        return get_event_manager().emit(event_type, source="service", data=event_data)
    return EventData(event_type=EventType.SERVICE_START)


def emit_kernel_event(event_name: str, data: Optional[Dict[str, Any]] = None) -> EventData:
    """Emit a kernel event"""
    event_map = {
        'Init': EventType.KERNEL_INIT,
        'Ready': EventType.KERNEL_READY,
        'Error': EventType.KERNEL_ERROR,
        'Command': EventType.KERNEL_COMMAND
    }
    event_type = event_map.get(event_name)
    if event_type:
        return get_event_manager().emit(event_type, source="kernel", data=data)
    return EventData(event_type=EventType.KERNEL_INIT)


def emit_network_event(event_name: str, data: Optional[Dict[str, Any]] = None) -> EventData:
    """Emit a network event"""
    event_map = {
        'Connect': EventType.NETWORK_CONNECT,
        'Disconnect': EventType.NETWORK_DISCONNECT,
        'Error': EventType.NETWORK_ERROR,
        'Data': EventType.NETWORK_DATA,
        'Update': EventType.NETWORK_UPDATE
    }
    event_type = event_map.get(event_name)
    if event_type:
        return get_event_manager().emit(event_type, source="network", data=data)
    return EventData(event_type=EventType.NETWORK_CONNECT)


def emit_user_event(event_name: str, username: str = "", data: Optional[Dict[str, Any]] = None) -> EventData:
    """Emit a user event"""
    event_map = {
        'Login': EventType.USER_LOGIN,
        'Logout': EventType.USER_LOGOUT,
        'Create': EventType.USER_CREATE,
        'Delete': EventType.USER_DELETE,
        'Change': EventType.USER_CHANGE
    }
    event_type = event_map.get(event_name)
    if event_type:
        event_data = data or {}
        event_data['username'] = username
        return get_event_manager().emit(event_type, source="user", data=event_data)
    return EventData(event_type=EventType.USER_LOGIN)


def emit_wheel_event(event_name: str, wheel: str = "", key: str = "", data: Optional[Dict[str, Any]] = None) -> EventData:
    """Emit a wheel event"""
    event_map = {
        'Change': EventType.WHEEL_CHANGE,
        'Read': EventType.WHEEL_READ,
        'Write': EventType.WHEEL_WRITE,
        'Init': EventType.WHEEL_INIT
    }
    event_type = event_map.get(event_name)
    if event_type:
        event_data = data or {}
        event_data['wheel'] = wheel
        event_data['key'] = key
        return get_event_manager().emit(event_type, source="wheel", data=event_data)
    return EventData(event_type=EventType.WHEEL_CHANGE)
