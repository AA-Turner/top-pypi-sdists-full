import json
import os
import uuid
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional


@dataclass
class SecretEntry:
    key: str
    value: str
    placeholder: str = field(default="")

    def __post_init__(self) -> None:
        if not self.placeholder:
            self.placeholder = f"{{{{SECRET_{uuid.uuid4().hex[:12]}}}}}"


class SecretManager:
    def __init__(self) -> None:
        self._secrets: Dict[str, SecretEntry] = {}
        self._value_to_placeholder: Dict[str, str] = {}
        self._placeholder_to_value: Dict[str, str] = {}

    def load_secrets(self, secrets_json: Optional[str] = None) -> int:
        if secrets_json is None:
            secrets_json = os.getenv("AGENT_SECRETS", "") or os.getenv(
                "USER_SECRETS", ""
            )
        if not secrets_json:
            return 0
        try:
            secrets_dict = json.loads(secrets_json)
            if not isinstance(secrets_dict, dict):
                return 0
            return self.register_secrets(secrets_dict)
        except json.JSONDecodeError:
            return 0

    def register_secrets(self, secrets: Dict[str, str]) -> int:
        count = 0
        for key, value in secrets.items():
            if value and len(str(value)) > 0:
                self.register_secret(key, str(value))
                count += 1
        return count

    def register_secret(self, key: str, value: str) -> str:
        if not value:
            return value
        if value in self._value_to_placeholder:
            return self._value_to_placeholder[value]
        entry = SecretEntry(key=key, value=value)
        self._secrets[key] = entry
        self._value_to_placeholder[value] = entry.placeholder
        self._placeholder_to_value[entry.placeholder] = value
        return entry.placeholder

    def mask(self, content: str) -> str:
        if not content or not self._value_to_placeholder:
            return content
        masked = str(content)
        sorted_secrets = sorted(
            self._value_to_placeholder.items(), key=lambda x: len(x[0]), reverse=True
        )
        for value, placeholder in sorted_secrets:
            if value in masked:
                masked = masked.replace(value, placeholder)
        return masked

    def unmask(self, content: str) -> str:
        if not content or not self._placeholder_to_value:
            return content
        unmasked = str(content)
        for placeholder, value in self._placeholder_to_value.items():
            if placeholder in unmasked:
                unmasked = unmasked.replace(placeholder, value)
        return unmasked

    def mask_dict(self, data: Any) -> Any:
        return self._transform(data, self.mask)

    def unmask_dict(self, data: Any) -> Any:
        return self._transform(data, self.unmask)

    def _transform(self, data: Any, fn: Callable[[str], str]) -> Any:
        if isinstance(data, str):
            return fn(data)
        elif isinstance(data, dict):
            return {k: self._transform(v, fn) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._transform(item, fn) for item in data]
        return data

    def get_secrets_for_prompt(self) -> str:
        if not self._secrets:
            return ""
        lines = []
        for key, entry in self._secrets.items():
            lines.append(
                f'- For field "{key}" -> TYPE THIS EXACT VALUE: {entry.placeholder}'
            )
        return (
            "\n\n## Available Secrets for Authentication\n"
            "CRITICAL: Type the placeholder value ({{SECRET_...}}), NOT the field name!\n\n"
            + "\n".join(lines)
            + "\n"
        )

    def has_secrets(self) -> bool:
        return len(self._secrets) > 0

    def get_secret_keys(self) -> List[str]:
        return list(self._secrets.keys())

    def clear(self) -> None:
        self._secrets.clear()
        self._value_to_placeholder.clear()
        self._placeholder_to_value.clear()
