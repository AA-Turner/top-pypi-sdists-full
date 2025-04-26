#  IBM Confidential
#  PID 5900-BAF
#  Copyright StreamSets Inc., an IBM Company 2024

import inspect
import sys

FUNCTION_CALLS_HEADERS_KEY = 'X-SS-Sdk-Functions'
INTERACTIVE_MODE_HEADERS_KEY = 'X-SS-Sdk-Interactive-mode'
SDK_FILE_PATH = 'python/streamsets/sdk'
MAX_THRESHOLD = 500


class AnalyticsHeaders:
    """Class to handle storing functions called during the Users session.

    This class stores the data in a dict of the form:
        {'X-SS-Sdk-Functions': <str of function name>,
         'X-SS-Sdk-Interactive-mode': <bool of whether in interactive mode>}
    """

    # maintain an _instance to enable this class to function as a Singleton
    _instance = None

    def __init__(self):
        self.interactive_mode = hasattr(sys, 'ps2')

        self.headers = None
        self.initalize_empty_headers()

    def initalize_empty_headers(self):
        self.headers = {FUNCTION_CALLS_HEADERS_KEY: None, INTERACTIVE_MODE_HEADERS_KEY: str(self.interactive_mode)}

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = AnalyticsHeaders()
        return cls._instance

    @classmethod
    def is_interactive_mode(cls):
        return cls.get_instance().interactive_mode

    @classmethod
    def add_attribute_to_headers(cls, class_obj, name):
        attribute_name = "{}.{}".format(class_obj.__name__, name)
        instance = cls.get_instance()
        instance.headers[FUNCTION_CALLS_HEADERS_KEY] = attribute_name

    @classmethod
    def reset_headers(cls):
        instance = cls.get_instance()
        instance.initalize_empty_headers()


def analytics_class_decorator(cls):
    """Class decorator that adds function user calls during their session to AnalyticsHeaders.

    This decorator overrides:
        1. __getattribute__: This ensures that every method, property and attribute that gets called goes through
        new_getattribute and can accurately be tracked.

        2. __setattr__: This ensures that setting any attribute/property goes through new_setattr and can accurately
         be tracked.

    Both methods go through the following logic:
    1. If the call is made from the user, track via AnalyticsHeaders.add_attribute_to_headers
    2. Call the original __getattribute__ or __setattr__
    """
    original_setattr = cls.__setattr__
    original_getattribute = cls.__getattribute__

    def new_setattr(self, name, value):
        """Overloads original __setattr__ to add metrics data."""
        # Make sure that func was called from the user script and not from an internal method
        caller_code = inspect.currentframe().f_back.f_code
        analytics_instance = AnalyticsHeaders.get_instance()
        if SDK_FILE_PATH not in caller_code.co_filename:
            analytics_instance.reset_headers()
            AnalyticsHeaders.add_attribute_to_headers(cls, name)

        return original_setattr(self, name, value)

    def new_getattribute(self, name):
        """Overloads original __getattribute__ to add metrics data."""
        # Make sure that func was called from the user script and not from an internal method
        caller_code = inspect.currentframe().f_back.f_code
        analytics_instance = AnalyticsHeaders.get_instance()
        if SDK_FILE_PATH not in caller_code.co_filename:
            analytics_instance.reset_headers()
            AnalyticsHeaders.add_attribute_to_headers(cls, name)

        return original_getattribute(self, name)

    cls.__setattr__ = new_setattr
    cls.__getattribute__ = new_getattribute

    return cls
