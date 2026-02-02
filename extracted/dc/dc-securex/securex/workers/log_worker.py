"""
Log Worker - Logs threats and fires callbacks
"""
import discord
import asyncio
from ..models import ThreatEvent


class LogWorker:
    """Worker that logs threats and triggers callbacks"""
    
    def __init__(self, sdk):
        self.sdk = sdk
        self.bot = sdk.bot
        self.log_queue = sdk.log_queue  # Use SDK's shared queue
        self._worker_task = None
        
        self.action_map = {
            discord.AuditLogAction.bot_add: "bot_add",
            discord.AuditLogAction.channel_create: "channel_create",
            discord.AuditLogAction.channel_delete: "channel_delete",
            discord.AuditLogAction.channel_update: "channel_update",
            discord.AuditLogAction.role_create: "role_create",
            discord.AuditLogAction.role_delete: "role_delete",
            discord.AuditLogAction.role_update: "role_update",
            discord.AuditLogAction.kick: "member_kick",
            discord.AuditLogAction.ban: "member_ban",
            discord.AuditLogAction.unban: "member_unban",
            discord.AuditLogAction.member_update: "member_update",
            discord.AuditLogAction.webhook_create: "webhook_create",
            discord.AuditLogAction.guild_update: "guild_update",
        }
    
    async def start(self):
        """Start the log worker"""
        if self._worker_task is None or self._worker_task.done():
            self._worker_task = asyncio.create_task(self._worker_loop())
            print("📝 Log Worker started")
    
    async def stop(self):
        """Stop the worker"""
        if self._worker_task:
            self._worker_task.cancel()
            self._worker_task = None
    
    async def _worker_loop(self):
        """Main worker loop"""
        while True:
            try:
                entry = await self.log_queue.get()
                await self._process_entry(entry)
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Error in log worker: {e}")
    
    async def _process_entry(self, entry):
        """Process log entry and fire callbacks"""
        try:
            guild = entry.guild
            executor = entry.user
            
            if executor.id == self.bot.user.id or executor.id == guild.owner_id:
                return
            
            violation_type = self.action_map.get(entry.action)
            if not violation_type:
                return
            
            guild_punishments = self.sdk.punishment_cache.get(guild.id, self.sdk.punishments)
            punishment_action = guild_punishments.get(violation_type, "none")
            
            threat_event = ThreatEvent(
                guild_id=guild.id,
                actor_id=executor.id,
                type=violation_type,
                target_id=getattr(entry.target, 'id', None),
                target_name=getattr(entry.target, 'name', 'Unknown'),
                prevented=True,
                restored=True,
                punishment_action=punishment_action,
                timestamp=entry.created_at
            )
            
            await self.sdk._trigger_callbacks('threat_detected', threat_event)
            
        except Exception as e:
            print(f"Error processing log entry: {e}")
