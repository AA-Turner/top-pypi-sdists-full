"""
AGENTICSTAR Platform SDK - Content Safety Validator
コンテンツセキュリティ検証（Prompt Shield + Moderation）

このモジュールは、AzureSecurityClientを使用したコンテンツの
セキュリティ検証を提供します。

guardrails_settings（DB等から取得）に応じてthreshold等を設定し、
コンテンツのバリデーションとマーキングを行います。

- Prompt Shield: Jailbreak攻撃検出
- Content Moderation: 有害コンテンツ検出
- Content Marking: コンテンツ出典明示

Example:
    from agenticstar_platform.security import (
        AzureSecurityClient,
        AzureSecurityConfig,
        ContentSafetyValidator,
        GuardrailsConfig,
    )

    # Security Client作成
    security_config = AzureSecurityConfig(
        content_safety_endpoint="https://xxx.cognitiveservices.azure.com",
        content_safety_api_key="xxx",
    )
    security_client = AzureSecurityClient(security_config)

    # GuardrailsConfig（DB等から取得した設定）
    guardrails = GuardrailsConfig(
        prompt_shield_enabled=True,
        moderation_threshold=2,
    )

    # Validator作成
    validator = ContentSafetyValidator(
        security_client=security_client,
        guardrails=guardrails,
    )

    # コンテンツ検証
    result = await validator.validate_and_sanitize(
        content="<コンテンツ>",
        source_type="web",
        source_url="https://example.com"
    )

    await security_client.close()
"""

import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from .base import (
    ContentModerationResult,
    PromptShieldResult,
    SecurityAPIError,
    SecurityClientProtocol,
)

logger = logging.getLogger(__name__)


@dataclass
class GuardrailsConfig:
    """Guardrails設定（DB guardrails_settings から取得）

    マーケットプレイス顧客が管理者UIから設定する値を想定。

    Attributes:
        prompt_shield_enabled: Prompt Shield有効化フラグ
        moderation_threshold: Moderationしきい値
            - 0: 無効
            - 2: 推奨（デフォルト）
            - 4: 緩い
            - 6: 極度のみ
        fail_on_error: エラー時に安全側に倒すかどうか（デフォルト: True）
        mark_content: 外部コンテンツにマーキングを追加するか
    """
    prompt_shield_enabled: bool = True
    moderation_threshold: int = 2
    fail_on_error: bool = True
    mark_content: bool = True

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GuardrailsConfig":
        """辞書から設定を作成

        Args:
            data: guardrails_settings辞書

        Returns:
            GuardrailsConfig instance
        """
        return cls(
            prompt_shield_enabled=data.get("prompt_shield_enabled", True),
            moderation_threshold=data.get("moderation_threshold", 2),
            fail_on_error=data.get("fail_on_error", True),
            mark_content=data.get("mark_content", True),
        )


@dataclass
class SanitizationResult:
    """サニタイズ結果

    Attributes:
        is_safe: コンテンツが安全かどうか
        marked_content: マーキング済みコンテンツ（unsafe時は空文字）
        metadata: 検証結果メタデータ
    """
    is_safe: bool
    marked_content: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


