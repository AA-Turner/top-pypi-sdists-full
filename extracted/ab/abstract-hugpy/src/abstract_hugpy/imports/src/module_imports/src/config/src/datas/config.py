from ..imports import *
logger = get_logFile(__name__)

def resolve_model_path(entry):
    """Return a valid model path or HF repo id from DEFAULT_PATHS entry."""
    if entry is None:
        logger.error("{entry}: DEFAULT_PATHS entry missing.")
        return None
    if isinstance(entry,str) and entry in MODULE_DEFAULTS:
       return MODULE_DEFAULTS.get(entry)

    if isinstance(entry, dict):
        local_path = entry.get("path")
        repo_id = entry.get("id")
        name = entry.get("name")

        if local_path and os.path.exists(local_path):
            logger.info(f"{name} resolved local model path: {local_path}")
            return local_path

        if repo_id:
            logger.info(f"{name} resolved remote repo id: {repo_id}")
            return repo_id

        logger.error(f"{name}: malformed entry: {entry}")
        return None

    if isinstance(entry, str):
        logger.info(f"{name} using direct model string: {entry}")
        return entry

    logger.error(f"{name}: invalid model path type: {type(entry)}")
    return None
