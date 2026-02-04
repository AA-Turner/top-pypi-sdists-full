"""
FortiOS Batch Transaction Support.

Provides atomic multi-request operations with automatic commit/rollback.
Available in FortiOS 6.4.0+.

Examples:
    >>> # Automatic mode - commits on success, aborts on error
    >>> with fgt.transaction() as txn:
    ...     fgt.api.cmdb.system.interface.post(name="vlan10", vlanid=10, ...)
    ...     fgt.api.cmdb.firewall.policy.post(srcintf=[{"name": "vlan10"}], ...)
    
    >>> # Review before commit
    >>> with fgt.transaction(auto_commit=False) as txn:
    ...     fgt.api.cmdb.system.interface.post(...)
    ...     cached = txn.show()  # Inspect cached commands
    ...     if confirm(cached):
    ...         txn.commit()
    ...     else:
    ...         txn.abort()
    
    >>> # Decorator for reusable patterns
    >>> @fgt.transactional(timeout=120)
    ... def setup_network():
    ...     fgt.api.cmdb.system.interface.post(...)
    ...     fgt.api.cmdb.firewall.policy.post(...)
    ...     return result
    >>> result = setup_network()
"""

from __future__ import annotations

import warnings
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .client import FortiOS

from hfortix_core.exceptions import APIError


class TransactionError(APIError):
    """Exception raised for transaction-related errors."""
    
    def __init__(self, message: str, transaction_id: int | None = None):
        super().__init__(message)
        self.transaction_id = transaction_id


