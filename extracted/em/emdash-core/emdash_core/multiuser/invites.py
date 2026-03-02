"""Invite code generation and management for multiuser sessions.

This module handles creating, validating, and managing invite codes
that allow users to join shared sessions.
"""

import json
import logging
import random
import string
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

from .models import InviteToken
from .protocols import InvalidInviteCodeError

log = logging.getLogger(__name__)

# Characters for invite codes (avoiding ambiguous: 0/O, 1/I/l)
INVITE_CHARS = "ABCDEFGHJKMNPQRSTUVWXYZ23456789"


def generate_invite_code(length: int = 6) -> str:
    """Generate a human-readable invite code.

    The code uses characters that are easy to read and type,
    avoiding ambiguous characters like 0/O, 1/I/l.

    Args:
        length: Length of the code (default 6)

    Returns:
        A random invite code like "ABC123"
    """
    return "".join(random.choice(INVITE_CHARS) for _ in range(length))


def normalize_invite_code(code: str) -> str:
    """Normalize an invite code for comparison.

    Handles common input variations like lowercase, extra spaces.

    Args:
        code: The raw invite code input

    Returns:
        Normalized uppercase code with no spaces
    """
    return code.strip().upper().replace(" ", "").replace("-", "")


class InviteManager:
    """Manages invite codes for shared sessions.

    Handles creation, validation, and tracking of invite codes
    with optional persistence.

    Usage:
        manager = InviteManager(storage_path)

        # Create invite
        token = manager.create_invite(session_id, owner_id)
        print(f"Share this code: {token.code}")

        # Validate and use
        session_id = manager.use_invite(code, user_id)
    """

    def __init__(
        self,
        storage_path: Optional[Path] = None,
        default_expiry_hours: int = 24,
        default_max_uses: int = 10,
    ):
        """Initialize the invite manager.

        Args:
            storage_path: Optional path for persisting invites
            default_expiry_hours: Default hours until invite expires
            default_max_uses: Default maximum uses per invite
        """
        self._storage_path = storage_path
        self._default_expiry_hours = default_expiry_hours
        self._default_max_uses = default_max_uses

        # In-memory store: code -> InviteToken
        self._invites: dict[str, InviteToken] = {}

        # Load from storage if exists
        if storage_path and storage_path.exists():
            self._load()

    def create_invite(
        self,
        session_id: str,
        created_by: str,
        expiry_hours: Optional[int] = None,
        max_uses: Optional[int] = None,
        code_length: int = 6,
    ) -> InviteToken:
        """Create a new invite code for a session.

        Args:
            session_id: Session to invite to
            created_by: User ID creating the invite
            expiry_hours: Hours until expiry (default from init)
            max_uses: Maximum uses (default from init)
            code_length: Length of the code

        Returns:
            The created InviteToken
        """
        # Generate unique code
        code = generate_invite_code(code_length)
        while code in self._invites:
            code = generate_invite_code(code_length)

        now = datetime.utcnow()
        expires_at = now + timedelta(hours=expiry_hours or self._default_expiry_hours)

        token = InviteToken(
            code=code,
            session_id=session_id,
            created_by=created_by,
            created_at=now.isoformat(),
            expires_at=expires_at.isoformat(),
            max_uses=max_uses or self._default_max_uses,
            use_count=0,
        )

        self._invites[code] = token
        self._persist()

        log.info(f"Created invite {code} for session {session_id}")
        return token

    def validate_invite(self, code: str) -> InviteToken:
        """Validate an invite code.

        Args:
            code: The invite code to validate

        Returns:
            The InviteToken if valid

        Raises:
            InvalidInviteCodeError: If code is invalid or expired
        """
        code = normalize_invite_code(code)

        token = self._invites.get(code)
        if not token:
            raise InvalidInviteCodeError(f"Invite code '{code}' not found")

        if not token.is_valid():
            if token.use_count >= token.max_uses:
                raise InvalidInviteCodeError(
                    f"Invite code '{code}' has reached maximum uses"
                )
            else:
                raise InvalidInviteCodeError(f"Invite code '{code}' has expired")

        return token

    def use_invite(self, code: str, user_id: str) -> str:
        """Use an invite code to join a session.

        Validates the code and increments its use count.

        Args:
            code: The invite code
            user_id: User attempting to join

        Returns:
            The session_id to join

        Raises:
            InvalidInviteCodeError: If code is invalid or expired
        """
        token = self.validate_invite(code)

        # Increment use count
        if not token.use():
            raise InvalidInviteCodeError(f"Invite code '{code}' could not be used")

        self._persist()

        log.info(f"User {user_id} used invite {token.code} for session {token.session_id}")
        return token.session_id

    def get_invite(self, code: str) -> Optional[InviteToken]:
        """Get an invite token by code.

        Args:
            code: The invite code

        Returns:
            The InviteToken if found, None otherwise
        """
        code = normalize_invite_code(code)
        return self._invites.get(code)

    def get_session_invites(self, session_id: str) -> list[InviteToken]:
        """Get all invites for a session.

        Args:
            session_id: Session to get invites for

        Returns:
            List of invite tokens for the session
        """
        return [
            token
            for token in self._invites.values()
            if token.session_id == session_id
        ]

    def revoke_invite(self, code: str) -> bool:
        """Revoke an invite code.

        Args:
            code: The invite code to revoke

        Returns:
            True if revoked, False if not found
        """
        code = normalize_invite_code(code)
        if code in self._invites:
            del self._invites[code]
            self._persist()
            log.info(f"Revoked invite {code}")
            return True
        return False

    def revoke_session_invites(self, session_id: str) -> int:
        """Revoke all invites for a session.

        Args:
            session_id: Session to revoke invites for

        Returns:
            Number of invites revoked
        """
        to_revoke = [
            code
            for code, token in self._invites.items()
            if token.session_id == session_id
        ]

        for code in to_revoke:
            del self._invites[code]

        if to_revoke:
            self._persist()
            log.info(f"Revoked {len(to_revoke)} invites for session {session_id}")

        return len(to_revoke)

    def cleanup_expired(self) -> int:
        """Remove expired invites.

        Returns:
            Number of invites removed
        """
        now = datetime.utcnow().isoformat()
        to_remove = [
            code
            for code, token in self._invites.items()
            if token.expires_at < now
        ]

        for code in to_remove:
            del self._invites[code]

        if to_remove:
            self._persist()
            log.info(f"Cleaned up {len(to_remove)} expired invites")

        return len(to_remove)

    def _persist(self) -> None:
        """Persist invites to storage."""
        if not self._storage_path:
            return

        try:
            self._storage_path.parent.mkdir(parents=True, exist_ok=True)
            data = {
                code: token.to_dict()
                for code, token in self._invites.items()
            }
            self._storage_path.write_text(json.dumps(data, indent=2))
        except Exception as e:
            log.warning(f"Failed to persist invites: {e}")

    def _load(self) -> None:
        """Load invites from storage."""
        if not self._storage_path or not self._storage_path.exists():
            return

        try:
            data = json.loads(self._storage_path.read_text())
            self._invites = {
                code: InviteToken.from_dict(token_data)
                for code, token_data in data.items()
            }
            log.debug(f"Loaded {len(self._invites)} invites")
        except Exception as e:
            log.warning(f"Failed to load invites: {e}")


# Global invite manager instance (lazily initialized)
_global_invite_manager: Optional[InviteManager] = None


def get_invite_manager(storage_path: Optional[Path] = None) -> InviteManager:
    """Get the global invite manager.

    Args:
        storage_path: Optional storage path (only used on first call)

    Returns:
        The global InviteManager instance
    """
    global _global_invite_manager
    if _global_invite_manager is None:
        _global_invite_manager = InviteManager(storage_path)
    return _global_invite_manager


def set_invite_manager(manager: InviteManager) -> None:
    """Set the global invite manager.

    Args:
        manager: The InviteManager to use globally
    """
    global _global_invite_manager
    _global_invite_manager = manager
