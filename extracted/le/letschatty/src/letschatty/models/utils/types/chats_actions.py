from enum import StrEnum

class ChatAction(StrEnum):
    TRANSFER = "transfer_chats_to_agent"
    UNARCHIVE = "unarchive_chats"
    ARCHIVE = "archive_chats"
    DESSIGN = "dessasign_agent_from_chats"
    READ = "mark_chats_as_read"
    UNREAD = "mark_chats_as_unread"
    STARRED = "mark_chats_as_starred"
    UNSTARRED = "mark_chats_as_unstarred"
    BLOCK = "block_chats"
    UNBLOCK = "unblock_chats"
