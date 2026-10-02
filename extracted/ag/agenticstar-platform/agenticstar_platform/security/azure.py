"""
AGENTICSTAR Platform SDK - Azure Security Client
Azure Content Safety + Language Service (PII) 統合クライアント

機能:
- Content Moderation (有害コンテンツ検出)
- Prompt Shield (Jailbreak攻撃検出)
- PII Detection & Masking (個人情報検出・マスキング)

Example:
    config = AzureSecurityConfig(
        content_safety_endpoint="https://xxx.cognitiveservices.azure.com",
        content_safety_api_key="xxx",
        language_endpoint="https://xxx.cognitiveservices.azure.com",
        language_api_key="xxx",
    )
    client = AzureSecurityClient(config)

    # 統合チェック
    result = await client.check_security(text, check_pii=True)
    if not result.allowed:
        print(f"Violations: {result.violations}")

    await client.close()
"""

import asyncio
import logging
import os
from typing import Any, Dict, List, Optional, Tuple

import httpx

from .base import (
    AzureSecurityConfig,
    ContentCategory,
    ContentModerationResult,
    PIIDetectionResult,
    PIIEntity,
    PromptShieldResult,
    SecurityAPIError,
    SecurityClientBase,
    SecurityConfigError,
    SecurityProvider,
)


def _env_window_count(name: str, default: int) -> int:
    """スライディングウィンドウ上限窓数を env で可変化（既定維持＝後方互換）。

    P3-1: agentic クライアント(Claude Code/Cursor)の実 prompt は 146〜225KB で、設計前提
    (~34KB / 8 窓 ≒72KB) を超える tail が未検査になる。LLM-gateway のような大入力常態の経路では
    env でこの窓数を引き上げて検査範囲を広げられるようにする（コスト=Azure CS 呼び出し回数増）。
    既定は 8 のまま（worker など既存利用者の挙動・コストは不変）。1..64 にクランプ。
    """
    try:
        v = int(os.getenv(name, str(default)))
    except (TypeError, ValueError):
        return default
    return max(1, min(64, v))

logger = logging.getLogger(__name__)


# Azure Content Safety の入力長制限。公式 docs (rest-contentsafety-2024-09-01) は
# 「userPrompt 1K characters」「documents 各要素 1K characters」「合計 100K characters」
# と記述しているが、本番で観測されたエラー
# ``total length of given documents 10002 exceeds the limit 10000``
# から、Azure 内部は実は 10000 単位 (chars or bytes 不明) で動いている。
# 観測ベースで 10000 - 500 (安全マージン) = 9500 を bytes 換算で採用。
# 公式 docs と Azure 実装が乖離しているため、将来 API 更新で挙動が変わる可能性あり。
# 旧実装は ``text[:10000]`` (文字数切り) で CJK / emoji 入力で実バイト超過 → 400。
_AZURE_CS_MAX_BYTES = 9500

# Content Safety (Moderation / Prompt Shield) のスライディングウィンドウ検査の上限窓数。
# 旧実装は先頭 9500 bytes だけ検査し残りを未検査のまま LLM に渡しており、9500 byte 以降に
# 置かれた境界跨ぎの prompt injection / 有害コンテンツを取りこぼしていた
# (Loki sbtestfeature 2026-06-27: Moderation 72 / Prompt Shield 61 件/日の頭切りを観測)。
# 重なり付きウィンドウで末尾まで検査する。8 窓 (512B 重なり) = 9500 + 7×(9500-512)
# = 72,416 bytes (約 71KiB) まで連続検査 (観測された実入力は最大 ~34KB)。これを超える
# 巨大入力 (まれな数 MB blob) は先頭分のみ検査し残りは未検査である旨を WARNING で残す。
# 通常サイズ (<=9500 bytes) は windows=[text] となり従来どおり 1 回呼び出し。
# 既定 8（≈72KiB）。AGENTICSTAR_AZURE_CS_MAX_WINDOWS で引き上げ可（例 16≈140KB / 24≈215KB）。
_AZURE_CS_MAX_WINDOWS = _env_window_count("AGENTICSTAR_AZURE_CS_MAX_WINDOWS", 8)
_AZURE_CS_WINDOW_OVERLAP_BYTES = 512
# Prompt Shield の 1 呼び出しで送る documents の件数上限 (Azure 側の件数上限は未確認のため、少なめの 5 件に抑える)
_AZURE_CS_MAX_DOCS_PER_REQUEST = 5

# Azure Language Service (PII Detection) per-document limit.
# Official spec: 5,120 characters / document, 125,000 / job (multi-document total).
# SDK は 1 ドキュメントしか送らないため per-document 制限が効く。
# BMP 外文字は UTF-16 で 2 code units を消費するため安全マージン取り 5000 採用。
_AZURE_LANG_MAX_CHARS_PER_DOC = 5000

# PII 検出のスライディングウィンドウ上限。旧実装は先頭 5000 文字だけ Azure に送り、
# それ以降の Azure-ML カテゴリ(氏名/住所等)が未マスクで LLM/memory/log へ流出していた
# (regex 補完は日本語パターンのみ救済。Loki demo01 2026-06-28 で PII truncated 多数を観測)。
# 文字単位の非重複ウィンドウで全文を走査し、各 entity の offset を窓開始位置で補正する。
# 8 窓まで走査。超過分は警告。通常 (<=5000 文字) は従来どおり 1 回。
# 既定 8（≈40K文字）。AGENTICSTAR_AZURE_LANG_MAX_WINDOWS で引き上げ可。
_AZURE_LANG_MAX_WINDOWS = _env_window_count("AGENTICSTAR_AZURE_LANG_MAX_WINDOWS", 8)
# 境界跨ぎの PII を取りこぼさないよう隣接窓を重ねる文字数（典型的な PII entity 長より大きく取る）。
_AZURE_LANG_WINDOW_OVERLAP_CHARS = 256

