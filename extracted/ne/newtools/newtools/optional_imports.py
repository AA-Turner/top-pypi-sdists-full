# (c) Deductive 2012-2020, all rights reserved
# This code is licensed under MIT license (see license.txt for details)

from functools import wraps

# global used for testing results without imports
NEVER_IMPORT = False


class DummyClass:
    """
    A dummy class that raises an import error when you try to do anything with it.

    Is returned in place of the requested module/package/function if an Import error occurs
    """

    def __init__(self, name):
        self.name = name

    def __getattr__(self, name):
        raise ImportError('{0} is not installed. Failed getting {1}()'.format(self.name, name))

    def __call__(self, *args, **kwargs):
        raise ImportError('{0} is not installed. Failed calling {0}()'.format(self.name))


class DummyAWSRetry:
    """
    Dummy implementation of AWSRetry class with fake backoff method
    """

    @classmethod
    def backoff(cls, *_, **__):
        def decorator(f):
            @wraps(f)
            def wrapper(*args, **kwargs):
                return f(*args, **kwargs)

            return wrapper

        return decorator


def import_wrapper(default):
    """
    A decorator to return a Dummy function if an ImportError is raised

    :param default: the dummy function to return
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                if NEVER_IMPORT:
                    raise ImportError
                return func(*args, **kwargs)
            except ImportError:
                return default

        return wrapper

    return decorator


# Now define each import in turn


# -----------------------------
@import_wrapper(DummyAWSRetry)
def get_aws_retry():
    from awsretry import AWSRetry
    return AWSRetry


AWSRetry = get_aws_retry()


# -----------------------------
@import_wrapper(DummyClass("s3fs"))
def get_s3fs():
    import s3fs
    return s3fs


s3fs = get_s3fs()


# -----------------------------
@import_wrapper(DummyClass("pandas"))
def get_pandas():
    import pandas
    return pandas


pandas = get_pandas()


# -----------------------------
@import_wrapper(DummyClass("numpy"))
def get_numpy():
    import numpy
    return numpy


numpy = get_numpy()


# -----------------------------

@import_wrapper(DummyClass("pyarrow"))
def get_pyarrow():
    import pyarrow
    return pyarrow


pyarrow = get_pyarrow()


# -----------------------------

@import_wrapper(DummyClass("boto3"))
def get_boto3():
    import boto3
    return boto3


boto3 = get_boto3()


# -----------------------------

@import_wrapper(DummyClass("botocore"))
def get_botocore():
    import botocore
    return botocore


botocore = get_botocore()


# -----------------------------

@import_wrapper(DummyClass("chardet.universaldetector"))
def get_universal_detector():
    from chardet.universaldetector import UniversalDetector
    return UniversalDetector


UniversalDetector = get_universal_detector()


# -----------------------------


@import_wrapper(DummyClass("sqlparse"))
def get_sqlparse():
    import sqlparse
    return sqlparse


sqlparse = get_sqlparse()

# -----------------------------


@import_wrapper(DummyClass("json_log_formatter"))
def get_json_log_formatter():
    import json_log_formatter
    return json_log_formatter


json_log_formatter = get_json_log_formatter()

#  Add new optional imports to the bottom of this file together with the dummy class
# -----------------------------
