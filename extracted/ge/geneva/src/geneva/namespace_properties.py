# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

SENSITIVE_NAMESPACE_PROPERTY_PARTS = (
    "access_key",
    "account_key",
    "api_key",
    "apikey",
    "credential",
    "password",
    "secret",
    "session_token",
    "token",
    "x_api_key",
    "x-api-key",
)


def is_sensitive_namespace_property(key: str) -> bool:
    key_lower = key.lower()
    normalized_key = key_lower.replace("-", "_")
    return any(
        part in key_lower or part in normalized_key
        for part in SENSITIVE_NAMESPACE_PROPERTY_PARTS
    )
