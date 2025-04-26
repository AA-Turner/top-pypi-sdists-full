import warnings


# Function wrapper that emits warnings for deprecated functions. Adds a deprecation indication in the returned function's
# docstring as well. Docstring here can't be dynamically generated, so we can't include the new function's name here.
def deprecation_warn(replacement_func, deprecated_func_name):
    """
    Emits a deprecation warning before running function.

    :param replacement_func: The replacement function to execute.
    :param deprecated_func_name: The name of the deprecated function.
    """

    def wrapper(*args, **kwargs):
        """
        This function is deprecated.
        """
        warnings.warn(
            "Function {0} has been deprecated. Please use {1} instead.".format(
                deprecated_func_name, replacement_func.__name__
            )
        )
        return replacement_func(*args, **kwargs)

    return wrapper


def __outer(func):
    def _dlt_get_dataset():
        # If decorators are chained together, this is the function that will be passed to the
        # next decorator.
        return None

    return _dlt_get_dataset
