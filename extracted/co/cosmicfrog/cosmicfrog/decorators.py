from functools import wraps
from inspect import signature
import uuid


ERROR_MESSAGES = {
    "workspace": "Workspace is required. Use 'Studio' if you are not sure.",
}

def requires_parameter(param_name):
    """
    Generic decorator to check if a specific parameter is passed.
    Class has to have a __handle_error__ method to handle the error.

    :param param_name: The name of the required parameter.
    :param error_message: The error message to return if the parameter is missing.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            sig = signature(func)
            param_names = list(sig.parameters.keys())

            if param_name not in kwargs:
                param_index = param_names.index(param_name) if param_name in param_names else -1
                if param_index == -1 or len(args) <= param_index - 1:
                    error_message = ERROR_MESSAGES.get(param_name, f"Parameter '{param_name}' is required.")
                    return self.__handle_error__(kwargs.get('_correlation_id', ''), error_message)

            return func(self, *args, **kwargs)
        return wrapper
    return decorator


def check_connection_type(required_type):
    """
    Decorator to check if the model is connected via the required connection type.
    connection_type: The required connection type. "app_key" | "engine" | "connection_string"
    :param required_type: The required connection type.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if self.connection_type != required_type:
                return {
                    "status": "error", 
                    "message": f"Functionality only supported for models connected via {required_type}."
                }
            return func(self, *args, **kwargs)
        return wrapper
    return decorator


def ensure_correlation_id(func):
    """
    Decorator to ensure a _correlation_id is set.
    Handles both positional and keyword arguments.
    If not provided, it generates a new UUID.
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        sig = signature(func)
        param_names = list(sig.parameters.keys())

        # Remove self parameter
        if param_names[0] == "self":
            param_names = param_names[1:]

        if "_correlation_id" in param_names:
            param_index = param_names.index("_correlation_id")

            if len(args) > param_index:
                if not args[param_index]:
                    args = (
                        args[:param_index]
                        + (str(uuid.uuid4()),)
                        + args[param_index + 1:]
                    )
            elif "_correlation_id" not in kwargs or not kwargs["_correlation_id"]:
                kwargs["_correlation_id"] = str(uuid.uuid4())

        return func(self, *args, **kwargs)
    return wrapper
