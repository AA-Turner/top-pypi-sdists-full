"""
Pydantic Models for CMDB - firewall/access_proxy6

Runtime validation models for firewall/access_proxy6 configuration.
Generated from FortiOS schema version unknown.
"""

from __future__ import annotations

from pydantic import BaseModel, Field, field_validator
from typing import Any, Literal, Optional
from enum import Enum

# ============================================================================
# Enum Definitions for Child Table Fields (for fields with 4+ allowed values)
# ============================================================================

class AccessProxy6ApiGateway6SslCipherSuitesCipherEnum(str, Enum):
    """Allowed values for cipher field in api-gateway6.ssl-cipher-suites."""
    TLS_AES_128_GCM_SHA256 = "TLS-AES-128-GCM-SHA256"
    TLS_AES_256_GCM_SHA384 = "TLS-AES-256-GCM-SHA384"
    TLS_CHACHA20_POLY1305_SHA256 = "TLS-CHACHA20-POLY1305-SHA256"
    TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256 = "TLS-ECDHE-RSA-WITH-CHACHA20-POLY1305-SHA256"
    TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256 = "TLS-ECDHE-ECDSA-WITH-CHACHA20-POLY1305-SHA256"
    TLS_DHE_RSA_WITH_CHACHA20_POLY1305_SHA256 = "TLS-DHE-RSA-WITH-CHACHA20-POLY1305-SHA256"
    TLS_DHE_RSA_WITH_AES_128_CBC_SHA = "TLS-DHE-RSA-WITH-AES-128-CBC-SHA"
    TLS_DHE_RSA_WITH_AES_256_CBC_SHA = "TLS-DHE-RSA-WITH-AES-256-CBC-SHA"
    TLS_DHE_RSA_WITH_AES_128_CBC_SHA256 = "TLS-DHE-RSA-WITH-AES-128-CBC-SHA256"
    TLS_DHE_RSA_WITH_AES_128_GCM_SHA256 = "TLS-DHE-RSA-WITH-AES-128-GCM-SHA256"
    TLS_DHE_RSA_WITH_AES_256_CBC_SHA256 = "TLS-DHE-RSA-WITH-AES-256-CBC-SHA256"
    TLS_DHE_RSA_WITH_AES_256_GCM_SHA384 = "TLS-DHE-RSA-WITH-AES-256-GCM-SHA384"
    TLS_DHE_DSS_WITH_AES_128_CBC_SHA = "TLS-DHE-DSS-WITH-AES-128-CBC-SHA"
    TLS_DHE_DSS_WITH_AES_256_CBC_SHA = "TLS-DHE-DSS-WITH-AES-256-CBC-SHA"
    TLS_DHE_DSS_WITH_AES_128_CBC_SHA256 = "TLS-DHE-DSS-WITH-AES-128-CBC-SHA256"
    TLS_DHE_DSS_WITH_AES_128_GCM_SHA256 = "TLS-DHE-DSS-WITH-AES-128-GCM-SHA256"
    TLS_DHE_DSS_WITH_AES_256_CBC_SHA256 = "TLS-DHE-DSS-WITH-AES-256-CBC-SHA256"
    TLS_DHE_DSS_WITH_AES_256_GCM_SHA384 = "TLS-DHE-DSS-WITH-AES-256-GCM-SHA384"
    TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA = "TLS-ECDHE-RSA-WITH-AES-128-CBC-SHA"
    TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256 = "TLS-ECDHE-RSA-WITH-AES-128-CBC-SHA256"
    TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256 = "TLS-ECDHE-RSA-WITH-AES-128-GCM-SHA256"
    TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA = "TLS-ECDHE-RSA-WITH-AES-256-CBC-SHA"
    TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384 = "TLS-ECDHE-RSA-WITH-AES-256-CBC-SHA384"
    TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384 = "TLS-ECDHE-RSA-WITH-AES-256-GCM-SHA384"
    TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA = "TLS-ECDHE-ECDSA-WITH-AES-128-CBC-SHA"
    TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256 = "TLS-ECDHE-ECDSA-WITH-AES-128-CBC-SHA256"
    TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256 = "TLS-ECDHE-ECDSA-WITH-AES-128-GCM-SHA256"
    TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA = "TLS-ECDHE-ECDSA-WITH-AES-256-CBC-SHA"
    TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA384 = "TLS-ECDHE-ECDSA-WITH-AES-256-CBC-SHA384"
    TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384 = "TLS-ECDHE-ECDSA-WITH-AES-256-GCM-SHA384"
    TLS_RSA_WITH_AES_128_CBC_SHA = "TLS-RSA-WITH-AES-128-CBC-SHA"
    TLS_RSA_WITH_AES_256_CBC_SHA = "TLS-RSA-WITH-AES-256-CBC-SHA"
    TLS_RSA_WITH_AES_128_CBC_SHA256 = "TLS-RSA-WITH-AES-128-CBC-SHA256"
    TLS_RSA_WITH_AES_128_GCM_SHA256 = "TLS-RSA-WITH-AES-128-GCM-SHA256"
    TLS_RSA_WITH_AES_256_CBC_SHA256 = "TLS-RSA-WITH-AES-256-CBC-SHA256"
    TLS_RSA_WITH_AES_256_GCM_SHA384 = "TLS-RSA-WITH-AES-256-GCM-SHA384"
    TLS_RSA_WITH_CAMELLIA_128_CBC_SHA = "TLS-RSA-WITH-CAMELLIA-128-CBC-SHA"
    TLS_RSA_WITH_CAMELLIA_256_CBC_SHA = "TLS-RSA-WITH-CAMELLIA-256-CBC-SHA"
    TLS_RSA_WITH_CAMELLIA_128_CBC_SHA256 = "TLS-RSA-WITH-CAMELLIA-128-CBC-SHA256"
    TLS_RSA_WITH_CAMELLIA_256_CBC_SHA256 = "TLS-RSA-WITH-CAMELLIA-256-CBC-SHA256"
    TLS_DHE_RSA_WITH_3DES_EDE_CBC_SHA = "TLS-DHE-RSA-WITH-3DES-EDE-CBC-SHA"
    TLS_DHE_RSA_WITH_CAMELLIA_128_CBC_SHA = "TLS-DHE-RSA-WITH-CAMELLIA-128-CBC-SHA"
    TLS_DHE_DSS_WITH_CAMELLIA_128_CBC_SHA = "TLS-DHE-DSS-WITH-CAMELLIA-128-CBC-SHA"
    TLS_DHE_RSA_WITH_CAMELLIA_256_CBC_SHA = "TLS-DHE-RSA-WITH-CAMELLIA-256-CBC-SHA"
    TLS_DHE_DSS_WITH_CAMELLIA_256_CBC_SHA = "TLS-DHE-DSS-WITH-CAMELLIA-256-CBC-SHA"
    TLS_DHE_RSA_WITH_CAMELLIA_128_CBC_SHA256 = "TLS-DHE-RSA-WITH-CAMELLIA-128-CBC-SHA256"
    TLS_DHE_DSS_WITH_CAMELLIA_128_CBC_SHA256 = "TLS-DHE-DSS-WITH-CAMELLIA-128-CBC-SHA256"
    TLS_DHE_RSA_WITH_CAMELLIA_256_CBC_SHA256 = "TLS-DHE-RSA-WITH-CAMELLIA-256-CBC-SHA256"
    TLS_DHE_DSS_WITH_CAMELLIA_256_CBC_SHA256 = "TLS-DHE-DSS-WITH-CAMELLIA-256-CBC-SHA256"
    TLS_DHE_RSA_WITH_SEED_CBC_SHA = "TLS-DHE-RSA-WITH-SEED-CBC-SHA"
    TLS_DHE_DSS_WITH_SEED_CBC_SHA = "TLS-DHE-DSS-WITH-SEED-CBC-SHA"
    TLS_DHE_RSA_WITH_ARIA_128_CBC_SHA256 = "TLS-DHE-RSA-WITH-ARIA-128-CBC-SHA256"
    TLS_DHE_RSA_WITH_ARIA_256_CBC_SHA384 = "TLS-DHE-RSA-WITH-ARIA-256-CBC-SHA384"
    TLS_DHE_DSS_WITH_ARIA_128_CBC_SHA256 = "TLS-DHE-DSS-WITH-ARIA-128-CBC-SHA256"
    TLS_DHE_DSS_WITH_ARIA_256_CBC_SHA384 = "TLS-DHE-DSS-WITH-ARIA-256-CBC-SHA384"
    TLS_RSA_WITH_SEED_CBC_SHA = "TLS-RSA-WITH-SEED-CBC-SHA"
    TLS_RSA_WITH_ARIA_128_CBC_SHA256 = "TLS-RSA-WITH-ARIA-128-CBC-SHA256"
    TLS_RSA_WITH_ARIA_256_CBC_SHA384 = "TLS-RSA-WITH-ARIA-256-CBC-SHA384"
    TLS_ECDHE_RSA_WITH_ARIA_128_CBC_SHA256 = "TLS-ECDHE-RSA-WITH-ARIA-128-CBC-SHA256"
    TLS_ECDHE_RSA_WITH_ARIA_256_CBC_SHA384 = "TLS-ECDHE-RSA-WITH-ARIA-256-CBC-SHA384"
    TLS_ECDHE_ECDSA_WITH_ARIA_128_CBC_SHA256 = "TLS-ECDHE-ECDSA-WITH-ARIA-128-CBC-SHA256"
    TLS_ECDHE_ECDSA_WITH_ARIA_256_CBC_SHA384 = "TLS-ECDHE-ECDSA-WITH-ARIA-256-CBC-SHA384"
    TLS_ECDHE_RSA_WITH_RC4_128_SHA = "TLS-ECDHE-RSA-WITH-RC4-128-SHA"
    TLS_ECDHE_RSA_WITH_3DES_EDE_CBC_SHA = "TLS-ECDHE-RSA-WITH-3DES-EDE-CBC-SHA"
    TLS_DHE_DSS_WITH_3DES_EDE_CBC_SHA = "TLS-DHE-DSS-WITH-3DES-EDE-CBC-SHA"
    TLS_RSA_WITH_3DES_EDE_CBC_SHA = "TLS-RSA-WITH-3DES-EDE-CBC-SHA"
    TLS_RSA_WITH_RC4_128_MD5 = "TLS-RSA-WITH-RC4-128-MD5"
    TLS_RSA_WITH_RC4_128_SHA = "TLS-RSA-WITH-RC4-128-SHA"
    TLS_DHE_RSA_WITH_DES_CBC_SHA = "TLS-DHE-RSA-WITH-DES-CBC-SHA"
    TLS_DHE_DSS_WITH_DES_CBC_SHA = "TLS-DHE-DSS-WITH-DES-CBC-SHA"
    TLS_RSA_WITH_DES_CBC_SHA = "TLS-RSA-WITH-DES-CBC-SHA"