# Azure 同期 PII の 1 リクエスト最大ドキュメント数（公式上限 5）。従来の 1 呼び出し=1 doc では
# 長い会話履歴の全量スキャン(数百〜千超テキスト)が S0 クォータ(300req/min)を単発で枯渇させた
# (2026-07-08 LLM Gateway 502/504 障害)。バッチ詰めで呼び出し数を最大 1/5 にする。
_AZURE_LANG_MAX_DOCS_PER_REQUEST = 5


def _env_retry_count(name: str, default: int) -> int:
    """429 リトライ回数を env で可変化（0 で無効、0..10 にクランプ）。"""
    try:
        v = int(os.getenv(name, str(default)))
    except (TypeError, ValueError):
        return default
    return max(0, min(10, v))


# 429 (rate limit) は Azure が Retry-After (通常 1 秒) を返す一時スロットル。従来は即 fail-closed
# → 呼び出し元(gateway)が 502 → クライアント自動リトライで枯渇が持続していた。
# Retry-After を尊重した bounded リトライで単発バーストを吸収する。
_AZURE_LANG_429_RETRIES = _env_retry_count("AGENTICSTAR_AZURE_LANG_429_RETRIES", 2)
_AZURE_LANG_RETRY_AFTER_CAP_SECONDS = 5.0


def _utf8_safe_truncate_bytes(text: str, max_bytes: int) -> Tuple[str, bool]:
    """UTF-8 で max_bytes 以下に切り詰める (マルチバイト境界 respect)。

    Python の ``text[:N]`` は文字数で切るため、CJK 等で Azure の 10000 バイト
    制限を超えて 400 を返される。本関数は UTF-8 にエンコードしてバイト数で切り、
    継続バイト ``0b10xxxxxx`` の途中で分断しないよう境界調整する。

    Returns:
        Tuple[str, bool]: 切り詰め後テキスト, 切り詰めが発生したか
    """
    if not text:
        return text, False
    encoded = text.encode('utf-8')
    if len(encoded) <= max_bytes:
        return text, False
    end = max_bytes
    while end > 0 and (encoded[end] & 0xC0) == 0x80:
        end -= 1
    return encoded[:end].decode('utf-8', errors='ignore'), True


def _utf8_safe_windows(
    text: str,
    window_bytes: int,
    overlap_bytes: int = _AZURE_CS_WINDOW_OVERLAP_BYTES,
    max_windows: int = _AZURE_CS_MAX_WINDOWS,
) -> Tuple[List[str], bool]:
    """text を UTF-8 バイト境界を尊重した重なり付きウィンドウ列に分割する。

    Azure Content Safety は 1 リクエスト約 10000 bytes 制限のため、長文は複数ウィンドウに
    分けて検査し結果を OR する。境界跨ぎの攻撃を取りこぼさないよう ``overlap_bytes`` だけ
    各ウィンドウを重ねる。``max_windows`` を超える分は検査せず ``clipped=True`` を返す。
    text が 1 ウィンドウに収まる通常ケースでは ``([text], False)`` を返し従来挙動を維持する。

    Returns:
        Tuple[List[str], bool]: ウィンドウ列, max_windows 超過で末尾を切り捨てたか
    """
    if not text:
        return [], False
    data = text.encode('utf-8')
    n = len(data)
    if n <= window_bytes:
        return [text], False
    step = max(1, window_bytes - max(0, overlap_bytes))
    windows: List[str] = []
    start = 0
    clipped = False
    while start < n:
        if len(windows) >= max_windows:
            clipped = True
            break
        end = min(start + window_bytes, n)
        # 終端がマルチバイト文字の継続バイト (0b10xxxxxx) の途中なら手前へ後退
        e = end
        while e > start and e < n and (data[e] & 0xC0) == 0x80:
            e -= 1
        # 始端が継続バイトの途中なら前進
        s = start
        while s < e and (data[s] & 0xC0) == 0x80:
            s += 1
        chunk = data[s:e].decode('utf-8', errors='ignore')
        if chunk:
            windows.append(chunk)
        if end >= n:
            break
        start += step
    return windows, clipped


