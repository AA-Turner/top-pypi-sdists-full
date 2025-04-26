import exceptions

"""
def throw_if_not_authenticated(func):
    def outer(*args, **kwargs):
        if not PhaxioApiV2.api_key or not PhaxioApiV2.api_secret:
            raise NotAuthenticatedException(
                'Need to set PhaxioApiV2.api_key and PhaxioApiV2.api_secret before using this function')
        func(*args, **kwargs)
    return outer
"""

class NotAuthenticatedException(Exception):
    pass