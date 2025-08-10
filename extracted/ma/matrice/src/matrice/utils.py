"""Utility functions for the Matrice package."""

import os
import json
import traceback
import subprocess
import logging
import inspect
import base64
import hashlib
from datetime import datetime, timezone
from functools import lru_cache, wraps
from typing import Any, List, Optional
from importlib.metadata import PackageNotFoundError, version

class ErrorType:
    NOT_FOUND = "NotFound"
    PRECONDITION_FAILED = "PreconditionFailed"
    VALIDATION_ERROR = "ValidationError"
    UNAUTHORIZED = "Unauthorized"
    UNAUTHENTICATED = "Unauthenticated"
    INTERNAL = "Internal"
    UNKNOWN = "Unknown"
    TIMEOUT = "Timeout"
    VALUE_ERROR = "ValueError"
    TYPE_ERROR = "TypeError"
    INDEX_ERROR = "IndexError"
    KEY_ERROR = "KeyError"
    ATTRIBUTE_ERROR = "AttributeError"
    IMPORT_ERROR = "ImportError"
    FILE_NOT_FOUND = "FileNotFound"
    PERMISSION_DENIED = "PermissionDenied"
    CONNECTION_ERROR = "ConnectionError"
    JSON_DECODE_ERROR = "JSONDecodeError"
    ASSERTION_ERROR = "AssertionError"
    RUNTIME_ERROR = "RuntimeError"
    MEMORY_ERROR = "MemoryError"
    OS_ERROR = "OSError"
    STOP_ITERATION = "StopIteration"

ERROR_TYPE_TO_MESSAGE = {
    ErrorType.NOT_FOUND: "The requested resource was not found.",
    ErrorType.PRECONDITION_FAILED: "A precondition for this request was not met.",
    ErrorType.VALIDATION_ERROR: "Some input values are invalid. Please check your request.",
    ErrorType.UNAUTHORIZED: "You do not have permission to perform this action.",
    ErrorType.UNAUTHENTICATED: "Authentication is required to access this resource.",
    ErrorType.INTERNAL: "An internal server error occurred. Please try again later.",
    ErrorType.UNKNOWN: "An unknown error occurred.",
    ErrorType.TIMEOUT: "The operation timed out. Please try again.",
    ErrorType.VALUE_ERROR: "An invalid value was provided.",
    ErrorType.TYPE_ERROR: "An operation was applied to an object of inappropriate type.",
    ErrorType.INDEX_ERROR: "An index is out of range.",
    ErrorType.KEY_ERROR: "A required key was not found in the dictionary.",
    ErrorType.ATTRIBUTE_ERROR: "The requested attribute is missing or invalid.",
    ErrorType.IMPORT_ERROR: "There was an issue importing a module or object.",
    ErrorType.FILE_NOT_FOUND: "The specified file could not be found.",
    ErrorType.PERMISSION_DENIED: "You do not have permission to access this file or resource.",
    ErrorType.CONNECTION_ERROR: "A connection error occurred. Check your network or endpoint.",
    ErrorType.JSON_DECODE_ERROR: "Failed to decode the JSON data. The format might be incorrect.",
    ErrorType.ASSERTION_ERROR: "An assertion failed during execution.",
    ErrorType.RUNTIME_ERROR: "A runtime error occurred.",
    ErrorType.MEMORY_ERROR: "The system ran out of memory while processing the request.",
    ErrorType.OS_ERROR: "An operating system-level error occurred.",
    ErrorType.STOP_ITERATION: "No further items in iterator.",
}

