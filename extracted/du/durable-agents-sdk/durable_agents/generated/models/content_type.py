from enum import Enum

class ContentType(str, Enum):
    Commit = "commit",
    Email = "email",
    Event = "event",
    File = "file",
    Initiative = "initiative",
    Issue = "issue",
    Memory = "memory",
    Message = "message",
    Page = "page",
    Post = "post",
    Pull_request = "pull_request",
    Text = "text",
    Transcript = "transcript",

