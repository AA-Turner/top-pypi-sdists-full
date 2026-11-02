from enum import StrEnum
class ChatStatusModification(StrEnum):
    ASSIGN = "assign"
    DESASSIGN = "desassign"
    BLOCK = "block"
    UNBLOCK = "unblock"
    STAR = "star"
    UNSTAR = "unstar"
    ARCHIVE = "archive"
    UNARCHIVE = "unarchive"
    READ = "read"
    UNREAD = "unread"
    TRANSFER = "transfer"

