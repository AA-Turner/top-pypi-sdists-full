######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.21.1+obcheckpoint(0.2.4);ob(v1)                                                   #
# Generated on 2025-07-11T23:29:18.565418                                                            #
######################################################################################################

from __future__ import annotations

import typing
import logging
if typing.TYPE_CHECKING:
    import metaflow.mf_extensions.outerbounds.plugins.apps.core.utils
    import metaflow.mf_extensions.outerbounds.plugins.apps.core._vendor.spinner.spinners
    import logging

from ......_vendor import click as click
from ._vendor.spinner.spinners import Spinners as Spinners

CAPSULE_DEBUG: bool

class MultiStepSpinner(object, metaclass=type):
    """
    A spinner that supports multi-step progress and configurable alignment.
    
    Parameters
    ----------
    spinner : Spinners
        Which spinner frames/interval to use.
    text : str
        Static text to display beside the spinner.
    color : str, optional
        Click color name.
    align : {'left','right'}
        Whether to render the spinner to the left (default) or right of the text.
    """
    def __init__(self, spinner: metaflow.mf_extensions.outerbounds.plugins.apps.core._vendor.spinner.spinners.Spinners = ..., text: str = '', color: typing.Optional[str] = None, align: str = 'right', file = ...):
        ...
    @property
    def main_text(self):
        ...
    def start(self):
        ...
    def stop(self):
        ...
    def log(self, *messages: str):
        """
        Pause the spinner, emit a ✔ + message, then resume.
        """
        ...
    def __enter__(self):
        ...
    def __exit__(self, exc_type, exc, tb):
        ...
    ...

class SpinnerLogHandler(logging.Handler, metaclass=type):
    def __init__(self, spinner: MultiStepSpinner, *args, **kwargs):
        ...
    def emit(self, record):
        ...
    ...

class MaximumRetriesExceeded(Exception, metaclass=type):
    def __init__(self, url, method, status_code, text):
        ...
    def __str__(self):
        ...
    ...

class TODOException(Exception, metaclass=type):
    ...

requests_funcs: list

def safe_requests_wrapper(requests_module_fn, *args, conn_error_retries = 2, retryable_status_codes = [409], logger_fn = None, **kwargs):
    """
    There are two categories of errors that we need to handle when dealing with any API server.
    1. HTTP errors. These are are errors that are returned from the API server.
        - How to handle retries for this case will be application specific.
    2. Errors when the API server may not be reachable (DNS resolution / network issues)
        - In this scenario, we know that something external to the API server is going wrong causing the issue.
        - Failing pre-maturely in the case might not be the best course of action since critical user jobs might crash on intermittent issues.
        - So in this case, we can just planely retry the request.
    
    This function handles the second case. It's a simple wrapper to handle the retry logic for connection errors.
    If this function is provided a `conn_error_retries` of 5, then the last retry will have waited 32 seconds.
    Generally this is a safe enough number of retries after which we can assume that something is really broken. Until then,
    there can be intermittent issues that would resolve themselves if we retry gracefully.
    """
    ...

