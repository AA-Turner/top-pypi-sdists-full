"""Custom exceptions for the verified local proxy."""


class VerifiedProxyError(Exception):
    """Base exception for verified local proxy errors."""

    pass


class ConfigurationError(VerifiedProxyError):
    """Error loading or validating configuration."""

    pass


class VerificationError(VerifiedProxyError):
    """Signature verification failed."""

    pass


class TargetNotRunningError(VerifiedProxyError):
    """Target server is not running on expected port."""

    pass
