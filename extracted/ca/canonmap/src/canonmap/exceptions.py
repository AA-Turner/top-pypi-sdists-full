class CanonMapError(Exception):
    """Base exception for all CanonMap errors."""

class MySQLConnectorError(CanonMapError):
    """Raised for errors in MySQLConnector operations."""