# Azure Language Service PII Categories (全189種)
AZURE_PII_CATEGORIES = [
    "ABARoutingNumber", "ARNationalIdentityNumber", "AUBankAccountNumber",
    "AUDriversLicenseNumber", "AUMedicalAccountNumber", "AUPassportNumber",
    "AUTaxFileNumber", "AUBusinessNumber", "AUCompanyNumber", "ATIdentityCard",
    "ATTaxIdentificationNumber", "ATValueAddedTaxNumber", "BENationalNumber",
    "BENationalNumberV2", "BEValueAddedTaxNumber", "BRCPFNumber",
    "BRLegalEntityNumber", "BRNationalIDRG", "BGUniformCivilNumber",
    "CABankAccountNumber", "CADriversLicenseNumber", "CAHealthServiceNumber",
    "CAPassportNumber", "CAPersonalHealthIdentification", "CASocialInsuranceNumber",
    "CLIdentityCardNumber", "CNResidentIdentityCardNumber", "CreditCardNumber",
    "HRIdentityCardNumber", "HRNationalIDNumber", "HRPersonalIdentificationNumber",
    "HRPersonalIdentificationOIBNumberV2", "CYIdentityCard", "CYTaxIdentificationNumber",
    "CZPersonalIdentityNumber", "CZPersonalIdentityV2", "DKPersonalIdentificationNumber",
    "DKPersonalIdentificationV2", "DrugEnforcementAgencyNumber", "EEPersonalIdentificationCode",
    "EUDebitCardNumber", "EUDriversLicenseNumber", "EUGPSCoordinates",
    "EUNationalIdentificationNumber", "EUPassportNumber", "EUSocialSecurityNumber",
    "EUTaxIdentificationNumber", "FIEuropeanHealthNumber", "FINationalID",
    "FINationalIDV2", "FIPassportNumber", "FRDriversLicenseNumber",
    "FRHealthInsuranceNumber", "FRNationalID", "FRPassportNumber",
    "FRSocialSecurityNumber", "FRTaxIdentificationNumber", "FRValueAddedTaxNumber",
    "DEDriversLicenseNumber", "DEPassportNumber", "DEIdentityCardNumber",
    "DETaxIdentificationNumber", "DEValueAddedNumber", "GRNationalIDCard",
    "GRNationalIDV2", "GRTaxIdentificationNumber", "HKIdentityCardNumber",
    "HUValueAddedNumber", "HUPersonalIdentificationNumber", "HUTaxIdentificationNumber",
    "INPermanentAccount", "INUniqueIdentificationNumber", "IDIdentityCardNumber",
    "InternationalBankingAccountNumber", "IEPersonalPublicServiceNumber",
    "IEPersonalPublicServiceNumberV2", "ILBankAccountNumber", "ILNationalID",
    "ITDriversLicenseNumber", "ITFiscalCode", "ITValueAddedTaxNumber",
    "JPBankAccountNumber", "JPDriversLicenseNumber", "JPPassportNumber",
    "JPResidentRegistrationNumber", "JPSocialInsuranceNumber", "JPMyNumberCorporate",
    "JPMyNumberPersonal", "JPResidenceCardNumber", "LVPersonalCode",
    "LTPersonalCode", "LUNationalIdentificationNumberNatural",
    "LUNationalIdentificationNumberNonNatural", "MYIdentityCardNumber",
    "MTIdentityCardNumber", "MTTaxIDNumber", "NLCitizensServiceNumber",
    "NLCitizensServiceNumberV2", "NLTaxIdentificationNumber", "NLValueAddedTaxNumber",
    "NZBankAccountNumber", "NZDriversLicenseNumber", "NZInlandRevenueNumber",
    "NZMinistryOfHealthNumber", "NZSocialWelfareNumber", "NOIdentityNumber",
    "PHUnifiedMultiPurposeIDNumber", "PLIdentityCard", "PLNationalID",
    "PLNationalIDV2", "PLPassportNumber", "PLTaxIdentificationNumber",
    "PLREGONNumber", "PTCitizenCardNumber", "PTCitizenCardNumberV2",
    "PTTaxIdentificationNumber", "ROPersonalNumericalCode", "RUPassportNumberDomestic",
    "RUPassportNumberInternational", "SANationalID", "SGNationalRegistrationIdentityCardNumber",
    "SKPersonalNumber", "SITaxIdentificationNumber", "SIUniqueMasterCitizenNumber",
    "ZAIdentificationNumber", "KRResidentRegistrationNumber", "ESDNI",
    "ESSocialSecurityNumber", "ESTaxIdentificationNumber", "SQLServerConnectionString",
    "SENationalID", "SENationalIDV2", "SEPassportNumber", "SETaxIdentificationNumber",
    "SWIFTCode", "CHSocialSecurityNumber", "TWNationalID", "TWPassportNumber",
    "TWResidentCertificate", "THPopulationIdentificationCode", "TRNationalIdentificationNumber",
    "UKDriversLicenseNumber", "UKElectoralRollNumber", "UKNationalHealthNumber",
    "UKNationalInsuranceNumber", "UKUniqueTaxpayerNumber", "USUKPassportNumber",
    "USBankAccountNumber", "USDriversLicenseNumber", "USIndividualTaxpayerIdentification",
    "USSocialSecurityNumber", "UAPassportNumberDomestic", "UAPassportNumberInternational",
    "Email", "Age", "PhoneNumber", "Person", "Address",
]


