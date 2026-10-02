"""
AGENTICSTAR Platform SDK - Event Types
イベントタイプ定義（フロントエンド表示出し分け対応）

SDKとして提供する汎用イベントタイプ定義
"""

from enum import Enum


class EventType(str, Enum):
    """
    AgentLoopPublisher粒度のイベントタイプ定義

    フロントエンドでのUI表示制御に使用される主要イベントタイプ
    """

    # フェーズ系イベント
    PHASE_START = "phase_start"
    PROGRESS_UPDATE = "progress_update"

    # AI思考プロセス
    THOUGHT_MESSAGE = "thought_message"

    # 完了系イベント
    COMPLETION_SUCCESS = "completion_success"
    COMPLETION_FAILURE = "completion_failure"

    # 相互作用イベント
    USER_INTERACTION_REQUIRED = "user_interaction_required"
    UNEXPECTED_ERROR = "unexpected_error"

    # HITL(Human-In-The-Loop)関連イベント
    HITL_REQUIRED_BROWSER_VNC = "hitl_required_browser_vnc"  # Pod環境: VNC経由でブラウザ介入
    HITL_REQUIRED_BROWSER_CLI = "hitl_required_browser_cli"  # CLI環境: ローカルブラウザ介入
    HITL_COMPLETED = "hitl_completed"  # HITL操作完了

    # ファイル作成イベント
    FILE_CREATED = "file_created"

    # パーミッション関連イベント
    PERMISSION_REQUEST = "permission_request"
    PERMISSION_RESPONSE = "permission_response"

    # 統一ツールイベント
    TOOL_START = "tool_start"  # ツール実行開始
    TOOL_RESULT = "tool_result"  # ツール実行結果

    # 最終結果
    FINAL_RESULT = "final_result"

    # 進捗メッセージ（Webhook専用）
    PROGRESS_MESSAGE = "progress_message"


class SubEventType(str, Enum):
    """
    ツール結果のサブイベントタイプ定義

    フロントエンドでの表示出し分けに使用
    例: search_webはWeb検索アイコン、file_editedはファイル編集アイコン
    """

    # Web検索関連
    SEARCH_WEB = "search_web"

    # コマンド実行関連
    COMMAND_EXECUTION = "command_execution"

    # ファイル操作関連
    FILE_OPERATION = "file_operation"

    # ローカルアシスタント関連
    LOCAL_ASSISTANT = "local_assistant"

    # MCPツール関連
    MCP_TOOL = "mcp_tool"

    # OpenCode互換ツールイベント
    FILE_EDITED = "file_edited"  # write, edit, multiedit
    FILE_READ = "file_read"  # read
    FILE_SEARCHED = "file_searched"  # grep, glob, ls
    BASH_EXECUTED = "bash_executed"  # bash
    WEB_FETCHED = "web_fetched"  # webfetch
    TASK_LAUNCHED = "task_launched"  # task
    TODO_UPDATED = "todo_updated"  # todo
    VIDEO_GENERATED = "video_generated"  # video_gen
    IMAGE_GENERATED = "image_generated"  # generation_image

    # Slide generation
    SLIDE_CREATED = "slide_created"  # save_html (slide preview)

    # macOS Automation
    MACOS_AUTOMATION = "macos_automation"  # macOS UI/app automation tools
