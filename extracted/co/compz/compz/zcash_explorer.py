"""
Zcash Blockchain Explorer Integration

This module provides real blockchain interaction via public Zcash APIs.
No need for running a full node - uses public block explorers.
"""

import requests
import base64
import json
from typing import Optional, Dict, Any
from datetime import datetime


class ZcashExplorer:
    """
    Interface to Zcash blockchain via public APIs.
    Supports both testnet and mainnet.
    """
    
    # Public block explorers
    EXPLORERS = {
        'testnet': {
            'base_url': 'https://api.zcha.in/v2/testnet',
            'name': 'zcha.in testnet'
        },
        'mainnet': {
            'base_url': 'https://api.zcha.in/v2/mainnet',
            'name': 'zcha.in mainnet'
        }
    }
    
    def __init__(self, testnet: bool = True):
        """
        Initialize Zcash Explorer client.
        
        Args:
            testnet: If True, use testnet; otherwise mainnet
        """
        self.testnet = testnet
        self.network = 'testnet' if testnet else 'mainnet'
        self.config = self.EXPLORERS[self.network]
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'CompZ/1.0.0',
            'Accept': 'application/json'
        })
    
    def get_transaction(self, txid: str) -> Optional[Dict[str, Any]]:
        """
        Fetch transaction details from blockchain.
        
        Args:
            txid: Transaction ID
            
        Returns:
            Transaction data or None if not found
        """
        try:
            url = f"{self.config['base_url']}/transactions/{txid}"
            response = self.session.get(url, timeout=30)
            
            if response.status_code == 404:
                return None
            
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.RequestException as e:
            print(f"⚠️  Error fetching transaction: {str(e)}")
            return None
    
    def get_memo_from_transaction(self, txid: str) -> Optional[str]:
        """
        Extract memo from a Zcash transaction.
        
        Args:
            txid: Transaction ID
            
        Returns:
            Decoded memo string or None
        """
        tx_data = self.get_transaction(txid)
        
        if not tx_data:
            return None
        
        # Try to extract memo from vShieldedOutput (Sapling)
        if 'vShieldedOutput' in tx_data:
            for output in tx_data['vShieldedOutput']:
                if 'memo' in output and output['memo']:
                    try:
                        # Memo is usually hex-encoded
                        memo_hex = output['memo']
                        memo_bytes = bytes.fromhex(memo_hex)
                        # Remove null padding
                        memo_str = memo_bytes.rstrip(b'\x00').decode('utf-8', errors='ignore')
                        if memo_str.strip():
                            return memo_str
                    except Exception:
                        continue
        
        # Try to extract from OP_RETURN in transparent outputs
        if 'vout' in tx_data:
            for vout in tx_data['vout']:
                if 'scriptPubKey' in vout:
                    script = vout['scriptPubKey']
                    if script.get('type') == 'nulldata' and 'asm' in script:
                        # OP_RETURN data
                        asm = script['asm']
                        if 'OP_RETURN' in asm:
                            try:
                                # Extract hex data after OP_RETURN
                                parts = asm.split()
                                if len(parts) > 1:
                                    hex_data = parts[1]
                                    memo_str = bytes.fromhex(hex_data).decode('utf-8', errors='ignore')
                                    if memo_str.strip():
                                        return memo_str
                            except Exception:
                                continue
        
        return None
    
    def verify_transaction_exists(self, txid: str) -> bool:
        """
        Check if a transaction exists on the blockchain.
        
        Args:
            txid: Transaction ID
            
        Returns:
            True if transaction exists, False otherwise
        """
        return self.get_transaction(txid) is not None
    
    def get_transaction_timestamp(self, txid: str) -> Optional[str]:
        """
        Get the timestamp of a transaction.
        
        Args:
            txid: Transaction ID
            
        Returns:
            ISO 8601 timestamp or None
        """
        tx_data = self.get_transaction(txid)
        
        if not tx_data:
            return None
        
        # Try different timestamp fields
        if 'timestamp' in tx_data:
            return datetime.fromtimestamp(tx_data['timestamp']).isoformat() + 'Z'
        
        if 'time' in tx_data:
            return datetime.fromtimestamp(tx_data['time']).isoformat() + 'Z'
        
        if 'blocktime' in tx_data:
            return datetime.fromtimestamp(tx_data['blocktime']).isoformat() + 'Z'
        
        return None
    
    def get_confirmations(self, txid: str) -> Optional[int]:
        """
        Get number of confirmations for a transaction.
        
        Args:
            txid: Transaction ID
            
        Returns:
            Number of confirmations or None
        """
        tx_data = self.get_transaction(txid)
        
        if not tx_data:
            return None
        
        return tx_data.get('confirmations', 0)
    
    def get_explorer_url(self, txid: str) -> str:
        """
        Get block explorer URL for a transaction.
        
        Args:
            txid: Transaction ID
            
        Returns:
            URL string
        """
        if self.testnet:
            return f"https://explorer.testnet.z.cash/tx/{txid}"
        else:
            return f"https://explorer.z.cash/tx/{txid}"


# Alternative: Use zcash-cli style API wrapper
class ZcashPublicAPI:
    """
    Wrapper for public Zcash API endpoints.
    Provides read-only blockchain access without running a node.
    """
    
    def __init__(self, testnet: bool = True):
        self.testnet = testnet
        self.explorer = ZcashExplorer(testnet=testnet)
    
    def getrawtransaction(self, txid: str, verbose: bool = True) -> Optional[Dict]:
        """
        Get raw transaction (compatible with zcash-cli interface).
        
        Args:
            txid: Transaction ID
            verbose: Return decoded transaction
            
        Returns:
            Transaction data
        """
        return self.explorer.get_transaction(txid)
    
    def gettransaction(self, txid: str) -> Optional[Dict]:
        """
        Get transaction details.
        
        Args:
            txid: Transaction ID
            
        Returns:
            Transaction data with CompZ-friendly format
        """
        tx_data = self.explorer.get_transaction(txid)
        
        if not tx_data:
            return None
        
        # Transform to CompZ-friendly format
        return {
            'txid': txid,
            'confirmations': tx_data.get('confirmations', 0),
            'time': tx_data.get('timestamp') or tx_data.get('time'),
            'blocktime': tx_data.get('blocktime'),
            'memo': self.explorer.get_memo_from_transaction(txid)
        }
    
    def getinfo(self) -> Dict:
        """Get blockchain info."""
        return {
            'version': '1.0.0',
            'protocolversion': 170100,
            'walletversion': 0,
            'balance': 0.0,
            'blocks': 0,
            'timeoffset': 0,
            'connections': 1,  # Connected via API
            'proxy': '',
            'difficulty': 0,
            'testnet': self.testnet,
            'keypoololdest': 0,
            'keypoolsize': 0,
            'paytxfee': 0.0001,
            'relayfee': 0.0001,
            'errors': ''
        }
