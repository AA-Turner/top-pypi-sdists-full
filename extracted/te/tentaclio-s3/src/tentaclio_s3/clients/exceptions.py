"""Client exceptions."""
from tentaclio.clients.exceptions import ClientError


class S3Error(ClientError):
    """Exception encountered over a S3 client connection."""
