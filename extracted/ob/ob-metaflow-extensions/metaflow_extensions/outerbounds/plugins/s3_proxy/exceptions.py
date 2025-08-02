from metaflow.exception import MetaflowException


class S3ProxyException(MetaflowException):
    headline = "S3 Proxy Error"


class S3ProxyConfigException(S3ProxyException):
    headline = "S3 Proxy Configuration Error"


class S3ProxyApiException(S3ProxyException):
    headline = "S3 Proxy API Error"
