"""
Zcash RPC client for self-hosted mode.

Handles communication with zcashd node via JSON-RPC.
"""

import requests
import time
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class ZcashClient:
    """
    Client for Zcash JSON-RPC API.
    
    Supports sending shielded transactions with memos and
    retrieving transaction details for verification.
    
    Attributes:
        rpc_url: Zcash RPC endpoint URL
        testnet: Whether using testnet
    """
    
    def __init__(
        self,
        rpc_url: str,
        rpc_user: str,
        rpc_pass: str,
        testnet: bool = True,
        default_address: Optional[str] = None
    ):
        """
        Initialize Zcash client.
        
        Args:
            rpc_url: RPC endpoint (e.g., "http://localhost:18232")
            rpc_user: RPC username
            rpc_pass: RPC password
            testnet: Whether using testnet
            default_address: Default z-address for transactions
        """
        self.rpc_url = rpc_url
        self.auth = (rpc_user, rpc_pass)
        self.testnet = testnet
        self.default_address = default_address
        
        # Validate connection
        try:
            self._validate_connection()
            logger.info(f"Connected to Zcash {'testnet' if testnet else 'mainnet'}")
        except Exception as e:
            logger.warning(f"Connection validation failed: {e}")
    
    def _rpc_call(self, method: str, params: list = None) -> Any:
        """
        Make JSON-RPC call to zcashd.
        
        Args:
            method: RPC method name
            params: Method parameters
        
        Returns:
            RPC result
        
        Raises:
            Exception: If RPC call fails
        """
        payload = {
            "jsonrpc": "2.0",
            "id": "compz",
            "method": method,
            "params": params or []
        }
        
        try:
            response = requests.post(
                self.rpc_url,
                json=payload,
                auth=self.auth,
                timeout=30
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise Exception(f"RPC connection failed: {str(e)}")
        
        result = response.json()
        
        if 'error' in result and result['error']:
            raise Exception(f"RPC Error: {result['error']}")
        
        return result.get('result')
    
    def _validate_connection(self):
        """Validate RPC connection and network."""
        try:
            info = self._rpc_call("getblockchaininfo")
            chain = info.get('chain')
            
            if self.testnet and chain != 'test':
                raise Exception(f"Expected testnet, got {chain}")
            elif not self.testnet and chain != 'main':
                raise Exception(f"Expected mainnet, got {chain}")
            
            logger.info(f"Connected to {chain} at block {info['blocks']}")
        except Exception as e:
            raise Exception(f"Failed to validate connection: {str(e)}")
    
    def send_transaction_with_memo(
        self,
        memo: str,
        amount: float = 0.0001,
        from_addr: Optional[str] = None,
        to_addr: Optional[str] = None
    ) -> str:
        """
        Send shielded transaction with memo.
        
        Args:
            memo: Text memo (max 512 bytes UTF-8)
            amount: Amount in ZEC (default: 0.0001)
            from_addr: Source z-address (default: self.default_address)
            to_addr: Destination z-address (default: send to self)
        
        Returns:
            Transaction ID (txid)
        
        Raises:
            Exception: If memo too long, insufficient funds, or RPC error
        """
        # Validate memo length
        memo_bytes = memo.encode('utf-8')
        if len(memo_bytes) > 512:
            raise ValueError(f"Memo too long: {len(memo_bytes)} bytes (max 512)")
        
        # Use default address if not provided
        from_addr = from_addr or self.default_address
        to_addr = to_addr or from_addr
        
        if not from_addr:
            raise ValueError("No source address specified")
        
        # Check balance
        balance = self._rpc_call("z_getbalance", [from_addr])
        if balance < amount + 0.0001:  # amount + fee
            raise Exception(f"Insufficient balance: {balance} ZEC")
        
        # Encode memo to hex
        memo_hex = memo_bytes.hex()
        
        # Pad to 512 bytes (1024 hex chars)
        memo_hex = memo_hex.ljust(1024, '0')
        
        # Create transaction
        logger.info(f"Sending transaction with memo: {memo[:50]}...")
        
        opid = self._rpc_call("z_sendmany", [
            from_addr,
            [{
                "address": to_addr,
                "amount": amount,
                "memo": memo_hex
            }],
            1,      # minconf
            0.0001  # fee
        ])
        
        logger.info(f"Operation created: {opid}")
        
        # Wait for completion
        txid = self._wait_for_operation(opid)
        
        logger.info(f"Transaction sent: {txid}")
        return txid
    
    def _wait_for_operation(self, opid: str, timeout: int = 120) -> str:
        """
        Wait for async z_sendmany operation to complete.
        
        Args:
            opid: Operation ID
            timeout: Max seconds to wait
        
        Returns:
            Transaction ID
        
        Raises:
            TimeoutError: If operation times out
            Exception: If operation fails
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            status_list = self._rpc_call("z_getoperationstatus", [[opid]])
            
            if not status_list:
                raise Exception(f"Operation {opid} not found")
            
            status_obj = status_list[0]
            status = status_obj.get('status')
            
            if status == 'success':
                txid = status_obj.get('result', {}).get('txid')
                if not txid:
                    raise Exception("Operation succeeded but no txid returned")
                return txid
            
            elif status == 'failed':
                error = status_obj.get('error', {})
                raise Exception(f"Transaction failed: {error}")
            
            elif status == 'executing':
                logger.debug("Transaction being processed...")
                time.sleep(2)
            
            else:
                logger.debug(f"Operation status: {status}")
                time.sleep(2)
        
        raise TimeoutError(f"Operation {opid} timed out after {timeout}s")
    
    def get_memo_by_txid(self, txid: str) -> str:
        """
        Extract memo from transaction.
        
        Args:
            txid: Transaction ID
        
        Returns:
            Decoded memo text (null bytes stripped)
        
        Raises:
            Exception: If memo not found or can't be decoded
        """
        # View transaction (requires viewing key)
        try:
            tx_view = self._rpc_call("z_viewtransaction", [txid])
        except Exception as e:
            logger.warning(f"z_viewtransaction failed: {e}")
            raise Exception("Cannot view memo - viewing key not available")
        
        # Extract memo from outputs
        for output in tx_view.get('outputs', []):
            memo_hex = output.get('memo')
            if not memo_hex:
                continue
            
            # Decode hex to bytes
            try:
                memo_bytes = bytes.fromhex(memo_hex)
                # Strip null padding
                memo_text = memo_bytes.rstrip(b'\x00').decode('utf-8')
                
                # Validate CompZ format
                if memo_text.startswith('compz:'):
                    return memo_text
            
            except Exception as e:
                logger.warning(f"Failed to decode memo: {e}")
                continue
        
        raise Exception(f"No CompZ memo found in transaction {txid}")
    
    def get_transaction_details(self, txid: str) -> Dict:
        """
        Get transaction details.
        
        Args:
            txid: Transaction ID
        
        Returns:
            Transaction details dictionary
        """
        try:
            return self._rpc_call("gettransaction", [txid])
        except Exception:
            # Fallback to getrawtransaction
            return self._rpc_call("getrawtransaction", [txid, 1])
    
    def wait_for_confirmations(self, txid: str, confirmations: int = 1) -> bool:
        """
        Wait for transaction to receive confirmations.
        
        Args:
            txid: Transaction ID
            confirmations: Number of confirmations to wait for
        
        Returns:
            True if confirmed
        """
        logger.info(f"Waiting for {confirmations} confirmations...")
        
        while True:
            try:
                tx = self._rpc_call("gettransaction", [txid])
                confs = tx.get('confirmations', 0)
                
                if confs >= confirmations:
                    logger.info(f"Transaction confirmed ({confs} confirmations)")
                    return True
                
                logger.debug(f"Current confirmations: {confs}/{confirmations}")
                time.sleep(10)  # Check every 10 seconds
            
            except Exception as e:
                logger.error(f"Error checking confirmations: {e}")
                time.sleep(10)
    
    def get_new_address(self, addr_type: str = "sapling") -> str:
        """
        Generate new z-address.
        
        Args:
            addr_type: Address type ("sapling" or "orchard")
        
        Returns:
            New z-address
        """
        return self._rpc_call("z_getnewaddress", [addr_type])
    
    def get_balance(self, address: Optional[str] = None) -> float:
        """
        Get balance for address.
        
        Args:
            address: Z-address (default: total balance)
        
        Returns:
            Balance in ZEC
        """
        if address:
            return self._rpc_call("z_getbalance", [address])
        else:
            return self._rpc_call("getbalance")
