"""
AGENTICSTAR Platform SDK - Security Module
マルチクラウド対応のセキュリティクライアント

サポートプロバイダー:
- Azure Content Safety + Language Service (実装済み)
- AWS Bedrock Guardrails / Comprehend (実装済み)
- Google Cloud:
    - PII: Cloud DLP (全リージョン対応)
    - Content Safety: Model Armor / Vertex AI Safety Filters + Gemini judge
      (マーケットプレイス全リージョン対応は vertex_ai_safety を使う, Refs #1952)

Example:
    # Azure Security (Content Safety + PII)
    from agenticstar_platform.security import (
        AzureSecurityClient,
        AzureSecurityConfig,
    )

    config = AzureSecurityConfig(
        content_safety_endpoint="https://xxx.cognitiveservices.azure.com",
        content_safety_api_key="xxx",
        language_endpoint="https://xxx.cognitiveservices.azure.com",
        language_api_key="xxx",
    )
    client = AzureSecurityClient(config)

    # 統合セキュリティチェック
    result = await client.check_security(
        text="user input",
        check_moderation=True,
        check_prompt_shield=True,
        check_pii=True,
    )

    if not result.allowed:
        print(f"Violations: {result.violations}")

    # PII検出・マスク
    pii_result = await client.detect_pii("My email is test@example.com")
    print(pii_result.masked_text)  # "My email is ***"

    await client.close()
"""

# Base classes and types
from .base import (
    # Enums
    SecurityProvider,
    ContentCategory,
    PIICategory,
    # Errors
    SecurityError,
    SecurityConfigError,
    SecurityAPIError,
    # Result types
    ContentModerationResult,
    PromptShieldResult,
    PIIEntity,
    PIIDetectionResult,
    SecurityCheckResult,
    # Config types
    AzureSecurityConfig,
    AWSSecurityConfig,
    GCPSecurityConfig,
    SecurityConfig,
    # Protocol/ABC
    SecurityClientProtocol,
    SecurityClientBase,
)

# Provider implementations
from .azure import AzureSecurityClient
from .aws import AWSSecurityClient
from .gcp import GCPSecurityClient

# Factory
from .factory import (
    create_security_client,
    create_content_safety_client,
    create_pii_client,
    detect_provider,
)

# Content Safety Validator
from .content_safety_validator import (
    ContentSafetyValidator,
    GuardrailsConfig,
    SanitizationResult,
)

# Backward compatibility alias
ExternalContentSanitizer = ContentSafetyValidator

__all__ = [
    # Enums
    "SecurityProvider",
    "ContentCategory",
    "PIICategory",
    # Errors
    "SecurityError",
    "SecurityConfigError",
    "SecurityAPIError",
    # Result types
    "ContentModerationResult",
    "PromptShieldResult",
    "PIIEntity",
    "PIIDetectionResult",
    "SecurityCheckResult",
    # Config types
    "AzureSecurityConfig",
    "AWSSecurityConfig",
    "GCPSecurityConfig",
    "SecurityConfig",
    # Protocol/ABC
    "SecurityClientProtocol",
    "SecurityClientBase",
    # Provider implementations
    "AzureSecurityClient",
    "AWSSecurityClient",
    "GCPSecurityClient",
    # Factory
    "create_security_client",
    "create_content_safety_client",
    "create_pii_client",
    "detect_provider",
    # Content Safety Validator
    "ContentSafetyValidator",
    "GuardrailsConfig",
    "SanitizationResult",
    # Backward compatibility
    "ExternalContentSanitizer",
]