class AccessProxy6ApiGateway6SslCipherSuitesVersionsEnum(str, Enum):
    """Allowed values for versions field in api-gateway6.ssl-cipher-suites."""
    TLS_1_0 = "tls-1.0"
    TLS_1_1 = "tls-1.1"
    TLS_1_2 = "tls-1.2"
    TLS_1_3 = "tls-1.3"

class AccessProxy6ApiGateway6ServiceEnum(str, Enum):
    """Allowed values for service field in api-gateway6."""
    HTTP = "http"
    HTTPS = "https"
    TCP_FORWARDING = "tcp-forwarding"
    SAMLSP = "samlsp"
    WEB_PORTAL = "web-portal"
    SAAS = "saas"

class AccessProxy6ApiGateway6LdbMethodEnum(str, Enum):
    """Allowed values for ldb_method field in api-gateway6."""
    STATIC = "static"
    ROUND_ROBIN = "round-robin"
    WEIGHTED = "weighted"
    FIRST_ALIVE = "first-alive"
    HTTP_HOST = "http-host"

class AccessProxy6ApiGateway6SslDhBitsEnum(str, Enum):
    """Allowed values for ssl_dh_bits field in api-gateway6."""
    V_768 = "768"
    V_1024 = "1024"
    V_1536 = "1536"
    V_2048 = "2048"
    V_3072 = "3072"
    V_4096 = "4096"

class AccessProxy6ApiGateway6SslMinVersionEnum(str, Enum):
    """Allowed values for ssl_min_version field in api-gateway6."""
    TLS_1_0 = "tls-1.0"
    TLS_1_1 = "tls-1.1"
    TLS_1_2 = "tls-1.2"
    TLS_1_3 = "tls-1.3"

class AccessProxy6ApiGateway6SslMaxVersionEnum(str, Enum):
    """Allowed values for ssl_max_version field in api-gateway6."""
    TLS_1_0 = "tls-1.0"
    TLS_1_1 = "tls-1.1"
    TLS_1_2 = "tls-1.2"
    TLS_1_3 = "tls-1.3"

