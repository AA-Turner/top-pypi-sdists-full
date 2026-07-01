"""Widgets for the Dreadnode Textual client."""

from dreadnode.app.tui.widgets.agent_dialog import AgentDialog
from dreadnode.app.tui.widgets.context_bar import AppBar, ContextBar, PageStatus, SessionContextBar
from dreadnode.app.tui.widgets.conversation import (
    ConversationView,
    StreamingDraft,
)
from dreadnode.app.tui.widgets.flash import Flash

# Legacy imports — kept for backward compatibility but no longer used in compose()
from dreadnode.app.tui.widgets.header_bar import HeaderBar
from dreadnode.app.tui.widgets.help_panel import render_help
from dreadnode.app.tui.widgets.human_prompt import HumanPromptWidget
from dreadnode.app.tui.widgets.mention_overlay import MentionOverlay
from dreadnode.app.tui.widgets.message_queue import MessageQueue
from dreadnode.app.tui.widgets.new_messages_pill import NewMessagesPill
from dreadnode.app.tui.widgets.overlay_mixin import OverlayMixin
from dreadnode.app.tui.widgets.permission_prompt import PermissionPrompt
from dreadnode.app.tui.widgets.profile_dialog import ProfileDialog
from dreadnode.app.tui.widgets.prompt_info import PromptInfo
from dreadnode.app.tui.widgets.session_sidebar import SessionListEntry, SessionSidebar
from dreadnode.app.tui.widgets.slash_overlay import SlashOverlay
from dreadnode.app.tui.widgets.status_bar import StatusBar
from dreadnode.app.tui.widgets.throbber import Throbber
from dreadnode.app.tui.widgets.tool_progress import ToolProgress
from dreadnode.app.tui.widgets.welcome import Welcome
from dreadnode.app.tui.widgets.whoami import WhoAmI

__all__ = [
    "AgentDialog",
    "AppBar",
    "ContextBar",
    "ConversationView",
    "Flash",
    "HeaderBar",
    "HumanPromptWidget",
    "MentionOverlay",
    "MessageQueue",
    "NewMessagesPill",
    "OverlayMixin",
    "PageStatus",
    "PermissionPrompt",
    "ProfileDialog",
    "PromptInfo",
    "SessionContextBar",
    "SessionListEntry",
    "SessionSidebar",
    "SlashOverlay",
    "StatusBar",
    "StreamingDraft",
    "Throbber",
    "ToolProgress",
    "Welcome",
    "WhoAmI",
    "render_help",
]
