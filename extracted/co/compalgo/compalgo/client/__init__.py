from __future__ import annotations

from typing import Union, Dict, Any, Optional

from .algorand import AlgorandClient, AnchorResult, explorer_url_for
from ..core.verdict import ComplianceVerdict, verdict_hash
from ..config import AlgoConfig


class CompliLedgerClient:
    def __init__(
        self,
        *,
        algod_url: str,
        algod_token: str = "",
        sender_mnemonic: str,
        network: str = "testnet",
        indexer_url: str = None,
        indexer_token: str = ""
    ):
        self._algo = AlgorandClient(
            algod_url=algod_url,
            algod_token=algod_token,
            network=network,
            indexer_url=indexer_url,
            indexer_token=indexer_token
        )
        self._mnemonic = sender_mnemonic
        self._network = network

    def mint_verdict(self, verdict: Union[ComplianceVerdict, Dict[str, Any]]) -> AnchorResult:
        v = verdict if isinstance(verdict, ComplianceVerdict) else ComplianceVerdict(**verdict)
        h = verdict_hash(v)
        note_text = f"CLG1|sha256:{h}"
        txid = self._algo.send_note_tx(self._mnemonic, note_text)
        return AnchorResult(txid=txid, explorer_url=explorer_url_for(txid, self._network), verdict_hash=h, network=self._network)

    def verify_verdict(self, verdict: Union[ComplianceVerdict, Dict[str, Any]], txid: str) -> bool:
        v = verdict if isinstance(verdict, ComplianceVerdict) else ComplianceVerdict(**verdict)
        h = verdict_hash(v)
        nt = self._algo.get_note_text(txid) or ""
        return nt.strip() == f"CLG1|sha256:{h}"
    
    @classmethod
    def from_env(cls, config: Optional[AlgoConfig] = None) -> "CompliLedgerClient":
        """
        Create a CompliLedgerClient from .env file or environment variables.
        
        Args:
            config: Optional AlgoConfig instance. If None, loads from .env/environment.
            
        Returns:
            CompliLedgerClient instance
            
        Raises:
            ValueError: If required configuration is missing
            
        Example:
            # Load from .env file
            client = CompliLedgerClient.from_env()
            
            # Or with explicit config
            cfg = AlgoConfig.from_env()
            client = CompliLedgerClient.from_env(cfg)
        """
        if config is None:
            config = AlgoConfig.from_env()
        
        config.validate(require_mnemonic=True)
        
        return cls(
            algod_url=config.algod_url,
            algod_token=config.algod_token,
            sender_mnemonic=config.mnemonic,
            network=config.network,
            indexer_url=config.indexer_url,
            indexer_token=config.indexer_token,
        )
