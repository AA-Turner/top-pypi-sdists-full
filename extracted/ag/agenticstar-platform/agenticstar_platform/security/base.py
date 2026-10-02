"""
AGENTICSTAR Platform SDK - Security Base
マルチクラウド対応セキュリティクライアントの基底クラス・インターフェース定義

サポートプロバイダー:
- Azure Content Safety + Language Service (PII)
- AWS Comprehend (PII + Content Moderation)
- Google Cloud DLP (PII)
"""

import logging
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Protocol, runtime_checkable

logger = logging.getLogger(__name__)


class SecurityProvider(str, Enum):
    """セキュリティプロバイダー種別"""
    AZURE = "azure"          # Azure Content Safety + Language Service
    AWS = "aws"              # AWS Comprehend
    GCP = "gcp"              # Google Cloud DLP


class ContentCategory(str, Enum):
    """有害コンテンツカテゴリ（プロバイダー共通）"""
    HATE = "hate"
    SEXUAL = "sexual"
    SELF_HARM = "self_harm"
    VIOLENCE = "violence"
    PROFANITY = "profanity"
    INSULT = "insult"
    THREAT = "threat"


class PIICategory(str, Enum):
    """PIIカテゴリ（プロバイダー共通・主要なもの）"""
    # 個人識別情報
    PERSON_NAME = "person_name"
    EMAIL = "email"
    PHONE_NUMBER = "phone_number"
    ADDRESS = "address"
    AGE = "age"
    DATE_OF_BIRTH = "date_of_birth"

    # 政府発行ID
    NATIONAL_ID = "national_id"
    PASSPORT_NUMBER = "passport_number"
    DRIVERS_LICENSE = "drivers_license"
    SOCIAL_SECURITY = "social_security"
    TAX_ID = "tax_id"

    # 金融情報
    CREDIT_CARD = "credit_card"
    BANK_ACCOUNT = "bank_account"
    SWIFT_CODE = "swift_code"
    IBAN = "iban"

    # 医療情報
    MEDICAL_RECORD = "medical_record"
    HEALTH_INSURANCE = "health_insurance"

    # 技術情報
    IP_ADDRESS = "ip_address"
    MAC_ADDRESS = "mac_address"
    URL = "url"

    # 認証情報
    PASSWORD = "password"
    API_KEY = "api_key"
    AWS_ACCESS_KEY = "aws_access_key"
    CONNECTION_STRING = "connection_string"

    # その他
    OTHER = "other"


class SecurityError(Exception):
    """Security操作の基底エラー"""
    pass


class SecurityConfigError(SecurityError):
    """Security設定エラー"""
    pass


class SecurityAPIError(SecurityError):
    """Security API呼び出しエラー"""

    def __init__(self, message: str, status_code: Optional[int] = None, error_code: str = "API_ERROR"):
        super().__init__(message)
        self.status_code = status_code
        self.error_code = error_code


# ============================================================
# Result Types
# ============================================================

@dataclass
class ContentModerationResult:
    """コンテンツモデレーション結果"""
    blocked: bool
    categories: Dict[ContentCategory, int] = field(default_factory=dict)  # category -> severity (0-6)
    threshold: int = 2
    raw_response: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    error_code: Optional[str] = None


@dataclass
class PromptShieldResult:
    """プロンプトシールド（Jailbreak攻撃検出）結果

    user_prompt_attack / documents_attack は攻撃経路の内訳（direct / indirect）。
    None は「未取得」（旧実装・旧プロバイダ経由）であり False（評価済み非検知）と
    区別すること。両方既知のとき attack_detected == (user_prompt_attack or
    documents_attack) が不変条件。
    """
    attack_detected: bool
    attack_type: Optional[str] = None  # jailbreak, injection, etc.
    confidence: float = 0.0
    raw_response: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    error_code: Optional[str] = None
    user_prompt_attack: Optional[bool] = None  # userPrompt 経由（direct）の検知
    documents_attack: Optional[bool] = None    # documents 経由（indirect）の検知


@dataclass
class PIIEntity:
    """検出されたPIIエンティティ"""
    category: PIICategory
    text: str
    offset: int
    length: int
    confidence: float
    provider_category: str = ""  # プロバイダー固有のカテゴリ名


