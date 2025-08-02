"""
Constants used throughout the inventory report manager.
"""

import re


class StorageInventoryConstants:
    """Centralized storage for inventory application constants"""

    # S3-specific inventory file column definitions
    S3_INVENTORY_COLUMNS = [
        "Bucket",
        "Key",
        "Size",
        "LastModifiedDate",
        "ETag",
        "StorageClass",
        "IsMultipartUploaded",
        "ReplicationStatus",
        "EncryptionStatus",
        "ObjectLockRetainUntilDate",
        "ObjectLockMode",
        "ObjectLockLegalHoldStatus",
        "IntelligentTieringAccessTier",
        "BucketKeyStatus",
        "ChecksumAlgorithm",
        "ObjectAccessControlList",
        "ObjectOwner",
    ]

    # Common settings across cloud storage systems
    # Keys to exclude from processing
    EXCLUDE_KEYS = [
        ".Trash",
        ".hive-staging",
        ".spark-staging",
        "__HIVE_DEFAULT_PARTITION__",
        "_SUCCESS",
    ]

    # Recognized compression extensions
    COMPRESSION_EXTS = {"gz", "snappy", "zip"}

    # Partition keys that are always treated as min/max
    FORCE_MINMAX_KEYS = {"year", "month", "day", "hour", "ds"}

    # Regex for extracting partition information
    PARTITION_REGEX = re.compile(r"([a-zA-Z0-9_]+)=([^/]+)")

    # Cap for distinct values in partition summaries
    DISTINCT_CAP = 1000
