"""User repository for the auth service.

Handles user CRUD, credential verification, and role management.
This file is scaffolded once and never overwritten.
"""

import hashlib
import secrets
import uuid

from fastapi import HTTPException

from csrd.repository import BaseRepository

from ..models.users import UserResponse, UserRolesResponse


class UserRepository(BaseRepository):
    """User, credential, and role storage backed by a database adapter."""

    # ── User CRUD ────────────────────────────────────────────────────

    async def create_user(self, username: str, password: str) -> UserResponse:
        """Create a new user with hashed credentials. Raises 409 if exists.

        The very first user registered is automatically granted the
        ``ADMIN`` role so there is always at least one admin available
        to manage subsequent users.
        """
        existing = await self.get_user_by_username(username)
        if existing is not None:
            raise HTTPException(status_code=409, detail="Username already taken")

        # Check if this will be the first user (before inserting).
        count_row = await self.fetch_one("SELECT COUNT(*) AS cnt FROM users")
        is_first_user = count_row is not None and int(count_row["cnt"]) == 0

        user_id = str(uuid.uuid4())
        await self.execute(
            "INSERT INTO users (id, username) VALUES (:id, :username)",
            {"id": user_id, "username": username},
        )

        password_hash = self._hash_password(password)
        await self.execute(
            "INSERT INTO user_credentials (user_id, password_hash) "
            "VALUES (:user_id, :password_hash)",
            {"user_id": user_id, "password_hash": password_hash},
        )

        if is_first_user:
            await self.execute(
                "INSERT INTO user_roles (user_id, role) VALUES (:user_id, :role)",
                {"user_id": user_id, "role": "ADMIN"},
            )

        return UserResponse(id=user_id, username=username)

    async def get_user(self, user_id: str) -> UserResponse:
        """Get a user by ID. Raises 404 if not found."""
        return await self.require_one(
            "SELECT id, username FROM users WHERE id = :id",
            {"id": user_id},
            model=UserResponse,
            detail="User not found",
        )

    async def list_users(self) -> list[UserResponse]:
        """Return all users ordered by username."""
        rows = await self.fetch_all(
            "SELECT id, username FROM users ORDER BY username",
        )
        return [self.apply_model(row, model=UserResponse) for row in rows]

    async def get_user_by_username(self, username: str) -> UserResponse | None:
        """Get a user by username, or ``None`` if not found."""
        row = await self.fetch_one(
            "SELECT id, username FROM users WHERE username = :username",
            {"username": username},
        )
        if row is None:
            return None
        return self.apply_model(row, model=UserResponse)

    # ── Credential verification ──────────────────────────────────────

    async def verify_credentials(self, username: str, password: str) -> UserResponse:
        """Verify username + password. Raises 401 on failure."""
        user = await self.get_user_by_username(username)
        if user is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        cred = await self.fetch_one(
            "SELECT password_hash FROM user_credentials WHERE user_id = :user_id",
            {"user_id": user.id},
        )
        if cred is None or not self._verify_password(password, cred["password_hash"]):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        return user

    # ── Role management ──────────────────────────────────────────────

    async def get_user_roles(self, user_id: str) -> UserRolesResponse:
        """Get all roles for a user. Raises 404 if user not found."""
        await self.get_user(user_id)  # ensures user exists (raises 404)
        rows = await self.fetch_all(
            "SELECT role FROM user_roles WHERE user_id = :user_id",
            {"user_id": user_id},
        )
        roles = [row["role"] for row in rows]
        return UserRolesResponse(user_id=user_id, roles=roles)

    async def add_role(self, user_id: str, role: str) -> UserRolesResponse:
        """Add a role to a user. Idempotent. Returns updated roles."""
        await self.get_user(user_id)  # ensures user exists (raises 404)

        # Check-first for dialect-agnostic idempotency (works on
        # SQLite, PostgreSQL, and MariaDB without dialect-specific SQL).
        existing = await self.fetch_one(
            "SELECT 1 FROM user_roles WHERE user_id = :user_id AND role = :role",
            {"user_id": user_id, "role": role},
        )
        if existing is None:
            await self.execute(
                "INSERT INTO user_roles (user_id, role) VALUES (:user_id, :role)",
                {"user_id": user_id, "role": role},
            )
        return await self.get_user_roles(user_id)

    # ── Password hashing ─────────────────────────────────────────────
    #
    # Uses PBKDF2-SHA256 with random salt. For production, consider
    # switching to bcrypt or argon2 for better resistance to GPU attacks.

    @staticmethod
    def _hash_password(password: str) -> str:
        salt = secrets.token_hex(16)
        dk = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000)
        return f"{salt}${dk.hex()}"

    @staticmethod
    def _verify_password(password: str, stored_hash: str) -> bool:
        salt, hash_hex = stored_hash.split("$", 1)
        dk = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000)
        return dk.hex() == hash_hex


__all__ = ("UserRepository",)