@dataclass
class PIIDetectionResult:
    """PII検出結果"""
    success: bool
    masked_text: str = ""
    entities: List[PIIEntity] = field(default_factory=list)
    categories_detected: List[PIICategory] = field(default_factory=list)
    raw_response: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    error_code: Optional[str] = None


@dataclass
class SecurityCheckResult:
    """統合セキュリティチェック結果"""
    allowed: bool
    violations: List[str] = field(default_factory=list)
    content_moderation: Optional[ContentModerationResult] = None
    prompt_shield: Optional[PromptShieldResult] = None
    pii_detection: Optional[PIIDetectionResult] = None


# ============================================================
# Config Types
# ============================================================

@dataclass
class AzureSecurityConfig:
    """Azure Security設定

    Note:
        api_keyはrepr=Falseでログ出力から除外されます。
    """
    # Content Safety
    content_safety_endpoint: str
    content_safety_api_key: str = field(repr=False)

    # Language Service (PII)
    language_endpoint: Optional[str] = None
    language_api_key: Optional[str] = field(default=None, repr=False)

    # 共通オプション
    enabled: bool = True
    prompt_shield_enabled: bool = True
    moderation_enabled: bool = True
    moderation_threshold: int = 2  # 0=disabled, 2=recommended, 4=loose, 6=extreme_only
    pii_enabled: bool = True
    pii_confidence_threshold: float = 0.7
    pii_mask_string: str = "***"
    timeout: float = 30.0

    @property
    def provider(self) -> SecurityProvider:
        return SecurityProvider.AZURE

    def __str__(self) -> str:
        return (
            f"AzureSecurityConfig(content_safety_endpoint={self.content_safety_endpoint!r}, "
            f"language_endpoint={self.language_endpoint!r}, api_keys=***)"
        )


@dataclass
class AWSSecurityConfig:
    """AWS Bedrock Guardrails + Comprehend 設定

    Bedrock Guardrails: Content Moderation + Prompt Shield
    Comprehend: PII Detection

    Note:
        aws_access_key_id, aws_secret_access_keyはrepr=Falseでログ出力から除外されます。
        IRSA環境では空文字で渡し、boto3のデフォルト認証チェーンを使用します。
    """
    aws_access_key_id: str = field(default="", repr=False)
    aws_secret_access_key: str = field(default="", repr=False)
    region_name: str = "us-east-1"

    # Bedrock Guardrails設定
    guardrail_id: str = ""
    guardrail_version: str = "DRAFT"

    # PII 検出経路の選択 (Refs #1873)
    #   "bedrock_guardrails": Bedrock Guardrails sensitiveInformationPolicy
    #     (多言語対応: 日本語含む。guardrail_id / guardrail_version を流用)
    #   "comprehend": Amazon Comprehend DetectPiiEntities (en/es のみ。レガシー)
    # default は "bedrock_guardrails" (多言語対応が AWS デフォルト動作)。
    pii_service: str = "bedrock_guardrails"

    # 共通オプション
    enabled: bool = False
    prompt_shield_enabled: bool = True
    moderation_enabled: bool = True
    moderation_threshold: int = 2
    pii_enabled: bool = True
    pii_confidence_threshold: float = 0.7
    pii_mask_string: str = "***"
    timeout: float = 30.0

    @property
    def provider(self) -> SecurityProvider:
        return SecurityProvider.AWS

    def __str__(self) -> str:
        return (
            f"AWSSecurityConfig(region_name={self.region_name!r}, "
            f"guardrail_id={self.guardrail_id!r}, credentials=***)"
        )


