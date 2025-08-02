from enum import Enum

class Environments(Enum):
    """
    Enumeration of possible application environments.

    Attributes:
        DEVELOPMENT: Represents the development environment.
        TESTING: Represents the testing environment.
        PRODUCTION: Represents the production environment.
    """

    DEVELOPMENT = 'development'
    TESTING = 'testing'
    PRODUCTION = 'production'