class AzureSecurityClient(SecurityClientBase):
    """
    Azure Security クライアント

    Azure Content Safety APIとLanguage Service APIを統合し、
    コンテンツモデレーション、Jailbreak攻撃検出、PII検出・マスキングを提供。

    Example:
        config = AzureSecurityConfig(
            content_safety_endpoint="https://xxx.cognitiveservices.azure.com",
            content_safety_api_key="xxx",
        )
        client = AzureSecurityClient(config)

        # Content Moderation
        result = await client.check_content_moderation("some text")
        if result.blocked:
            print("Content blocked")

        # Prompt Shield
        result = await client.check_prompt_shield("user prompt")
        if result.attack_detected:
            print("Attack detected")

        # PII Detection
        result = await client.detect_pii("My email is test@example.com")
        print(result.masked_text)  # "My email is ***"

        await client.close()
    """

    def __init__(self, config: AzureSecurityConfig):
        """
        Initialize Azure Security Client

        Content SafetyまたはPII（Language Service）のどちらか一方でも設定があれば初期化可能。
        両方未設定の場合のみエラー。

        Args:
            config: AzureSecurityConfig instance

        Raises:
            SecurityConfigError: Content SafetyとPII両方が未設定の場合
        """
        super().__init__(config)

        # Content SafetyまたはPIIのどちらかが設定されていればOK
        has_content_safety = bool(config.content_safety_endpoint and config.content_safety_api_key)
        has_pii = bool(config.language_endpoint and config.language_api_key)

        if not has_content_safety and not has_pii:
            raise SecurityConfigError(
                "At least one of Content Safety or PII (Language Service) must be configured. "
                "Provide content_safety_endpoint/api_key or language_endpoint/api_key."
            )

        self._azure_config: AzureSecurityConfig = config
        self._http_client: Optional[httpx.AsyncClient] = None
        self._enabled = config.enabled
        self._has_content_safety = has_content_safety
        self._has_pii = has_pii

        # ログ出力
        cs_status = f"{config.content_safety_endpoint[:30]}..." if has_content_safety else "disabled"
        pii_status = "enabled" if has_pii else "disabled"
        logger.info(
            f"AzureSecurityClient initialized - "
            f"content_safety={cs_status}, "
            f"pii={pii_status}"
        )

    @property
    def provider(self) -> SecurityProvider:
        return SecurityProvider.AZURE

    def _get_http_client(self) -> httpx.AsyncClient:
        """HTTP clientを取得（遅延初期化）"""
        if self._http_client is None or self._http_client.is_closed:
            self._http_client = httpx.AsyncClient(timeout=self._azure_config.timeout)
        return self._http_client

    async def check_content_moderation(
        self,
        text: str,
        threshold: Optional[int] = None,
    ) -> ContentModerationResult:
        """
        有害コンテンツをチェック（Azure Content Safety Moderation API）

        Args:
            text: チェック対象テキスト（最大10,000文字）
            threshold: しきい値（0=無効, 2=推奨, 4=緩い, 6=極度のみ）

        Returns:
            ContentModerationResult: モデレーション結果
        """
        if not self._enabled:
            return ContentModerationResult(blocked=False, error="Client disabled")

        if not self._has_content_safety:
            return ContentModerationResult(blocked=False, error="Content Safety not configured")

        if not self._azure_config.moderation_enabled:
            return ContentModerationResult(blocked=False, threshold=0)

        # Azure API は空文字 / 空白のみを 400 (InvalidRequestBody) で弾く。
        # 早期 return で API call を避ける。
        if not text or not text.strip():
            return ContentModerationResult(blocked=False)

        effective_threshold = threshold if threshold is not None else self._azure_config.moderation_threshold
        if effective_threshold == 0:
            return ContentModerationResult(blocked=False, threshold=0)

        try:
            endpoint = (
                f"{self._azure_config.content_safety_endpoint.rstrip('/')}"
                f"/contentsafety/text:analyze?api-version=2024-09-01"
            )

            # 長文は先頭だけでなく重なり付きウィンドウで末尾まで検査し結果を OR する
            # (旧実装は先頭 9500 bytes 頭切りで尾部が未検査のまま LLM に渡っていた)。
            # 通常サイズ (<=9500 bytes) は windows=[text] となり従来どおり 1 回呼び出し。
            windows, clipped = _utf8_safe_windows(text, _AZURE_CS_MAX_BYTES)
            if clipped:
                logger.warning(
                    "Moderation: input %d bytes exceeds inspection budget "
                    "(%d windows x %d bytes). Tail beyond budget was NOT inspected.",
                    len(text.encode('utf-8')), _AZURE_CS_MAX_WINDOWS, _AZURE_CS_MAX_BYTES,
                )

            client = self._get_http_client()
            headers = {
                "Ocp-Apim-Subscription-Key": self._get_api_key(self._azure_config.content_safety_api_key),
                "Content-Type": "application/json",
            }

            # 通常 windows は 1 要素以上 (空/空白は上の早期 return で除外済み)。防御的に、
            # 検査対象が無ければ fail-open で許可する (旧挙動と一致。意図を明示)。
            if not windows:
                return ContentModerationResult(blocked=False, threshold=effective_threshold)

            # カテゴリ別severity は全ウィンドウの最大、blocked はいずれかで超過したら True
            categories: Dict[ContentCategory, int] = {}
            blocked = False
            last_result: Optional[Dict[str, Any]] = None
            blocking_result: Optional[Dict[str, Any]] = None

            for chunk in windows:
                request_body = {
                    "text": chunk,
                    "categories": ["Hate", "Sexual", "SelfHarm", "Violence"],
                    "outputType": "FourSeverityLevels",
                }
                response = await client.post(endpoint, headers=headers, json=request_body)
                if response.status_code != 200:
                    error_msg = f"Status {response.status_code}: {response.text}"
                    logger.error(f"Content Safety Moderation API error: {error_msg}")
                    raise SecurityAPIError(error_msg, response.status_code)

                result = response.json()
                last_result = result
                for cat in result.get("categoriesAnalysis", []):
                    category_name = cat.get("category", "").lower()
                    severity = cat.get("severity", 0)
                    normalized_cat = self._normalize_content_category(category_name)
                    if severity > categories.get(normalized_cat, -1):
                        categories[normalized_cat] = severity
                    if severity >= effective_threshold:
                        blocked = True
                        if blocking_result is None:
                            blocking_result = result  # 違反を出した窓の応答を診断用に残す
                        logger.warning(
                            f"Content moderation blocked: {category_name} "
                            f"severity={severity} >= threshold={effective_threshold}"
                        )

            return ContentModerationResult(
                blocked=blocked,
                categories=categories,
                threshold=effective_threshold,
                raw_response=blocking_result if blocking_result is not None else last_result,
            )

        except SecurityAPIError:
            raise
        except httpx.RequestError as e:
            logger.error(f"Content Safety Moderation request failed: {e}")
            raise SecurityAPIError(str(e), error_code="REQUEST_ERROR")
        except Exception as e:
            logger.error(f"Error in content moderation: {e}")
            raise SecurityAPIError(str(e), error_code="UNKNOWN_ERROR")

    async def check_prompt_shield(
        self,
        user_prompt: str,
        documents: Optional[List[str]] = None,
    ) -> PromptShieldResult:
        """
        Jailbreak攻撃を検出（Azure Content Safety Prompt Shield API）

        Args:
            user_prompt: ユーザープロンプト（長い場合は重なり付きウィンドウに分けて検査）
            documents: ドキュメント内容（オプション、外部コンテンツ検証用。userPrompt と同じく
                重なり付きウィンドウに分けて末尾まで検査する）

        Returns:
            PromptShieldResult: Prompt Shield結果
        """
        if not self._enabled:
            return PromptShieldResult(attack_detected=False, error="Client disabled")

        if not self._has_content_safety:
            return PromptShieldResult(attack_detected=False, error="Content Safety not configured")

        if not self._azure_config.prompt_shield_enabled:
            return PromptShieldResult(attack_detected=False)

        # Azure API は空文字 / 空白のみを 400 で弾く。早期 return。
        if not user_prompt or not user_prompt.strip():
            return PromptShieldResult(attack_detected=False)

        try:
            endpoint = (
                f"{self._azure_config.content_safety_endpoint.rstrip('/')}"
                f"/contentsafety/text:shieldPrompt?api-version=2024-09-01"
            )

            # userPrompt は重なり付きウィンドウで末尾まで検査して結果を OR する
            # (旧実装は先頭 9500 bytes 頭切りで境界跨ぎの jailbreak を取りこぼしていた)。
            # 通常サイズ (<=9500 bytes) は prompt_windows=[user_prompt] で従来どおり 1 回。
            prompt_windows, clipped = _utf8_safe_windows(user_prompt, _AZURE_CS_MAX_BYTES)
            if clipped:
                logger.warning(
                    "Prompt Shield: input %d bytes exceeds inspection budget "
                    "(%d windows x %d bytes). Tail beyond budget was NOT inspected — "
                    "boundary-spanning attacks may evade detection.",
                    len(user_prompt.encode('utf-8')), _AZURE_CS_MAX_WINDOWS, _AZURE_CS_MAX_BYTES,
                )

            # documents も userPrompt と同じく重なり付きウィンドウで末尾まで検査して結果を OR する
            # (旧実装は全 documents を合計 9500 bytes に頭切りして最初の呼び出しでだけ送り、警告も出さなかった =
            # 外部コンテンツの 9.5KB より後ろに置かれた間接 injection を見ていなかった)。1 呼び出しの documents は
            # 合計 _AZURE_CS_MAX_BYTES 以下・_AZURE_CS_MAX_DOCS_PER_REQUEST 件以下に詰める。documents の束が
            # userPrompt の窓より多いときは、残りの呼び出しに userPrompt の最初の窓を付ける (Azure は userPrompt を
            # 必須とする)。通常サイズは従来どおり 1 回。
            doc_batches: List[List[str]] = []
            if documents:
                doc_windows: List[str] = []
                docs_clipped = False
                for doc in documents:
                    windows, clipped_doc = _utf8_safe_windows(doc or "", _AZURE_CS_MAX_BYTES)
                    doc_windows.extend(windows)
                    docs_clipped = docs_clipped or clipped_doc
                if docs_clipped:
                    logger.warning(
                        "Prompt Shield: a document exceeds inspection budget "
                        "(%d windows x %d bytes). Tail beyond budget was NOT inspected.",
                        _AZURE_CS_MAX_WINDOWS, _AZURE_CS_MAX_BYTES,
                    )
                batch: List[str] = []
                used = 0
                for window in doc_windows:
                    size = len(window.encode('utf-8'))
                    if batch and (used + size > _AZURE_CS_MAX_BYTES or len(batch) >= _AZURE_CS_MAX_DOCS_PER_REQUEST):
                        doc_batches.append(batch)
                        batch, used = [], 0
                    batch.append(window)
                    used += size
                if batch:
                    doc_batches.append(batch)

            client = self._get_http_client()
            headers = {
                "Ocp-Apim-Subscription-Key": self._get_api_key(self._azure_config.content_safety_api_key),
                "Content-Type": "application/json",
            }

            # 通常 prompt_windows は 1 要素以上 (空/空白は上の早期 return で除外済み)。
            # 防御的に、検査対象が無ければ攻撃なし扱い (旧挙動と一致。意図を明示)。
            if not prompt_windows:
                return PromptShieldResult(attack_detected=False)

            user_prompt_attack = False
            documents_attack = False
            last_result: Optional[Dict[str, Any]] = None
            attack_result: Optional[Dict[str, Any]] = None
            for idx in range(max(len(prompt_windows), len(doc_batches))):
                chunk = prompt_windows[idx] if idx < len(prompt_windows) else prompt_windows[0]
                request_body: Dict[str, Any] = {"userPrompt": chunk}
                if idx < len(doc_batches):
                    request_body["documents"] = doc_batches[idx]

                response = await client.post(endpoint, headers=headers, json=request_body)
                if response.status_code != 200:
                    error_msg = f"Status {response.status_code}: {response.text}"
                    logger.error(f"Prompt Shield API error: {error_msg}")
                    raise SecurityAPIError(error_msg, response.status_code)

                result = response.json()
                last_result = result
                user_analysis = result.get("userPromptAnalysis", {})
                window_attack = False
                if user_analysis.get("attackDetected", False):
                    user_prompt_attack = True
                    window_attack = True
                # 外部コンテンツ(documents)経由の間接 injection も検出する。
                # 旧実装は documents を送るだけで documentsAnalysis を読んでおらず、
                # ドキュメント側の jailbreak を取りこぼしていた (Rule 5.2)。
                # userPrompt / documents は経路別に保持する（guardrail_alerts の
                # prompt_shield_origin 用。OR に潰すと direct/indirect の内訳が失われる）。
                for doc_analysis in (result.get("documentsAnalysis") or []):
                    if doc_analysis.get("attackDetected", False):
                        documents_attack = True
                        window_attack = True
                if window_attack and attack_result is None:
                    attack_result = result  # 攻撃を検出した窓の応答を診断用に残す

            attack_detected = user_prompt_attack or documents_attack
            attack_type = "jailbreak" if attack_detected else None
            if attack_detected:
                logger.warning("Prompt Shield detected jailbreak attack")

            return PromptShieldResult(
                attack_detected=attack_detected,
                attack_type=attack_type,
                raw_response=attack_result if attack_result is not None else last_result,
                user_prompt_attack=user_prompt_attack,
                documents_attack=documents_attack,
            )

        except SecurityAPIError:
            raise
        except httpx.RequestError as e:
            logger.error(f"Prompt Shield request failed: {e}")
            raise SecurityAPIError(str(e), error_code="REQUEST_ERROR")
        except Exception as e:
            logger.error(f"Error in prompt shield: {e}")
            raise SecurityAPIError(str(e), error_code="UNKNOWN_ERROR")

    async def detect_pii(
        self,
        text: str,
        mask: bool = True,
        language: str = "ja",
        confidence_threshold: Optional[float] = None,
    ) -> PIIDetectionResult:
        """
        PIIを検出・マスク（Azure Language Service PII Detection API）

        Args:
            text: チェック対象テキスト（最大125,000文字）
            mask: マスク処理を行うかどうか
            language: テキストの言語コード（"ja", "en"等）。デフォルト"ja"
            confidence_threshold: 信頼度閾値。Noneの場合は config の pii_confidence_threshold を使う。
                クライアントを使い回しつつリクエスト毎に閾値を変えたい場合に指定する。

        Returns:
            PIIDetectionResult: PII検出結果

        Note:
            実体は detect_pii_batch（5 docs/request バッチ + 429 リトライ）への委譲。
            単一テキストの外部挙動（fail-closed 空文字・エラーコード）は従来互換。
        """
        results = await self.detect_pii_batch(
            [text], mask=mask, language=language, confidence_threshold=confidence_threshold
        )
        return results[0]

    def _pii_window_spans(self, text: str) -> List[Tuple[int, str]]:
        """PII 検査用スライディングウィンドウ (win_start, window_text) 列を返す。

        PII は文字単位の重なり付きウィンドウで全文を走査する。先頭 5000 文字だけ検査すると
        それ以降の Azure-ML カテゴリ(氏名/住所等)が未マスクで LLM/memory/log へ漏れる。
        境界跨ぎの PII を取りこぼさないよう隣接窓を OVERLAP 文字重ねる。
        通常 (<=5000 文字) は 1 窓で従来挙動。
        """
        W = _AZURE_LANG_MAX_CHARS_PER_DOC
        step = max(1, W - _AZURE_LANG_WINDOW_OVERLAP_CHARS)
        n = len(text)
        # MAXW 窓で覆える文字数 = step*(MAXW-1) + W
        n_inspect = min(n, step * (_AZURE_LANG_MAX_WINDOWS - 1) + W)
        if n > n_inspect:
            logger.warning(
                "PII Detection: input %d chars exceeds inspection budget "
                "(%d windows). Tail beyond %d chars NOT scanned for PII.",
                n, _AZURE_LANG_MAX_WINDOWS, n_inspect,
            )
        spans: List[Tuple[int, str]] = []
        for win_start in range(0, max(1, n_inspect), step):
            window_text = text[win_start:win_start + W]
            if window_text:
                spans.append((win_start, window_text))
        return spans

    async def _post_pii_with_retry(
        self,
        client: httpx.AsyncClient,
        endpoint: str,
        headers: Dict[str, str],
        request_body: Dict[str, Any],
    ) -> httpx.Response:
        """PII API POST。429 は Retry-After を尊重して bounded リトライ（超過時は最後の応答を返す）。

        Azure S0 の 429 は "retry after 1 second" を案内する一時スロットル。即 fail-closed にすると
        呼び出し元が 502 を返しクライアント自動リトライで枯渇が増幅する（2026-07-08 障害）。
        """
        attempt = 0
        while True:
            response = await client.post(endpoint, headers=headers, json=request_body)
            if response.status_code != 429 or attempt >= _AZURE_LANG_429_RETRIES:
                return response
            attempt += 1
            retry_after = response.headers.get("Retry-After")
            try:
                delay = max(0.0, float(retry_after)) if retry_after is not None else 1.0 * attempt
            except (TypeError, ValueError):
                delay = 1.0 * attempt
            delay = min(delay, _AZURE_LANG_RETRY_AFTER_CAP_SECONDS)
            logger.warning(
                "Language Service PII 429; retrying in %.1fs (attempt %d/%d)",
                delay, attempt, _AZURE_LANG_429_RETRIES,
            )
            await asyncio.sleep(delay)

    @staticmethod
    def _parse_pii_doc_id(doc_id: Any) -> Tuple[Optional[int], int]:
        """バッチ doc id "{text_idx}:{win_start}" を (text_idx, win_start) に分解。不正は (None, 0)。"""
        try:
            ti_s, _, ws_s = str(doc_id).partition(":")
            return int(ti_s), int(ws_s or 0)
        except (TypeError, ValueError):
            return None, 0

    async def detect_pii_batch(
        self,
        texts: List[str],
        mask: bool = True,
        language: str = "ja",
        confidence_threshold: Optional[float] = None,
    ) -> List[PIIDetectionResult]:
        """複数テキストの PII を一括検出・マスク（Azure 同期 PII の 5 documents/request バッチ）。

        従来の 1 呼び出し=1 ドキュメントでは長い会話履歴（数百〜千超テキスト）の全量スキャンが
        S0 クォータ(300req/min)を単発で枯渇させた（2026-07-08 LLM Gateway 502/504 障害）。
        全テキストのウィンドウを 5 docs/request に詰めて呼び出し数を最大 1/5 にする。

        Returns:
            texts と同順・同長の PIIDetectionResult。失敗はテキスト単位（success=False,
            masked_text="" の fail-closed）。429 がリトライ後も解消しない場合は
            error_code="RATE_LIMITED" で未確定テキストを一括失敗させ、以降の Azure 呼び出しを
            中止する（枯渇中の追い打ち防止。呼び出し元は 429 + Retry-After 化を推奨）。
        """
        threshold = (
            confidence_threshold
            if confidence_threshold is not None
            else self._azure_config.pii_confidence_threshold
        )
        if not texts:
            return []
        if not self._enabled:
            return [PIIDetectionResult(success=False, error="Client disabled") for _ in texts]
        if not self._has_pii:
            return [
                PIIDetectionResult(success=False, error="PII (Language Service) not configured")
                for _ in texts
            ]
        if not self._azure_config.pii_enabled:
            return [PIIDetectionResult(success=True, masked_text=t) for t in texts]

        results: List[Optional[PIIDetectionResult]] = [None] * len(texts)
        failures: Dict[int, Tuple[str, str]] = {}  # text_idx -> (error, error_code)
        entities_by_text: Dict[int, List[PIIEntity]] = {}
        seen_spans_by_text: Dict[int, set] = {}  # 重なり窓で二重検出した entity の (offset,length) を除去

        # 全テキストのウィンドウを (text_idx, win_start, window_text) に展開して 5 docs ずつ詰める
        docs: List[Tuple[int, int, str]] = []
        for ti, text in enumerate(texts):
            if not text:
                results[ti] = PIIDetectionResult(success=True, masked_text="")
                continue
            for win_start, window_text in self._pii_window_spans(text):
                docs.append((ti, win_start, window_text))

        last_result: Optional[Dict[str, Any]] = None
        try:
            endpoint = (
                f"{self._azure_config.language_endpoint.rstrip('/')}"
                f"/language/:analyze-text?api-version=2024-11-01"
            )
            client = self._get_http_client()
            headers = {
                "Ocp-Apim-Subscription-Key": self._get_api_key(self._azure_config.language_api_key),
                "Content-Type": "application/json",
            }

            aborted: Optional[Tuple[str, str]] = None  # 以降のチャンクを中止した理由 (error, error_code)
            for chunk_start in range(0, len(docs), _AZURE_LANG_MAX_DOCS_PER_REQUEST):
                chunk = docs[chunk_start:chunk_start + _AZURE_LANG_MAX_DOCS_PER_REQUEST]
                request_body = {
                    "kind": "PiiEntityRecognition",
                    "parameters": {
                        "modelVersion": "latest",
                        "domain": "none",
                        "loggingOptOut": True,
                        # Azure offset を Python str index (code point) と一致させる
                        "stringIndexType": "UnicodeCodePoint",
                        "piiCategories": AZURE_PII_CATEGORIES,
                    },
                    "analysisInput": {
                        "documents": [
                            {"id": f"{ti}:{win_start}", "language": language, "text": window_text}
                            for ti, win_start, window_text in chunk
                        ]
                    },
                }
                response = await self._post_pii_with_retry(client, endpoint, headers, request_body)
                if response.status_code == 429:
                    # リトライ後も枯渇継続。残チャンクへの追い打ちを止め、未確定テキストを一括失敗させる
                    aborted = (f"Status 429: {response.text}", "RATE_LIMITED")
                    logger.error(
                        "Language Service PII rate limited after retries "
                        "(aborting %d remaining docs)", len(docs) - chunk_start,
                    )
                    break
                if response.status_code != 200:
                    error_msg = f"Status {response.status_code}: {response.text}"
                    logger.error(f"Language Service PII API error: {error_msg}")
                    # データ保護優先: fail-closed (旧挙動踏襲)。同種エラーの連発を避け残チャンクも中止
                    aborted = (error_msg, "API_ERROR")
                    break

                result = response.json()
                last_result = result
                results_block = result.get("results", {})
                documents = results_block.get("documents", [])
                doc_errors = results_block.get("errors") or []
                # 200 でも document-level error は該当テキストのみ fail-closed（他テキストは継続）
                for de in doc_errors:
                    ti, _ = self._parse_pii_doc_id((de or {}).get("id"))
                    err_msg = f"PII document error: {(de or {}).get('error')}"
                    logger.error(f"Language Service PII API error: {err_msg}")
                    if ti is not None:
                        failures.setdefault(ti, (err_msg, "API_ERROR"))
                if not documents and not doc_errors:
                    # 旧実装は documents 無しを空文字 return していた(データ保護優先)ので fail-closed 踏襲
                    # (window が "無 PII" の場合は documents は非空で entities が空配列になる)。
                    error_msg = "PII malformed response (no documents)"
                    logger.error(f"Language Service PII API error: {error_msg}")
                    aborted = (error_msg, "API_ERROR")
                    break

                # fail-closed: 送信した doc が documents にも errors にも返らない場合、その text は
                # 「未走査のまま success」になってしまう（旧 1doc/req 実装は documents 欠落=fail-closed）。
                # 欠落 doc の text を失敗させて未マスク PII の素通りを防ぐ。
                returned_ids = {str(d.get("id")) for d in documents if isinstance(d, dict)}
                returned_ids |= {str((de or {}).get("id")) for de in doc_errors}
                for ti, win_start, _wt in chunk:
                    if f"{ti}:{win_start}" not in returned_ids and ti not in failures:
                        err_msg = f"PII response missing document {ti}:{win_start}"
                        logger.error(f"Language Service PII API error: {err_msg}")
                        failures[ti] = (err_msg, "API_ERROR")

                for doc in documents:
                    ti, win_start = self._parse_pii_doc_id(doc.get("id"))
                    if ti is None or ti in failures:
                        continue
                    ents = entities_by_text.setdefault(ti, [])
                    seen_spans = seen_spans_by_text.setdefault(ti, set())
                    for entity in doc.get("entities", []):
                        confidence = entity.get("confidenceScore", 0)
                        if confidence < threshold:
                            continue
                        abs_offset = entity.get("offset", 0) + win_start  # 窓開始位置で全文 offset へ補正
                        length = entity.get("length", 0)
                        span = (abs_offset, length)
                        if span in seen_spans:  # 重なり領域での同一 entity 二重検出を除去
                            continue
                        seen_spans.add(span)
                        provider_category = entity.get("category", "Unknown")
                        ents.append(PIIEntity(
                            category=self._normalize_pii_category(provider_category),
                            text=entity.get("text", ""),
                            offset=abs_offset,
                            length=length,
                            confidence=confidence,
                            provider_category=provider_category,
                        ))

            if aborted:
                for ti in range(len(texts)):
                    if results[ti] is None and ti not in failures:
                        failures[ti] = aborted

        except httpx.RequestError as e:
            logger.error(f"Language Service PII request failed: {e}")
            for ti in range(len(texts)):
                if results[ti] is None and ti not in failures:
                    failures[ti] = (str(e), "REQUEST_ERROR")
        except Exception as e:
            logger.error(f"Error in PII detection: {e}")
            for ti in range(len(texts)):
                if results[ti] is None and ti not in failures:
                    failures[ti] = (str(e), "UNKNOWN_ERROR")

        # テキスト単位の確定（regex 補完 → マージ → マスク適用は従来 detect_pii と同一手順）
        for ti, text in enumerate(texts):
            if results[ti] is not None:
                continue
            if ti in failures:
                err_msg, err_code = failures[ti]
                results[ti] = PIIDetectionResult(
                    success=False, masked_text="", error=err_msg, error_code=err_code,
                )
                continue

            # 正規表現による日本語PII補完（全クラウド共通・全文走査）
            entities = self._merge_pii_entities(
                entities_by_text.get(ti, []), self._detect_pii_by_regex(text)
            )
            categories_detected = list({e.category for e in entities})

            # マスク処理（全文に対し offset 降順で適用）
            masked_text = text
            if mask and entities:
                sorted_entities = sorted(entities, key=lambda x: x.offset, reverse=True)
                for entity in sorted_entities:
                    masked_text = (
                        masked_text[:entity.offset]
                        + self._azure_config.pii_mask_string
                        + masked_text[entity.offset + entity.length:]
                    )
            if entities:
                logger.info(f"PII detected and masked: {categories_detected}")

            results[ti] = PIIDetectionResult(
                success=True,
                masked_text=masked_text,
                entities=entities,
                categories_detected=categories_detected,
                raw_response=last_result,
            )

        return results  # type: ignore[return-value]

    async def close(self) -> None:
        """クライアントリソースをクローズ

        Note:
            例外が発生してもリソースを確実にクリーンアップします。
        """
        try:
            if self._http_client and not self._http_client.is_closed:
                await self._http_client.aclose()
        except Exception as e:
            logger.warning(f"Error closing HTTP client: {e}")
        finally:
            self._http_client = None
            self._enabled = False
            logger.debug("AzureSecurityClient closed")
