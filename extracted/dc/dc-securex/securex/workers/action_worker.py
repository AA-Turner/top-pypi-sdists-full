"""
Action Worker - Instant punishment for unauthorized actions
"""
import discord
import asyncio


class ActionWorker:
    """Worker that bans/punishes violators instantly"""
    
    def __init__(self, sdk):
        self.sdk = sdk
        self.bot = sdk.bot
        self.action_queue = sdk.action_queue  # Use SDK's shared queue
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
        """Start the action worker"""
        if self._worker_task is None or self._worker_task.done():
            self._worker_task = asyncio.create_task(self._worker_loop())
            print("⚡ Action Worker started")
    
    async def stop(self):
        """Stop the worker"""
        if self._worker_task:
            self._worker_task.cancel()
            self._worker_task = None
    
    async def _worker_loop(self):
        """Main worker loop"""
        while True:
            try:
                entry = await self.action_queue.get()
                await self._process_entry(entry)
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Error in action worker: {e}")
    
    async def _process_entry(self, entry):
        """Process audit log entry"""
        try:
            guild = entry.guild
            executor = entry.user
            
            if executor.id == self.bot.user.id:
                return
            
            if executor.id == guild.owner_id:
                return
            
            whitelist_set = self.sdk.whitelist_cache.get(guild.id, set())
            if executor.id in whitelist_set:
                return
            
            # Get punishment using new multi-server aware method
            punishment_action = await self.sdk.get_punishment(guild.id, violation_type)
            
            if punishment_action != "none":
                try:
                    punishment_result = await self.sdk.punisher.punish(
                        guild=guild,
                        user=executor,
                        violation_type=violation_type,
                        details=f"{violation_type} on {getattr(entry.target, 'name', 'Unknown')}",
                        sdk=self.sdk
                    )
                    print(f"👢 {punishment_result.title()} {executor.name} for {violation_type}")
                except Exception as e:
                    print(f"Cannot punish {executor.name}: {e}")
            
        except Exception as e:
            print(f"Error processing action entry: {e}")