@dataclass
class GCPSecurityConfig:
    """Google Cloud Content Safety + PII 設定

    Content Safety 経路は2種類:
      - Model Armor sanitizeUserPrompt (asia-northeast1/asia-southeast1 では
        Limited Support により Malicious URL / Multi-language 等が使えない)
      - Vertex AI Safety Filters + Gemini judge (全リージョンで多言語対応)

    PII は Cloud DLP を使用 (global endpoint で全リージョン利用可)。

    マーケットプレイス向け(全リージョンで機能落ちさせない)配布では
    content_safety_backend="vertex_ai_safety" を選択する。

    Note:
        credentials_path, credentials_jsonはrepr=Falseでログ出力から除外されます。
        Workload Identity環境ではcredentials指定不要（デフォルト認証を使用）。
    """
    project_id: str
    credentials_path: Optional[str] = field(default=None, repr=False)
    credentials_json: Optional[str] = field(default=None, repr=False)

    # Content Safety 経路の選択 (Refs #1952)
    #   "model_armor": Model Armor sanitizeUserPrompt (レガシー・一部リージョン制限あり)
    #   "vertex_ai_safety": Vertex AI Safety Filters + Gemini judge (全リージョン対応)
    content_safety_backend: str = "model_armor"

    # Model Armor設定
    model_armor_template: str = ""
    model_armor_region: str = ""

    # Vertex AI Safety Filters 設定 (Refs #1952)
    vertex_ai_location: str = "global"
    # HARM_CATEGORY_* → BLOCK_THRESHOLD のマップ。
    # 未指定時は Vertex AI のデフォルト (通常 BLOCK_MEDIUM_AND_ABOVE) を使う。
    vertex_harm_thresholds: Dict[str, str] = field(default_factory=dict)
    # Prompt Injection / Jailbreak 判定に使うGeminiモデル。
    # 空文字を渡しても _init_vertex_ai_clients が "gemini-2.5-flash" に
    # フォールバックするため judge は常に有効（judge を無効化する手段は現状なし）。
    vertex_judge_model: str = "gemini-2.5-flash"

    # Cloud DLP設定
    dlp_location: str = "global"

    # 共通オプション
    enabled: bool = False
    prompt_shield_enabled: bool = True
    moderation_enabled: bool = True
    moderation_threshold: int = 2
    pii_enabled: bool = True
    pii_confidence_threshold: float = 0.7
    pii_mask_string: str = "***"
    timeout: float = 30.0

    @property
    def provider(self) -> SecurityProvider:
        return SecurityProvider.GCP

    def __str__(self) -> str:
        return (
            f"GCPSecurityConfig(project_id={self.project_id!r}, "
            f"model_armor_template={self.model_armor_template!r}, credentials=***)"
        )


# Union type for configs
SecurityConfig = AzureSecurityConfig | AWSSecurityConfig | GCPSecurityConfig


# ============================================================
# Protocol / ABC
# ============================================================

@runtime_checkable
class SecurityClientProtocol(Protocol):
    """セキュリティクライアントプロトコル

    すべてのセキュリティプロバイダー実装が満たすべきインターフェース
    """

    @property
    def enabled(self) -> bool:
        """クライアントが有効かどうか"""
        ...

    @property
    def provider(self) -> SecurityProvider:
        """プロバイダー種別"""
        ...

    async def check_content_moderation(
        self,
        text: str,
        threshold: Optional[int] = None,
    ) -> ContentModerationResult:
        """有害コンテンツをチェック"""
        ...

    async def check_prompt_shield(
        self,
        user_prompt: str,
        documents: Optional[List[str]] = None,
    ) -> PromptShieldResult:
        """Jailbreak攻撃を検出"""
        ...

    async def detect_pii(
        self,
        text: str,
        mask: bool = True,
        language: str = "ja",
        confidence_threshold: Optional[float] = None,
    ) -> PIIDetectionResult:
        """PIIを検出・マスク

        confidence_threshold が None の場合は config の pii_confidence_threshold を使う。
        クライアントを使い回しつつリクエスト毎に閾値を変えたい場合に指定する。
        """
        ...

    async def check_security(
        self,
        text: str,
        check_moderation: bool = True,
        check_prompt_shield: bool = True,
        check_pii: bool = False,
        fail_on_error: bool = True,
    ) -> SecurityCheckResult:
        """統合セキュリティチェック（fail_on_error=True: エラー時は安全側に倒す）"""
        ...

    async def close(self) -> None:
        """クライアントリソースをクローズ"""
        ...


