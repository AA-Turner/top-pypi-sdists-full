from .logger_callable import (
    jsonify,
    Path,
    print_or_log,
)
# initialize_call_log lives in abstract_essentials (the single source).
from .imports import initialize_call_log


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
