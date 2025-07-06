"""Utility functions for the Matrice package."""

import os
import json
import traceback
import subprocess
import logging
import inspect
import importlib
from functools import lru_cache, wraps


def _make_hashable(obj):
    """Recursively convert unhashable types to hashable ones."""
    if isinstance(obj, (list, tuple)):
        return tuple(_make_hashable(e) for e in obj)
    elif isinstance(obj, dict):
        return tuple(sorted((k, _make_hashable(v)) for k, v in obj.items()))
    elif isinstance(obj, set):
        return tuple(sorted(_make_hashable(e) for e in obj))
    elif hasattr(obj, '__dict__') and not isinstance(obj, type):
        # Handle custom objects by converting their __dict__ to a hashable form
        try:
            return ('__object__', obj.__class__.__name__, _make_hashable(obj.__dict__))
        except (AttributeError, TypeError):
            # If we can't make the object hashable, use its string representation
            return ('__str__', str(obj))
    else:
        # For primitive types and other hashable objects
        try:
            hash(obj)
            return obj
        except TypeError:
            # If it's not hashable, convert to string as last resort
            return ('__str__', str(obj))


def cacheable(f):
    """Wraps a function to make its args hashable before caching."""

    @lru_cache(maxsize=128)
    def wrapped(*args_hashable, **kwargs_hashable):
        try:
            return f(*args_hashable, **kwargs_hashable)
        except Exception as e:
            # If there's an error with unhashable arguments, log and re-raise
            logging.warning(f"Error in cacheable function {f.__name__}: {str(e)}")
            raise

    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            hashable_args = tuple(_make_hashable(arg) for arg in args)
            hashable_kwargs = {k: _make_hashable(v) for k, v in kwargs.items()}
            return wrapped(*hashable_args, **hashable_kwargs)
        except Exception as e:
            # If there's an error in making args hashable, fall back to original function
            logging.warning(
                f"Caching failed for {f.__name__}, using original function: {str(e)}"
            )
            return f(*args, **kwargs)

    return wrapper


@lru_cache(maxsize=1)
def _get_error_logging_producer():
    """Get the Kafka producer for error logging. Cached since it has no arguments."""
    try:
        from confluent_kafka import Producer
        return Producer({
            "bootstrap.servers": "34.66.122.137:9092",
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
    filename,
    function_name,
    error_message,
    traceback_str=None,
    additional_info=None,
):
    """Log error to the backend system.

    Args:
        filename (str): Name of the file where error occurred
        function_name (str): Name of the function where error occurred
        error_message (str): Error message to log
        traceback_str (str, optional): Traceback string. If None, will be generated. Defaults to None.
        additional_info (dict, optional): Additional information to include in the log. Defaults to None.
    """
    if traceback_str is None:
        traceback_str = traceback.format_exc()

    more_info = {}
    if additional_info and isinstance(additional_info, dict):
        more_info.update(additional_info)

    action_id = os.environ.get("MATRICE_ACTION_ID")
    if action_id:
        more_info["actionId"] = action_id

    # Try to send to Kafka if available
    try:
        producer = _get_error_logging_producer()
        if producer:
            producer.produce(
                "error_logs",
                value=json.dumps({
                    "serviceName": "matrice-sdk",
                    "stackTrace": traceback_str,
                    "errorType": "Internal",
                    "description": error_message,
                    "fileName": filename,
                    "functionName": function_name,
                    "moreInfo": more_info,
                }).encode('utf-8')
            )
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

                # Get parameter names and values (safely)
                try:
                    sig = inspect.signature(func)
                    bound_args = sig.bind(*args, **kwargs)
                    bound_args.apply_defaults()
                    # Limit parameter string length for very large arguments
                    param_str = ", ".join(
                        f"{name}={repr(value)[:100] + '...' if isinstance(value, (str, bytes, list, dict)) and len(repr(value)) > 100 else repr(value)}"
                        for name, value in bound_args.arguments.items()
                    )
                except Exception:
                    param_str = "unable to format parameters"

                traceback_str = traceback.format_exc().rstrip()

                # Log detailed error info
                error_msg = f"Exception in {func_file}, function '{func_name}({param_str})': {str(e)}"
                logging.error(error_msg)
                print(error_msg)

                # Additional context for the error log
                additional_info = {"parameters": param_str}

                # Use the log_error parameter from the decorator
                nonlocal log_error
                if log_error:
                    try:
                        send_error_log(
                            filename=func_file,
                            function_name=func_name,
                            error_message=error_msg,
                            traceback_str=traceback_str,
                            additional_info=additional_info,
                        )
                    except Exception as logging_error:
                        logging.error(f"Failed to log error: {str(logging_error)}")

                if raise_exception:
                    raise
                return default_return

        return wrapper

    # Handle both @log_errors and @log_errors(default_return=value) syntax
    if func is None:
        return decorator
    return decorator(func)


def handle_response(response, success_message, failure_message):
    """Handle API response and return appropriate result.

    Args:
        response (dict): API response
        success_message (str): Message to return on success
        failure_message (str): Message to return on failure

    Returns:
        tuple: (result, error, message)
    """
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
    """Check if an item with the given name already exists for the specified service.

    Args:
        session: Session object containing RPC client
        service (str): The name of the service to check (e.g., 'dataset', 'annotation')
        name (str): The name of the item to check for duplication

    Returns:
        tuple: (API response, error_message, status_message)

    Example:
        >>> resp, err, msg = check_for_duplicate('dataset', 'MyDataset')
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Duplicate check result: {resp}")
    """
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
            "path": f"/v1/deployment/check_for_duplicate?deploymentName={name}",
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
    """Fetch a summary of the specified service in the project.

    Args:
        session: Session object containing RPC client
        project_id (str): The project ID
        service_name (str): Service to fetch summary for ('annotations', 'models', etc)

    Returns:
        tuple: (summary_data, error_message)

    Example:
        >>> summary, error = get_summary(rpc, project_id, 'models')
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Summary: {summary}")
    """
    service_paths = {
        "annotations": "/v1/annotations/summary",
        "models": "/v1/model/summary",
        "exports": "/v1/model/summaryExported",
        "deployments": "/v1/deployment/summary",
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
        importlib.import_module(package_name.replace('-', '_'))
        return True
    except ImportError:
        return False


@lru_cache(maxsize=64)
def _install_package(package_name):
    """Helper function to install a package using subprocess.
    This function is separated from the cached function to avoid issues with subprocess.
    """
    try:
        subprocess.run(
            ["pip", "install", package_name],
            check=True,
        )
        logging.info(
            "Successfully installed %s",
            package_name,
        )
        return True
    except subprocess.CalledProcessError as exc:
        logging.error(
            "Failed to install %s: %s",
            package_name,
            exc,
        )
        return False
    except Exception as e:
        logging.error("Unexpected error installing %s: %s", package_name, str(e))
        return False


def dependencies_check(package_names):
    """Check and install required dependencies.

    Args:
        package_names (str or list): Package name(s) to check/install

    Returns:
        bool: True if all packages were installed successfully, False otherwise
    """
    if not isinstance(package_names, list):
        package_names = [package_names]

    success = True
    for package_name in package_names:
        # Check if package is already installed before attempting to install
        if _is_package_installed(package_name):
            logging.debug(f"Package {package_name} is already installed, skipping installation")
            continue
            
        if not _install_package(package_name):
            success = False

    return success
