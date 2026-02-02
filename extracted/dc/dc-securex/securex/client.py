"""
SecureX SDK - Main Client
Backend-only anti-nuke protection system
"""
import discord
import asyncio
from pathlib import Path
from typing import Dict, List, Callable, Optional
from .backup.manager import BackupManager
from .handlers.channel import ChannelHandler
from .handlers.role import RoleHandler
from .handlers.member import MemberHandler
from .utils.whitelist import WhitelistManager
from .utils.punishment import PunishmentExecutor
from .models import ThreatEvent, BackupInfo
from .workers import ActionWorker, CleanupWorker, LogWorker, GuildWorker
from .storage import create_storage_backend


class SecureX:
    """
    Main SecureX SDK class for anti-nuke protection.
    Backend-only - no UI, no commands, just pure protection logic.
    """
    
    def __init__(
        self,
        bot: discord.Client,
        storage: Optional[create_storage_backend] = None,
        backup_dir: str = "./data/backups",
        storage_backend: str = "sqlite",
        postgres_url: Optional[str] = None,
        postgres_pool_size: int = 10,
        punishments: Optional[Dict[str, str]] = None,
        timeout_duration: int = 600,
        notify_user: bool = True
    ):
        """
        Initialize SecureX SDK.
        
        Args:
            bot: Your discord.Client or commands.Bot instance
            backup_dir: Directory to store backups (default: ./data/backups)
            storage_backend: "sqlite" or "postgres" (default: "sqlite")
            postgres_url: PostgreSQL connection URL (required if storage_backend="postgres")
            postgres_pool_size: Connection pool size for PostgreSQL (default: 10)
            punishments: Dict mapping violation types to punishment actions
            timeout_duration: Duration in seconds for timeout punishment (default: 600)
            notify_user: Whether to DM violators about punishment (default: True)
        """
        self.bot = bot
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.storage_backend_type = storage_backend
        
        # Create storage backend
        if storage:
            self.storage = storage
        elif storage_backend == "postgres":
            if not postgres_url:
                raise ValueError("postgres_url required when storage_backend='postgres'")
            self.storage = create_storage_backend(
                "postgres",
                url=postgres_url,
                pool_size=postgres_pool_size
            )
        else:
            self.storage = create_storage_backend(
                "sqlite",
                db_path=str(self.backup_dir / "securex.db")
            )
        
        # Managers now use storage abstraction
        self.backup_manager = BackupManager(self, self.storage)
        self.whitelist = WhitelistManager(self, self.storage)
        
        
        self._callbacks: Dict[str, List[Callable]] = {
            'threat_detected': [],
            'backup_completed': [],
            'restore_completed': [],
            'whitelist_changed': [],
        }
        
        
        self.default_punishments = {
            # Bot Safety
            "bot_add": "none",
            
            # Channel Protection
            "channel_create": "none",
            "channel_delete": "none",
            "channel_update": "none",
            
            # Role Protection
            "role_create": "none",
            "role_delete": "none",
            "role_update": "none",
            
            # Member Safety
            "member_ban": "none",
            "member_kick": "none",
            "member_unban": "none",
            "member_update": "none",
            
            # Webhook Protection
            "webhook_create": "none",
            "webhook_delete": "none",
            "webhook_update": "none",
            
            # Server Integrity
            "guild_update": "none"
        }
        
        
        self.punisher = PunishmentExecutor(bot)
        self.timeout_duration = timeout_duration
        self.notify_punished_user = notify_user
        
        
        self.action_queue = asyncio.Queue(maxsize=1000)
        self.log_queue = asyncio.Queue(maxsize=1000)
        self.cleanup_queue = asyncio.Queue(maxsize=1000)
        self.guild_queue = asyncio.Queue(maxsize=1000)
        
        
        self.whitelist_cache = {}  
        self.punishment_cache = {}  
        
        
        self._worker_tasks = []
        
        
        # Initialize handlers
        self.channel_handler = ChannelHandler(self)
        self.role_handler = RoleHandler(self)
        self.member_handler = MemberHandler(self)
        
        # Initialize workers
        self.action_worker = ActionWorker(self)
        self.cleanup_worker = CleanupWorker(self)
        self.log_worker = LogWorker(self)
        self.guild_worker = GuildWorker(self)
        
        self._register_audit_log_listener()
        
        
        self._register_events()
    
    def _register_audit_log_listener(self):
        """Register INSTANT audit log event listener (v2.0 - 5-10ms response)"""
        @self.bot.event
        async def on_audit_log_entry_create(entry: discord.AuditLogEntry):
            try:
                await self.action_queue.put(entry)
                await self.log_queue.put(entry)
                await self.cleanup_queue.put(entry)
                await self.guild_queue.put(entry)
            except asyncio.QueueFull as e:
                print(f"⚠️ Queue full: {e}")

    def _register_events(self):
        """Register Discord event listeners for restorations"""
        # NOTE: These handlers are for RESTORATION (restoring deletions/reverting updates)
        # The audit log listener handles DETECTION (detecting unauthorized creations)
        # Both are needed!
        
        @self.bot.event
        async def on_guild_channel_delete(channel):
            await self.channel_handler.on_channel_delete(channel)
        
        @self.bot.event
        async def on_guild_channel_update(before, after):
            await self.channel_handler.on_channel_update(before, after)
        
        @self.bot.event
        async def on_guild_role_delete(role):
            await self.role_handler.on_role_delete(role)
        
        @self.bot.event
        async def on_guild_role_update(before, after):
            await self.role_handler.on_role_update(before, after)
        
        @self.bot.event
        async def on_member_ban(guild, user):
            await self.member_handler.on_member_ban(guild, user)
        
        @self.bot.event
        async def on_member_update(before, after):
            await self.member_handler.on_member_update(before, after)

    
    def on(self, event_name: str):
        """
        Decorator to register callbacks for SDK events.
        
        Usage:
            @sx.on('threat_detected')
            async def handle_threat(event: ThreatEvent):
                print(f"Threat: {event.type}")
        """
        def decorator(func: Callable):
            if event_name in self._callbacks:
                self._callbacks[event_name].append(func)
            return func
        return decorator
    
    @property
    def on_threat_detected(self):
        """Convenience decorator for threat_detected events"""
        return self.on('threat_detected')
    
    @property
    def on_backup_completed(self):
        """Convenience decorator for backup_completed events"""
        return self.on('backup_completed')
    
    @property
    def on_restore_completed(self):
        """Convenience decorator for restore_completed events"""
        return self.on('restore_completed')
    
    @property
    def on_whitelist_changed(self):
        """Convenience decorator for whitelist_changed events"""
        return self.on('whitelist_changed')
    
    async def _trigger_callbacks(self, event_name: str, *args, **kwargs):
        """Trigger all registered callbacks for an event"""
        if event_name in self._callbacks:
            for callback in self._callbacks[event_name]:
                try:
                    if asyncio.iscoroutinefunction(callback):
                        await callback(*args, **kwargs)
                    else:
                        callback(*args, **kwargs)
                except Exception as e:
                    print(f"Error in callback for {event_name}: {e}")
    
    async def enable(
        self,
        guild_id: Optional[int] = None,
        whitelist: Optional[List[int]] = None,
        auto_backup: bool = True,
        punishments: Optional[Dict[str, str]] = None,
        timeout_duration: Optional[int] = None,
        notify_user: Optional[bool] = None
    ):
        """
        Enable SecureX protection.
        
        Args:
            guild_id: Guild ID to enable protection for (required if using whitelist)
            whitelist: List of user IDs to whitelist (global for this session)
            auto_backup: Enable automatic backups every 30 minutes (default: True)
            punishments: Dict mapping violation types to punishment actions (Global default overrides)
            timeout_duration: Override timeout duration in seconds
            notify_user: Override whether to DM violators
        """
        
        # 1. Initialize storage (connection pool for PostgreSQL)
        if hasattr(self.storage, 'initialize'):
            await self.storage.initialize()
        
        # 2. Preload data from storage to RAM
        await self.whitelist.preload_all()
        await self.backup_manager.preload_all()
        
        # 3. Load guild-specific punishment overrides
        if hasattr(self.storage, 'load_all_punishment_configs'):
            configs = await self.storage.load_all_punishment_configs()
            self.punishment_cache.update(configs)
            if configs:
                print(f"📦 Loaded punishment configs for {len(configs)} guilds")
        
        # 4. Process Runtime Overrides (passed to enable)
        if guild_id and whitelist:
            for user_id in whitelist:
                await self.whitelist.add(guild_id, user_id)
            self.whitelist_cache[guild_id] = self.whitelist_cache.get(guild_id, set()) | set(whitelist)
        
        if punishments:
            if guild_id:
                # Set for specific guild (persistently)
                for v_type, action in punishments.items():
                    await self.set_punishment(guild_id, v_type, action)
            else:
                # Update global defaults (in-memory)
                self.default_punishments.update(punishments)
        
        # Update settings if provided
        if timeout_duration is not None:
            self.timeout_duration = timeout_duration
        if notify_user is not None:
            self.notify_punished_user = notify_user
        
        # 5. Start Workers
        await self.action_worker.start()
        await self.cleanup_worker.start()
        await self.log_worker.start()
        await self.guild_worker.start()
        
        if auto_backup:
            self.backup_manager.start_auto_backup()
            self.backup_manager.start_auto_refresh()
        
        if guild_id:
            await self.backup_manager.create_backup(guild_id)
            
        print("""
 ######  ########  ######  ##     ## ########  ######## ##     ##          ######  ########  ##    ## 
##    ## ##       ##    ## ##     ## ##     ## ##        ##   ##          ##    ## ##     ## ##   ##  
##       ##       ##       ##     ## ##     ## ##         ## ##           ##       ##     ## ##  ##   
 ######  ######   ##       ##     ## ########  ######      ###    #######  ######  ##     ## #####    
      ## ##       ##       ##     ## ##   ##   ##         ## ##                 ## ##     ## ##  ##   
##    ## ##       ##    ## ##     ## ##    ##  ##        ##   ##          ##    ## ##     ## ##   ##  
 ######  ########  ######   #######  ##     ## ######## ##     ##          ######  ########  ##    ##  
""")
        if punishments:
            enabled_punishments = {k: v for k, v in punishments.items() if v != "none"}
            if enabled_punishments:
                scope = f"GUILD {guild_id}" if guild_id else "GLOBAL"
                print(f"⚠️  Punishments active ({scope}) for {len(enabled_punishments)} violation types")
    
    
    async def create_backup(self, guild_id: int) -> BackupInfo:
        """
        Create a backup for the specified guild.
        
        Args:
            guild_id: The guild ID to backup
            
        Returns:
            BackupInfo object with backup results
        """
        return await self.backup_manager.create_backup(guild_id)
    
    async def restore_channel(self, guild: discord.Guild, channel: discord.abc.GuildChannel):
        """
        Restore a deleted channel from backup.
        
        Args:
            guild: The guild object
            channel: The deleted channel object
            
        Returns:
            The newly created channel or None if restoration failed
        """
        return await self.backup_manager.restore_channel(guild, channel)
    
    async def restore_role(self, guild: discord.Guild, role_id: int) -> bool:
        """
        Restore a deleted role from backup.
        
        Args:
            guild: The guild object
            role_id: The ID of the deleted role
            
        Returns:
            True if successful, False otherwise
        """
        return await self.backup_manager.restore_role(guild, role_id)
    
    async def set_punishment(self, guild_id: int, violation_type: str, action: str):
        """
        Set a specific punishment for a violation type in a guild.
        Persists to storage backend.
        
        Args:
            guild_id: ID of the guild
            violation_type: Type of violation (e.g., 'channel_delete')
            action: Punishment action ('none', 'kick', 'ban', etc.)
        """
        if violation_type not in self.default_punishments:
            print(f"⚠️ Warning: Unknown violation type '{violation_type}'")
            
        # 1. Update In-Memory Cache
        if guild_id not in self.punishment_cache:
            self.punishment_cache[guild_id] = {}
        self.punishment_cache[guild_id][violation_type] = action
        
        # 2. Persist to Storage
        if hasattr(self.storage, 'save_punishment'):
            await self.storage.save_punishment(guild_id, violation_type, action)
            
    async def get_punishment(self, guild_id: int, violation_type: str) -> str:
        """
        Get the punishment action for a specific guild and violation type.
        Falls back to global default if not set for guild.
        """
        # 1. Check Guild Cache
        if guild_id in self.punishment_cache:
            if violation_type in self.punishment_cache[guild_id]:
                return self.punishment_cache[guild_id][violation_type]
        
        # 2. Fallback to Global Default
        return self.default_punishments.get(violation_type, "none")
        
    async def get_punishment_config(self, guild_id: int) -> Dict[str, str]:
        """
        Get the complete effective punishment config for a guild.
        Merges global defaults with guild overrides.
        """
        effective_config = self.default_punishments.copy()
        
        if guild_id in self.punishment_cache:
            effective_config.update(self.punishment_cache[guild_id])
            
        return effective_config