class AccessProxy6ApiGatewaySslCipherSuitesCipherEnum(str, Enum):
    """Allowed values for cipher field in api-gateway.ssl-cipher-suites."""
    TLS_AES_128_GCM_SHA256 = "TLS-AES-128-GCM-SHA256"
    TLS_AES_256_GCM_SHA384 = "TLS-AES-256-GCM-SHA384"
    TLS_CHACHA20_POLY1305_SHA256 = "TLS-CHACHA20-POLY1305-SHA256"
    TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256 = "TLS-ECDHE-RSA-WITH-CHACHA20-POLY1305-SHA256"
    TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256 = "TLS-ECDHE-ECDSA-WITH-CHACHA20-POLY1305-SHA256"
    TLS_DHE_RSA_WITH_CHACHA20_POLY1305_SHA256 = "TLS-DHE-RSA-WITH-CHACHA20-POLY1305-SHA256"
    TLS_DHE_RSA_WITH_AES_128_CBC_SHA = "TLS-DHE-RSA-WITH-AES-128-CBC-SHA"
    TLS_DHE_RSA_WITH_AES_256_CBC_SHA = "TLS-DHE-RSA-WITH-AES-256-CBC-SHA"
    TLS_DHE_RSA_WITH_AES_128_CBC_SHA256 = "TLS-DHE-RSA-WITH-AES-128-CBC-SHA256"
    TLS_DHE_RSA_WITH_AES_128_GCM_SHA256 = "TLS-DHE-RSA-WITH-AES-128-GCM-SHA256"
    TLS_DHE_RSA_WITH_AES_256_CBC_SHA256 = "TLS-DHE-RSA-WITH-AES-256-CBC-SHA256"
    TLS_DHE_RSA_WITH_AES_256_GCM_SHA384 = "TLS-DHE-RSA-WITH-AES-256-GCM-SHA384"
    TLS_DHE_DSS_WITH_AES_128_CBC_SHA = "TLS-DHE-DSS-WITH-AES-128-CBC-SHA"
    TLS_DHE_DSS_WITH_AES_256_CBC_SHA = "TLS-DHE-DSS-WITH-AES-256-CBC-SHA"
    TLS_DHE_DSS_WITH_AES_128_CBC_SHA256 = "TLS-DHE-DSS-WITH-AES-128-CBC-SHA256"
    TLS_DHE_DSS_WITH_AES_128_GCM_SHA256 = "TLS-DHE-DSS-WITH-AES-128-GCM-SHA256"
    TLS_DHE_DSS_WITH_AES_256_CBC_SHA256 = "TLS-DHE-DSS-WITH-AES-256-CBC-SHA256"
    TLS_DHE_DSS_WITH_AES_256_GCM_SHA384 = "TLS-DHE-DSS-WITH-AES-256-GCM-SHA384"
    TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA = "TLS-ECDHE-RSA-WITH-AES-128-CBC-SHA"
    TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256 = "TLS-ECDHE-RSA-WITH-AES-128-CBC-SHA256"
    TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256 = "TLS-ECDHE-RSA-WITH-AES-128-GCM-SHA256"
    TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA = "TLS-ECDHE-RSA-WITH-AES-256-CBC-SHA"
    TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384 = "TLS-ECDHE-RSA-WITH-AES-256-CBC-SHA384"
    TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384 = "TLS-ECDHE-RSA-WITH-AES-256-GCM-SHA384"
    TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA = "TLS-ECDHE-ECDSA-WITH-AES-128-CBC-SHA"
    TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256 = "TLS-ECDHE-ECDSA-WITH-AES-128-CBC-SHA256"
    TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256 = "TLS-ECDHE-ECDSA-WITH-AES-128-GCM-SHA256"
    TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA = "TLS-ECDHE-ECDSA-WITH-AES-256-CBC-SHA"
    TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA384 = "TLS-ECDHE-ECDSA-WITH-AES-256-CBC-SHA384"
    TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384 = "TLS-ECDHE-ECDSA-WITH-AES-256-GCM-SHA384"
    TLS_RSA_WITH_AES_128_CBC_SHA = "TLS-RSA-WITH-AES-128-CBC-SHA"
    TLS_RSA_WITH_AES_256_CBC_SHA = "TLS-RSA-WITH-AES-256-CBC-SHA"
    TLS_RSA_WITH_AES_128_CBC_SHA256 = "TLS-RSA-WITH-AES-128-CBC-SHA256"
    TLS_RSA_WITH_AES_128_GCM_SHA256 = "TLS-RSA-WITH-AES-128-GCM-SHA256"
    TLS_RSA_WITH_AES_256_CBC_SHA256 = "TLS-RSA-WITH-AES-256-CBC-SHA256"
    TLS_RSA_WITH_AES_256_GCM_SHA384 = "TLS-RSA-WITH-AES-256-GCM-SHA384"
    TLS_RSA_WITH_CAMELLIA_128_CBC_SHA = "TLS-RSA-WITH-CAMELLIA-128-CBC-SHA"
    TLS_RSA_WITH_CAMELLIA_256_CBC_SHA = "TLS-RSA-WITH-CAMELLIA-256-CBC-SHA"
    TLS_RSA_WITH_CAMELLIA_128_CBC_SHA256 = "TLS-RSA-WITH-CAMELLIA-128-CBC-SHA256"
    TLS_RSA_WITH_CAMELLIA_256_CBC_SHA256 = "TLS-RSA-WITH-CAMELLIA-256-CBC-SHA256"
    TLS_DHE_RSA_WITH_3DES_EDE_CBC_SHA = "TLS-DHE-RSA-WITH-3DES-EDE-CBC-SHA"
    TLS_DHE_RSA_WITH_CAMELLIA_128_CBC_SHA = "TLS-DHE-RSA-WITH-CAMELLIA-128-CBC-SHA"
    TLS_DHE_DSS_WITH_CAMELLIA_128_CBC_SHA = "TLS-DHE-DSS-WITH-CAMELLIA-128-CBC-SHA"
    TLS_DHE_RSA_WITH_CAMELLIA_256_CBC_SHA = "TLS-DHE-RSA-WITH-CAMELLIA-256-CBC-SHA"
    TLS_DHE_DSS_WITH_CAMELLIA_256_CBC_SHA = "TLS-DHE-DSS-WITH-CAMELLIA-256-CBC-SHA"
    TLS_DHE_RSA_WITH_CAMELLIA_128_CBC_SHA256 = "TLS-DHE-RSA-WITH-CAMELLIA-128-CBC-SHA256"
    TLS_DHE_DSS_WITH_CAMELLIA_128_CBC_SHA256 = "TLS-DHE-DSS-WITH-CAMELLIA-128-CBC-SHA256"
    TLS_DHE_RSA_WITH_CAMELLIA_256_CBC_SHA256 = "TLS-DHE-RSA-WITH-CAMELLIA-256-CBC-SHA256"
    TLS_DHE_DSS_WITH_CAMELLIA_256_CBC_SHA256 = "TLS-DHE-DSS-WITH-CAMELLIA-256-CBC-SHA256"
    TLS_DHE_RSA_WITH_SEED_CBC_SHA = "TLS-DHE-RSA-WITH-SEED-CBC-SHA"
    TLS_DHE_DSS_WITH_SEED_CBC_SHA = "TLS-DHE-DSS-WITH-SEED-CBC-SHA"
    TLS_DHE_RSA_WITH_ARIA_128_CBC_SHA256 = "TLS-DHE-RSA-WITH-ARIA-128-CBC-SHA256"
    TLS_DHE_RSA_WITH_ARIA_256_CBC_SHA384 = "TLS-DHE-RSA-WITH-ARIA-256-CBC-SHA384"
    TLS_DHE_DSS_WITH_ARIA_128_CBC_SHA256 = "TLS-DHE-DSS-WITH-ARIA-128-CBC-SHA256"
    TLS_DHE_DSS_WITH_ARIA_256_CBC_SHA384 = "TLS-DHE-DSS-WITH-ARIA-256-CBC-SHA384"
    TLS_RSA_WITH_SEED_CBC_SHA = "TLS-RSA-WITH-SEED-CBC-SHA"
    TLS_RSA_WITH_ARIA_128_CBC_SHA256 = "TLS-RSA-WITH-ARIA-128-CBC-SHA256"
    TLS_RSA_WITH_ARIA_256_CBC_SHA384 = "TLS-RSA-WITH-ARIA-256-CBC-SHA384"
    TLS_ECDHE_RSA_WITH_ARIA_128_CBC_SHA256 = "TLS-ECDHE-RSA-WITH-ARIA-128-CBC-SHA256"
    TLS_ECDHE_RSA_WITH_ARIA_256_CBC_SHA384 = "TLS-ECDHE-RSA-WITH-ARIA-256-CBC-SHA384"
    TLS_ECDHE_ECDSA_WITH_ARIA_128_CBC_SHA256 = "TLS-ECDHE-ECDSA-WITH-ARIA-128-CBC-SHA256"
    TLS_ECDHE_ECDSA_WITH_ARIA_256_CBC_SHA384 = "TLS-ECDHE-ECDSA-WITH-ARIA-256-CBC-SHA384"
    TLS_ECDHE_RSA_WITH_RC4_128_SHA = "TLS-ECDHE-RSA-WITH-RC4-128-SHA"
    TLS_ECDHE_RSA_WITH_3DES_EDE_CBC_SHA = "TLS-ECDHE-RSA-WITH-3DES-EDE-CBC-SHA"
    TLS_DHE_DSS_WITH_3DES_EDE_CBC_SHA = "TLS-DHE-DSS-WITH-3DES-EDE-CBC-SHA"
    TLS_RSA_WITH_3DES_EDE_CBC_SHA = "TLS-RSA-WITH-3DES-EDE-CBC-SHA"
    TLS_RSA_WITH_RC4_128_MD5 = "TLS-RSA-WITH-RC4-128-MD5"
    TLS_RSA_WITH_RC4_128_SHA = "TLS-RSA-WITH-RC4-128-SHA"
    TLS_DHE_RSA_WITH_DES_CBC_SHA = "TLS-DHE-RSA-WITH-DES-CBC-SHA"
    TLS_DHE_DSS_WITH_DES_CBC_SHA = "TLS-DHE-DSS-WITH-DES-CBC-SHA"
    TLS_RSA_WITH_DES_CBC_SHA = "TLS-RSA-WITH-DES-CBC-SHA"

