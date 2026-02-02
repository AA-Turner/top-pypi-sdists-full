"""
SQLite-based storage backend with WAL mode.
Replaces JSON file storage with a single database for better performance and concurrency.
"""

import aiosqlite
import json
from pathlib import Path
from typing import Optional, Dict, List, Set
from datetime import datetime
from .base_storage import BaseStorageBackend


class SqliteStorageBackend(BaseStorageBackend):
    """SQLite database storage backend with WAL mode enabled"""
    
    def __init__(self, db_path: str = "./data/securex.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialized = False
    
    async def _get_connection(self) -> aiosqlite.Connection:
        """Get a database connection and ensure initialization"""
        conn = await aiosqlite.connect(self.db_path)
        
        if not self._initialized:
            await self._initialize_db(conn)
            self._initialized = True
        
        return conn
    
    async def _initialize_db(self, conn: aiosqlite.Connection) -> None:
        """Initialize database schema and enable WAL mode"""
        # Enable WAL mode for better concurrency
        await conn.execute("PRAGMA journal_mode=WAL")
        await conn.execute("PRAGMA synchronous=NORMAL")
        
        # Create tables
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS channel_backups (
                guild_id INTEGER PRIMARY KEY,
                backup_data TEXT NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS role_backups (
                guild_id INTEGER PRIMARY KEY,
                backup_data TEXT NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS guild_settings (
                guild_id INTEGER PRIMARY KEY,
                settings_data TEXT NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS whitelists (
                guild_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (guild_id, user_id)
            )
        """)
        
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS user_tokens (
                guild_id INTEGER PRIMARY KEY,
                token TEXT NOT NULL,
                set_by INTEGER,
                description TEXT,
                last_used TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        await conn.execute("""
            CREATE TABLE IF NOT EXISTS guild_punishments (
                guild_id INTEGER NOT NULL,
                violation_type TEXT NOT NULL,
                action TEXT NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (guild_id, violation_type)
            )
        """)
        
        # Create indexes for better query performance
        await conn.execute("CREATE INDEX IF NOT EXISTS idx_whitelist_guild ON whitelists(guild_id)")
        await conn.execute("CREATE INDEX IF NOT EXISTS idx_whitelist_user ON whitelists(user_id)")
        
        await conn.commit()
        print(f"✅ SQLite database initialized at {self.db_path} with WAL mode enabled")
    
    # ===== Backup Operations =====
    
    async def save_channel_backup(self, guild_id: int, backup_data: dict) -> None:
        """Save channel backup to database"""
        conn = await self._get_connection()
        try:
            await conn.execute(
                """
                INSERT OR REPLACE INTO channel_backups (guild_id, backup_data, updated_at)
                VALUES (?, ?, ?)
                """,
                (guild_id, json.dumps(backup_data), datetime.now().isoformat())
            )
            await conn.commit()
        finally:
            await conn.close()
    
    async def load_channel_backup(self, guild_id: int) -> Optional[dict]:
        """Load channel backup from database"""
        conn = await self._get_connection()
        try:
            async with conn.execute(
                "SELECT backup_data FROM channel_backups WHERE guild_id = ?",
                (guild_id,)
            ) as cursor:
                row = await cursor.fetchone()
                return json.loads(row[0]) if row else None
        finally:
            await conn.close()
    
    async def save_role_backup(self, guild_id: int, backup_data: dict) -> None:
        """Save role backup to database"""
        conn = await self._get_connection()
        try:
            await conn.execute(
                """
                INSERT OR REPLACE INTO role_backups (guild_id, backup_data, updated_at)
                VALUES (?, ?, ?)
                """,
                (guild_id, json.dumps(backup_data), datetime.now().isoformat())
            )
            await conn.commit()
        finally:
            await conn.close()
    
    async def load_role_backup(self, guild_id: int) -> Optional[dict]:
        """Load role backup from database"""
        conn = await self._get_connection()
        try:
            async with conn.execute(
                "SELECT backup_data FROM role_backups WHERE guild_id = ?",
                (guild_id,)
            ) as cursor:
                row = await cursor.fetchone()
                return json.loads(row[0]) if row else None
        finally:
            await conn.close()
    
    async def save_guild_settings(self, guild_id: int, settings_data: dict) -> None:
        """Save guild settings to database"""
        conn = await self._get_connection()
        try:
            await conn.execute(
                """
                INSERT OR REPLACE INTO guild_settings (guild_id, settings_data, updated_at)
                VALUES (?, ?, ?)
                """,
                (guild_id, json.dumps(settings_data), datetime.now().isoformat())
            )
            await conn.commit()
        finally:
            await conn.close()
    
    async def load_guild_settings(self, guild_id: int) -> Optional[dict]:
        """Load guild settings from database"""
        conn = await self._get_connection()
        try:
            async with conn.execute(
                "SELECT settings_data FROM guild_settings WHERE guild_id = ?",
                (guild_id,)
            ) as cursor:
                row = await cursor.fetchone()
                return json.loads(row[0]) if row else None
        finally:
            await conn.close()
    
    async def load_all_guild_settings(self) -> Dict[int, dict]:
        """Load all guild settings from database"""
        conn = await self._get_connection()
        try:
            async with conn.execute("SELECT guild_id, settings_data FROM guild_settings") as cursor:
                rows = await cursor.fetchall()
                return {row[0]: json.loads(row[1]) for row in rows}
        finally:
            await conn.close()
    
    async def save_all_guild_settings(self, all_settings: Dict[int, dict]) -> None:
        """Save all guild settings to database"""
        conn = await self._get_connection()
        try:
            for guild_id, settings_data in all_settings.items():
                await conn.execute(
                    """
                    INSERT OR REPLACE INTO guild_settings (guild_id, settings_data, updated_at)
                    VALUES (?, ?, ?)
                    """,
                    (guild_id, json.dumps(settings_data), datetime.now().isoformat())
                )
            await conn.commit()
        finally:
            await conn.close()
    
    # ===== Whitelist Operations =====
    
    async def add_whitelist_user(self, guild_id: int, user_id: int) -> None:
        """Add user to whitelist"""
        conn = await self._get_connection()
        try:
            await conn.execute(
                """
                INSERT OR IGNORE INTO whitelists (guild_id, user_id, added_at)
                VALUES (?, ?, ?)
                """,
                (guild_id, user_id, datetime.now().isoformat())
            )
            await conn.commit()
        finally:
            await conn.close()
    
    async def remove_whitelist_user(self, guild_id: int, user_id: int) -> None:
        """Remove user from whitelist"""
        conn = await self._get_connection()
        try:
            await conn.execute(
                "DELETE FROM whitelists WHERE guild_id = ? AND user_id = ?",
                (guild_id, user_id)
            )
            await conn.commit()
        finally:
            await conn.close()
    
    async def get_whitelist_users(self, guild_id: int) -> Set[int]:
        """Get all whitelisted users for a guild"""
        conn = await self._get_connection()
        try:
            async with conn.execute(
                "SELECT user_id FROM whitelists WHERE guild_id = ?",
                (guild_id,)
            ) as cursor:
                rows = await cursor.fetchall()
                return {row[0] for row in rows}
        finally:
            await conn.close()
    
    async def is_whitelisted(self, guild_id: int, user_id: int) -> bool:
        """Check if user is whitelisted"""
        conn = await self._get_connection()
        try:
            async with conn.execute(
                "SELECT 1 FROM whitelists WHERE guild_id = ? AND user_id = ?",
                (guild_id, user_id)
            ) as cursor:
                row = await cursor.fetchone()
                return row is not None
        finally:
            await conn.close()
    
    async def clear_whitelist(self, guild_id: int) -> None:
        """Clear all whitelisted users for a guild"""
        conn = await self._get_connection()
        try:
            await conn.execute(
                "DELETE FROM whitelists WHERE guild_id = ?",
                (guild_id,)
            )
            await conn.commit()
        finally:
            await conn.close()
    
    async def load_all_whitelists(self) -> Dict[int, Set[int]]:
        """Load all whitelists at once"""
        conn = await self._get_connection()
        try:
            async with conn.execute("SELECT guild_id, user_id FROM whitelists") as cursor:
                rows = await cursor.fetchall()
                whitelists: Dict[int, Set[int]] = {}
                for guild_id, user_id in rows:
                    if guild_id not in whitelists:
                        whitelists[guild_id] = set()
                    whitelists[guild_id].add(user_id)
                return whitelists
        finally:
            await conn.close()

    # ===== Punishment Config Operations =====

    async def save_punishment(self, guild_id: int, violation_type: str, action: str) -> None:
        """Save specific punishment rule for a guild"""
        conn = await self._get_connection()
        try:
            await conn.execute(
                """
                INSERT OR REPLACE INTO guild_punishments 
                (guild_id, violation_type, action, updated_at)
                VALUES (?, ?, ?, ?)
                """,
                (guild_id, violation_type, action, datetime.now().isoformat())
            )
            await conn.commit()
        finally:
            await conn.close()

    async def load_punishment_config(self, guild_id: int) -> Dict[str, str]:
        """Load all punishment rules for a guild"""
        conn = await self._get_connection()
        try:
            async with conn.execute(
                "SELECT violation_type, action FROM guild_punishments WHERE guild_id = ?",
                (guild_id,)
            ) as cursor:
                rows = await cursor.fetchall()
                return {row[0]: row[1] for row in rows}
        finally:
            await conn.close()

    async def load_all_punishment_configs(self) -> Dict[int, Dict[str, str]]:
        """Load all punishment configs for all guilds"""
        conn = await self._get_connection()
        try:
            async with conn.execute("SELECT guild_id, violation_type, action FROM guild_punishments") as cursor:
                rows = await cursor.fetchall()
                configs: Dict[int, Dict[str, str]] = {}
                for guild_id, v_type, action in rows:
                    if guild_id not in configs:
                        configs[guild_id] = {}
                    configs[guild_id][v_type] = action
                return configs
        finally:
            await conn.close()
    
    # ===== User Token Operations =====
    
    async def save_user_token(self, guild_id: int, token: str, set_by: Optional[int] = None,
                            description: Optional[str] = None) -> None:
        """Save user token for a guild"""
        conn = await self._get_connection()
        try:
            await conn.execute(
                """
                INSERT OR REPLACE INTO user_tokens 
                (guild_id, token, set_by, description, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (guild_id, token, set_by, description, datetime.now().isoformat())
            )
            await conn.commit()
        finally:
            await conn.close()
    
    async def load_user_token(self, guild_id: int) -> Optional[dict]:
        """Load user token for a guild"""
        conn = await self._get_connection()
        try:
            async with conn.execute(
                """
                SELECT token, set_by, description, last_used, created_at 
                FROM user_tokens WHERE guild_id = ?
                """,
                (guild_id,)
            ) as cursor:
                row = await cursor.fetchone()
                if row:
                    return {
                        'token': row[0],
                        'set_by': row[1],
                        'description': row[2],
                        'last_used': row[3],
                        'created_at': row[4]
                    }
                return None
        finally:
            await conn.close()
    
    async def update_token_last_used(self, guild_id: int) -> None:
        """Update last_used timestamp for a token"""
        conn = await self._get_connection()
        try:
            await conn.execute(
                "UPDATE user_tokens SET last_used = ? WHERE guild_id = ?",
                (datetime.now().isoformat(), guild_id)
            )
            await conn.commit()
        finally:
            await conn.close()
    
    async def load_all_user_tokens(self) -> Dict[int, dict]:
        """Load all user tokens at once"""
        conn = await self._get_connection()
        try:
            async with conn.execute(
                "SELECT guild_id, token, set_by, description, last_used, created_at FROM user_tokens"
            ) as cursor:
                rows = await cursor.fetchall()
                return {
                    row[0]: {
                        'token': row[1],
                        'set_by': row[2],
                        'description': row[3],
                        'last_used': row[4],
                        'created_at': row[5]
                    }
                    for row in rows
                }
        finally:
            await conn.close()
