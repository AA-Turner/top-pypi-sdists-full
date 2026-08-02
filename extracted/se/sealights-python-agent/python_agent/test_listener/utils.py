import logging
import os

log = logging.getLogger(__name__)


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        key = "%s-%s" % (cls, os.getpid())
        if key not in cls._instances:
            cls._instances[key] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[key]


def get_test_name_from_identifier(test_identifier):
    if not test_identifier:
        return ""
    if "/" not in test_identifier:
        return test_identifier
    test_name_parts = test_identifier.split("/")[1:]
    return "/".join(test_name_parts)


def get_execution_id_from_identifier(test_identifier):
    if not test_identifier:
        return ""
    return test_identifier.split("/")[0]
