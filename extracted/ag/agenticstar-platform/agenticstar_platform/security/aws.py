"""
AGENTICSTAR Platform SDK - AWS Security Client
AWS Bedrock Guardrails + Comprehend 統合クライアント

機能:
- Content Moderation: Bedrock Guardrails ApplyGuardrail API
- Prompt Shield: Bedrock Guardrails PROMPT_ATTACK フィルタ
- PII Detection: Comprehend DetectPiiEntities API

Example:
    config = AWSSecurityConfig(
        region_name="us-east-1",
        guardrail_id="guardrail-xxxxx",
    )
    client = AWSSecurityClient(config)

    # Content Moderation + Prompt Shield (Bedrock Guardrails)
    result = await client.check_content_moderation("some text", threshold=2)
    shield = await client.check_prompt_shield("user prompt")

    # PII Detection (Comprehend)
    pii = await client.detect_pii("My SSN is 123-45-6789")
    print(pii.masked_text)

    await client.close()
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional

from .base import (
    AWSSecurityConfig,
    ContentCategory,
    ContentModerationResult,
    PIICategory,
    PIIDetectionResult,
    PIIEntity,
    PromptShieldResult,
    SecurityAPIError,
    SecurityClientBase,
    SecurityConfigError,
    SecurityProvider,
)

logger = logging.getLogger(__name__)

# boto3 availability check
try:
    import boto3
    from botocore.exceptions import ClientError
    BOTO3_AVAILABLE = True
except ImportError:
    boto3 = None
    ClientError = Exception
    BOTO3_AVAILABLE = False

# Bedrock Guardrails のアクション → ContentCategory マッピング
_BEDROCK_CATEGORY_MAP = {
    "HATE": ContentCategory.HATE,
    "INSULTS": ContentCategory.INSULT,
    "SEXUAL": ContentCategory.SEXUAL,
    "VIOLENCE": ContentCategory.VIOLENCE,
    "MISCONDUCT": ContentCategory.SELF_HARM,
    "PROMPT_ATTACK": ContentCategory.THREAT,
}

# Bedrock Guardrails の強度 → 数値スコアマッピング
_BEDROCK_STRENGTH_SCORE = {
    "NONE": 0,
    "LOW": 2,
    "MEDIUM": 4,
    "HIGH": 6,
}

# Comprehend PII タイプ → PIICategory マッピング
_COMPREHEND_PII_MAP = {
    "NAME": PIICategory.PERSON_NAME,
    "EMAIL": PIICategory.EMAIL,
    "PHONE": PIICategory.PHONE_NUMBER,
    "ADDRESS": PIICategory.ADDRESS,
    "AGE": PIICategory.AGE,
    "DATE_TIME": PIICategory.DATE_OF_BIRTH,
    "PASSPORT_NUMBER": PIICategory.PASSPORT_NUMBER,
    "DRIVER_ID": PIICategory.DRIVERS_LICENSE,
    "US_SOCIAL_SECURITY_NUMBER": PIICategory.SOCIAL_SECURITY,
    "SSN": PIICategory.SOCIAL_SECURITY,
    "CREDIT_DEBIT_NUMBER": PIICategory.CREDIT_CARD,
    "CREDIT_DEBIT_CVV": PIICategory.CREDIT_CARD,
    "CREDIT_DEBIT_EXPIRY": PIICategory.CREDIT_CARD,
    "BANK_ACCOUNT_NUMBER": PIICategory.BANK_ACCOUNT,
    "BANK_ROUTING": PIICategory.BANK_ACCOUNT,
    "SWIFT_CODE": PIICategory.SWIFT_CODE,
    "INTERNATIONAL_BANK_ACCOUNT_NUMBER": PIICategory.IBAN,
    "IP_ADDRESS": PIICategory.IP_ADDRESS,
    "MAC_ADDRESS": PIICategory.MAC_ADDRESS,
    "URL": PIICategory.URL,
    "PASSWORD": PIICategory.PASSWORD,
    "PIN": PIICategory.PASSWORD,
    "AWS_ACCESS_KEY": PIICategory.AWS_ACCESS_KEY,
    "AWS_SECRET_KEY": PIICategory.AWS_ACCESS_KEY,
    "USERNAME": PIICategory.PERSON_NAME,
}

# Bedrock Guardrails sensitiveInformationPolicy PII タイプ → PIICategory マッピング
# (Comprehend と type 名が異なる: CREDIT_DEBIT_CARD_NUMBER vs CREDIT_DEBIT_NUMBER 等)
_BEDROCK_PII_MAP = {
    "NAME": PIICategory.PERSON_NAME,
    "EMAIL": PIICategory.EMAIL,
    "PHONE": PIICategory.PHONE_NUMBER,
    "ADDRESS": PIICategory.ADDRESS,
    "USERNAME": PIICategory.OTHER,
    "PASSWORD": PIICategory.PASSWORD,
    "CREDIT_DEBIT_CARD_NUMBER": PIICategory.CREDIT_CARD,
    "CREDIT_DEBIT_CARD_CVV": PIICategory.CREDIT_CARD,
    "CREDIT_DEBIT_CARD_EXPIRY": PIICategory.CREDIT_CARD,
    "PIN": PIICategory.PASSWORD,
    "IP_ADDRESS": PIICategory.IP_ADDRESS,
    "MAC_ADDRESS": PIICategory.MAC_ADDRESS,
    "URL": PIICategory.URL,
    "AWS_ACCESS_KEY": PIICategory.AWS_ACCESS_KEY,
    "AWS_SECRET_KEY": PIICategory.API_KEY,
    "DRIVER_ID": PIICategory.DRIVERS_LICENSE,
    "LICENSE_PLATE": PIICategory.OTHER,
    "VEHICLE_IDENTIFICATION_NUMBER": PIICategory.OTHER,
    "INTERNATIONAL_BANK_ACCOUNT_NUMBER": PIICategory.IBAN,
    "SWIFT_CODE": PIICategory.SWIFT_CODE,
    "US_BANK_ACCOUNT_NUMBER": PIICategory.BANK_ACCOUNT,
    "US_BANK_ROUTING_NUMBER": PIICategory.BANK_ACCOUNT,
    "US_INDIVIDUAL_TAX_IDENTIFICATION_NUMBER": PIICategory.TAX_ID,
    "US_PASSPORT_NUMBER": PIICategory.PASSPORT_NUMBER,
    "US_SOCIAL_SECURITY_NUMBER": PIICategory.SOCIAL_SECURITY,
    "CA_HEALTH_NUMBER": PIICategory.HEALTH_INSURANCE,
    "CA_SOCIAL_INSURANCE_NUMBER": PIICategory.NATIONAL_ID,
    "UK_NATIONAL_HEALTH_SERVICE_NUMBER": PIICategory.HEALTH_INSURANCE,
    "UK_NATIONAL_INSURANCE_NUMBER": PIICategory.NATIONAL_ID,
    "UK_UNIQUE_TAXPAYER_REFERENCE_NUMBER": PIICategory.TAX_ID,
}


class AWSSecurityClient(SecurityClientBase):
    """
    AWS Bedrock Guardrails + Comprehend セキュリティクライアント

    Bedrock Guardrails: Content Moderation (ApplyGuardrail) + Prompt Shield (PROMPT_ATTACK)
    Comprehend: PII Detection (DetectPiiEntities)

    IRSA環境ではcredentials不要（boto3のデフォルト認証チェーンを使用）。

    Example:
        config = AWSSecurityConfig(
            region_name="us-east-1",
            guardrail_id="guardrail-xxxxx",
            enabled=True,
        )
        client = AWSSecurityClient(config)
        result = await client.check_security("user input")
    """

    def __init__(self, config: AWSSecurityConfig):
        super().__init__(config)

        if not BOTO3_AVAILABLE:
            raise SecurityConfigError(
                "boto3 package is not installed. "
                "Install with: pip install boto3"
            )

        self._aws_config: AWSSecurityConfig = config
        self._comprehend_client = None
        self._bedrock_runtime_client = None

        try:
            # IRSA環境ではcredentialsが空のため、デフォルト認証チェーンを使用
            if config.aws_access_key_id and config.aws_secret_access_key:
                session = boto3.Session(
                    aws_access_key_id=self._get_api_key(config.aws_access_key_id),
                    aws_secret_access_key=self._get_api_key(config.aws_secret_access_key),
                    region_name=config.region_name,
                )
            else:
                session = boto3.Session(region_name=config.region_name)

            self._comprehend_client = session.client('comprehend')

            if config.guardrail_id:
                self._bedrock_runtime_client = session.client('bedrock-runtime')

            self._enabled = config.enabled

            logger.info(
                f"AWSSecurityClient initialized - region={config.region_name}, "
                f"guardrail_id={config.guardrail_id or 'none'}"
            )

        except Exception as e:
            logger.error(f"Failed to initialize AWS client: {e}")
            raise SecurityConfigError(f"Failed to initialize AWS client: {e}") from e

    @property
    def provider(self) -> SecurityProvider:
        return SecurityProvider.AWS

    async def check_content_moderation(
        self,
        text: str,
        threshold: Optional[int] = None,
    ) -> ContentModerationResult:
        """
        有害コンテンツをチェック（Bedrock Guardrails ApplyGuardrail）

        Bedrock Guardrails の Content Filters を使用して有害コンテンツを検出。
        guardrail_id が未設定の場合は NOT_CONFIGURED を返す。

        Args:
            text: チェック対象テキスト
            threshold: しきい値（0=無効, 2=LOW, 4=MEDIUM, 6=HIGH）

        Returns:
            ContentModerationResult
        """
        if not self._bedrock_runtime_client or not self._aws_config.guardrail_id:
            return ContentModerationResult(
                blocked=False,
                error="Bedrock Guardrails not configured (guardrail_id is empty)",
                error_code="NOT_CONFIGURED",
            )

        effective_threshold = threshold if threshold is not None else self._aws_config.moderation_threshold
        if effective_threshold == 0:
            return ContentModerationResult(blocked=False, threshold=0)

        try:
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self._bedrock_runtime_client.apply_guardrail(
                    guardrailIdentifier=self._aws_config.guardrail_id,
                    guardrailVersion=self._aws_config.guardrail_version,
                    source="INPUT",
                    content=[{"text": {"text": text}}],
                ),
            )

            action = response.get("action", "NONE")
            blocked = action == "GUARDRAIL_INTERVENED"

            # カテゴリ別スコアを抽出
            categories: Dict[ContentCategory, int] = {}
            for assessment in response.get("assessments", []):
                for filter_result in assessment.get("contentPolicy", {}).get("filters", []):
                    filter_type = filter_result.get("type", "")
                    confidence = filter_result.get("confidence", "NONE")
                    score = _BEDROCK_STRENGTH_SCORE.get(confidence, 0)
                    category = _BEDROCK_CATEGORY_MAP.get(filter_type)
                    if category:
                        categories[category] = score

            return ContentModerationResult(
                blocked=blocked,
                categories=categories,
                threshold=effective_threshold,
                raw_response=response,
            )

        except ClientError as e:
            logger.error(f"Bedrock Guardrails API error: {e}")
            raise SecurityAPIError(str(e), error_code="API_ERROR")
        except Exception as e:
            logger.error(f"Bedrock Guardrails unexpected error: {e}")
            raise SecurityAPIError(str(e), error_code="UNKNOWN_ERROR")

    async def check_prompt_shield(
        self,
        user_prompt: str,
        documents: Optional[List[str]] = None,
    ) -> PromptShieldResult:
        """
        Jailbreak攻撃を検出（Bedrock Guardrails PROMPT_ATTACK フィルタ）

        Bedrock Guardrails の PROMPT_ATTACK カテゴリで
        Jailbreak + Prompt Injection の両方を検知。
        guardrail_id が未設定の場合は NOT_CONFIGURED を返す。

        Args:
            user_prompt: ユーザープロンプト
            documents: ドキュメント内容（オプション）

        Returns:
            PromptShieldResult
        """
        if not self._bedrock_runtime_client or not self._aws_config.guardrail_id:
            return PromptShieldResult(
                attack_detected=False,
                error="Bedrock Guardrails not configured (guardrail_id is empty)",
                error_code="NOT_CONFIGURED",
            )

        try:
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self._bedrock_runtime_client.apply_guardrail(
                    guardrailIdentifier=self._aws_config.guardrail_id,
                    guardrailVersion=self._aws_config.guardrail_version,
                    source="INPUT",
                    content=[{"text": {"text": user_prompt}}],
                ),
            )

            # PROMPT_ATTACK の検出を確認
            attack_detected = False
            attack_type = None
            confidence = 0.0

            for assessment in response.get("assessments", []):
                for filter_result in assessment.get("contentPolicy", {}).get("filters", []):
                    if filter_result.get("type") == "PROMPT_ATTACK":
                        filter_action = filter_result.get("action", "NONE")
                        if filter_action == "BLOCKED":
                            attack_detected = True
                            attack_type = "prompt_attack"
                            filter_confidence = filter_result.get("confidence", "NONE")
                            confidence = _BEDROCK_STRENGTH_SCORE.get(filter_confidence, 0) / 6.0

            return PromptShieldResult(
                attack_detected=attack_detected,
                attack_type=attack_type,
                confidence=confidence,
                raw_response=response,
            )

        except ClientError as e:
            logger.error(f"Bedrock Guardrails Prompt Shield error: {e}")
            raise SecurityAPIError(str(e), error_code="API_ERROR")
        except Exception as e:
            logger.error(f"Bedrock Guardrails Prompt Shield unexpected error: {e}")
            raise SecurityAPIError(str(e), error_code="UNKNOWN_ERROR")

    async def detect_pii(
        self,
        text: str,
        mask: bool = True,
        language: str = "ja",
        confidence_threshold: Optional[float] = None,
    ) -> PIIDetectionResult:
        """
        PIIを検出・マスク

        pii_service の値で経路を切り替える (Refs #1873):
          - "bedrock_guardrails": Bedrock Guardrails sensitiveInformationPolicy
            (多言語対応。日本語含む)
          - "comprehend" (default): Amazon Comprehend DetectPiiEntities
            (en/es のみ対応。それ以外の言語は en にフォールバック)

        Args:
            text: 検出対象テキスト
            mask: マスキングを行うか
            language: 言語コード（ja, en 等）。bedrock_guardrails 経路では参照しない
            confidence_threshold: 信頼度閾値。Noneの場合は config の pii_confidence_threshold を使う

        Returns:
            PIIDetectionResult
        """
        threshold = (
            confidence_threshold
            if confidence_threshold is not None
            else self._aws_config.pii_confidence_threshold
        )

        if self._aws_config.pii_service == "bedrock_guardrails":
            return await self._detect_pii_via_bedrock_guardrail(text)

        if not self._comprehend_client:
            return PIIDetectionResult(
                success=False,
                masked_text="",
                error="Comprehend client not initialized",
                error_code="NOT_CONFIGURED",
            )

        # Comprehend DetectPiiEntities の実対応言語は en / es のみ。
        # それ以外 (ja, fr 等) は API が ValidationException を返すため en にフォールバック。
        # 多言語 PII マスキングが必要な場合は pii_service="bedrock_guardrails" を使う。
        supported_languages = {"en", "es"}
        if language not in supported_languages:
            language = "en"

        try:
            # Comprehend DetectPiiEntities の制限: 最大100,000バイト（UTF-8）
            # 超過する場合はチャンク分割して処理
            max_bytes = 100000
            text_bytes = text.encode("utf-8")

            if len(text_bytes) <= max_bytes:
                chunks = [(text, 0)]
            else:
                chunks = self._split_text_into_chunks(text, max_bytes)
                logger.info(f"Text split into {len(chunks)} chunks for Comprehend API limit")

            all_entities: List[PIIEntity] = []

            for chunk_text, chunk_offset in chunks:
                response = await asyncio.get_event_loop().run_in_executor(
                    None,
                    lambda ct=chunk_text, lang=language: self._comprehend_client.detect_pii_entities(
                        Text=ct,
                        LanguageCode=lang,
                    ),
                )

                for entity in response.get("Entities", []):
                    score = entity.get("Score", 0.0)
                    if score < threshold:
                        continue

                    pii_type = entity.get("Type", "OTHER")
                    begin = entity.get("BeginOffset", 0) + chunk_offset
                    end = entity.get("EndOffset", 0) + chunk_offset
                    entity_text = text[begin:end]

                    category = _COMPREHEND_PII_MAP.get(pii_type, PIICategory.OTHER)

                    all_entities.append(PIIEntity(
                        category=category,
                        text=entity_text,
                        offset=begin,
                        length=end - begin,
                        confidence=score,
                        provider_category=pii_type,
                    ))

            # 正規表現による日本語PII補完（全クラウド共通）
            regex_entities = self._detect_pii_by_regex(text)
            entities = self._merge_pii_entities(all_entities, regex_entities)

            # マスキング（降順でオフセット処理して位置ずれ防止）
            masked_text = text
            if mask and entities:
                for entity in sorted(entities, key=lambda e: e.offset, reverse=True):
                    start = entity.offset
                    end = entity.offset + entity.length
                    masked_text = masked_text[:start] + self._aws_config.pii_mask_string + masked_text[end:]

            categories_detected = list({e.category for e in entities})

            return PIIDetectionResult(
                success=True,
                masked_text=masked_text,
                entities=entities,
                categories_detected=categories_detected,
            )

        except ClientError as e:
            error_msg = f"Comprehend PII detection error: {e}"
            logger.error(error_msg)
            return PIIDetectionResult(
                success=False,
                masked_text="",
                error=error_msg,
                error_code="API_ERROR",
            )
        except Exception as e:
            error_msg = f"Comprehend PII detection unexpected error: {e}"
            logger.error(error_msg)
            return PIIDetectionResult(
                success=False,
                masked_text="",
                error=error_msg,
                error_code="UNEXPECTED_ERROR",
            )

    async def _detect_pii_via_bedrock_guardrail(self, text: str) -> PIIDetectionResult:
        """Bedrock Guardrails sensitiveInformationPolicy 経由で PII を検出・マスク

        AWS Comprehend は en/es しか対応していないため、多言語 (日本語含む) の
        PII マスキングは Bedrock Guardrails の sensitiveInformationPolicy で行う。

        ApplyGuardrail API は source=OUTPUT で叩いたとき sensitiveInformationPolicy
        が engage する (source=INPUT では engage しない) ため、常に OUTPUT で呼ぶ。

        Refs #1873
        """
        if not self._bedrock_runtime_client or not self._aws_config.guardrail_id:
            return PIIDetectionResult(
                success=False,
                masked_text="",
                error="Bedrock Guardrails not configured (guardrail_id is empty)",
                error_code="NOT_CONFIGURED",
            )

        if not text:
            return PIIDetectionResult(success=True, masked_text="")

        try:
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self._bedrock_runtime_client.apply_guardrail(
                    guardrailIdentifier=self._aws_config.guardrail_id,
                    guardrailVersion=self._aws_config.guardrail_version,
                    source="OUTPUT",
                    content=[{"text": {"text": text}}],
                ),
            )
        except ClientError as e:
            error_msg = f"Bedrock Guardrails PII detection error: {e}"
            logger.error(error_msg)
            return PIIDetectionResult(
                success=False,
                masked_text="",
                error=error_msg,
                error_code="API_ERROR",
            )
        except Exception as e:
            error_msg = f"Bedrock Guardrails PII detection unexpected error: {e}"
            logger.error(error_msg)
            return PIIDetectionResult(
                success=False,
                masked_text="",
                error=error_msg,
                error_code="UNEXPECTED_ERROR",
            )

        action = response.get("action", "NONE")
        outputs = response.get("outputs", [])
        masked_text = outputs[0].get("text", "") if outputs else ""

        if action == "NONE":
            return PIIDetectionResult(
                success=True,
                masked_text=text,
                entities=[],
                categories_detected=[],
                raw_response=response,
            )

        entities: List[PIIEntity] = []
        for assessment in response.get("assessments", []):
            sip = assessment.get("sensitiveInformationPolicy") or {}
            for pii in sip.get("piiEntities", []):
                if not pii.get("detected"):
                    continue
                pii_type = pii.get("type", "OTHER")
                match_text = pii.get("match", "")
                category = _BEDROCK_PII_MAP.get(pii_type, PIICategory.OTHER)
                entities.append(
                    PIIEntity(
                        category=category,
                        text=match_text,
                        offset=0,
                        length=len(match_text),
                        confidence=1.0,
                        provider_category=pii_type,
                    )
                )

        categories_detected = list({e.category for e in entities})

        return PIIDetectionResult(
            success=True,
            masked_text=masked_text or text,
            entities=entities,
            categories_detected=categories_detected,
            raw_response=response,
        )

    @staticmethod
    def _split_text_into_chunks(text: str, max_bytes: int) -> List[tuple]:
        """テキストをバイト数上限でチャンク分割する

        文の区切り（句点・改行）を優先して分割し、PIIが分断されるリスクを軽減する。

        Args:
            text: 分割対象テキスト
            max_bytes: 1チャンクあたりの最大バイト数

        Returns:
            [(chunk_text, char_offset), ...] のリスト
        """
        chunks = []
        start = 0

        while start < len(text):
            # max_bytes以内に収まる最大の文字位置を探す
            end = start
            while end < len(text):
                candidate = text[start:end + 1]
                if len(candidate.encode("utf-8")) > max_bytes:
                    break
                end += 1

            if end == start:
                # 1文字でもmax_bytesを超える場合（通常ありえない）
                end = start + 1
            else:
                # 句点・改行で区切りを探す（直前500文字以内）
                best_break = -1
                search_start = max(start, end - 500)
                for i in range(end - 1, search_start - 1, -1):
                    if text[i] in ('。', '\n', '.', '!', '?', '！', '？'):
                        best_break = i + 1
                        break
                if best_break > start:
                    end = best_break

            chunks.append((text[start:end], start))
            start = end

        return chunks

    async def close(self) -> None:
        """クライアントリソースをクローズ"""
        try:
            pass
        except Exception as e:
            logger.warning(f"Error during cleanup: {e}")
        finally:
            self._comprehend_client = None
            self._bedrock_runtime_client = None
            self._enabled = False
            logger.debug("AWSSecurityClient closed")
