#
# Copyright 2025 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.


class OAuthValidationErr(ValueError):
    """
    The base exception for all OAuth validation errors
    """


class OAuthProviderNotFound(OAuthValidationErr):
    pass


class OAuthFlowSessionExpired(OAuthValidationErr):
    """
    The OAuth flow session has expired
    """


class OAuthError(Exception):
    """
    The base exception for all OAuth flow errors
    TODO: Let's see if we have more specific errors derived from this one if not we should remove this class
    """


class OAuthFlowError(OAuthError):
    """
    The OAuth flow has failed
    """

    def __init__(self, provider_id: str, error_code: str, message: str) -> None:
        super().__init__(message)

        self.provider_id = provider_id
        self.error_code = error_code
