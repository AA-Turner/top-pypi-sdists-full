import json

from mistralai.extra.workflows.encoding import (
    PayloadEncoder,
    PayloadEncryptionConfig,
    PayloadEncryptionMode,
)


class TraceEncoder:
    """Temporal-specific encoder for masking encrypted data in traces."""

    def __init__(
        self,
        encryption_config: PayloadEncryptionConfig | None = None,
    ) -> None:
        self.encryption_config = encryption_config

    def encode_trace_data(self, data: str) -> str:
        if self.encryption_config is None:
            return data

        if self.encryption_config.mode == PayloadEncryptionMode.FULL:
            return "**ENCRYPTED**"

        if self.encryption_config.mode == PayloadEncryptionMode.PARTIAL:
            try:
                obj = json.loads(data)
            except json.decoder.JSONDecodeError:
                return data
            encrypted_fields = PayloadEncoder._extract_encrypted_fields(obj)
            for encrypted_field in encrypted_fields:
                encrypted_field["data"] = "**ENCRYPTED**"
            return json.dumps(obj)

        return data