class AccessProxy6ApiGatewaySslCipherSuitesVersionsEnum(str, Enum):
    """Allowed values for versions field in api-gateway.ssl-cipher-suites."""
    TLS_1_0 = "tls-1.0"
    TLS_1_1 = "tls-1.1"
    TLS_1_2 = "tls-1.2"
    TLS_1_3 = "tls-1.3"

class AccessProxy6ApiGatewayServiceEnum(str, Enum):
    """Allowed values for service field in api-gateway."""
    HTTP = "http"
    HTTPS = "https"
    TCP_FORWARDING = "tcp-forwarding"
    SAMLSP = "samlsp"
    WEB_PORTAL = "web-portal"
    SAAS = "saas"

class AccessProxy6ApiGatewayLdbMethodEnum(str, Enum):
    """Allowed values for ldb_method field in api-gateway."""
    STATIC = "static"
    ROUND_ROBIN = "round-robin"
    WEIGHTED = "weighted"
    FIRST_ALIVE = "first-alive"
    HTTP_HOST = "http-host"

class AccessProxy6ApiGatewaySslDhBitsEnum(str, Enum):
    """Allowed values for ssl_dh_bits field in api-gateway."""
    V_768 = "768"
    V_1024 = "1024"
    V_1536 = "1536"
    V_2048 = "2048"
    V_3072 = "3072"
    V_4096 = "4096"

class AccessProxy6ApiGatewaySslMinVersionEnum(str, Enum):
    """Allowed values for ssl_min_version field in api-gateway."""
    TLS_1_0 = "tls-1.0"
    TLS_1_1 = "tls-1.1"
    TLS_1_2 = "tls-1.2"
    TLS_1_3 = "tls-1.3"

class AccessProxy6ApiGatewaySslMaxVersionEnum(str, Enum):
    """Allowed values for ssl_max_version field in api-gateway."""
    TLS_1_0 = "tls-1.0"
    TLS_1_1 = "tls-1.1"
    TLS_1_2 = "tls-1.2"
    TLS_1_3 = "tls-1.3"

# ============================================================================
# Child Table Models (sorted deepest-first so nested models are defined before their parents)
# ============================================================================

class AccessProxy6ApiGateway6SslCipherSuites(BaseModel):
    """
    Child table model for api-gateway6.ssl-cipher-suites.
    
    SSL/TLS cipher suites to offer to a server, ordered by priority.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    priority: int | None = Field(ge=0, le=4294967295, default=0, description="SSL/TLS cipher suites priority.")    
    cipher: AccessProxy6ApiGateway6SslCipherSuitesCipherEnum = Field(description="Cipher suite name.")    
    versions: list[AccessProxy6ApiGateway6SslCipherSuitesVersionsEnum] = Field(default_factory=list, description="SSL/TLS versions that the cipher suite can be used with.")
class AccessProxy6ApiGateway6RealserversSshHostKey(BaseModel):
    """
    Child table model for api-gateway6.realservers.ssh-host-key.
    
    One or more server host key.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str | None = Field(max_length=79, default=None, description="Server host key name.")  # datasource: ['firewall.ssh.host-key.name']
class AccessProxy6ApiGateway6Realservers(BaseModel):
    """
    Child table model for api-gateway6.realservers.
    
    Select the real servers that this Access Proxy will distribute traffic to.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: int | None = Field(ge=0, le=4294967295, default=0, serialization_alias="id", description="Real server ID.")    
    addr_type: Literal["ip", "fqdn"] = Field(default="ip", description="Type of address.")    
    address: str | None = Field(max_length=79, default=None, description="Address or address group of the real server.")  # datasource: ['firewall.address6.name', 'firewall.addrgrp6.name']    
    ip: str = Field(default="::", description="IPv6 address of the real server.")    
    domain: str | None = Field(max_length=255, default=None, description="Wildcard domain name of the real server.")    
    port: int | None = Field(ge=1, le=65535, default=443, description="Port for communicating with the real server.")    
    mappedport: str | None = Field(default=None, description="Port for communicating with the real server.")    
    status: Literal["active", "standby", "disable"] | None = Field(default="active", description="Set the status of the real server to active so that it can accept traffic, or on standby or disabled so no traffic is sent.")    
    type_: Literal["tcp-forwarding", "ssh"] | None = Field(default="tcp-forwarding", serialization_alias="type", description="TCP forwarding server type.")    
    external_auth: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable use of external browser as user-agent for SAML user authentication.")    
    tunnel_encryption: Literal["enable", "disable"] | None = Field(default="disable", description="Tunnel encryption.")    
    weight: int | None = Field(ge=1, le=255, default=1, description="Weight of the real server. If weighted load balancing is enabled, the server with the highest weight gets more connections.")    
    http_host: str | None = Field(max_length=63, default=None, description="HTTP server domain name in HTTP header.")    
    health_check: Literal["disable", "enable"] | None = Field(default="disable", description="Enable to check the responsiveness of the real server before forwarding traffic.")    
    health_check_proto: Literal["ping", "http", "tcp-connect"] | None = Field(default="ping", description="Protocol of the health check monitor to use when polling to determine server's connectivity status.")    
    holddown_interval: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable holddown timer. Server will be considered active and reachable once the holddown period has expired (30 seconds).")    
    translate_host: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable translation of hostname/IP from virtual server to real server.")    
    ssh_client_cert: str | None = Field(max_length=79, default=None, description="Set access-proxy SSH client certificate profile.")  # datasource: ['firewall.access-proxy-ssh-client-cert.name']    
    ssh_host_key_validation: Literal["disable", "enable"] | None = Field(default="disable", description="Enable/disable SSH real server host key validation.")    
    ssh_host_key: list[AccessProxy6ApiGateway6RealserversSshHostKey] = Field(default_factory=list, description="One or more server host key.")    
    verify_cert: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable certificate verification of the real server.")
class AccessProxy6ApiGateway6Quic(BaseModel):
    """
    Child table model for api-gateway6.quic.
    
    QUIC setting.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    max_idle_timeout: int | None = Field(ge=1, le=60000, default=30000, description="Maximum idle timeout milliseconds (1 - 60000, default = 30000).")    
    max_udp_payload_size: int | None = Field(ge=1200, le=1500, default=1500, description="Maximum UDP payload size in bytes (1200 - 1500, default = 1500).")    
    active_connection_id_limit: int | None = Field(ge=1, le=8, default=2, description="Active connection ID limit (1 - 8, default = 2).")    
    ack_delay_exponent: int | None = Field(ge=1, le=20, default=3, description="ACK delay exponent (1 - 20, default = 3).")    
    max_ack_delay: int | None = Field(ge=1, le=16383, default=25, description="Maximum ACK delay in milliseconds (1 - 16383, default = 25).")    
    max_datagram_frame_size: int | None = Field(ge=1, le=1500, default=1500, description="Maximum datagram frame size in bytes (1 - 1500, default = 1500).")    
    active_migration: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable active migration (default = disable).")    
    grease_quic_bit: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable grease QUIC bit (default = enable).")
