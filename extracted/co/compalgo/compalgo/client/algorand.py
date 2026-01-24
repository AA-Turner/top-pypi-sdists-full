from __future__ import annotations

import base64
from dataclasses import dataclass
from typing import Optional

from algosdk.v2client import algod
from algosdk import transaction, mnemonic, account


@dataclass
class AnchorResult:
    txid: str
    explorer_url: str
    verdict_hash: str
    network: str


def explorer_url_for(txid: str, network: str = "testnet") -> str:
    base = "https://testnet.algoexplorer.io/tx/" if network == "testnet" else "https://algoexplorer.io/tx/"
    return f"{base}{txid}"


class AlgorandClient:
    def __init__(
        self,
        algod_url: str,
        algod_token: str,
        network: str = "testnet",
        indexer_url: Optional[str] = None,
        indexer_token: str = ""
    ):
        self.algod = algod.AlgodClient(algod_token, algod_url)
        self.network = network
        self.indexer_client = None
        
        # Initialize indexer if URL provided
        if indexer_url:
            try:
                from .indexer import IndexerClient
                self.indexer_client = IndexerClient(indexer_url, indexer_token)
            except ImportError:
                pass  # Indexer not available

    def send_note_tx(self, sender_mnemonic: str, note_text: str) -> str:
        sender_sk = mnemonic.to_private_key(sender_mnemonic)
        sender_addr = account.address_from_private_key(sender_sk)
        params = self.algod.suggested_params()
        params.flat_fee = True
        params.fee = max(params.min_fee, 1000)
        txn = transaction.PaymentTxn(
            sender=sender_addr,
            sp=params,
            receiver=sender_addr,
            amt=0,
            note=note_text.encode("utf-8"),
        )
        signed = txn.sign(sender_sk)
        txid = self.algod.send_transaction(signed)
        transaction.wait_for_confirmation(self.algod, txid, 4)
        return txid

    def get_note_text(self, txid: str, use_indexer: bool = False) -> Optional[str]:
        """
        Get note text from a transaction
        
        Args:
            txid: Transaction ID
            use_indexer: Force use of Indexer instead of algod
            
        Returns:
            Decoded note text or None
        """
        # Try algod first (for recent transactions)
        if not use_indexer:
            try:
                info = self.algod.pending_transaction_info(txid)
                # note is base64 in different nesting levels depending on SDK version
                note_b64 = (
                    info.get("txn", {}).get("txn", {}).get("note")
                    or info.get("txn", {}).get("note")
                    or info.get("note")
                )
                if note_b64:
                    raw = base64.b64decode(note_b64)
                    return raw.decode("utf-8", errors="ignore")
            except Exception:
                pass  # Fall through to indexer
        
        # Fallback to indexer for historical transactions
        if self.indexer_client:
            try:
                return self.indexer_client.get_note_from_transaction(txid)
            except Exception:
                pass
        
        return None