class ErrorLog:
    def __init__(
        self,
        service_name: str,
        stack_trace: str,
        error_type: str,
        description: str,
        file_name: str,
        function_name: str,
        hash: str,
        action_record_id: str = None,
        created_at: datetime = None,
        is_resolved: bool = False,
        more_info: Optional[Any] = None,
    ):
        self.action_record_id = action_record_id
        self.service_name = service_name
        self.created_at = created_at or datetime.now(timezone.utc)
        self.stack_trace = stack_trace
        self.error_type = error_type
        self.description = description
        self.file_name = file_name
        self.function_name = function_name
        self.hash = hash
        self.is_resolved = is_resolved
        self.more_info = more_info

    def to_dict(self) -> dict:
        return {
            "actionRecordId": self.action_record_id,
            "serviceName": self.service_name,
            "createdAt": self.created_at.astimezone(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z"),
            "stackTrace": self.stack_trace,
            "errorType": self.error_type,
            "description": self.description,
            "fileName": self.file_name,
            "functionName": self.function_name,
            "hash": self.hash,
            "isResolved": self.is_resolved,
            "moreInfo": self.more_info,
        }

class AppError(Exception):
    def __init__(
        self,
        error_type: str,
        error: Exception,
        service_name: str,
        details: Optional[List[Any]] = None,
        action_id: Optional[str] = None,
        session_id: Optional[str] = None,
    ):
        self.error_type = error_type
        self.error = error
        self.service_name = service_name
        self.details = details or []
        self.action_id = action_id or os.environ.get("MATRICE_ACTION_ID")
        self.session_id = session_id or os.environ.get("MATRICE_SESSION_ID") or None
        self.message = ERROR_TYPE_TO_MESSAGE.get(error_type, "An unknown error occurred.")
        super().__init__(self.message)

    def append(self, *details: Any) -> "AppError":
        self.details.extend(details)
        return self

    def generate_hash(self) -> str:
        error_str = f"{self.error_type}{str(self.error)}{self.service_name}{''.join(str(d) for d in self.details)}"
        return hashlib.sha256(error_str.encode()).hexdigest()

def _make_hashable(obj):
    """Recursively convert unhashable types to hashable ones."""
    if isinstance(obj, (list, tuple)):
        return tuple(_make_hashable(e) for e in obj)
    elif isinstance(obj, dict):
        return tuple(sorted((k, _make_hashable(v)) for k, v in obj.items()))
    elif isinstance(obj, set):
        return tuple(sorted(_make_hashable(e) for e in obj))
    elif hasattr(obj, '__dict__') and not isinstance(obj, type):
        try:
            return ('__object__', obj.__class__.__name__, _make_hashable(obj.__dict__))
        except (AttributeError, TypeError):
            return ('__str__', str(obj))
    else:
        try:
            hash(obj)
            return obj
        except TypeError:
            return ('__str__', str(obj))

def cacheable(f):
    """Wraps a function to make its args hashable before caching."""
    @lru_cache(maxsize=128)
    def wrapped(*args_hashable, **kwargs_hashable):
        try:
            return f(*args_hashable, **kwargs_hashable)
        except Exception as e:
            logging.warning(f"Error in cacheable function {f.__name__}: {str(e)}")
            raise

    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            hashable_args = tuple(_make_hashable(arg) for arg in args)
            hashable_kwargs = {k: _make_hashable(v) for k, v in kwargs.items()}
            return wrapped(*hashable_args, **hashable_kwargs)
        except Exception as e:
            logging.warning(f"Caching failed for {f.__name__}, using original function: {str(e)}")
            return f(*args, **kwargs)

    return wrapper

@lru_cache(maxsize=1)
def _get_error_logging_producer(rpc_client=None ,access_key=None, secret_key=None):
    """Get the Kafka producer for error logging, fetching config via RPC."""
    try:
        from confluent_kafka import Producer
        
        access_key = access_key or os.environ.get("MATRICE_ACCESS_KEY_ID")
        secret_key = secret_key or os.environ.get("MATRICE_SECRET_ACCESS_KEY")

        if not access_key or not secret_key:
            raise ValueError(
                "Access key and Secret key are required. "
                "Set them as environment variables MATRICE_ACCESS_KEY_ID and MATRICE_SECRET_ACCESS_KEY or pass them explicitly."
            )


        os.environ["MATRICE_ACCESS_KEY_ID"] = access_key
        os.environ["MATRICE_SECRET_ACCESS_KEY"] = secret_key

        try:
            if rpc_client is None:
                from matrice.rpc import RPC
                ## Importing RPC here to avoid cyclic import issues
                rpc_client = RPC(access_key=access_key, secret_key=secret_key)
        except ImportError:
            raise ImportError("RPC client is not available. Check for cyclic import.")
        
        path = "/v1/actions/get_kafka_info"

        response = rpc_client.get(path=path, raise_exception=True)

        if not response or not response.get("success"):
            raise ValueError(f"Failed to fetch Kafka config: {response.get('message', 'No response')}")

        # Decode base64 fields
        encoded_ip = response["data"]["ip"]
        encoded_port = response["data"]["port"]
        ip = base64.b64decode(encoded_ip).decode("utf-8")
        port = base64.b64decode(encoded_port).decode("utf-8")
        bootstrap_servers = f"{ip}:{port}"

        
        return Producer({
            "bootstrap.servers": bootstrap_servers,
            "acks": "all",
            "retries": 3,
            "retry.backoff.ms": 1000,
            "request.timeout.ms": 30000,
            "max.in.flight.requests.per.connection": 5,
            "linger.ms": 10,
            "batch.size": 4096,
            "queue.buffering.max.ms": 50,
            "log_level": 0,
        })
    except ImportError:
        # Handle case where kafka_utils is not available
        logging.warning("KafkaUtils not available, error logging to Kafka disabled")
        return None

def send_error_log(
    filename: str,
    function_name: str,
    error_message: str,
    traceback_str: Optional[str] = None,
    additional_info: Optional[dict] = None,
    error_type: str = ErrorType.INTERNAL,
    service_name: str = "matrice-sdk",
    action_id: Optional[str] = None,
    session_id: Optional[str] = None,
    access_key: Optional[str] = None,
    secret_key: Optional[str] = None,
):
    """Log error to the backend system, sending to Kafka."""
    if traceback_str is None:
        traceback_str = traceback.format_exc().rstrip()

    more_info = {}
    if additional_info and isinstance(additional_info, dict):
        more_info.update(additional_info)

    secret_key = secret_key or os.environ.get("MATRICE_SECRET_ACCESS_KEY")
    if not secret_key:
        raise ValueError("Secret key is required for RPC authentication")
    
    access_key = access_key or os.environ.get("MATRICE_ACCESS_KEY_ID")
    if not access_key:
        raise ValueError("Access key is required for RPC authentication")
    
    action_id = action_id or os.environ.get("MATRICE_ACTION_ID")
    ## verify ENV var name
    if action_id:
        more_info["actionId"] = action_id

    session_id = session_id or os.environ.get("MATRICE_SESSION_ID") or None
    if session_id:
        more_info["sessionId"] = session_id

    # Generate hash
    error_str = f"{error_type}{error_message}{service_name}{json.dumps(more_info)}"
    error_hash = hashlib.sha256(error_str.encode()).hexdigest()

    error_log = ErrorLog(
        service_name=service_name,
        stack_trace=traceback_str,
        error_type=error_type,
        description=error_message,
        file_name=filename,
        function_name=function_name,
        hash=error_hash,
        action_record_id=action_id,
        more_info=more_info,
    )

    def print_callback(err, msg):
        if err:
            print(f"Delivery failed: {err}")
            logging.error(f"Delivery failed: {err}")
        else:
            print(f"Delivery succeeded: {msg.offset()}")
            logging.info(f"Delivery succeeded: {msg.offset()}")

    try:
        producer = _get_error_logging_producer()
        if producer:
            producer.produce(
                topic="error_logs",
                value=json.dumps(error_log.to_dict()).encode('utf-8'),
                key=service_name.encode('utf-8')
                # callback=print_callback
            )
           
            producer.flush()
    except Exception as e:
        logging.error(f"Failed to send error log to Kafka: {str(e)}")

            
def log_errors(func=None, default_return=None, raise_exception=False, log_error=True):
    """Decorator to automatically log exceptions raised in functions.

    This decorator catches any exceptions raised in the decorated function,
    logs them using the log_error function, and optionally re-raises the exception.

    Args:
        func: The function to decorate
        default_return: Value to return if an exception occurs (default: None)
        raise_exception: Whether to raise the exception (default: False)
        log_error: Whether to log the error (default: True)
    Returns:
        The wrapped function with error logging
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                # Get function details
                func_name = func.__name__
                try:
                    func_file = os.path.abspath(inspect.getfile(func))
                except (TypeError, ValueError):
                    func_file = "unknown_file"

                # Get parameter names and values
                try:
                    sig = inspect.signature(func)
                    bound_args = sig.bind(*args, **kwargs)
                    bound_args.apply_defaults()
                    param_str = ", ".join(
                        f"{name}={repr(value)[:100] + '...' if isinstance(value, (str, bytes, list, dict)) and len(repr(value)) > 100 else repr(value)}"
                        for name, value in bound_args.arguments.items()
                    )
                except Exception:
                    param_str = "unable to format parameters"

                traceback_str = traceback.format_exc().rstrip()
                error_msg = f"Exception in {func_file}, function '{func_name}({param_str})': {str(e)}"
                print(error_msg)  # Debug print for development
                logging.error(error_msg)
                
                error_type = type(e).__name__ if type(e).__name__ in ErrorType.__dict__.values() else ErrorType.INTERNAL
                
                service_name = "matrice-sdk"
                ## NOTE: Hardcoded value : Need to reconsider while refactoring py-sdk packages

                # Additional context for the error log
                additional_info = {"parameters": param_str}

                if log_error :
                # and error_type in [ErrorType.INTERNAL, ErrorType.UNKNOWN]:
                    try:
                        send_error_log(
                            filename=func_file,
                            function_name=func_name,
                            error_message=error_msg,
                            traceback_str=traceback_str,
                            additional_info=additional_info,
                            error_type=error_type,
                            service_name=service_name,
                            action_id=os.environ.get("MATRICE_ACTION_ID"),
                            session_id=os.environ.get("MATRICE_SESSION_ID") or None,
                        )
                    except Exception as logging_error:
                        logging.error(f"Failed to log error: {str(logging_error)}")

                if raise_exception:
                    raise AppError(
                        error_type=error_type,
                        error=e,
                        service_name=service_name,
                        details=[param_str],
                        action_id=os.environ.get("MATRICE_ACTION_ID"),
                        session_id=os.environ.get("MATRICE_SESSION_ID") or None,
                    )
                return default_return

        return wrapper

    if func is None:
        return decorator
    return decorator(func)

def handle_response(response, success_message, failure_message):
    """Handle API response and return appropriate result."""
    if response and response.get("success"):
        result = response.get("data")
        error = None
        message = success_message
    else:
        result = None
        error = response.get("message") if response else "No response received"
        message = failure_message
    return result, error, message

def check_for_duplicate(session, service, name):
    """Check if an item with the given name already exists for the specified service."""
    service_config = {
        "dataset": {
            "path": f"/v1/dataset/check_for_duplicate?datasetName={name}",
            "item_name": "Dataset",
        },
        "annotation": {
            "path": f"/v1/annotations/check_for_duplicate?annotationName={name}",
            "item_name": "Annotation",
        },
        "model_export": {
            "path": f"/v1/model/model_export/check_for_duplicate?modelExportName={name}",
            "item_name": "Model export",
        },
        "model": {
            "path": f"/v1/model/model_train/check_for_duplicate?modelTrainName={name}",
            "item_name": "Model Train",
        },
        "projects": {
            "path": f"/v1/project/check_for_duplicate?name={name}",
            "item_name": "Project",
        },
        "deployment": {
            "path": f"/v1/inference/check_for_duplicate?deploymentName={name}",
            "item_name": "Deployment",
        },
    }
    if service not in service_config:
        return (
            None,
            f"Invalid service: {service}",
            "Service not supported",
        )
    config = service_config[service]
    resp = session.rpc.get(path=config["path"])
    if resp and resp.get("success"):
        if resp.get("data") == "true":
            return handle_response(
                resp,
                f"{config['item_name']} with this name already exists",
                f"Could not check for this {service} name",
            )
        return handle_response(
            resp,
            f"{config['item_name']} with this name does not exist",
            f"Could not check for this {service} name",
        )
    return handle_response(
        resp,
        "",
        f"Could not check for this {service} name",
    )

def get_summary(session, project_id, service_name):
    """Fetch a summary of the specified service in the project."""
    service_paths = {
        "annotations": "/v1/annotations/summary",
        "models": "/v1/model/summary",
        "exports": "/v1/model/summaryExported",
        "deployments": "/v1/inference/summary",
    }
    success_messages = {
        "annotations": "Annotation summary fetched successfully",
        "models": "Model summary fetched successfully",
        "exports": "Model Export Summary fetched successfully",
        "deployments": "Deployment summary fetched successfully",
    }
    error_messages = {
        "annotations": "Could not fetch annotation summary",
        "models": "Could not fetch models summary",
        "exports": "Could not fetch models export summary",
        "deployments": "An error occurred while trying to fetch deployment summary.",
    }
    if service_name not in service_paths:
        return (
            None,
            f"Invalid service name: {service_name}",
        )
    path = f"{service_paths[service_name]}?projectId={project_id}"
    resp = session.rpc.get(path=path)
    return handle_response(
        resp,
        success_messages.get(service_name, "Operation successful"),
        error_messages.get(service_name, "Operation failed"),
    )

def _is_package_installed(package_name):
    """Check if a package is already installed."""
    try:
        version(package_name.replace('-', '_'))
        return True
    except (ImportError, OSError, PackageNotFoundError):
        return False

@lru_cache(maxsize=64)
def _install_package(package_name):
    """Helper function to install a package using subprocess."""
    try:
        subprocess.run(
            ["pip", "install", package_name],
            check=True,
        )
        logging.info("Successfully installed %s", package_name)
        return True
    except subprocess.CalledProcessError as exc:
        logging.error("Failed to install %s: %s", package_name, exc)
        return False
    except Exception as e:
        logging.error("Unexpected error installing %s: %s", package_name, str(e))
        return False

def dependencies_check(package_names):
    """Check and install required dependencies."""
    if not isinstance(package_names, list):
        package_names = [package_names]

    success = True
    for package_name in package_names:
        if _is_package_installed(package_name):
            logging.debug(f"Package {package_name} is already installed, skipping installation")
            continue
        if not _install_package(package_name):
            success = False
    return success

