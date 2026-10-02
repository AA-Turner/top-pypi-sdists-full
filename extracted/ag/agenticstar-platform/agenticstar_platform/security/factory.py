"""
AGENTICSTAR Platform SDK - Security Client Factory
agent_configurations テーブルの config JSON からプロバイダーを自動判別し、
適切な SecurityClient を生成するファクトリ関数

config JSON の内容に基づいてプロバイダーを判別:
- AWS: service が bedrock_guardrails / comprehend
- GCP: service が model_armor / dlp / vertex_ai_safety
- Azure: base_url に cognitiveservices.azure.com を含む、または api_key + base_url の組み合わせ

Example:
    from agenticstar_platform.security.factory import create_security_client

    # agent_configurations テーブルから取得した config JSON
    content_safety_config = {
        "region": "japaneast",
        "api_key": "xxx",
        "base_url": "https://resource.cognitiveservices.azure.com/"
    }
    client = create_security_client(content_safety_config)
    # → AzureSecurityClient が返る

    aws_config = {
        "service": "bedrock_guardrails",
        "region": "us-east-1",
        "guardrail_id": "guardrail-xxxxx"
    }
    client = create_security_client(aws_config)
    # → AWSSecurityClient が返る
"""

import logging
from typing import Any, Dict, Optional

from .base import (
    AWSSecurityConfig,
    AzureSecurityConfig,
    GCPSecurityConfig,
    SecurityClientBase,
    SecurityConfigError,
    SecurityProvider,
)

logger = logging.getLogger(__name__)

# AWS サービス名
_AWS_SERVICES = {"bedrock_guardrails", "comprehend"}
# GCP サービス名
# vertex_ai_safety: マーケットプレイス向け全リージョン対応 Content Safety (Refs #1952)
_GCP_SERVICES = {"model_armor", "dlp", "vertex_ai_safety"}


def detect_provider(config: Dict[str, Any]) -> SecurityProvider:
    """config JSON からセキュリティプロバイダーを自動判別する

    判別ルール:
    1. service キー（AWS/GCPは generate_config_<cloud>.sh で必ず設定される）
    2. base_url のドメイン（Azureは cognitiveservices.azure.com）
    3. api_key + base_url の存在（Azureフォールバック）

    Args:
        config: agent_configurations テーブルの config カラムの値（dict）

    Returns:
        SecurityProvider: 判別されたプロバイダー

    Raises:
        SecurityConfigError: プロバイダーを判別できない場合
    """
    if not config:
        raise SecurityConfigError("config が空です")

    # 1. service キーによる明示的な判別（AWS/GCP）
    service = config.get("service", "").lower()
    if service in _AWS_SERVICES:
        return SecurityProvider.AWS
    if service in _GCP_SERVICES:
        return SecurityProvider.GCP

    # 2. base_url による判別（Azure）
    base_url = config.get("base_url", "")
    if "cognitiveservices.azure.com" in base_url:
        return SecurityProvider.AZURE

    # 3. api_key + base_url の組み合わせ（Azureフォールバック）
    if "api_key" in config and "base_url" in config:
        return SecurityProvider.AZURE

    raise SecurityConfigError(
        f"config JSON からプロバイダーを判別できません: keys={list(config.keys())}"
    )


def create_security_client(
    config: Dict[str, Any],
    pii_config: Optional[Dict[str, Any]] = None,
) -> SecurityClientBase:
    """config JSON から適切な SecurityClient を生成する

    content_safety と pii_language の config を組み合わせてクライアントを生成する。
    Azure の場合は content_safety と pii_language が同じリソースを共有するため、
    両方の config を統合して1つのクライアントを生成する。

    Args:
        config: agent_configurations の content_safety または主要な config JSON
        pii_config: agent_configurations の pii_language の config JSON（オプション）
            Azure の場合、language_endpoint / language_api_key として使用

    Returns:
        SecurityClientBase: プロバイダーに対応した SecurityClient インスタンス

    Raises:
        SecurityConfigError: クライアント生成に失敗した場合
    """
    provider = detect_provider(config)

    logger.info(f"セキュリティプロバイダー自動判別: {provider.value}")

    if provider == SecurityProvider.AZURE:
        return _create_azure_client(config, pii_config)
    elif provider == SecurityProvider.AWS:
        return _create_aws_client(config, pii_config)
    elif provider == SecurityProvider.GCP:
        return _create_gcp_client(config, pii_config)
    else:
        raise SecurityConfigError(f"未対応のプロバイダー: {provider}")


