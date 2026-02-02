"""
Data models for SecureX SDK.
These objects are returned to developers - no UI included.
"""
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from typing import Optional, List, Dict
import json


@dataclass
class ThreatEvent:
    """
    Represents a detected security threat.
    
    Attributes:
        type: Type of threat (e.g., "channel_delete", "role_create")
        guild_id: ID of the guild where threat occurred
        actor_id: ID of user who performed the action
        target_id: ID of the affected resource
        target_name: Name of the affected resource
        prevented: Whether the action was prevented
        restored: Whether restoration was successful
        timestamp: When the threat was detected
        details: Additional context about the threat
    """
    type: str
    guild_id: int
    actor_id: int
    target_id: int
    target_name: str
    prevented: bool
    restored: bool
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    details: Dict = field(default_factory=dict)
    punishment_action: Optional[str] = None  
    
    def to_dict(self) -> dict:
        """Convert to dictionary for serialization"""
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        return data
    
    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict())


@dataclass
class BackupInfo:
    """
    Information about a server backup.
    
    Attributes:
        guild_id: ID of the backed up guild
        timestamp: When backup was created
        channel_count: Number of channels backed up
        role_count: Number of roles backed up
        backup_path: Path to backup file
        success: Whether backup completed successfully
    """
    guild_id: int
    timestamp: datetime
    channel_count: int
    role_count: int
    backup_path: str
    success: bool = True
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        return data


@dataclass
class RestoreResult:
    """
    Result of a restoration operation.
    
    Attributes:
        success: Overall success status
        items_restored: Number of items successfully restored
        items_failed: Number of items that failed to restore
        errors: List of error messages
        duration: Time taken in seconds
        details: Additional restoration details
    """
    success: bool
    items_restored: int
    items_failed: int
    errors: List[str] = field(default_factory=list)
    duration: float = 0.0
    details: Dict = field(default_factory=dict)
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return asdict(self)


@dataclass
class WhitelistChange:
    """
    Represents a whitelist modification.
    
    Attributes:
        guild_id: Guild where change occurred
        user_id: User added/removed from whitelist
        action: "added" or "removed"
        timestamp: When the change occurred
        moderator_id: Who made the change
    """
    guild_id: int
    user_id: int
    action: str  
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    moderator_id: Optional[int] = None
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        return data


@dataclass
class UserToken:
    """
    Represents a user token for guild-level API operations.
    
    Attributes:
        guild_id: Guild this token is associated with
        token: The user authentication token
        set_by: User ID who set this token
        timestamp: When the token was added/updated
        last_used: When the token was last used (optional)
        description: Optional description/note about the token
    """
    guild_id: int
    token: str
    set_by: Optional[int] = None
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    last_used: Optional[datetime] = None
    description: Optional[str] = None
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        if self.last_used:
            data['last_used'] = self.last_used.isoformat()
        return data
    
    def mark_used(self):
        """Mark this token as used (updates last_used timestamp)"""
        self.last_used = datetime.now(timezone.utc)
