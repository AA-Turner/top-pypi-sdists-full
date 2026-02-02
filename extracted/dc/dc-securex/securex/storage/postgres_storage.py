"""
PostgreSQL storage backend with connection pooling and WAL-based concurrency.
Requires asyncpg: pip install dc-securex[postgres]
"""

try:
    import asyncpg
except ImportError:
    raise ImportError(
        "PostgreSQL backend requires asyncpg. "
        "Install with: pip install dc-securex[postgres]"
    )

import json
from datetime import datetime, timezone
from typing import Optional, Dict, Set
from .base_storage import BaseStorageBackend


class PostgresStorageBackend(BaseStorageBackend):
    """PostgreSQL storage with connection pooling and WAL optimization"""
    
    def __init__(
        self, 
        url: str,
        pool_size: int = 10,
        max_overflow: int = 20
    ):
        self.url = url
        self.pool = None
        
        # Connection pool settings
        self.min_pool_size = 5
        self.max_pool_size = pool_size
        self.max_overflow = max_overflow
        self.command_timeout = 60
    
    async def initialize(self):
        """Create connection pool and ensure schema exists"""
        print("🔄 Initializing PostgreSQL connection pool...")
        
        try:
            self.pool = await asyncpg.create_pool(
                self.url,
                min_size=self.min_pool_size,
                max_size=self.max_pool_size,
                max_queries=50000,  # Queries before connection reset
                max_inactive_connection_lifetime=300,  # 5 min idle timeout
                command_timeout=self.command_timeout,
                server_settings={
                    'jit': 'off',  # Disable JIT for faster small queries
                }
            )
            
            # Create schema if not exists
            await self._ensure_schema()
            
            print(f"✅ PostgreSQL pool ready ({self.min_pool_size}-{self.max_pool_size} connections)")
            
        except Exception as e:
            print(f"❌ Failed to initialize PostgreSQL: {e}")
            raise
    
    async def close(self):
        """Gracefully close connection pool"""
        if self.pool:
            await self.pool.close()
            print("✅ PostgreSQL connection pool closed")
    
    async def _ensure_schema(self):
        """Create tables and indexes if they don't exist"""
        async with self.pool.acquire() as conn:
            # Channel backups table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS channel_backups (
                    guild_id BIGINT PRIMARY KEY,
                    backup_data JSONB NOT NULL,
                    timestamp TIMESTAMPTZ DEFAULT NOW()
                )
            """)
            
            # Role backups table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS role_backups (
                    guild_id BIGINT PRIMARY KEY,
                    backup_data JSONB NOT NULL,
                    timestamp TIMESTAMPTZ DEFAULT NOW()
                )
            """)
            
            # Guild settings table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS guild_settings (
                    guild_id BIGINT PRIMARY KEY,
                    settings JSONB NOT NULL,
                    timestamp TIMESTAMPTZ DEFAULT NOW()
                )
            """)
            
            # Whitelists table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS whitelists (
                    guild_id BIGINT NOT NULL,
                    user_id BIGINT NOT NULL,
                    added_by BIGINT,
                    added_at TIMESTAMPTZ DEFAULT NOW(),
                    PRIMARY KEY (guild_id, user_id)
                )
            """)
            
            # User tokens table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS user_tokens (
                    guild_id BIGINT PRIMARY KEY,
                    token TEXT NOT NULL,
                    set_by BIGINT,
                    set_at TIMESTAMPTZ DEFAULT NOW(),
                    last_used TIMESTAMPTZ,
                    description TEXT
                )
            """)

            # Guild punishments table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS guild_punishments (
                    guild_id BIGINT NOT NULL,
                    violation_type TEXT NOT NULL,
                    action TEXT NOT NULL,
                    updated_at TIMESTAMPTZ DEFAULT NOW(),
                    PRIMARY KEY (guild_id, violation_type)
                )
            """)
            
            # Create indexes for performance
            await conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_channel_backup_timestamp 
                ON channel_backups(timestamp)
            """)
            
            await conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_channel_backup_data 
                ON channel_backups USING GIN(backup_data)
            """)
            
            await conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_role_backup_timestamp 
                ON role_backups(timestamp)
            """)
            
            await conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_role_backup_data 
                ON role_backups USING GIN(backup_data)
            """)
            
            await conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_whitelist_guild 
                ON whitelists(guild_id)
            """)
            
            await conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_whitelist_user 
                ON whitelists(user_id)
            """)
    
    # ===== Backup Operations =====
    
    async def save_channel_backup(self, guild_id: int, backup_data: dict) -> None:
        """Save channel backup with atomic UPSERT (non-blocking)"""
        async with self.pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO channel_backups (guild_id, backup_data, timestamp)
                VALUES ($1, $2, NOW())
                ON CONFLICT (guild_id) 
                DO UPDATE SET 
                    backup_data = EXCLUDED.backup_data,
                    timestamp = EXCLUDED.timestamp
            """, guild_id, json.dumps(backup_data))
    
    async def load_channel_backup(self, guild_id: int) -> Optional[dict]:
        """Load channel backup (never blocks on concurrent writes)"""
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT backup_data FROM channel_backups WHERE guild_id = $1",
                guild_id
            )
            if row:
                return json.loads(row['backup_data'])
            return None
    
    async def save_role_backup(self, guild_id: int, backup_data: dict) -> None:
        """Save role backup with atomic UPSERT"""
        async with self.pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO role_backups (guild_id, backup_data, timestamp)
                VALUES ($1, $2, NOW())
                ON CONFLICT (guild_id) 
                DO UPDATE SET 
                    backup_data = EXCLUDED.backup_data,
                    timestamp = EXCLUDED.timestamp
            """, guild_id, json.dumps(backup_data))
    
    async def load_role_backup(self, guild_id: int) -> Optional[dict]:
        """Load role backup"""
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT backup_data FROM role_backups WHERE guild_id = $1",
                guild_id
            )
            if row:
                return json.loads(row['backup_data'])
            return None
    
    async def save_guild_settings(self, guild_id: int, settings_data: dict) -> None:
        """Save guild settings with atomic UPSERT"""
        async with self.pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO guild_settings (guild_id, settings, timestamp)
                VALUES ($1, $2, NOW())
                ON CONFLICT (guild_id) 
                DO UPDATE SET 
                    settings = EXCLUDED.settings,
                    timestamp = EXCLUDED.timestamp
            """, guild_id, json.dumps(settings_data))
    
    async def load_guild_settings(self, guild_id: int) -> Optional[dict]:
        """Load guild settings"""
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT settings FROM guild_settings WHERE guild_id = $1",
                guild_id
            )
            if row:
                return json.loads(row['settings'])
            return None
    
    async def load_all_guild_settings(self) -> Dict[int, dict]:
        """Load all guild settings at once (for cache preloading)"""
        async with self.pool.acquire() as conn:
            rows = await conn.fetch("SELECT guild_id, settings FROM guild_settings")
            return {row['guild_id']: json.loads(row['settings']) for row in rows}
    
    async def save_all_guild_settings(self, all_settings: Dict[int, dict]) -> None:
        """Batch save all guild settings"""
        async with self.pool.acquire() as conn:
            # Use transaction for batch update
            async with conn.transaction():
                for guild_id, settings in all_settings.items():
                    await conn.execute("""
                        INSERT INTO guild_settings (guild_id, settings, timestamp)
                        VALUES ($1, $2, NOW())
                        ON CONFLICT (guild_id) 
                        DO UPDATE SET 
                            settings = EXCLUDED.settings,
                            timestamp = EXCLUDED.timestamp
                    """, guild_id, json.dumps(settings))
    
    # ===== Whitelist Operations =====
    
    async def add_whitelist_user(self, guild_id: int, user_id: int) -> None:
        """Add user to whitelist"""
        async with self.pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO whitelists (guild_id, user_id, added_at)
                VALUES ($1, $2, NOW())
                ON CONFLICT (guild_id, user_id) DO NOTHING
            """, guild_id, user_id)
    
    async def remove_whitelist_user(self, guild_id: int, user_id: int) -> None:
        """Remove user from whitelist"""
        async with self.pool.acquire() as conn:
            await conn.execute(
                "DELETE FROM whitelists WHERE guild_id = $1 AND user_id = $2",
                guild_id, user_id
            )
    
    async def get_whitelist_users(self, guild_id: int) -> Set[int]:
        """Get all whitelisted users for a guild"""
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT user_id FROM whitelists WHERE guild_id = $1",
                guild_id
            )
            return {row['user_id'] for row in rows}
    
    async def is_whitelisted(self, guild_id: int, user_id: int) -> bool:
        """Lightning-fast whitelist check with index scan"""
        async with self.pool.acquire() as conn:
            exists = await conn.fetchval("""
                SELECT EXISTS(
                    SELECT 1 FROM whitelists 
                    WHERE guild_id = $1 AND user_id = $2
                )
            """, guild_id, user_id)
            return exists
    
    async def clear_whitelist(self, guild_id: int) -> None:
        """Clear all whitelisted users for a guild"""
        async with self.pool.acquire() as conn:
            await conn.execute(
                "DELETE FROM whitelists WHERE guild_id = $1",
                guild_id
            )
    
    async def load_all_whitelists(self) -> Dict[int, Set[int]]:
        """Load all whitelists at once (for cache preloading)"""
        async with self.pool.acquire() as conn:
            rows = await conn.fetch("SELECT guild_id, user_id FROM whitelists")
            
            whitelists = {}
            for row in rows:
                guild_id = row['guild_id']
                user_id = row['user_id']
                if guild_id not in whitelists:
                    whitelists[guild_id] = set()
                whitelists[guild_id].add(user_id)
            
            return whitelists
            
    # ===== Punishment Config Operations =====

    async def save_punishment(self, guild_id: int, violation_type: str, action: str) -> None:
        """Save specific punishment rule for a guild (atomic UPSERT)"""
        async with self.pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO guild_punishments (guild_id, violation_type, action, updated_at)
                VALUES ($1, $2, $3, NOW())
                ON CONFLICT (guild_id, violation_type) 
                DO UPDATE SET 
                    action = EXCLUDED.action,
                    updated_at = EXCLUDED.updated_at
            """, guild_id, violation_type, action)

    async def load_punishment_config(self, guild_id: int) -> Dict[str, str]:
        """Load all punishment rules for a guild"""
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT violation_type, action FROM guild_punishments WHERE guild_id = $1",
                guild_id
            )
            return {row['violation_type']: row['action'] for row in rows}

    async def load_all_punishment_configs(self) -> Dict[int, Dict[str, str]]:
        """Load all punishment configs for all guilds"""
        async with self.pool.acquire() as conn:
            rows = await conn.fetch("SELECT guild_id, violation_type, action FROM guild_punishments")
            
            configs = {}
            for row in rows:
                guild_id = row['guild_id']
                v_type = row['violation_type']
                action = row['action']
                
                if guild_id not in configs:
                    configs[guild_id] = {}
                configs[guild_id][v_type] = action
            
            return configs
    
    # ===== User Token Operations =====
    
    async def save_user_token(
        self, 
        guild_id: int, 
        token: str, 
        set_by: Optional[int] = None,
        description: Optional[str] = None
    ) -> None:
        """Save user token"""
        async with self.pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO user_tokens (guild_id, token, set_by, set_at, description)
                VALUES ($1, $2, $3, NOW(), $4)
                ON CONFLICT (guild_id) 
                DO UPDATE SET 
                    token = EXCLUDED.token,
                    set_by = EXCLUDED.set_by,
                    set_at = EXCLUDED.set_at,
                    description = EXCLUDED.description
            """, guild_id, token, set_by, description)
    
    async def load_user_token(self, guild_id: int) -> Optional[dict]:
        """Load user token for guild"""
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT token, set_by, set_at, last_used, description FROM user_tokens WHERE guild_id = $1",
                guild_id
            )
            if row:
                return {
                    'token': row['token'],
                    'set_by': row['set_by'],
                    'set_at': row['set_at'],
                    'last_used': row['last_used'],
                    'description': row['description']
                }
            return None
    
    async def update_token_last_used(self, guild_id: int) -> None:
        """Update last_used timestamp for a token"""
        async with self.pool.acquire() as conn:
            await conn.execute(
                "UPDATE user_tokens SET last_used = NOW() WHERE guild_id = $1",
                guild_id
            )
    
    async def load_all_user_tokens(self) -> Dict[int, dict]:
        """Load all user tokens at once"""
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT guild_id, token, set_by, set_at, last_used, description FROM user_tokens"
            )
            return {
                row['guild_id']: {
                    'token': row['token'],
                    'set_by': row['set_by'],
                    'set_at': row['set_at'],
                    'last_used': row['last_used'],
                    'description': row['description']
                }
                for row in rows
            }