class AccessProxy6ApiGateway6Application(BaseModel):
    """
    Child table model for api-gateway6.application.
    
    SaaS application controlled by this Access Proxy.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str | None = Field(max_length=79, default=None, description="SaaS application name.")
class AccessProxy6ApiGateway6(BaseModel):
    """
    Child table model for api-gateway6.
    
    Set IPv6 API Gateway.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: int | None = Field(ge=0, le=4294967295, default=0, serialization_alias="id", description="API Gateway ID.")    
    url_map: str = Field(max_length=511, default="/", description="URL pattern to match.")    
    service: AccessProxy6ApiGateway6ServiceEnum = Field(default=AccessProxy6ApiGateway6ServiceEnum.HTTPS, description="Service.")    
    ldb_method: AccessProxy6ApiGateway6LdbMethodEnum | None = Field(default=AccessProxy6ApiGateway6LdbMethodEnum.STATIC, description="Method used to distribute sessions to real servers.")    
    virtual_host: str | None = Field(max_length=79, default=None, description="Virtual host.")  # datasource: ['firewall.access-proxy-virtual-host.name']    
    url_map_type: Literal["sub-string", "wildcard", "regex"] = Field(default="sub-string", description="Type of url-map.")    
    h2_support: Literal["enable", "disable"] = Field(default="enable", description="HTTP2 support, default=Enable.")    
    h3_support: Literal["enable", "disable"] | None = Field(default="disable", description="HTTP3/QUIC support, default=Disable.")    
    quic: AccessProxy6ApiGateway6Quic | None = Field(default=None, description="QUIC setting.")    
    realservers: list[AccessProxy6ApiGateway6Realservers] = Field(default_factory=list, description="Select the real servers that this Access Proxy will distribute traffic to.")    
    application: list[AccessProxy6ApiGateway6Application] = Field(description="SaaS application controlled by this Access Proxy.")    
    persistence: Literal["none", "http-cookie"] | None = Field(default="none", description="Configure how to make sure that clients connect to the same server every time they make a request that is part of the same session.")    
    http_cookie_domain_from_host: Literal["disable", "enable"] | None = Field(default="disable", description="Enable/disable use of HTTP cookie domain from host field in HTTP.")    
    http_cookie_domain: str | None = Field(max_length=35, default=None, description="Domain that HTTP cookie persistence should apply to.")    
    http_cookie_path: str | None = Field(max_length=35, default=None, description="Limit HTTP cookie persistence to the specified path.")    
    http_cookie_generation: int | None = Field(ge=0, le=4294967295, default=0, description="Generation of HTTP cookie to be accepted. Changing invalidates all existing cookies.")    
    http_cookie_age: int | None = Field(ge=0, le=525600, default=60, description="Time in minutes that client web browsers should keep a cookie. Default is 60 minutes. 0 = no time limit.")    
    http_cookie_share: Literal["disable", "same-ip"] | None = Field(default="same-ip", description="Control sharing of cookies across API Gateway. Use of same-ip means a cookie from one virtual server can be used by another. Disable stops cookie sharing.")    
    https_cookie_secure: Literal["disable", "enable"] | None = Field(default="disable", description="Enable/disable verification that inserted HTTPS cookies are secure.")    
    saml_server: str | None = Field(max_length=35, default=None, description="SAML service provider configuration for VIP authentication.")  # datasource: ['user.saml.name']    
    saml_redirect: Literal["disable", "enable"] | None = Field(default="enable", description="Enable/disable SAML redirection after successful authentication.")    
    ssl_dh_bits: AccessProxy6ApiGateway6SslDhBitsEnum | None = Field(default=AccessProxy6ApiGateway6SslDhBitsEnum.V_2048, description="Number of bits to use in the Diffie-Hellman exchange for RSA encryption of SSL sessions.")    
    ssl_algorithm: Literal["high", "medium", "low"] | None = Field(default="high", description="Permitted encryption algorithms for the server side of SSL full mode sessions according to encryption strength.")    
    ssl_cipher_suites: list[AccessProxy6ApiGateway6SslCipherSuites] = Field(default_factory=list, description="SSL/TLS cipher suites to offer to a server, ordered by priority.")    
    ssl_min_version: AccessProxy6ApiGateway6SslMinVersionEnum | None = Field(default=AccessProxy6ApiGateway6SslMinVersionEnum.TLS_1_1, description="Lowest SSL/TLS version acceptable from a server.")    
    ssl_max_version: AccessProxy6ApiGateway6SslMaxVersionEnum | None = Field(default=AccessProxy6ApiGateway6SslMaxVersionEnum.TLS_1_3, description="Highest SSL/TLS version acceptable from a server.")    
    ssl_renegotiation: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable secure renegotiation to comply with RFC 5746.")    
    ssl_vpn_web_portal: str | None = Field(max_length=35, default=None, description="Agentless VPN web portal.")  # datasource: ['vpn.ssl.web.portal.name']
class AccessProxy6ApiGatewaySslCipherSuites(BaseModel):
    """
    Child table model for api-gateway.ssl-cipher-suites.
    
    SSL/TLS cipher suites to offer to a server, ordered by priority.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    priority: int | None = Field(ge=0, le=4294967295, default=0, description="SSL/TLS cipher suites priority.")    
    cipher: AccessProxy6ApiGatewaySslCipherSuitesCipherEnum = Field(description="Cipher suite name.")    
    versions: list[AccessProxy6ApiGatewaySslCipherSuitesVersionsEnum] = Field(default_factory=list, description="SSL/TLS versions that the cipher suite can be used with.")
class AccessProxy6ApiGatewayRealserversSshHostKey(BaseModel):
    """
    Child table model for api-gateway.realservers.ssh-host-key.
    
    One or more server host key.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str | None = Field(max_length=79, default=None, description="Server host key name.")  # datasource: ['firewall.ssh.host-key.name']
