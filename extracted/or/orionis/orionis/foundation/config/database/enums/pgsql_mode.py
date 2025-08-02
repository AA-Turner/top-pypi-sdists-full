from enum import Enum

class PGSQLSSLMode(Enum):
    """
    SSL modes for PostgreSQL connections.
    Corresponds to the 'sslmode' parameter in libpq.

    Official values documented at:
    https://www.postgresql.org/docs/current/libpq-ssl.html

    - DISABLE: No SSL (not secure)
    - ALLOW: Attempts SSL, silently falls back if unavailable
    - PREFER: Uses SSL if available (common default)
    - REQUIRE: Requires SSL (no certificate validation)
    - VERIFY_CA: Validates the server certificate against the CA
    - VERIFY_FULL: Validates both the certificate and the host name (most secure)
    """

    DISABLE = "disable"          # No SSL (not secure)
    ALLOW = "allow"              # Attempts SSL, silently falls back if unavailable
    PREFER = "prefer"            # Uses SSL if available (common default)
    REQUIRE = "require"          # Requires SSL (no certificate validation)
    VERIFY_CA = "verify-ca"      # Validates the server certificate against the CA
    VERIFY_FULL = "verify-full"  # Validates both the certificate and the host name (most secure)
