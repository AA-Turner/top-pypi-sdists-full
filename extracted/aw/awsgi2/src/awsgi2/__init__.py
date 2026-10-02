""" A WSGI gateway for the AWS API Gateway/Lambda proxy integration """
__version__ = "1.0.2"  # NOTE Use `bump2version --config-file patch` to bump versions correctly


from .wrapper import response

__all__ = ("response",)
