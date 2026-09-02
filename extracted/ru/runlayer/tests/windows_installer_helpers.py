"""Shared payload builders for Windows installer tests."""

import json

from runlayer_cli.windows_installer_verifier import WINDOWS_SIGNER_IDENTITY_EKU_OID


AIWATCH_UPGRADE_CODE = "{E3A2F1C0-7B4D-4E9A-8C6F-1D2E3F4A5B6C}"
AIWATCH_PRODUCT_NAME = "Runlayer AI Watch"


def authenticode_payload(
    *,
    status: str = "Valid",
    signer_name: str = "Anysource Inc",
    issuer_name: str = "Microsoft ID Verified CS EOC CA 04",
    eku_oids: list[str] | None = None,
    upgrade_code: str = AIWATCH_UPGRADE_CODE,
    product_name: str = AIWATCH_PRODUCT_NAME,
    product_version: str = "2.0.0",
    template: str = "x64;1033",
    self_update_ready: str = "1",
) -> str:
    return json.dumps(
        {
            "Status": status,
            "SignerName": signer_name,
            "IssuerName": issuer_name,
            "EnhancedKeyUsageOids": (
                [WINDOWS_SIGNER_IDENTITY_EKU_OID] if eku_oids is None else eku_oids
            ),
            "MsiUpgradeCode": upgrade_code,
            "MsiProductName": product_name,
            "MsiProductVersion": product_version,
            "MsiTemplate": template,
            "MsiSelfUpdateReady": self_update_ready,
        }
    )
