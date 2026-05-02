class Constants:
    """
    Constants class contains a set of constant values used for logging messages
    throughout the application, particularly in the context of managing
    connections and channels with RabbitMQ.
    """

    GENERIC_ERROR = "Error: {}"
    """Generic error message with a placeholder for additional details."""

    # Constants for log messages
    CONNECTION_OPENED = "Connection opened"
    """Indicates that a connection has been successfully opened."""

    CONNECTION_OPENED_DEBUG = "Connection opened: {}"
    """Provides detailed debug information when a connection is opened."""

    CONNECTION_NOT_ESTABLISHED = "Connection not established"
    """Indicates that a connection has not been established."""

    CONNECTION_CLOSED = "Connection closed: {}"
    """Indicates that a connection has been closed, with details."""

    CONNECTION_CLOSED_DEBUG = "Connection closed: {}"
    """Provides detailed debug information when a connection is closed."""

    CONNECTION_NOT_OPEN_ERROR = "Connection not open"
    """Error message indicating that an operation was attempted on a connection that isn't open."""

    CONNECTION_OPEN_ERROR = "Connection open error: {}"
    """Specific error message when there's an issue opening a connection."""

    CONNECTION_OPEN_ERROR_DEBUG = "Connection {} open error: {}"
    """Detailed debug information for a connection open error."""

    CONNECTION_FAILED = "Failed to connect to RabbitMQ: {}"
    """Indicates a failure to connect to RabbitMQ, with details."""

    ATTEMPT_RECONNECT = "Attempt to reconnect {}/{} in {} seconds..."
    """Message indicating an attempt to reconnect to RabbitMQ, showing the attempt number, total attempts, and wait time."""

    RECONNECT_FAILED = "Reached the maximum number of reconnection attempts ({})."
    """Message indicating that the maximum number of reconnection attempts has been reached."""

    CONNECTION_CLOSING_ERROR = "Error in closing connection: {}"
    """Error message when there's an issue closing a connection."""

    MAX_RECONNECT_ATTEMPTS_REACHED = (
        "Reached the maximum number of reconnection attempts ({})."
    )
    """Indicates that the maximum number of reconnection attempts has been reached (similar to RECONNECT_FAILED)."""

    CONNECTION_NOT_OPENED = "Connection not opened"
    """Indicates that a connection was not opened when expected."""

    CHANNEL_OPENED = "Channel opened"
    """Indicates that a channel has been successfully opened."""

    CHANNEL_OPENED_DEBUG = "Channel opened: {}"
    """Provides detailed debug information when a channel is opened."""

    CHANNEL_OPEN_FAILED = "Failed to open channel: {}"
    """Indicates a failure to open a channel, with details."""

    CHANNEL_OPEN_ERROR = "Error in opening channel: {}"
    """Specific error message when there's an issue opening a channel."""

    CHANNEL_OPEN_ERROR_DEBUG = "Channel {} open error: {}"
    """Detailed debug information for a channel open error."""

    CHANNEL_CLOSED = "RabbitMQ channel closed."
    """Indicates that a RabbitMQ channel has been closed."""

    CHANNEL_CLOSING_ERROR = "Error in closing channel: {}"
    """Error message when there's an issue closing a channel."""

    CHANNEL_NOT_OPENED = "Channel not opened"
    """Indicates that a channel was not opened when expected."""

    QUEUE_DECLARED = "[x] {} declared"
    """Message indicating that a queue has been declared, with the queue name."""

    QUEUE_DECLARED_DEBUG = "[x] {} declared: {}"
    """Provides detailed debug information when a queue is declared."""

    START_CONSUMING = "{}: Start consuming on {}"
    """Indicates the start of message consumption on a specified queue."""

    START_CONSUMING_NO_QUEUE = "{}: No listening queue declared"
    """Indicates an attempt to start consuming without a declared queue."""

    MESSAGE_RECEIVED = "Received message: {} on channel: {}"
    """Message indicating that a message has been received on a specific channel."""

    MESSAGE_RECEIVED_DEBUG = (
        "Received message: {} on channel: {}, method: {}, properties: {}"
    )
    """Provides detailed debug information when a message is received."""

    MESSAGE_SENT = "Message sent to {}: {}"
    """Indicates that a message has been sent to a specific destination."""

    MESSAGE_SENDING_ERROR = "Error while sending message: {}"
    """Error message when there's an issue sending a message."""

    MESSAGE_SENDING_ERROR_DEBUG = (
        "Error while sending message: {} on channel: {}, error: {}"
    )
    """Provides detailed debug information for a message sending error."""

    MESSAGE_SEND_FAILED = "Failed to send message: {}"
    """Indicates that a message failed to be sent."""

    MESSAGE_PROCESSING_ERROR = "Error while processing message: {}"
    """Error message when there's an issue processing a message."""

    MESSAGE_PROCESSING_ERROR_DEBUG = "Error while processing message: {} on channel: {}, method: {}, properties: {}, error: {}"
    """Provides detailed debug information for a message processing error."""

    ERROR_EXECUTION_CALLBACK = "Error during the execution of on_event_callback: {}"
    """Error message for issues during the execution of an event callback."""

    ERROR_STACK_TRACE = "Details of the stack trace: {}"
    """Provides details of a stack trace when an error occurs."""

    ERROR_CALLBACK_NOT_ASYNC = (
        "on_event_callback is not set correctly or is not asynchronous."
    )
    """Error message indicating that the event callback is not set up correctly or is not asynchronous."""

    ERROR_CALLBACK_NOT_ASYNC_PROVIDED = "The provided callback is not asynchronous."
    """Error message indicating that the provided callback is not asynchronous."""
