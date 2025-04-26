class InvalidMappingError(ValueError):
    """
    General errors related to the acquisition of an identity mapping; for
    example, if an external program returns an incorrectly-formatted
    response or if the response does not match the input request.
    """


class IdentityMappingError(ValueError):
    """
    General errors related to invoking the identity mapping logic; for
    example, if an external program returns an error.
    """