class Transaction:
    """
    FortiOS batch transaction manager.
    
    Supports atomic multi-request operations with automatic commit/abort.
    Available in FortiOS 6.4.0+.
    
    Transaction changes are cached and not applied until committed.
    Use abort() to rollback all changes.
    
    Attributes:
        transaction_id: Unique transaction ID assigned by FortiOS
        is_active: Whether transaction is currently active
        is_committed: Whether transaction has been committed
        is_aborted: Whether transaction has been aborted
    
    Examples:
        >>> # Automatic mode (default)
        >>> with fgt.transaction() as txn:
        ...     fgt.api.cmdb.system.interface.post(name="vlan10", ...)
        ...     fgt.api.cmdb.firewall.policy.post(srcintf=[{"name": "vlan10"}], ...)
        ... # Auto-commits on success, auto-aborts on exception
        
        >>> # Review before commit
        >>> with fgt.transaction(auto_commit=False) as txn:
        ...     fgt.api.cmdb.system.interface.post(...)
        ...     cached = txn.show()  # Inspect what will be committed
        ...     if confirm(cached):
        ...         txn.commit()
        ...     else:
        ...         txn.abort()
        
        >>> # Manual error handling
        >>> with fgt.transaction(auto_abort=False) as txn:
        ...     try:
        ...         fgt.api.cmdb.system.interface.post(...)
        ...     except Exception as e:
        ...         log_error(e)
        ...         txn.abort()
    
    Note:
        - Multiple transactions can run simultaneously if they don't modify same tables
        - Nested transactions are not supported
        - Transactions expire after timeout if not committed
        - Some tables may not support transactions
    """
    
    def __init__(
        self,
        client: FortiOS,
        timeout: int = 60,
        vdom: str | None = None,
        auto_commit: bool = True,
        auto_abort: bool = True,
    ):
        """
        Initialize transaction.
        
        Args:
            client: FortiOS client instance
            timeout: Transaction timeout in seconds (default 60)
            vdom: VDOM for transaction (uses client default if None)
            auto_commit: Auto-commit on context exit if no errors (default True)
            auto_abort: Auto-abort on exception (default True)
        """
        self._client = client
        self._timeout = timeout
        self._vdom = vdom or getattr(client, '_vdom', 'root')
        self._auto_commit = auto_commit
        self._auto_abort = auto_abort
        
        self._transaction_id: int | None = None
        self._committed = False
        self._aborted = False
        self._started = False
    
    @property
    def transaction_id(self) -> int | None:
        """Get transaction ID."""
        return self._transaction_id
    
    @property
    def is_active(self) -> bool:
        """Check if transaction is active (started but not committed/aborted)."""
        return self._started and not self._committed and not self._aborted
    
    @property
    def is_committed(self) -> bool:
        """Check if transaction has been committed."""
        return self._committed
    
    @property
    def is_aborted(self) -> bool:
        """Check if transaction has been aborted."""
        return self._aborted
    
    def start(self) -> int:
        """
        Start transaction.
        
        Returns:
            Transaction ID assigned by FortiOS
            
        Raises:
            TransactionError: If transaction already started or client has active transaction
            
        Examples:
            >>> txn = fgt.transaction(auto_commit=False, auto_abort=False)
            >>> txn.start()
            >>> # ... make requests ...
            >>> txn.commit()
        """
        if self._started:
            raise TransactionError(
                "Transaction already started",
                transaction_id=self._transaction_id
            )
        
        # Check if client has another active transaction
        if hasattr(self._client, '_active_transaction'):  # type: ignore[attr-defined]
            active_txn = self._client._active_transaction  # type: ignore[attr-defined]
            if active_txn is not None and active_txn is not self:
                active_id = active_txn.transaction_id
                raise TransactionError(
                    f"Client already has an active transaction (ID: {active_id}). "
                    "Nested transactions are not supported by FortiOS.",
                    transaction_id=active_id
                )
        
        # POST /api/v2/cmdb?action=transaction-start
        response = self._client._client.post(  # type: ignore[attr-defined]
            api_type='cmdb',
            path='',
            params={
                'action': 'transaction-start',
                'vdom': self._vdom
            },
            data={'timeout': self._timeout},
            raw_json=True,
        )
        
        # Extract transaction ID from response
        # Response format: {"results": {"transaction_id": 12345}, "vdom": "root", "path": "cmdb", ...}
        if not isinstance(response, dict):
            raise TransactionError(
                f"Invalid response type from transaction-start: {type(response)}",
                transaction_id=None
            )
        
        if 'results' not in response:
            raise TransactionError(
                f"Missing 'results' in transaction-start response. Got: {response}",
                transaction_id=None
            )
        
        # FortiOS returns transaction_id with underscore, not hyphen
        results = response['results']
        if 'transaction_id' in results:
            self._transaction_id = results['transaction_id']
        elif 'transaction-id' in results:
            self._transaction_id = results['transaction-id']
        else:
            raise TransactionError(
                f"Missing 'transaction_id' in results. Got: {results}",
                transaction_id=None
            )
        
        self._started = True
        
        # Set transaction on HTTP client so all requests use it
        self._client._client.set_transaction(self._transaction_id)  # type: ignore[attr-defined]
        self._client._active_transaction = self  # type: ignore[attr-defined]
        
        return self._transaction_id  # type: ignore[return-value]
    
    def show(self) -> dict[str, Any]:
        """
        Show cached commands (FortiOS 7.4.1+).
        
        Returns cached configuration commands that will be applied when committed.
        Useful for reviewing changes before committing.
        
        Returns:
            Dictionary with cached configuration commands
            
        Raises:
            TransactionError: If transaction not started or already committed/aborted
            
        Examples:
            >>> with fgt.transaction(auto_commit=False) as txn:
            ...     fgt.api.cmdb.system.interface.post(name="vlan10", ...)
            ...     
            ...     # Review what will be committed
            ...     cached = txn.show()
            ...     print(cached['results'])  # List of CLI commands
            ...     
            ...     if user_approves(cached):
            ...         txn.commit()
        """
        if not self.is_active:
            raise TransactionError(
                "No active transaction to show",
                transaction_id=self._transaction_id
            )
        
        # GET /api/v2/cmdb?action=transaction-show&transaction_id=X
        response = self._client._client.get(  # type: ignore[attr-defined]
            api_type='cmdb',
            path='',
            params={
                'action': 'transaction-show',
                'transaction_id': self._transaction_id
            },
            raw_json=True,
        )
        
        return response
    
    def commit(self) -> dict[str, Any]:
        """
        Commit transaction and apply all cached changes.
        
        All requests made within the transaction will be applied atomically.
        
        Returns:
            API response from commit operation
            
        Raises:
            TransactionError: If transaction not active or already committed
            
        Examples:
            >>> with fgt.transaction(auto_commit=False) as txn:
            ...     fgt.api.cmdb.system.interface.post(...)
            ...     fgt.api.cmdb.firewall.policy.post(...)
            ...     txn.commit()  # Explicitly commit
        """
        if not self.is_active:
            raise TransactionError(
                "No active transaction to commit",
                transaction_id=self._transaction_id
            )
        
        if self._committed:
            raise TransactionError(
                "Transaction already committed",
                transaction_id=self._transaction_id
            )
        
        # POST /api/v2/cmdb?action=transaction-commit
        response = self._client._client.post(  # type: ignore[attr-defined]
            api_type='cmdb',
            path='',
            params={
                'action': 'transaction-commit',
                'vdom': self._vdom
            },
            data={'transaction_id': self._transaction_id},
            raw_json=True,
        )
        
        self._committed = True
        self._cleanup()
        
        return response
    
    def abort(self) -> dict[str, Any]:
        """
        Abort transaction and rollback all changes.
        
        All cached commands are discarded and no changes are applied.
        This is the FortiOS API term for rollback.
        
        Returns:
            API response from abort operation
            
        Raises:
            TransactionError: If transaction not started or already committed
            
        Examples:
            >>> with fgt.transaction(auto_commit=False) as txn:
            ...     fgt.api.cmdb.system.interface.post(...)
            ...     
            ...     if something_wrong():
            ...         txn.abort()  # Rollback all changes
        """
        if not self._started:
            raise TransactionError(
                "No transaction to abort",
                transaction_id=self._transaction_id
            )
        
        if self._aborted:
            return {"status": "success", "message": "Already aborted"}
        
        if self._committed:
            raise TransactionError(
                "Cannot abort - transaction already committed",
                transaction_id=self._transaction_id
            )
        
        # POST /api/v2/cmdb?action=transaction-abort
        response = self._client._client.post(  # type: ignore[attr-defined]
            api_type='cmdb',
            path='',
            params={
                'action': 'transaction-abort',
                'vdom': self._vdom
            },
            data={'transaction_id': self._transaction_id},
            raw_json=True,
        )
        
        self._aborted = True
        self._cleanup()
        
        return response
    
    def rollback(self) -> dict[str, Any]:
        """
        Alias for abort() - rollback all transaction changes.
        
        Provided for developer familiarity with database transaction terminology.
        Internally calls abort() which is the FortiOS API term.
        
        Returns:
            API response from abort operation
            
        Examples:
            >>> with fgt.transaction(auto_commit=False) as txn:
            ...     fgt.api.cmdb.system.interface.post(...)
            ...     txn.rollback()  # Same as txn.abort()
        """
        return self.abort()
    
    def _cleanup(self):
        """Clean up transaction state from client and HTTP client."""
        # Clear transaction from HTTP client
        if hasattr(self._client, '_client'):
            self._client._client.set_transaction(None)  # type: ignore[attr-defined]
        
        # Clear active transaction from client
        if hasattr(self._client, '_active_transaction'):
            self._client._active_transaction = None  # type: ignore[attr-defined]
    
    def __enter__(self):
        """Context manager entry - starts transaction."""
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Context manager exit.
        
        Behavior depends on auto_commit and auto_abort settings:
        - If no exception and auto_commit=True: commits transaction
        - If exception and auto_abort=True: aborts transaction
        - Otherwise: user must manually commit/abort
        """
        # No exception occurred
        if exc_type is None:
            if self._auto_commit and not self._committed and not self._aborted:
                try:
                    self.commit()
                except Exception as e:
                    # Commit failed - try to abort if auto_abort enabled
                    if self._auto_abort:
                        try:
                            self.abort()
                        except:
                            pass
                    raise
            elif not self._committed and not self._aborted:
                # auto_commit=False - user should have committed manually
                # Abort if auto_abort enabled, otherwise warn
                if self._auto_abort:
                    self.abort()
                else:
                    warnings.warn(
                        f"Transaction {self._transaction_id} was not committed or aborted. "
                        f"It will expire after {self._timeout} seconds.",
                        ResourceWarning,
                        stacklevel=2
                    )
        
        # Exception occurred
        else:
            if self._auto_abort and not self._aborted and not self._committed:
                try:
                    self.abort()
                except Exception as abort_error:
                    # Log abort error but don't suppress original exception
                    warnings.warn(
                        f"Failed to abort transaction {self._transaction_id}: {abort_error}",
                        RuntimeWarning,
                        stacklevel=2
                    )
        
        return False  # Don't suppress exceptions
    
    def __repr__(self):
        """String representation of transaction."""
        status = "active" if self.is_active else "inactive"
        if self._committed:
            status = "committed"
        elif self._aborted:
            status = "aborted"
        return f"<Transaction id={self._transaction_id} status={status} vdom={self._vdom}>"
