from enum import Enum

class Strategy(Enum):
    """
    Enumeration representing the different types of queues supported by the system.
    Attributes:
        FIFO: (First-In, First-Out) Elements are processed in the order they arrive.
        LIFO: (Last-In, First-Out) The most recent elements are processed first.
        PRIORITY: Elements are processed according to their assigned priority, not necessarily in arrival order.
    Use this enumeration to specify the queue behavior in the system configuration.
    """

    FIFO = 'fifo'
    LIFO = 'lifo'
    PRIORITY = 'priority'