class AccessProxy6ApiGatewayRealservers(BaseModel):
    """
    Child table model for api-gateway.realservers.
    
    Select the real servers that this Access Proxy will distribute traffic to.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: int | None = Field(ge=0, le=4294967295, default=0, serialization_alias="id", description="Real server ID.")    
    addr_type: Literal["ip", "fqdn"] = Field(default="ip", description="Type of address.")    
    address: str | None = Field(max_length=79, default=None, description="Address or address group of the real server.")  # datasource: ['firewall.address.name', 'firewall.addrgrp.name']    
    ip: str = Field(default="0.0.0.0", description="IP address of the real server.")    
    domain: str | None = Field(max_length=255, default=None, description="Wildcard domain name of the real server.")    
    port: int | None = Field(ge=1, le=65535, default=443, description="Port for communicating with the real server.")    
    mappedport: str | None = Field(default=None, description="Port for communicating with the real server.")    
    status: Literal["active", "standby", "disable"] | None = Field(default="active", description="Set the status of the real server to active so that it can accept traffic, or on standby or disabled so no traffic is sent.")    
    type_: Literal["tcp-forwarding", "ssh"] | None = Field(default="tcp-forwarding", serialization_alias="type", description="TCP forwarding server type.")    
    external_auth: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable use of external browser as user-agent for SAML user authentication.")    
    tunnel_encryption: Literal["enable", "disable"] | None = Field(default="disable", description="Tunnel encryption.")    
    weight: int | None = Field(ge=1, le=255, default=1, description="Weight of the real server. If weighted load balancing is enabled, the server with the highest weight gets more connections.")    
    http_host: str | None = Field(max_length=63, default=None, description="HTTP server domain name in HTTP header.")    
    health_check: Literal["disable", "enable"] | None = Field(default="disable", description="Enable to check the responsiveness of the real server before forwarding traffic.")    
    health_check_proto: Literal["ping", "http", "tcp-connect"] | None = Field(default="ping", description="Protocol of the health check monitor to use when polling to determine server's connectivity status.")    
    holddown_interval: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable holddown timer. Server will be considered active and reachable once the holddown period has expired (30 seconds).")    
    translate_host: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable translation of hostname/IP from virtual server to real server.")    
    ssh_client_cert: str | None = Field(max_length=79, default=None, description="Set access-proxy SSH client certificate profile.")  # datasource: ['firewall.access-proxy-ssh-client-cert.name']    
    ssh_host_key_validation: Literal["disable", "enable"] | None = Field(default="disable", description="Enable/disable SSH real server host key validation.")    
    ssh_host_key: list[AccessProxy6ApiGatewayRealserversSshHostKey] = Field(default_factory=list, description="One or more server host key.")    
    verify_cert: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable certificate verification of the real server.")
class AccessProxy6ApiGatewayQuic(BaseModel):
    """
    Child table model for api-gateway.quic.
    
    QUIC setting.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    max_idle_timeout: int | None = Field(ge=1, le=60000, default=30000, description="Maximum idle timeout milliseconds (1 - 60000, default = 30000).")    
    max_udp_payload_size: int | None = Field(ge=1200, le=1500, default=1500, description="Maximum UDP payload size in bytes (1200 - 1500, default = 1500).")    
    active_connection_id_limit: int | None = Field(ge=1, le=8, default=2, description="Active connection ID limit (1 - 8, default = 2).")    
    ack_delay_exponent: int | None = Field(ge=1, le=20, default=3, description="ACK delay exponent (1 - 20, default = 3).")    
    max_ack_delay: int | None = Field(ge=1, le=16383, default=25, description="Maximum ACK delay in milliseconds (1 - 16383, default = 25).")    
    max_datagram_frame_size: int | None = Field(ge=1, le=1500, default=1500, description="Maximum datagram frame size in bytes (1 - 1500, default = 1500).")    
    active_migration: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable active migration (default = disable).")    
    grease_quic_bit: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable grease QUIC bit (default = enable).")
class AccessProxy6ApiGatewayApplication(BaseModel):
    """
    Child table model for api-gateway.application.
    
    SaaS application controlled by this Access Proxy.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str | None = Field(max_length=79, default=None, description="SaaS application name.")
class AccessProxy6ApiGateway(BaseModel):
    """
    Child table model for api-gateway.
    
    Set IPv4 API Gateway.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: int | None = Field(ge=0, le=4294967295, default=0, serialization_alias="id", description="API Gateway ID.")    
    url_map: str = Field(max_length=511, default="/", description="URL pattern to match.")    
    service: AccessProxy6ApiGatewayServiceEnum = Field(default=AccessProxy6ApiGatewayServiceEnum.HTTPS, description="Service.")    
    ldb_method: AccessProxy6ApiGatewayLdbMethodEnum | None = Field(default=AccessProxy6ApiGatewayLdbMethodEnum.STATIC, description="Method used to distribute sessions to real servers.")    
    virtual_host: str | None = Field(max_length=79, default=None, description="Virtual host.")  # datasource: ['firewall.access-proxy-virtual-host.name']    
    url_map_type: Literal["sub-string", "wildcard", "regex"] = Field(default="sub-string", description="Type of url-map.")    
    h2_support: Literal["enable", "disable"] = Field(default="enable", description="HTTP2 support, default=Enable.")    
    h3_support: Literal["enable", "disable"] | None = Field(default="disable", description="HTTP3/QUIC support, default=Disable.")    
    quic: AccessProxy6ApiGatewayQuic | None = Field(default=None, description="QUIC setting.")    
    realservers: list[AccessProxy6ApiGatewayRealservers] = Field(default_factory=list, description="Select the real servers that this Access Proxy will distribute traffic to.")    
    application: list[AccessProxy6ApiGatewayApplication] = Field(description="SaaS application controlled by this Access Proxy.")    
    persistence: Literal["none", "http-cookie"] | None = Field(default="none", description="Configure how to make sure that clients connect to the same server every time they make a request that is part of the same session.")    
    http_cookie_domain_from_host: Literal["disable", "enable"] | None = Field(default="disable", description="Enable/disable use of HTTP cookie domain from host field in HTTP.")    
    http_cookie_domain: str | None = Field(max_length=35, default=None, description="Domain that HTTP cookie persistence should apply to.")    
    http_cookie_path: str | None = Field(max_length=35, default=None, description="Limit HTTP cookie persistence to the specified path.")    
    http_cookie_generation: int | None = Field(ge=0, le=4294967295, default=0, description="Generation of HTTP cookie to be accepted. Changing invalidates all existing cookies.")    
    http_cookie_age: int | None = Field(ge=0, le=525600, default=60, description="Time in minutes that client web browsers should keep a cookie. Default is 60 minutes. 0 = no time limit.")    
    http_cookie_share: Literal["disable", "same-ip"] | None = Field(default="same-ip", description="Control sharing of cookies across API Gateway. Use of same-ip means a cookie from one virtual server can be used by another. Disable stops cookie sharing.")    
    https_cookie_secure: Literal["disable", "enable"] | None = Field(default="disable", description="Enable/disable verification that inserted HTTPS cookies are secure.")    
    saml_server: str | None = Field(max_length=35, default=None, description="SAML service provider configuration for VIP authentication.")  # datasource: ['user.saml.name']    
    saml_redirect: Literal["disable", "enable"] | None = Field(default="enable", description="Enable/disable SAML redirection after successful authentication.")    
    ssl_dh_bits: AccessProxy6ApiGatewaySslDhBitsEnum | None = Field(default=AccessProxy6ApiGatewaySslDhBitsEnum.V_2048, description="Number of bits to use in the Diffie-Hellman exchange for RSA encryption of SSL sessions.")    
    ssl_algorithm: Literal["high", "medium", "low"] | None = Field(default="high", description="Permitted encryption algorithms for the server side of SSL full mode sessions according to encryption strength.")    
    ssl_cipher_suites: list[AccessProxy6ApiGatewaySslCipherSuites] = Field(default_factory=list, description="SSL/TLS cipher suites to offer to a server, ordered by priority.")    
    ssl_min_version: AccessProxy6ApiGatewaySslMinVersionEnum | None = Field(default=AccessProxy6ApiGatewaySslMinVersionEnum.TLS_1_1, description="Lowest SSL/TLS version acceptable from a server.")    
    ssl_max_version: AccessProxy6ApiGatewaySslMaxVersionEnum | None = Field(default=AccessProxy6ApiGatewaySslMaxVersionEnum.TLS_1_3, description="Highest SSL/TLS version acceptable from a server.")    
    ssl_renegotiation: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable secure renegotiation to comply with RFC 5746.")    
    ssl_vpn_web_portal: str | None = Field(max_length=35, default=None, description="Agentless VPN web portal.")  # datasource: ['vpn.ssl.web.portal.name']
# ============================================================================
# Enum Definitions (for fields with 4+ allowed values)
# ============================================================================


# ============================================================================
# Main Model
# ============================================================================

