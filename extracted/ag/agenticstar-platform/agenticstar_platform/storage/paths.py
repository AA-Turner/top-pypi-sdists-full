"""
AGENTICSTAR Platform SDK - Storage Path Conventions
フロントエンド・バックエンド間で共有するストレージパスの命名規則

AgenticStar プラットフォーム全体で統一されたパス構造を提供:
- plans/{plan_id}/{subdir}/{filename}   … エージェント実行成果物
- uploads/{conversation_id}/{message_id}/{filename} … ユーザーアップロード

Usage:
    from agenticstar_platform.storage.paths import StoragePaths

    # プランパス構築
    prefix = StoragePaths.plan_prefix("exec-123", "files")
    # → "plans/exec-123/files"

    path = StoragePaths.plan_path("exec-123", "files", "report.pdf")
    # → "plans/exec-123/files/report.pdf"

    # アップロードパス構築
    prefix = StoragePaths.upload_prefix("conv-456", "msg-789")
    # → "uploads/conv-456/msg-789"

    # サブディレクトリ定数
    StoragePaths.SUBDIR_FILES        # "files"
    StoragePaths.SUBDIR_DOWNLOADS    # "downloads"
    StoragePaths.SUBDIR_SCREENSHOTS  # "screenshots"
    StoragePaths.SUBDIR_DELIVERABLES # "deliverables"
"""

from typing import Final


