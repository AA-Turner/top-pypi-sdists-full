from enum import Enum

class SQLiteJournalMode(Enum):
    """
    Enumeration of SQLite journal modes.
    SQLite uses different journal modes to control how transactions are logged and how database integrity is maintained. 
    Each mode offers a trade-off between performance, durability, and concurrency.
    Members:
        DELETE:   (Default) The journal file is deleted at the end of each transaction.
        TRUNCATE: The journal file is truncated to zero bytes instead of being deleted.
        PERSIST:  The journal file is retained but marked as inactive after a transaction.
        MEMORY:   The journal is kept in volatile memory, offering faster performance but less safety.
        WAL:      Write-Ahead Logging mode, which can improve concurrency and performance.
        OFF:      Disables journaling entirely, providing no protection against failures.
    """

    DELETE = "DELETE"      # (Default) The journal file is deleted at the end of the transaction.
    TRUNCATE = "TRUNCATE"  # Empties (truncates) the journal file to zero bytes instead of deleting it.
    PERSIST = "PERSIST"    # Keeps the journal file but marks it as inactive.
    MEMORY = "MEMORY"      # Keeps the journal in memory (faster, less safe).
    WAL = "WAL"            # Uses Write-Ahead Logging, improves concurrency and performance in many cases.
    OFF = "OFF"            # Disables journaling (risky: no protection against failures).