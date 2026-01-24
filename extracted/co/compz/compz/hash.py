"""
SHA-256 hashing for compliance data.

Provides cryptographic hashing of normalized compliance data
for blockchain anchoring and verification.
"""

import hashlib
from typing import Union, Dict, Any
from .normalize import normalize_json


def hash_compliance(data: Union[str, Dict, Any]) -> str:
    """
    Compute SHA-256 hash of compliance data.
    
    If data is not already a normalized JSON string, it will be
    normalized first using canonical JSON normalization.
    
    Args:
        data: Either a normalized JSON string or a data structure
              that will be normalized
    
    Returns:
        Hex string prefixed with "0x" (e.g., "0xabc123...")
    
    Example:
        >>> data = {"repo_id": "test", "risk_score": 50}
        >>> hash_compliance(data)
        '0x...'  # 66 character hex string (0x + 64 hex digits)
    """
    # If data is not a string, normalize it first
    if not isinstance(data, str):
        data = normalize_json(data)
    
    # Compute SHA-256 hash
    hash_bytes = hashlib.sha256(data.encode('utf-8')).digest()
    
    # Return as 0x-prefixed hex string
    return '0x' + hash_bytes.hex()


def verify_hash(data: Union[str, Dict, Any], expected_hash: str) -> bool:
    """
    Verify that data matches expected hash.
    
    Args:
        data: Compliance data (will be normalized if needed)
        expected_hash: Expected hash (with or without 0x prefix)
    
    Returns:
        True if hash matches, False otherwise
    
    Example:
        >>> data = {"repo_id": "test"}
        >>> h = hash_compliance(data)
        >>> verify_hash(data, h)
        True
        >>> verify_hash({"different": "data"}, h)
        False
    """
    computed_hash = hash_compliance(data)
    
    # Normalize expected_hash (add 0x if missing)
    if not expected_hash.startswith('0x'):
        expected_hash = '0x' + expected_hash
    
    return computed_hash.lower() == expected_hash.lower()


def hash_file(filepath: str) -> str:
    """
    Compute SHA-256 hash of a file's contents.
    
    Useful for hashing large compliance reports that are
    stored as files rather than in-memory data structures.
    
    Args:
        filepath: Path to file
    
    Returns:
        Hex string prefixed with "0x"
    """
    hasher = hashlib.sha256()
    
    with open(filepath, 'rb') as f:
        # Read file in chunks to handle large files
        for chunk in iter(lambda: f.read(4096), b''):
            hasher.update(chunk)
    
    return '0x' + hasher.hexdigest()


def create_memo(compliance_hash: str, version: str = "v1") -> str:
    """
    Create CompZ memo format for Zcash transaction.
    
    Format: compz:<version>:<hash>
    
    Args:
        compliance_hash: SHA-256 hash (with or without 0x prefix)
        version: Protocol version (default: "v1")
    
    Returns:
        Memo string in CompZ format
    
    Example:
        >>> create_memo("0xabc123...")
        'compz:v1:0xabc123...'
    
    Raises:
        ValueError: If memo would exceed 512 bytes
    """
    # Ensure hash has 0x prefix
    if not compliance_hash.startswith('0x'):
        compliance_hash = '0x' + compliance_hash
    
    # Create memo
    memo = f"compz:{version}:{compliance_hash}"
    
    # Validate length (Zcash memo field is 512 bytes max)
    if len(memo.encode('utf-8')) > 512:
        raise ValueError(f"Memo too long: {len(memo)} bytes (max 512)")
    
    return memo


def parse_memo(memo: str) -> Dict[str, str]:
    """
    Parse CompZ memo to extract protocol version and hash.
    
    Args:
        memo: Memo string from Zcash transaction
    
    Returns:
        Dictionary with 'version' and 'hash' keys
    
    Example:
        >>> parse_memo("compz:v1:0xabc123...")
        {'version': 'v1', 'hash': '0xabc123...'}
    
    Raises:
        ValueError: If memo is not in valid CompZ format
    """
    # Strip whitespace and null bytes
    memo = memo.strip().rstrip('\x00')
    
    if not memo.startswith('compz:'):
        raise ValueError("Invalid CompZ memo: must start with 'compz:'")
    
    try:
        # Split memo: compz:v1:0xhash
        parts = memo.split(':', 2)
        
        if len(parts) != 3:
            raise ValueError("Invalid CompZ memo format")
        
        protocol, version, hash_value = parts
        
        return {
            'version': version,
            'hash': hash_value
        }
    
    except Exception as e:
        raise ValueError(f"Failed to parse CompZ memo: {str(e)}")
