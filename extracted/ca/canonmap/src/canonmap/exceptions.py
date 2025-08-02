class CanonMapError(Exception):
    """Base exception for all CanonMap errors."""

class MySQLConnectorError(CanonMapError):
    """Raised for errors in MySQLConnector operations."""

class DatabaseManagerError(CanonMapError):
    """Raised for errors in DatabaseManager operations."""

class TableManagerError(CanonMapError):
    """Raised for errors in TableManager operations."""

class FieldManagerError(CanonMapError):
    """Raised for errors in FieldManager operations."""

class UserManagerError(CanonMapError):
    """Raised for errors in UserManager operations."""

class MatchingError(CanonMapError):
    """Raised for errors in Matching operations."""