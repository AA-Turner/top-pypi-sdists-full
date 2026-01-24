"""
Algorand Indexer integration for historical transaction verification

Extends the basic algod-based verification to support querying older transactions
that are no longer in the pending transaction pool.
"""
from __future__ import annotations

import base64
from typing import Optional
from algosdk.v2client import indexer


class IndexerClient:
    """
    Wrapper for Algorand Indexer API to query historical transactions
    """
    
    def __init__(self, indexer_url: str, indexer_token: str = ""):
        """
        Initialize Indexer client
        
        Args:
            indexer_url: URL of Algorand Indexer API
            indexer_token: Optional API token
        """
        self.indexer = indexer.IndexerClient(indexer_token, indexer_url)
    
    def get_transaction(self, txid: str) -> Optional[dict]:
        """
        Get transaction details by TXID
        
        Args:
            txid: Transaction ID to lookup
            
        Returns:
            Transaction dict or None if not found
        """
        try:
            response = self.indexer.transaction(txid)
            return response.get("transaction")
        except Exception as e:
            # Transaction not found or other error
            return None
    
    def get_note_from_transaction(self, txid: str) -> Optional[str]:
        """
        Extract note field from a transaction
        
        Args:
            txid: Transaction ID
            
        Returns:
            Decoded note text or None
        """
        tx = self.get_transaction(txid)
        if not tx:
            return None
        
        # Note is base64 encoded in the transaction
        note_b64 = tx.get("note")
        if not note_b64:
            return None
        
        try:
            raw = base64.b64decode(note_b64)
            return raw.decode("utf-8", errors="ignore")
        except Exception:
            return None
    
    def search_transactions_by_note(
        self,
        note_prefix: str,
        limit: int = 10,
        next_token: Optional[str] = None
    ) -> dict:
        """
        Search for transactions with a specific note prefix
        
        Args:
            note_prefix: Prefix to search for (e.g., "CLG1")
            limit: Max results to return
            next_token: Pagination token
            
        Returns:
            Response dict with transactions and next token
        """
        # Encode note prefix to base64
        note_b64 = base64.b64encode(note_prefix.encode()).decode()
        
        params = {
            "limit": limit,
            "note-prefix": note_b64,
        }
        if next_token:
            params["next"] = next_token
        
        try:
            response = self.indexer.search_transactions(**params)
            return {
                "transactions": response.get("transactions", []),
                "next_token": response.get("next-token"),
            }
        except Exception as e:
            return {"transactions": [], "next_token": None}
    
    def get_account_transactions(
        self,
        address: str,
        limit: int = 10,
        next_token: Optional[str] = None
    ) -> dict:
        """
        Get transactions for a specific account
        
        Args:
            address: Algorand address
            limit: Max results
            next_token: Pagination token
            
        Returns:
            Response dict with transactions
        """
        try:
            response = self.indexer.search_transactions_by_address(
                address=address,
                limit=limit,
                next_page=next_token
            )
            return {
                "transactions": response.get("transactions", []),
                "next_token": response.get("next-token"),
            }
        except Exception:
            return {"transactions": [], "next_token": None}