class StoragePaths:
    """AgenticStar ストレージパス命名規則

    フロントエンド (ChatBoard) とバックエンド (Autonomous Agent) 間で
    共有するパス構造を定義する。
    """

    # ========== Top-level prefixes ==========
    PLANS_PREFIX: Final[str] = "plans"
    UPLOADS_PREFIX: Final[str] = "uploads"
    # 所有者スコープ namespace（マルチテナント汎用、PLANS/UPLOADS と同列の命名規則）
    USERS_PREFIX: Final[str] = "users"

    # ========== Subdirectory constants ==========
    SUBDIR_FILES: Final[str] = "files"
    SUBDIR_DOWNLOADS: Final[str] = "downloads"
    SUBDIR_SCREENSHOTS: Final[str] = "screenshots"
    SUBDIR_DELIVERABLES: Final[str] = "deliverables"
    SUBDIR_COT: Final[str] = ".CoT"

    # ========== Default subdirectory ==========
    DEFAULT_SUBDIR: Final[str] = SUBDIR_FILES

    # ========== Path builders ==========

    @staticmethod
    def plan_prefix(plan_id: str, subdir: str = "") -> str:
        """プラン成果物のストレージプレフィックスを構築

        Args:
            plan_id: 実行ID / プランID
            subdir: サブディレクトリ（files, screenshots 等）

        Returns:
            "plans/{plan_id}/{subdir}" or "plans/{plan_id}"

        Raises:
            ValueError: plan_id が空文字列の場合
        """
        if not plan_id:
            raise ValueError("plan_id must not be empty")
        if subdir:
            return f"{StoragePaths.PLANS_PREFIX}/{plan_id}/{subdir}"
        return f"{StoragePaths.PLANS_PREFIX}/{plan_id}"

    @staticmethod
    def plan_path(plan_id: str, subdir: str, filename: str) -> str:
        """プラン成果物のフルパスを構築

        Args:
            plan_id: 実行ID / プランID
            subdir: サブディレクトリ
            filename: ファイル名

        Returns:
            "plans/{plan_id}/{subdir}/{filename}"

        Raises:
            ValueError: plan_id, subdir, filename のいずれかが空文字列の場合
        """
        if not plan_id:
            raise ValueError("plan_id must not be empty")
        if not subdir:
            raise ValueError("subdir must not be empty")
        if not filename:
            raise ValueError("filename must not be empty")
        return f"{StoragePaths.PLANS_PREFIX}/{plan_id}/{subdir}/{filename}"

    @staticmethod
    def owner_prefix(owner_id: str, inner: str = "") -> str:
        """所有者スコープのストレージプレフィックスを構築（マルチテナント汎用）。

        任意の prefix を所有者名前空間 `users/{owner_id}/` 配下に入れる汎用ヘルパー。
        PLANS_PREFIX / UPLOADS_PREFIX と同列のストレージ命名規則であり、
        特定アプリ機能（成果物ブラウザ等）には依存しない。

        Args:
            owner_id: 所有者識別子（テナント / ユーザー ID 等）
            inner: 所有者配下に配置する相対 prefix（空可。例: "plans/exec-1/files"）

        Returns:
            "users/{owner_id}/{inner}" or "users/{owner_id}"

        Raises:
            ValueError: owner_id が空、または owner_id / inner に path traversal
                        (".." セグメント) や不正文字 ("/" in owner_id, NUL, 先頭スラッシュ)
                        が含まれる場合
        """
        if not owner_id:
            raise ValueError("owner_id must not be empty")
        # owner_id は単一セグメント (テナント/ユーザーID)。区切り文字や traversal を拒否。
        if "/" in owner_id or "\x00" in owner_id or owner_id in (".", ".."):
            raise ValueError("owner_id contains invalid characters")
        if inner:
            # inner は相対 prefix。先頭スラッシュ / NUL / ".." セグメントを拒否。
            if inner.startswith("/") or "\x00" in inner:
                raise ValueError("inner must be a relative prefix without leading slash or NUL")
            if any(seg == ".." for seg in inner.split("/")):
                raise ValueError("inner must not contain '..' path traversal")
            return f"{StoragePaths.USERS_PREFIX}/{owner_id}/{inner}"
        return f"{StoragePaths.USERS_PREFIX}/{owner_id}"

    @staticmethod
    def upload_prefix(conversation_id: str, message_id: str) -> str:
        """ユーザーアップロードのストレージプレフィックスを構築

        末尾スラッシュなし（plan_prefix と統一）。

        Args:
            conversation_id: 会話ID
            message_id: メッセージID

        Returns:
            "uploads/{conversation_id}/{message_id}"

        Raises:
            ValueError: conversation_id または message_id が空文字列の場合
        """
        if not conversation_id:
            raise ValueError("conversation_id must not be empty")
        if not message_id:
            raise ValueError("message_id must not be empty")
        return f"{StoragePaths.UPLOADS_PREFIX}/{conversation_id}/{message_id}"

    @staticmethod
    def upload_path(
        conversation_id: str, message_id: str, filename: str
    ) -> str:
        """ユーザーアップロードのフルパスを構築

        Args:
            conversation_id: 会話ID
            message_id: メッセージID
            filename: ファイル名

        Returns:
            "uploads/{conversation_id}/{message_id}/{filename}"

        Raises:
            ValueError: conversation_id, message_id, filename のいずれかが空文字列の場合
        """
        if not conversation_id:
            raise ValueError("conversation_id must not be empty")
        if not message_id:
            raise ValueError("message_id must not be empty")
        if not filename:
            raise ValueError("filename must not be empty")
        return f"{StoragePaths.UPLOADS_PREFIX}/{conversation_id}/{message_id}/{filename}"

    @staticmethod
    def input_uploads_prefix(user_id: str, conversation_id: str, message_id: str) -> str:
        """入力添付（チャットUIから渡されたファイル）の owner-scoped prefix を構築。

        フロントエンドは添付を ``users/{owner}/uploads/{conv}/{msg}/`` に保存し、
        プラットフォームは owner を ``USER_ID``、会話/メッセージ ID を ``CONVERSATION_ID`` /
        ``MESSAGE_ID`` として Pod 起動時に環境変数へ注入する。本メソッドはその規約 prefix を
        返す。取得は ``download_objects_by_prefix`` と併用する。

        Example:
            >>> import os
            >>> prefix = StoragePaths.input_uploads_prefix(
            ...     os.environ["USER_ID"],
            ...     os.environ["CONVERSATION_ID"],
            ...     os.environ["MESSAGE_ID"],
            ... )
            >>> await storage.download_objects_by_prefix(prefix, dest_dir="/tmp/inputs")

        Returns:
            "users/{user_id}/uploads/{conversation_id}/{message_id}"
        """
        if not conversation_id:
            raise ValueError("conversation_id must not be empty")
        if not message_id:
            raise ValueError("message_id must not be empty")
        return StoragePaths.owner_prefix(
            user_id, f"{StoragePaths.UPLOADS_PREFIX}/{conversation_id}/{message_id}"
        )