def create_content_safety_client(config: Dict[str, Any]) -> SecurityClientBase:
    """content_safety 用の config JSON からクライアントを生成する

    content_safety 専用のショートカット。
    Content Moderation と Prompt Shield に使用。

    Args:
        config: agent_configurations の content_safety config JSON

    Returns:
        SecurityClientBase: プロバイダーに対応した SecurityClient インスタンス
    """
    return create_security_client(config)


def create_pii_client(config: Dict[str, Any]) -> SecurityClientBase:
    """pii_language 用の config JSON からクライアントを生成する

    PII Detection / Masking 専用のショートカット。
    Azure の場合は language_endpoint として設定される。

    Args:
        config: agent_configurations の pii_language config JSON

    Returns:
        SecurityClientBase: プロバイダーに対応した SecurityClient インスタンス
    """
    provider = detect_provider(config)

    if provider == SecurityProvider.AZURE:
        # Azure の PII は Language Service を使用
        azure_config = AzureSecurityConfig(
            content_safety_endpoint="",
            content_safety_api_key="",
            language_endpoint=config.get("base_url", ""),
            language_api_key=config.get("api_key", ""),
            pii_enabled=True,
            moderation_enabled=False,
            prompt_shield_enabled=False,
        )
        from .azure import AzureSecurityClient
        return AzureSecurityClient(azure_config)
    else:
        return create_security_client(config)


def _create_azure_client(
    config: Dict[str, Any],
    pii_config: Optional[Dict[str, Any]] = None,
) -> SecurityClientBase:
    """Azure SecurityClient を生成"""
    from .azure import AzureSecurityClient

    azure_config = AzureSecurityConfig(
        content_safety_endpoint=config.get("base_url", ""),
        content_safety_api_key=config.get("api_key", ""),
        language_endpoint=(pii_config or config).get("base_url", ""),
        language_api_key=(pii_config or config).get("api_key", ""),
    )

    return AzureSecurityClient(azure_config)


def _create_aws_client(
    config: Dict[str, Any],
    pii_config: Optional[Dict[str, Any]] = None,
) -> SecurityClientBase:
    """AWS SecurityClient を生成

    pii_service の解決優先順位 (Refs #1873):
      1. pii_config["service"] (pii_language の service)
      2. config["service"] (content_safety の service / 単独呼び出し時)
      3. "bedrock_guardrails" (多言語対応がデフォルト動作)

    "bedrock_guardrails" のとき detect_pii() が Bedrock Guardrails 経由になる。
    "comprehend" を明示指定したときのみ従来の Amazon Comprehend 経由。
    """
    from .aws import AWSSecurityClient

    pii_service = str(
        (pii_config or {}).get("service")
        or config.get("service")
        or "bedrock_guardrails"
    ).lower()

    aws_config = AWSSecurityConfig(
        aws_access_key_id=config.get("aws_access_key_id", ""),
        aws_secret_access_key=config.get("aws_secret_access_key", ""),
        region_name=config.get("region", "us-east-1"),
        guardrail_id=config.get("guardrail_id", ""),
        guardrail_version=str(config.get("guardrail_version", "DRAFT")),
        pii_service=pii_service,
        enabled=True,
    )

    return AWSSecurityClient(aws_config)


def _create_gcp_client(
    config: Dict[str, Any],
    pii_config: Optional[Dict[str, Any]] = None,
) -> SecurityClientBase:
    """GCP SecurityClient を生成

    service=vertex_ai_safety のときは Vertex AI Safety Filters + Gemini judge を
    Content Safety バックエンドとして選択する (Refs #1952)。
    それ以外は従来通り Model Armor を使う。
    """
    from .gcp import GCPSecurityClient

    service = str(config.get("service", "")).lower()
    content_safety_backend = (
        "vertex_ai_safety" if service == "vertex_ai_safety" else "model_armor"
    )

    harm_thresholds = config.get("harm_categories") or {}
    if not isinstance(harm_thresholds, dict):
        harm_thresholds = {}

    gcp_config = GCPSecurityConfig(
        project_id=config.get("project_id", ""),
        content_safety_backend=content_safety_backend,
        model_armor_template=config.get("template_name", ""),
        model_armor_region=config.get("location", "") if content_safety_backend == "model_armor" else "",
        vertex_ai_location=config.get("location", "global") if content_safety_backend == "vertex_ai_safety" else "global",
        vertex_harm_thresholds=harm_thresholds,
        vertex_judge_model=config.get("judge_model", "gemini-2.5-flash"),
        dlp_location=(pii_config or config).get("location", "global"),
        credentials_path=config.get("credentials_path"),
        credentials_json=config.get("credentials_json"),
        enabled=True,
    )

    return GCPSecurityClient(gcp_config)
