"""
CompZ SDK Client - Dual-mode compliance attestation client.

Supports two modes:
1. Demo Mode: Uses CompZ public testnet gateway (zero setup)
2. Self-Hosted: Uses your own Zcash node (full privacy)
"""

import os
import requests
from typing import Optional, Dict, Union
from datetime import datetime

from .models import ComplianceResult, AnchorResult, VerificationResult
from .normalize import normalize_json
from .hash import hash_compliance, create_memo, parse_memo


class CompZClient:
    """
    CompZ SDK Client for anchoring and verifying compliance data.
    
    The client automatically selects the appropriate mode based on
    configuration. If no RPC URL is provided, it uses demo mode.
    
    Attributes:
        DEMO_ENDPOINT: Public demo gateway URL
        mode: Current mode ("demo" or "self-hosted")
    
    Examples:
        # Demo mode (zero setup)
        >>> client = CompZClient()
        >>> result = client.anchor({"repo_id": "test"})
        
        # Self-hosted mode
        >>> client = CompZClient(
        ...     rpc_url="http://localhost:18232",
        ...     rpc_user="user",
        ...     rpc_pass="pass"
        ... )
        >>> result = client.anchor({"repo_id": "test"})
    """
    
    # Public demo endpoint (to be hosted)
    DEMO_ENDPOINT = os.getenv("COMPZ_DEMO_ENDPOINT", "https://api.compz.dev")
    
    def __init__(
        self,
        rpc_url: Optional[str] = None,
        rpc_user: Optional[str] = None,
        rpc_pass: Optional[str] = None,
        default_address: Optional[str] = None,
        mode: str = "auto",
        testnet: bool = True
    ):
        """
        Initialize CompZ client.
        
        Args:
            rpc_url: Zcash RPC URL (for self-hosted mode)
            rpc_user: RPC username
            rpc_pass: RPC password
            default_address: Default z-address for transactions
            mode: "demo", "self-hosted", or "auto" (default)
            testnet: Whether to use testnet (default: True)
        """
        # Check environment variables if not provided
        rpc_url = rpc_url or os.getenv("ZCASH_RPC_URL") or None
        rpc_user = rpc_user or os.getenv("ZCASH_RPC_USER") or None
        rpc_pass = rpc_pass or os.getenv("ZCASH_RPC_PASS") or None
        default_address = default_address or os.getenv("ZCASH_DEFAULT_ADDRESS") or None
        
        # Treat empty strings as None
        if rpc_url == "": rpc_url = None
        if rpc_user == "": rpc_user = None
        if rpc_pass == "": rpc_pass = None
        if default_address == "": default_address = None
        
        # Check for viewing key (enables read-only blockchain access)
        viewing_key = os.getenv('ZCASH_VIEWING_KEY')
        
        # Determine mode
        if mode == "demo" or (mode == "auto" and rpc_url is None):
            if viewing_key:
                self.mode = "blockchain-readonly"
                self.endpoint = None
                self.testnet = testnet
                self.default_address = default_address
                print("✅ BLOCKCHAIN READ MODE - Real Zcash integration")
                print(f"🌐 Network: {'testnet' if testnet else 'mainnet'}")
                print("📖 Can verify transactions on real blockchain")
                print("📤 For sending: Use Zashi wallet (python3 real_zashi_integration.py)")
            else:
                self.mode = "local-only"
                self.endpoint = None
                print("⚠️  LOCAL MODE - No blockchain connection")
                print("📊 Hashing and verification work locally")
                print("💡 For real blockchain transactions:")
                print("   1. Configure Zcash RPC in .env, OR")
                print("   2. Use Zashi wallet: python3 real_zashi_integration.py")
        else:
            self.mode = "self-hosted"
            self.rpc_url = rpc_url
            self.rpc_user = rpc_user
            self.rpc_pass = rpc_pass
            self.default_address = default_address
            self.testnet = testnet
            print("✅ Using self-hosted mode")
            print(f"🌐 Network: {'testnet' if testnet else 'mainnet'}")
            print(f"📡 RPC: {rpc_url}")
        
        self._session = requests.Session()
    
    def anchor(
        self,
        compliance_data: Union[Dict, ComplianceResult],
        wait_for_confirmation: bool = False
    ) -> AnchorResult:
        """
        Anchor compliance data to Zcash blockchain.
        
        Args:
            compliance_data: Compliance data (dict or ComplianceResult)
            wait_for_confirmation: Whether to wait for block confirmation
        
        Returns:
            AnchorResult with transaction details
        
        Example:
            >>> client = CompZClient()
            >>> result = client.anchor({
            ...     "repo_id": "myorg/myrepo",
            ...     "risk_score": 25.5,
            ...     "timestamp": "2024-01-01T00:00:00Z"
            ... })
            >>> print(result.txid)
        """
        # Convert Pydantic model to dict if needed
        if isinstance(compliance_data, ComplianceResult):
            compliance_data = compliance_data.model_dump()
        
        # Normalize and hash
        normalized = normalize_json(compliance_data)
        comp_hash = hash_compliance(normalized)
        
        print(f"📊 Normalized data: {len(normalized)} bytes")
        print(f"🔐 Hash: {comp_hash[:20]}...")
        
        # Anchor based on mode
        if self.mode == "local-only" or self.mode == "blockchain-readonly":
            raise RuntimeError(
                f"Cannot anchor to blockchain in {self.mode} mode.\n"
                "To create real transactions:\n"
                "  1. Use Zashi wallet integration: compz pay <json_file> --amount 0.0001 --serve --qr\n"
                "  2. Configure ZCASH_RPC_URL in .env for self-hosted mode (requires full node)"
            )
        elif self.mode == "demo":
            result = self._anchor_demo(comp_hash, data)
        else:
            result = self._anchor_selfhosted(comp_hash, wait_for_confirmation)
        
        print(f"✅ Anchored! TXID: {result.txid}")
        if result.explorer_url:
            print(f"🔍 Explorer: {result.explorer_url}")
        
        return result
    
    def _anchor_demo(self, comp_hash: str, data: Dict) -> AnchorResult:
        """Anchor using demo gateway."""
        try:
            response = self._session.post(
                f"{self.endpoint}/api/v1/anchor",
                json={
                    "hash": comp_hash,
                    "data": data  # Gateway doesn't store, just for analytics
                },
                timeout=60
            )
            response.raise_for_status()
            result_data = response.json()
            
            return AnchorResult(**result_data)
        
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Demo mode anchor failed: {str(e)}")
    
    def _anchor_selfhosted(self, comp_hash: str, wait: bool) -> AnchorResult:
        """Anchor using self-hosted node."""
        from .zcash_client import ZcashClient
        
        try:
            # Initialize Zcash client
            zcash = ZcashClient(
                self.rpc_url,
                self.rpc_user,
                self.rpc_pass,
                self.testnet,
                self.default_address
            )
            
            # Create memo
            memo = create_memo(comp_hash)
            
            # Send transaction
            txid = zcash.send_transaction_with_memo(memo)
            
            # Optionally wait for confirmation
            if wait:
                print("⏳ Waiting for confirmation...")
                zcash.wait_for_confirmations(txid, confirmations=1)
            
            # Create result
            network = "testnet" if self.testnet else "mainnet"
            explorer_base = (
                "https://explorer.testnet.z.cash" if self.testnet
                else "https://explorer.z.cash"
            )
            
            return AnchorResult(
                hash=comp_hash,
                txid=txid,
                network=network,
                timestamp=datetime.utcnow().isoformat() + "Z",
                mode="self-hosted",
                explorer_url=f"{explorer_base}/tx/{txid}"
            )
        
        except Exception as e:
            raise RuntimeError(f"Self-hosted anchor failed: {str(e)}")
    
    def verify(
        self,
        compliance_data: Union[Dict, ComplianceResult],
        txid: str
    ) -> VerificationResult:
        """
        Verify compliance data against blockchain transaction.
        
        Args:
            compliance_data: Compliance data to verify
            txid: Zcash transaction ID
        
        Returns:
            VerificationResult with validation details
        
        Example:
            >>> client = CompZClient()
            >>> result = client.verify(
            ...     {"repo_id": "test"},
            ...     "9c8f7e6d5c4b3a2..."
            ... )
            >>> print(result.valid)
            True
        """
        # Convert Pydantic model to dict if needed
        if isinstance(compliance_data, ComplianceResult):
            compliance_data = compliance_data.model_dump()
        
        # Recompute hash
        local_hash = hash_compliance(compliance_data)
        
        print(f"🔍 Verifying against TXID: {txid}")
        print(f"🔐 Local hash: {local_hash[:20]}...")
        
        # Verify based on mode
        if self.mode == "local-only":
            raise RuntimeError(
                "Cannot verify against blockchain in local-only mode.\n"
                "To verify real transactions:\n"
                "  1. Configure ZCASH_VIEWING_KEY in .env for read-only mode\n"
                "  2. Or configure ZCASH_RPC_URL for self-hosted mode\n"
                "  3. Then run: compz verify <file> <txid>"
            )
        elif self.mode == "blockchain-readonly":
            result = self._verify_via_explorer(txid, local_hash)
        else:
            result = self._verify_selfhosted(txid, local_hash)
        
        if result.valid:
            print("✅ VALID - Hashes match!")
        else:
            print(f"❌ INVALID - {result.reason}")
        
        return result
    
    def _verify_demo(
        self,
        data: Dict,
        txid: str,
        local_hash: str
    ) -> VerificationResult:
        """Verify using demo gateway."""
        try:
            response = self._session.post(
                f"{self.endpoint}/api/v1/verify",
                json={
                    "data": data,
                    "txid": txid
                },
                timeout=30
            )
            response.raise_for_status()
            result_data = response.json()
            
            return VerificationResult(**result_data)
        
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Demo mode verify failed: {str(e)}")
    
    def _verify_selfhosted(self, txid: str, local_hash: str) -> VerificationResult:
        """Verify using self-hosted node."""
        from .zcash_client import ZcashClient
        
        try:
            # Initialize Zcash client
            zcash = ZcashClient(
                self.rpc_url,
                self.rpc_user,
                self.rpc_pass,
                self.testnet,
                self.default_address
            )
            
            # Get memo from transaction
            memo = zcash.get_memo_by_txid(txid)
            
            # Parse memo
            parsed = parse_memo(memo)
            onchain_hash = parsed['hash']
            
            # Compare hashes
            valid = local_hash.lower() == onchain_hash.lower()
            
            # Get transaction details
            tx_details = zcash.get_transaction_details(txid)
            
            return VerificationResult(
                valid=valid,
                local_hash=local_hash,
                onchain_hash=onchain_hash,
                txid=txid,
                reason="Hashes match" if valid else "Hash mismatch detected",
                block_time=tx_details.get('time'),
                confirmations=tx_details.get('confirmations')
            )
        
        except Exception as e:
            return VerificationResult(
                valid=False,
                local_hash=local_hash,
                onchain_hash="",
                txid=txid,
                reason=f"Verification failed: {str(e)}"
            )
    
    def _verify_via_explorer(self, txid: str, local_hash: str) -> VerificationResult:
        """Verify using public blockchain explorer (read-only mode)."""
        from .zcash_explorer import ZcashExplorer
        
        try:
            print("🔍 Querying Zcash blockchain via public API...")
            
            # Initialize explorer
            explorer = ZcashExplorer(testnet=self.testnet)
            
            # Check if transaction exists
            if not explorer.verify_transaction_exists(txid):
                return VerificationResult(
                    valid=False,
                    local_hash=local_hash,
                    onchain_hash="",
                    txid=txid,
                    reason="Transaction not found on blockchain"
                )
            
            print("✅ Transaction found on blockchain")
            
            # Get memo from transaction
            memo = explorer.get_memo_from_transaction(txid)
            
            if not memo:
                return VerificationResult(
                    valid=False,
                    local_hash=local_hash,
                    onchain_hash="",
                    txid=txid,
                    reason="No memo found in transaction. This may not be a CompZ transaction."
                )
            
            print(f"📝 Memo found: {memo[:50]}...")
            
            # Parse memo
            try:
                parsed = parse_memo(memo)
                onchain_hash = parsed['hash']
            except Exception as e:
                return VerificationResult(
                    valid=False,
                    local_hash=local_hash,
                    onchain_hash="",
                    txid=txid,
                    reason=f"Invalid memo format: {str(e)}"
                )
            
            # Compare hashes
            valid = local_hash.lower() == onchain_hash.lower()
            
            # Get transaction details
            timestamp = explorer.get_transaction_timestamp(txid)
            confirmations = explorer.get_confirmations(txid)
            
            return VerificationResult(
                valid=valid,
                local_hash=local_hash,
                onchain_hash=onchain_hash,
                txid=txid,
                reason="Hashes match - verified on blockchain!" if valid else "Hash mismatch detected",
                block_time=timestamp,
                confirmations=confirmations
            )
        
        except Exception as e:
            return VerificationResult(
                valid=False,
                local_hash=local_hash,
                onchain_hash="",
                txid=txid,
                reason=f"Blockchain verification failed: {str(e)}"
            )
    
    def get_status(self) -> Dict:
        """
        Get SDK status and configuration.
        
        Returns:
            Status dictionary
        """
        status = {
            "mode": self.mode,
            "version": "1.0.0"
        }
        
        if self.mode == "local-only":
            status["blockchain_connected"] = False
            status["hashing"] = "✅ Working"
            status["verification"] = "✅ Local only"
            status["note"] = "Configure ZCASH_VIEWING_KEY for blockchain verification"
        elif self.mode == "blockchain-readonly":
            status["blockchain_connected"] = True
            status["blockchain_access"] = "Read-only (Public API)"
            status["network"] = "testnet" if self.testnet else "mainnet"
            status["hashing"] = "✅ Working"
            status["verification"] = "✅ Real blockchain"
            status["sending"] = "Via Zashi wallet"
            status["note"] = "Can verify real transactions on Zcash blockchain"
        else:
            status["blockchain_connected"] = True
            status["rpc_url"] = self.rpc_url
            status["network"] = "testnet" if self.testnet else "mainnet"
            status["address"] = self.default_address[:20] + "..." if self.default_address else None
        
        return status