class AccessProxy6Model(BaseModel):
    """
    Pydantic model for firewall/access_proxy6 configuration.
    
    Configure IPv6 access proxy.
    
    Validation Rules:        - name: max_length=79 pattern=        - vip: max_length=79 pattern=        - auth_portal: pattern=        - auth_virtual_host: max_length=79 pattern=        - log_blocked_traffic: pattern=        - add_vhost_domain_to_dnsdb: pattern=        - svr_pool_multiplex: pattern=        - svr_pool_ttl: min=0 max=2147483647 pattern=        - svr_pool_server_max_request: min=0 max=2147483647 pattern=        - svr_pool_server_max_concurrent_request: min=0 max=2147483647 pattern=        - decrypted_traffic_mirror: max_length=35 pattern=        - api_gateway: pattern=        - api_gateway6: pattern=    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        validate_assignment = True  # Validate on attribute assignment
        use_enum_values = True  # Use enum values instead of names
    
    # ========================================================================
    # Model Fields
    # ========================================================================
    
    name: str | None = Field(max_length=79, default=None, description="Access Proxy name.")    
    vip: str = Field(max_length=79, description="Virtual IP name.")  # datasource: ['firewall.vip6.name']    
    auth_portal: Literal["disable", "enable"] | None = Field(default="disable", description="Enable/disable authentication portal.")    
    auth_virtual_host: str | None = Field(max_length=79, default=None, description="Virtual host for authentication portal.")  # datasource: ['firewall.access-proxy-virtual-host.name']    
    log_blocked_traffic: Literal["enable", "disable"] | None = Field(default="enable", description="Enable/disable logging of blocked traffic.")    
    add_vhost_domain_to_dnsdb: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable adding vhost/domain to dnsdb for ztna dox tunnel.")    
    svr_pool_multiplex: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable server pool multiplexing (default = disable). Share connected server in HTTP, HTTPS, and web-portal api-gateway.")    
    svr_pool_ttl: int | None = Field(ge=0, le=2147483647, default=15, description="Time-to-live in the server pool for idle connections to servers.")    
    svr_pool_server_max_request: int | None = Field(ge=0, le=2147483647, default=0, description="Maximum number of requests that servers in server pool handle before disconnecting (default = unlimited).")    
    svr_pool_server_max_concurrent_request: int | None = Field(ge=0, le=2147483647, default=0, description="Maximum number of concurrent requests that servers in server pool could handle (default = unlimited).")    
    decrypted_traffic_mirror: str | None = Field(max_length=35, default=None, description="Decrypted traffic mirror.")  # datasource: ['firewall.decrypted-traffic-mirror.name']    
    api_gateway: list[AccessProxy6ApiGateway] = Field(default_factory=list, description="Set IPv4 API Gateway.")    
    api_gateway6: list[AccessProxy6ApiGateway6] = Field(default_factory=list, description="Set IPv6 API Gateway.")    
    # ========================================================================
    # Custom Validators
    # ========================================================================
    
    @field_validator('vip')
    @classmethod
    def validate_vip(cls, v: Any) -> Any:
        """
        Validate vip field.
        
        Datasource: ['firewall.vip6.name']
        
        Note:
            This validator only checks basic constraints.
            To validate that referenced object exists, query the API.
        """
        # Basic validation passed via Field() constraints
        # Additional datasource validation could be added here
        return v    
    @field_validator('auth_virtual_host')
    @classmethod
    def validate_auth_virtual_host(cls, v: Any) -> Any:
        """
        Validate auth_virtual_host field.
        
        Datasource: ['firewall.access-proxy-virtual-host.name']
        
        Note:
            This validator only checks basic constraints.
            To validate that referenced object exists, query the API.
        """
        # Basic validation passed via Field() constraints
        # Additional datasource validation could be added here
        return v    
    @field_validator('decrypted_traffic_mirror')
    @classmethod
    def validate_decrypted_traffic_mirror(cls, v: Any) -> Any:
        """
        Validate decrypted_traffic_mirror field.
        
        Datasource: ['firewall.decrypted-traffic-mirror.name']
        
        Note:
            This validator only checks basic constraints.
            To validate that referenced object exists, query the API.
        """
        # Basic validation passed via Field() constraints
        # Additional datasource validation could be added here
        return v    
    # ========================================================================
    # Helper Methods
    # ========================================================================
    
    def to_fortios_dict(self) -> dict[str, Any]:
        """
        Convert model to FortiOS API payload format.
        
        Returns:
            Dict suitable for POST/PUT operations
        """
        # Export with exclude_none to avoid sending null values
        return self.model_dump(exclude_none=True, by_alias=True)
    
    @classmethod
    def from_fortios_response(cls, data: dict[str, Any]) -> "AccessProxy6Model":
        """
        Create model instance from FortiOS API response.
        
        Args:
            data: Response data from API
            
        Returns:
            Validated model instance
        """
        return cls(**data)
    # ========================================================================
    # Datasource Validation Methods
    # ========================================================================    
    async def validate_vip_references(self, client: Any) -> list[str]:
        """
        Validate vip references exist in FortiGate.
        
        This method checks if referenced objects exist by calling exists() on
        the appropriate API endpoints. This is an OPTIONAL validation step that
        can be called before posting to the API to catch reference errors early.
        
        Datasource endpoints checked:
        - firewall/vip6        
        Args:
            client: FortiOS client instance (from fgt._client)
            
        Returns:
            List of validation error messages (empty if all valid)
            
        Example:
            >>> from hfortix_fortios import FortiOS
            >>> 
            >>> fgt = FortiOS(host="192.168.1.1", token="your-token")
            >>> policy = AccessProxy6Model(
            ...     vip="invalid-name",
            ... )
            >>> 
            >>> # Validate before posting
            >>> errors = await policy.validate_vip_references(fgt._client)
            >>> if errors:
            ...     print("Validation failed:", errors)
            ... else:
            ...     result = await fgt.api.cmdb.firewall.access_proxy6.post(policy.to_fortios_dict())
        """
        errors: list[str] = []
        
        # Validate scalar field
        value = getattr(self, "vip", None)
        if not value:
            return errors
        
        # Check all datasource endpoints
        found = False
        if await client.api.cmdb.firewall.vip6.exists(value):
            found = True
        
        if not found:
            errors.append(
                f"Vip '{value}' not found in "
                "firewall/vip6"
            )        
        return errors    
    async def validate_auth_virtual_host_references(self, client: Any) -> list[str]:
        """
        Validate auth_virtual_host references exist in FortiGate.
        
        This method checks if referenced objects exist by calling exists() on
        the appropriate API endpoints. This is an OPTIONAL validation step that
        can be called before posting to the API to catch reference errors early.
        
        Datasource endpoints checked:
        - firewall/access-proxy-virtual-host        
        Args:
            client: FortiOS client instance (from fgt._client)
            
        Returns:
            List of validation error messages (empty if all valid)
            
        Example:
            >>> from hfortix_fortios import FortiOS
            >>> 
            >>> fgt = FortiOS(host="192.168.1.1", token="your-token")
            >>> policy = AccessProxy6Model(
            ...     auth_virtual_host="invalid-name",
            ... )
            >>> 
            >>> # Validate before posting
            >>> errors = await policy.validate_auth_virtual_host_references(fgt._client)
            >>> if errors:
            ...     print("Validation failed:", errors)
            ... else:
            ...     result = await fgt.api.cmdb.firewall.access_proxy6.post(policy.to_fortios_dict())
        """
        errors: list[str] = []
        
        # Validate scalar field
        value = getattr(self, "auth_virtual_host", None)
        if not value:
            return errors
        
        # Check all datasource endpoints
        found = False
        if await client.api.cmdb.firewall.access_proxy_virtual_host.exists(value):
            found = True
        
        if not found:
            errors.append(
                f"Auth-Virtual-Host '{value}' not found in "
                "firewall/access-proxy-virtual-host"
            )        
        return errors    
    async def validate_decrypted_traffic_mirror_references(self, client: Any) -> list[str]:
        """
        Validate decrypted_traffic_mirror references exist in FortiGate.
        
        This method checks if referenced objects exist by calling exists() on
        the appropriate API endpoints. This is an OPTIONAL validation step that
        can be called before posting to the API to catch reference errors early.
        
        Datasource endpoints checked:
        - firewall/decrypted-traffic-mirror        
        Args:
            client: FortiOS client instance (from fgt._client)
            
        Returns:
            List of validation error messages (empty if all valid)
            
        Example:
            >>> from hfortix_fortios import FortiOS
            >>> 
            >>> fgt = FortiOS(host="192.168.1.1", token="your-token")
            >>> policy = AccessProxy6Model(
            ...     decrypted_traffic_mirror="invalid-name",
            ... )
            >>> 
            >>> # Validate before posting
            >>> errors = await policy.validate_decrypted_traffic_mirror_references(fgt._client)
            >>> if errors:
            ...     print("Validation failed:", errors)
            ... else:
            ...     result = await fgt.api.cmdb.firewall.access_proxy6.post(policy.to_fortios_dict())
        """
        errors: list[str] = []
        
        # Validate scalar field
        value = getattr(self, "decrypted_traffic_mirror", None)
        if not value:
            return errors
        
        # Check all datasource endpoints
        found = False
        if await client.api.cmdb.firewall.decrypted_traffic_mirror.exists(value):
            found = True
        
        if not found:
            errors.append(
                f"Decrypted-Traffic-Mirror '{value}' not found in "
                "firewall/decrypted-traffic-mirror"
            )        
        return errors    
    async def validate_api_gateway_references(self, client: Any) -> list[str]:
        """
        Validate api_gateway references exist in FortiGate.
        
        This method checks if referenced objects exist by calling exists() on
        the appropriate API endpoints. This is an OPTIONAL validation step that
        can be called before posting to the API to catch reference errors early.
        
        Datasource endpoints checked:
        - vpn/ssl/web/portal        
        Args:
            client: FortiOS client instance (from fgt._client)
            
        Returns:
            List of validation error messages (empty if all valid)
            
        Example:
            >>> from hfortix_fortios import FortiOS
            >>> 
            >>> fgt = FortiOS(host="192.168.1.1", token="your-token")
            >>> policy = AccessProxy6Model(
            ...     api_gateway=[{"ssl-vpn-web-portal": "invalid-name"}],
            ... )
            >>> 
            >>> # Validate before posting
            >>> errors = await policy.validate_api_gateway_references(fgt._client)
            >>> if errors:
            ...     print("Validation failed:", errors)
            ... else:
            ...     result = await fgt.api.cmdb.firewall.access_proxy6.post(policy.to_fortios_dict())
        """
        errors: list[str] = []
        
        # Validate child table items
        values = getattr(self, "api_gateway", [])
        if not values:
            return errors
        
        for item in values:
            if isinstance(item, dict):
                value = item.get("ssl-vpn-web-portal")
            else:
                value = getattr(item, "ssl-vpn-web-portal", None)
            
            if not value:
                continue
            
            # Check all datasource endpoints
            found = False
            if await client.api.cmdb.vpn.ssl.web.portal.exists(value):
                found = True
            
            if not found:
                errors.append(
                    f"Api-Gateway '{value}' not found in "
                    "vpn/ssl/web/portal"
                )        
        return errors    
    async def validate_api_gateway6_references(self, client: Any) -> list[str]:
        """
        Validate api_gateway6 references exist in FortiGate.
        
        This method checks if referenced objects exist by calling exists() on
        the appropriate API endpoints. This is an OPTIONAL validation step that
        can be called before posting to the API to catch reference errors early.
        
        Datasource endpoints checked:
        - vpn/ssl/web/portal        
        Args:
            client: FortiOS client instance (from fgt._client)
            
        Returns:
            List of validation error messages (empty if all valid)
            
        Example:
            >>> from hfortix_fortios import FortiOS
            >>> 
            >>> fgt = FortiOS(host="192.168.1.1", token="your-token")
            >>> policy = AccessProxy6Model(
            ...     api_gateway6=[{"ssl-vpn-web-portal": "invalid-name"}],
            ... )
            >>> 
            >>> # Validate before posting
            >>> errors = await policy.validate_api_gateway6_references(fgt._client)
            >>> if errors:
            ...     print("Validation failed:", errors)
            ... else:
            ...     result = await fgt.api.cmdb.firewall.access_proxy6.post(policy.to_fortios_dict())
        """
        errors: list[str] = []
        
        # Validate child table items
        values = getattr(self, "api_gateway6", [])
        if not values:
            return errors
        
        for item in values:
            if isinstance(item, dict):
                value = item.get("ssl-vpn-web-portal")
            else:
                value = getattr(item, "ssl-vpn-web-portal", None)
            
            if not value:
                continue
            
            # Check all datasource endpoints
            found = False
            if await client.api.cmdb.vpn.ssl.web.portal.exists(value):
                found = True
            
            if not found:
                errors.append(
                    f"Api-Gateway6 '{value}' not found in "
                    "vpn/ssl/web/portal"
                )        
        return errors    
    async def validate_all_references(self, client: Any) -> list[str]:
        """
        Validate ALL datasource references in this model.
        
        Convenience method that runs all validate_*_references() methods
        and aggregates the results.
        
        Args:
            client: FortiOS client instance (from fgt._client)
            
        Returns:
            List of all validation errors found
            
        Example:
            >>> errors = await policy.validate_all_references(fgt._client)
            >>> if errors:
            ...     for error in errors:
            ...         print(f"  - {error}")
        """
        all_errors = []
        
        errors = await self.validate_vip_references(client)
        all_errors.extend(errors)        
        errors = await self.validate_auth_virtual_host_references(client)
        all_errors.extend(errors)        
        errors = await self.validate_decrypted_traffic_mirror_references(client)
        all_errors.extend(errors)        
        errors = await self.validate_api_gateway_references(client)
        all_errors.extend(errors)        
        errors = await self.validate_api_gateway6_references(client)
        all_errors.extend(errors)        
        return all_errors

# ============================================================================
# Type Aliases for Convenience
# ============================================================================

Dict = dict[str, Any]  # For backward compatibility

# ============================================================================
# Module Exports
# ============================================================================

__all__ = [
    "AccessProxy6Model",    "AccessProxy6ApiGateway",    "AccessProxy6ApiGateway.Quic",    "AccessProxy6ApiGateway.Realservers",    "AccessProxy6ApiGateway.Realservers.SshHostKey",    "AccessProxy6ApiGateway.Application",    "AccessProxy6ApiGateway.SslCipherSuites",    "AccessProxy6ApiGateway6",    "AccessProxy6ApiGateway6.Quic",    "AccessProxy6ApiGateway6.Realservers",    "AccessProxy6ApiGateway6.Realservers.SshHostKey",    "AccessProxy6ApiGateway6.Application",    "AccessProxy6ApiGateway6.SslCipherSuites",]


# ============================================================================
# Generated by hfortix generator v0.6.0
# Schema: 1.7.4
# Generated: 2026-02-02T00:53:56.992364Z
# ============================================================================