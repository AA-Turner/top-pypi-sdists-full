from enum import Enum

class MySQLEngine(Enum):
    """
    Enumeration of supported MySQL storage engines.

    Attributes:
        INNODB: Default transactional storage engine, supports ACID compliance and foreign keys.
        MYISAM: Legacy non-transactional storage engine, faster for read-heavy workloads but lacks transaction support.
        MEMORY: Stores all data in RAM for fast access, data is lost on server restart.
        NDB: Clustered storage engine designed for distributed MySQL setups.

    Use this enum to specify the desired storage engine when configuring MySQL database tables.
    """
    INNODB = "InnoDB"      # Default engine (transactional)
    MYISAM = "MyISAM"      # Legacy engine (non-transactional)
    MEMORY = "MEMORY"      # In-memory storage
    NDB = "NDB"            # Clustered storage engine