class ContentSafetyValidator:
    """外部コンテンツのセキュリティ検証とマーキング

    AzureSecurityClient（または他のSecurityClientProtocol実装）を使用し、
    guardrails_settingsに基づいてコンテンツを検証・マーキングします。

    マーケットプレイス顧客がDB設定に応じてセキュリティ強度を調整可能。

    Example:
        sanitizer = ContentSafetyValidator(
            security_client=azure_client,
            guardrails=GuardrailsConfig(
                prompt_shield_enabled=True,
                moderation_threshold=2,
            ),
        )

        result = await sanitizer.validate_and_sanitize(
            content="外部コンテンツ",
            source_type="web",
            source_url="https://example.com",
        )

        if result.is_safe:
            print(result.marked_content)
    """

    def __init__(
        self,
        security_client: SecurityClientProtocol,
        guardrails: Optional[GuardrailsConfig] = None,
    ):
        """
        Initialize External Content Sanitizer

        Args:
            security_client: SecurityClientProtocol実装（AzureSecurityClient等）
            guardrails: Guardrails設定（省略時はデフォルト値使用）
        """
        self._client = security_client
        self._guardrails = guardrails or GuardrailsConfig()

        logger.info(
            f"ContentSafetyValidator initialized - "
            f"prompt_shield={self._guardrails.prompt_shield_enabled}, "
            f"moderation_threshold={self._guardrails.moderation_threshold}"
        )

    @property
    def guardrails(self) -> GuardrailsConfig:
        """現在のguardrails設定を取得"""
        return self._guardrails

    def update_guardrails(self, guardrails: GuardrailsConfig) -> None:
        """guardrails設定を更新（動的設定変更対応）

        Args:
            guardrails: 新しいGuardrails設定
        """
        self._guardrails = guardrails
        logger.info(
            f"ContentSafetyValidator guardrails updated - "
            f"prompt_shield={guardrails.prompt_shield_enabled}, "
            f"moderation_threshold={guardrails.moderation_threshold}"
        )

    async def validate_and_sanitize(
        self,
        content: str,
        source_type: str,
        source_url: Optional[str] = None,
        user_prompt: Optional[str] = None,
    ) -> SanitizationResult:
        """
        外部コンテンツの検証とサニタイズ

        AzureSecurityClientを使用し、guardrails設定に基づいてコンテンツを検証。
        安全な場合はマーキング済みコンテンツを返却。

        Args:
            content: 外部から取得したコンテンツ
            source_type: コンテンツの種類 ("web", "browser", "api", "mcp")
            source_url: コンテンツの取得元URL（オプション）
            user_prompt: ユーザープロンプト（Prompt Shield検証用）

        Returns:
            SanitizationResult: 検証結果
        """
        if not content:
            return SanitizationResult(
                is_safe=True,
                marked_content="",
                metadata={"validation": "empty_content"},
            )

        metadata: Dict[str, Any] = {
            "source_type": source_type,
            "source_url": source_url,
            "content_length": len(content),
            "validation_passed": False,
            "guardrails": {
                "prompt_shield_enabled": self._guardrails.prompt_shield_enabled,
                "moderation_threshold": self._guardrails.moderation_threshold,
            },
        }

        try:
            # Step 1: Content Moderation（有害コンテンツ検出）
            if self._guardrails.moderation_threshold > 0:
                moderation_result = await self._client.check_content_moderation(
                    text=content,
                    threshold=self._guardrails.moderation_threshold,
                )

                metadata["moderation"] = {
                    "blocked": moderation_result.blocked,
                    "categories": {
                        cat.value: severity
                        for cat, severity in moderation_result.categories.items()
                    },
                }

                if moderation_result.blocked:
                    logger.warning(
                        f"ContentSafetyValidator: Content blocked by moderation "
                        f"in {source_type} from {source_url or 'unknown source'}"
                    )
                    return SanitizationResult(
                        is_safe=False,
                        marked_content="",
                        metadata=metadata,
                    )

                if moderation_result.error and self._guardrails.fail_on_error:
                    logger.error(
                        f"ContentSafetyValidator: Moderation error (fail-close) - "
                        f"{moderation_result.error}"
                    )
                    metadata["error"] = moderation_result.error
                    return SanitizationResult(
                        is_safe=False,
                        marked_content="",
                        metadata=metadata,
                    )

            # Step 2: Prompt Shield（Jailbreak攻撃検出）
            if self._guardrails.prompt_shield_enabled:
                # user_prompt または content をプロンプトとして使用
                # documents には外部コンテンツを渡す（間接的インジェクション検出用）
                shield_result = await self._client.check_prompt_shield(
                    user_prompt=user_prompt or content,
                    documents=[content],
                )

                metadata["prompt_shield"] = {
                    "attack_detected": shield_result.attack_detected,
                    "attack_type": shield_result.attack_type,
                }

                if shield_result.attack_detected:
                    logger.warning(
                        f"ContentSafetyValidator: Jailbreak attack detected "
                        f"in {source_type} from {source_url or 'unknown source'}"
                    )
                    return SanitizationResult(
                        is_safe=False,
                        marked_content="",
                        metadata=metadata,
                    )

                if shield_result.error and self._guardrails.fail_on_error:
                    # NOT_SUPPORTED (AWS/GCP等) は fail-close 対象外
                    if shield_result.error_code != "NOT_SUPPORTED":
                        logger.error(
                            f"ContentSafetyValidator: Prompt shield error (fail-close) - "
                            f"{shield_result.error}"
                        )
                        metadata["error"] = shield_result.error
                        return SanitizationResult(
                            is_safe=False,
                            marked_content="",
                            metadata=metadata,
                        )

        except SecurityAPIError as e:
            logger.error(f"ContentSafetyValidator: Security API error - {e}")
            metadata["error"] = str(e)
            if self._guardrails.fail_on_error:
                return SanitizationResult(
                    is_safe=False,
                    marked_content="",
                    metadata=metadata,
                )
        except Exception as e:
            logger.error(f"ContentSafetyValidator: Unexpected error - {e}")
            metadata["error"] = str(e)
            if self._guardrails.fail_on_error:
                return SanitizationResult(
                    is_safe=False,
                    marked_content="",
                    metadata=metadata,
                )

        # Step 3: Content marking（コンテンツの出典明示）
        if self._guardrails.mark_content:
            marked_content = self.mark_content(content, source_type, source_url)
        else:
            marked_content = content

        metadata["validation_passed"] = True
        logger.info(
            f"ContentSafetyValidator: Content validated successfully "
            f"({source_type}, {len(content)} chars)"
        )

        return SanitizationResult(
            is_safe=True,
            marked_content=marked_content,
            metadata=metadata,
        )

    async def validate_multiple(
        self,
        contents: List[Tuple[str, str, Optional[str]]],
        user_prompt: Optional[str] = None,
    ) -> Tuple[bool, List[str], List[Dict[str, Any]]]:
        """
        複数の外部コンテンツを一括検証

        Args:
            contents: [(content, source_type, source_url), ...] のリスト
            user_prompt: ユーザープロンプト（共通）

        Returns:
            Tuple[all_safe, marked_contents, metadata_list]:
                - all_safe: bool - 全て安全かどうか
                - marked_contents: List[str] - マーキング済みコンテンツリスト
                - metadata_list: List[Dict] - 各コンテンツの検証結果
        """
        marked_contents: List[str] = []
        metadata_list: List[Dict[str, Any]] = []
        all_safe = True

        for content, source_type, source_url in contents:
            result = await self.validate_and_sanitize(
                content=content,
                source_type=source_type,
                source_url=source_url,
                user_prompt=user_prompt,
            )

            if not result.is_safe:
                all_safe = False
                logger.warning(
                    f"ContentSafetyValidator: Blocked content from {source_type} "
                    f"({source_url or 'unknown'})"
                )

            marked_contents.append(result.marked_content)
            metadata_list.append(result.metadata)

        return all_safe, marked_contents, metadata_list

    @staticmethod
    def mark_content(
        content: str,
        source_type: str,
        source_url: Optional[str] = None,
    ) -> str:
        """
        外部コンテンツにソース情報をマーキング

        マーカー形式: [EXT:{source_type}|{source_url}]{content}[/EXT]
        - source_typeのみの場合: [EXT:WEB]{content}[/EXT]
        - URLありの場合: [EXT:WEB|https://example.com]{content}[/EXT]

        Args:
            content: 外部コンテンツ
            source_type: コンテンツの種類
            source_url: 取得元URL

        Returns:
            str: マーキング済みコンテンツ
        """
        source_label = source_type.upper()
        if source_url:
            source_label += f"|{source_url}"

        return f"[EXT:{source_label}]{content}[/EXT]"

    @staticmethod
    def unmark_content(marked_content: str) -> Tuple[str, Optional[str], Optional[str]]:
        """
        マーキング済みコンテンツからオリジナルコンテンツを抽出

        Args:
            marked_content: マーキング済みコンテンツ

        Returns:
            Tuple[content, source_type, source_url]:
                - content: オリジナルコンテンツ
                - source_type: コンテンツの種類（マーキングなしの場合None）
                - source_url: 取得元URL（なしの場合None）
        """
        import re

        pattern = r'\[EXT:([A-Z]+)(?:\|([^\]]+))?\](.*?)\[/EXT\]'
        match = re.match(pattern, marked_content, re.DOTALL)

        if not match:
            return marked_content, None, None

        source_type = match.group(1).lower()
        source_url = match.group(2)
        content = match.group(3)

        return content, source_type, source_url
