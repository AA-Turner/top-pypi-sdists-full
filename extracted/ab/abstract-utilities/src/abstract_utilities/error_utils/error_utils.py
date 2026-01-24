from .imports import *
def try_func(func, *args, logger=None, level='error', **kwargs):
    """
    Execute a function with try-except and log exceptions.
    
    Args:
        func: Function to execute.
        *args: Positional arguments for the function.
        logger: Logger object, logger method (e.g., logger.error), or None.
        level (str): Logging level for exceptions (e.g., 'error').
        **kwargs: Keyword arguments for the function.
    
    Returns:
        Result of the function if successful.
    
    Raises:
        Exception: If the function fails and logger is used to log the error.
    """
    log_callable = get_logger_callable(logger=logger, level=level)
    try:
        return func(*args, **kwargs)
    except Exception as e:
        if log_callable:
            log_callable(f"Exception in {func.__name__}: {str(e)}")
        raise
