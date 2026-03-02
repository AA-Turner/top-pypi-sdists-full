#!/usr/bin/env python3
"""
Script to verify EVM signature from SIWE authentication payload.

The message format is: "Permission to AvaPay {nonce}"
where nonce is obtained from the backend.

Dependencies:
    pip install eth-account

Usage:
    python check_signature.py [message]

    If message is not provided, it will only verify that the signature
    can recover the correct address.
"""

import logging

from eth_account import Account
from eth_account.messages import encode_defunct

logger = logging.getLogger(__name__)


def verify_evm_signature(signature: str, expected_address: str, message: str):
    """
    Verify an EIP-191 personal signature.

    Args:
        signature: The signature hex string (0x prefixed)
        expected_address: The Ethereum address that should have signed (0x prefixed)
        message: Message that was signed

    Returns:
        (is_valid, recovered_address, message_used)
    """
    try:
        # Ensure signature has 0x prefix
        if not signature.startswith("0x"):
            signature = "0x" + signature

        # Ensure address has 0x prefix and normalize to lowercase for comparison
        if not expected_address.startswith("0x"):
            expected_address = "0x" + expected_address

        message_encoded = encode_defunct(text=message)
        recovered_address = Account.recover_message(message_encoded, signature=signature)

        # Verify address matches
        is_valid = recovered_address == expected_address

        return is_valid, recovered_address, message

    except Exception as e:
        logger.warning(f"Error verifying signature: {e}")
        return False, None, None
