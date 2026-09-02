from .imports import *
from .logger_callable import *
def initialize_call_log(value=None,
                        data=None,
                        logMsg=None,
                        log_level=None):
    """
    Inspect the stack to find the first caller *outside* this module,
    then log its function name and file path.
    """
    # Grab the current stack
    stack = inspect.stack()
    caller_name = "<unknown>"
    caller_path = "<unknown>"
    log_level = log_level or 'info'
    try:
        # Starting at index=1 to skip initialize_call_log itself
        for frame_info in stack[1:]:
            modname = frame_info.frame.f_globals.get("__name__", "")
            # Skip over frames in your logging modules:
            if not modname.startswith("abstract_utilities.log_utils") \
               and not modname.startswith("abstract_flask.request_utils") \
               and not modname.startswith("logging"):
                caller_name = frame_info.function
                caller_path = frame_info.filename
                break
    finally:
        # Avoid reference cycles
        del stack

    logMsg = logMsg or "initializing"
    full_message = (
        f"{logMsg}\n"
        f"calling_function: {caller_name}\n"
        f"path: {caller_path}\n"
        f"data: {data}"
    )

    print_or_log(full_message,level=log_level)
def _normalize(obj):
    """Recursively turn PosixPath into str, sets into list, etc."""
    if isinstance(obj, Path):
        return str(obj)
    if isinstance(obj, dict):
        return {k: _normalize(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple, set)):
        return [_normalize(x) for x in obj]
    return obj
def get_json_call_response(value=None, status_code=None, data=None, logMsg=None, callLog=False):
    response_body = {}
    if status_code == 200:
        response_body["success"] = True
        response_body["result"] = _normalize(value)
        logMsg = logMsg or "success"
        if callLog:
            initialize_call_log(value=value,
                            data=data,
                            logMsg=logMsg,
                            log_level='info')
    else:
        response_body["success"] = False
        response_body["error"] = _normalize(value)
        logMsg = logMsg or f"ERROR: {logMsg}"
        initialize_call_log(value=value,
                            data=data,
                            logMsg=logMsg,
                            log_level='error')
    return jsonify(response_body), status_code
