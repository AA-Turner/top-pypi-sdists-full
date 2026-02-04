"""Type stubs for hfortix_fortios.transaction module."""

from __future__ import annotations

from typing import Any, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_fortios.client import FortiOS

class TransactionError(Exception):
    """Exception raised for transaction-related errors."""
    ...

class Transaction:
    """FortiOS batch transaction manager.
    
    Provides atomic configuration changes with commit/rollback support.
    """
    
    def __init__(
        self,
        client: FortiOS,
        timeout: int = 60,
        vdom: Optional[str] = None,
        auto_commit: bool = True,
        auto_abort: bool = True,
    ) -> None:
        """Initialize transaction.
        
        Args:
            client: FortiOS client instance
            timeout: Transaction timeout in seconds (default: 60)
            vdom: VDOM for transaction (default: client's VDOM)
            auto_commit: Auto-commit on successful exit (default: True)
            auto_abort: Auto-abort on exception (default: True)
        """
        ...
    
    @property
    def transaction_id(self) -> Optional[int]:
        """Get the transaction ID."""
        ...
    
    @property
    def is_active(self) -> bool:
        """Check if transaction is active."""
        ...
    
    @property
    def is_committed(self) -> bool:
        """Check if transaction has been committed."""
        ...
    
    @property
    def is_aborted(self) -> bool:
        """Check if transaction has been aborted."""
        ...
    
    def start(self) -> int:
        """Start the transaction.
        
        Returns:
            Transaction ID
            
        Raises:
            TransactionError: If another transaction is already active
        """
        ...
    
    def commit(self) -> dict[str, Any]:
        """Commit all cached changes.
        
        Returns:
            API response
            
        Raises:
            TransactionError: If transaction is not active
        """
        ...
    
    def abort(self) -> dict[str, Any]:
        """Abort and rollback all changes.
        
        Returns:
            API response
            
        Raises:
            TransactionError: If transaction is not active
        """
        ...
    
    def rollback(self) -> dict[str, Any]:
        """Alias for abort(). Rollback all changes.
        
        Returns:
            API response
            
        Raises:
            TransactionError: If transaction is not active
        """
        ...
    
    def show(self) -> dict[str, Any]:
        """Show cached commands (FortiOS 7.4.1+).
        
        Returns:
            API response with cached commands
            
        Raises:
            TransactionError: If transaction is not active
        """
        ...
    
    def __enter__(self) -> Transaction:
        """Context manager entry."""
        ...
    
    def __exit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Any,
    ) -> None:
        """Context manager exit."""
        ...
