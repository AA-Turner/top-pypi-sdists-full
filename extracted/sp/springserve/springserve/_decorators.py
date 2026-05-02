"""
AWS ELB 5XX error looks like:

<html>
<head><title>503 Service Temporarily Unavailable</title></head>
<body bgcolor="white">
<center><h1>503 Service Temporarily Unavailable</h1></center>
</body>
</html>
"""
import time
import sys
import warnings

_msg = None
try:
    from link import lnk
    from link.wrappers.springservewrappers import SpringServeAPIResponseWrapper
    _msg = lnk.msg
except:
    pass


AWS_ELB_ERROR_MESSAGES = ("503 Service Temporarily Unavailable", "502 Bad Gateway")
RACK_ATTACK_STATUS_CODE = 429
RACK_ATTACK_MESSAGE = "Retry later\n"

def deprecated(message):
    def deprecated_decorator(func):
        def deprecated_func(*args, **kwargs):
            warnings.warn("{} is a deprecated function. {}".format(func.__name__, message),
                        category=DeprecationWarning,
                        stacklevel=2)
            warnings.simplefilter('default', DeprecationWarning)
            return func(*args, **kwargs)
        return deprecated_func
    return deprecated_decorator

def is_resp_in_elb_error_messages(resp):
    if (sys.version_info >= (3, 0)):
        return any([e in resp.text for e in AWS_ELB_ERROR_MESSAGES])
    else:
        return any([e in resp.content for e in AWS_ELB_ERROR_MESSAGES])


def raw_response_retry(api_call, limit=4, sleep_duration=5, backoff_factor=2):
    """
    Decorator for SpringServe API to handle retries (with exponential backoff) in the case
    of a rate-limit or 5XX error.

    Sleep duration and backoff factor control wait time between successive failures, e.g.
    sleep_duration 3 and backoff_factor 2 means sleep 3s, 6s, 12s, 24s

    :param int limit: Max number of retry attempts
    :param int sleep_duration: Initial sleep time
    :param float/int backoff_factor: Factor to increase sleep between successive retries.
    """
    def wrapped(*args, **kwargs):
        sleeps = sleep_duration
        num_attempts = 0
        while num_attempts < limit:
            # make the API call
            resp = api_call(*args, **kwargs)

            aws_check = (
                    # make sure it's the link response object
                    isinstance(resp, SpringServeAPIResponseWrapper) and
                    # HTTP status codes that are valid for retries
                    resp.status_code >= 500 and resp.status_code < 600 and
                    # content matches one of our error messages - note that ELB error
                    # messages will not be JSON (they are HTML strings) so cannot check
                    # resp.json attribute, as this will not always be valid
                    is_resp_in_elb_error_messages(resp)
                    )

            rack_attack_check = (
                    isinstance(resp, SpringServeAPIResponseWrapper) and
                    resp.status_code == RACK_ATTACK_STATUS_CODE and
                    resp.content == RACK_ATTACK_MESSAGE
                    )

            if aws_check or rack_attack_check:
                _msg.warn("Encountered rate-limit (attempt {}), sleeping".format(num_attempts))
                num_attempts += 1
                time.sleep(sleeps)
                sleeps *= backoff_factor
            # call was either successful, or an error outside of the purview of this
            # handler
            else:
                return resp

        # We've hit max retry attempts, return anyways
        return resp

    return wrapped