class SecurityClientBase(ABC):
    """セキュリティクライアント基底クラス

    共通のユーティリティメソッドを提供

    Example:
        async with AzureSecurityClient(config) as client:
            result = await client.check_security(text)
    """

    def __init__(self, config: SecurityConfig):
        self._config = config
        self._enabled = False

    async def __aenter__(self) -> "SecurityClientBase":
        """Context Manager: 開始時の処理"""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context Manager: 終了時にリソースをクローズ"""
        await self.close()

    @property
    def enabled(self) -> bool:
        return self._enabled

    @property
    @abstractmethod
    def provider(self) -> SecurityProvider:
        """プロバイダー種別"""
        pass

    def _get_api_key(self, value: Any) -> str:
        """APIキーを取得（SecretStr対応）"""
        if hasattr(value, 'get_secret_value'):
            return value.get_secret_value()
        return str(value) if value else ""

    def _normalize_content_category(self, provider_category: str) -> ContentCategory:
        """プロバイダー固有カテゴリを共通カテゴリに正規化"""
        mapping = {
            # Azure
            "hate": ContentCategory.HATE,
            "sexual": ContentCategory.SEXUAL,
            "selfharm": ContentCategory.SELF_HARM,
            "self_harm": ContentCategory.SELF_HARM,
            "violence": ContentCategory.VIOLENCE,
            # AWS
            "hate_speech": ContentCategory.HATE,
            "sexual_content": ContentCategory.SEXUAL,
            "self-harm": ContentCategory.SELF_HARM,
            "violent_content": ContentCategory.VIOLENCE,
            "profanity": ContentCategory.PROFANITY,
            "insult": ContentCategory.INSULT,
            # GCP - future
        }
        return mapping.get(provider_category.lower(), ContentCategory.HATE)

    def _normalize_pii_category(self, provider_category: str) -> PIICategory:
        """プロバイダー固有PIIカテゴリを共通カテゴリに正規化"""
        # Azure / AWS / GCP のPIIカテゴリをマッピング
        mapping = {
            # Person
            "person": PIICategory.PERSON_NAME,
            "name": PIICategory.PERSON_NAME,

            # Contact
            "email": PIICategory.EMAIL,
            "phonenumber": PIICategory.PHONE_NUMBER,
            "phone_number": PIICategory.PHONE_NUMBER,
            "address": PIICategory.ADDRESS,
            "age": PIICategory.AGE,

            # Government ID
            "usnationalid": PIICategory.NATIONAL_ID,
            "jpnationalid": PIICategory.NATIONAL_ID,
            "national_id": PIICategory.NATIONAL_ID,
            "jpmynumberpersonal": PIICategory.NATIONAL_ID,
            "uspassportnumber": PIICategory.PASSPORT_NUMBER,
            "jppassportnumber": PIICategory.PASSPORT_NUMBER,
            "passport": PIICategory.PASSPORT_NUMBER,
            "usdriverslicensenumber": PIICategory.DRIVERS_LICENSE,
            "jpdriverslicensenumber": PIICategory.DRIVERS_LICENSE,
            "drivers_license": PIICategory.DRIVERS_LICENSE,
            "ussocialsecuritynumber": PIICategory.SOCIAL_SECURITY,
            "jpsocialinsurancenumber": PIICategory.SOCIAL_SECURITY,
            "ssn": PIICategory.SOCIAL_SECURITY,

            # Financial
            "creditcardnumber": PIICategory.CREDIT_CARD,
            "credit_card": PIICategory.CREDIT_CARD,
            "usbankaccountnumber": PIICategory.BANK_ACCOUNT,
            "jpbankaccountnumber": PIICategory.BANK_ACCOUNT,
            "bank_account": PIICategory.BANK_ACCOUNT,
            "swiftcode": PIICategory.SWIFT_CODE,
            "internationalbankingaccountnumber": PIICategory.IBAN,
            "iban": PIICategory.IBAN,

            # Health
            "medical_record_number": PIICategory.MEDICAL_RECORD,
            "health_insurance_id": PIICategory.HEALTH_INSURANCE,

            # Tech
            "ipaddress": PIICategory.IP_ADDRESS,
            "ip_address": PIICategory.IP_ADDRESS,
            "mac_address": PIICategory.MAC_ADDRESS,
            "url": PIICategory.URL,

            # Credentials
            "password": PIICategory.PASSWORD,
            "aws_access_key": PIICategory.AWS_ACCESS_KEY,
            "sqlserverconnectionstring": PIICategory.CONNECTION_STRING,
        }

        normalized = provider_category.lower().replace(" ", "").replace("_", "")
        for key, value in mapping.items():
            if key.replace("_", "") in normalized:
                return value
        return PIICategory.OTHER

    # ================================================================
    # 日本語PII正規表現補完レイヤー（全プロバイダー共通）
    # ================================================================

    # 日本固有PIIの正規表現パターン
    _JP_PII_PATTERNS: List[tuple] = [
        # マイナンバー（個人番号12桁）— 前後にキーワードがある場合のみ
        (
            re.compile(
                r'(?:マイナンバー|個人番号|my\s*number)[：:\s]*(\d{4}\s?\d{4}\s?\d{4})',
                re.IGNORECASE,
            ),
            PIICategory.NATIONAL_ID,
            "JP_MY_NUMBER_PERSONAL",
        ),
        # 法人番号（13桁）
        (
            re.compile(
                r'(?:法人番号|corporate\s*number)[：:\s]*(\d{13})',
                re.IGNORECASE,
            ),
            PIICategory.NATIONAL_ID,
            "JP_CORPORATE_NUMBER",
        ),
        # 日本の郵便番号（〒XXX-XXXX or XXX-XXXX）
        (
            re.compile(r'〒?\d{3}-\d{4}'),
            PIICategory.ADDRESS,
            "JP_POSTAL_CODE",
        ),
        # 日本の電話番号（固定電話: 0X-XXXX-XXXX, 携帯: 0X0-XXXX-XXXX）
        (
            re.compile(r'0\d{1,4}-\d{1,4}-\d{3,4}'),
            PIICategory.PHONE_NUMBER,
            "JP_PHONE_NUMBER",
        ),
        # 日本のパスポート番号（2文字+7桁）
        (
            re.compile(
                r'(?:パスポート|旅券|passport)[：:\s]*([A-Z]{2}\d{7})',
                re.IGNORECASE,
            ),
            PIICategory.PASSPORT_NUMBER,
            "JP_PASSPORT_NUMBER",
        ),
        # 日本の運転免許証番号（12桁数字）
        (
            re.compile(
                r'(?:免許証|運転免許|driver.?s?\s*license)[：:\s]*(\d{12})',
                re.IGNORECASE,
            ),
            PIICategory.DRIVERS_LICENSE,
            "JP_DRIVERS_LICENSE",
        ),
    ]

    def _detect_pii_by_regex(self, text: str) -> List["PIIEntity"]:
        """正規表現による日本語PII補完検出

        各プロバイダーのdetect_pii()結果を補完するために使用。
        パターンが明確な日本固有PIIを正規表現で検出する。

        Args:
            text: 検出対象テキスト

        Returns:
            検出されたPIIEntityのリスト
        """
        entities = []
        for pattern, category, provider_category in self._JP_PII_PATTERNS:
            for match in pattern.finditer(text):
                # グループがある場合はグループ1（PII値本体）、なければマッチ全体
                if match.lastindex and match.lastindex >= 1:
                    start = match.start(1)
                    end = match.end(1)
                    entity_text = match.group(1)
                else:
                    start = match.start()
                    end = match.end()
                    entity_text = match.group()

                entities.append(PIIEntity(
                    category=category,
                    text=entity_text,
                    offset=start,
                    length=end - start,
                    confidence=0.9,
                    provider_category=provider_category,
                ))
        return entities

    def _merge_pii_entities(
        self,
        provider_entities: List["PIIEntity"],
        regex_entities: List["PIIEntity"],
    ) -> List["PIIEntity"]:
        """プロバイダー検出結果と正規表現検出結果をマージ（重複排除）

        オフセット範囲が重複するエンティティはプロバイダー側を優先する。

        Args:
            provider_entities: プロバイダーAPI由来のエンティティ
            regex_entities: 正規表現由来のエンティティ

        Returns:
            マージ済みのエンティティリスト
        """
        if not regex_entities:
            return provider_entities

        merged = list(provider_entities)

        for regex_entity in regex_entities:
            r_start = regex_entity.offset
            r_end = r_start + regex_entity.length

            # プロバイダー検出済みエンティティとオフセット範囲が重複するか確認
            is_duplicate = False
            for existing in provider_entities:
                e_start = existing.offset
                e_end = e_start + existing.length
                if r_start < e_end and r_end > e_start:
                    is_duplicate = True
                    break

            if not is_duplicate:
                merged.append(regex_entity)

        return merged

    # ================================================================
    # Abstract methods
    # ================================================================

    @abstractmethod
    async def check_content_moderation(
        self,
        text: str,
        threshold: Optional[int] = None,
    ) -> ContentModerationResult:
        pass

    @abstractmethod
    async def check_prompt_shield(
        self,
        user_prompt: str,
        documents: Optional[List[str]] = None,
    ) -> PromptShieldResult:
        pass

    @abstractmethod
    async def detect_pii(
        self,
        text: str,
        mask: bool = True,
        language: str = "ja",
        confidence_threshold: Optional[float] = None,
    ) -> PIIDetectionResult:
        pass

    async def detect_pii_batch(
        self,
        texts: List[str],
        mask: bool = True,
        language: str = "ja",
        confidence_threshold: Optional[float] = None,
    ) -> List[PIIDetectionResult]:
        """複数テキストの PII 検出（デフォルト実装: detect_pii の逐次呼び出し）。

        プロバイダ側にバッチ API がある場合はオーバーライドして呼び出し回数を削減する
        （Azure Language は 5 documents/request を許容）。結果は texts と同順・同長で、
        失敗はテキスト単位の PIIDetectionResult(success=False) として返す（例外にしない）。
        """
        return [
            await self.detect_pii(
                t, mask=mask, language=language, confidence_threshold=confidence_threshold
            )
            for t in texts
        ]

    async def check_security(
        self,
        text: str,
        check_moderation: bool = True,
        check_prompt_shield: bool = True,
        check_pii: bool = False,
        fail_on_error: bool = True,
    ) -> SecurityCheckResult:
        """統合セキュリティチェック（デフォルト実装）

        Args:
            text: チェック対象テキスト
            check_moderation: 有害コンテンツチェックを行うか
            check_prompt_shield: Jailbreak攻撃検出を行うか
            check_pii: PII検出を行うか
            fail_on_error: エラー時にviolationとするか（デフォルト: True = fail-close）

        Returns:
            SecurityCheckResult: 統合セキュリティチェック結果

        Note:
            fail_on_error=Trueの場合、セキュリティチェックでエラーが発生すると
            「安全側に倒す」動作となり、コンテンツは許可されません。
            本番環境では常にfail_on_error=Trueを推奨します。
        """
        violations = []
        moderation_result = None
        shield_result = None
        pii_result = None

        # Content Moderation
        if check_moderation:
            moderation_result = await self.check_content_moderation(text)
            if moderation_result.blocked:
                violations.append("harmful_content")
            elif moderation_result.error and fail_on_error:
                violations.append("moderation_error")
                logger.warning(f"Content moderation failed (fail-close): {moderation_result.error}")

        # Prompt Shield
        if check_prompt_shield:
            shield_result = await self.check_prompt_shield(text)
            if shield_result.attack_detected:
                violations.append("jailbreak_attack")
            elif shield_result.error and fail_on_error:
                # NOT_SUPPORTED (AWS/GCP) は fail-close 対象外
                if shield_result.error_code != "NOT_SUPPORTED":
                    violations.append("prompt_shield_error")
                    logger.warning(f"Prompt shield failed (fail-close): {shield_result.error}")

        # PII Detection
        if check_pii:
            pii_result = await self.detect_pii(text, mask=True)
            if pii_result.entities:
                violations.append("pii_detected")
            elif not pii_result.success and fail_on_error:
                # PII検出エラー時は安全側に倒す（潜在的PII漏洩防止）
                violations.append("pii_detection_error")
                logger.warning(f"PII detection failed (fail-close): {pii_result.error}")

        return SecurityCheckResult(
            allowed=len(violations) == 0,
            violations=violations,
            content_moderation=moderation_result,
            prompt_shield=shield_result,
            pii_detection=pii_result,
        )

    @abstractmethod
    async def close(self) -> None:
        pass
