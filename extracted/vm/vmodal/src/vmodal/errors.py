from typing import List, Dict, Tuple, Optional, Any, Union
from dataclasses import dataclass
import os,sys
import fire


class SdkError(Exception):
    def __init__(self, message: str, status_code: int = 0, body: Any = None, details: Any = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.body = body
        self.details = details

    def __str__(self) -> str:
        parts = [str(self.message or self.__class__.__name__)]
        if self.status_code:
            parts.append(f"status={int(self.status_code)}")
        blob = ""
        if self.details not in (None, "", [], {}):
            blob = str(self.details)
        elif self.body not in (None, "", [], {}):
            blob = str(self.body)
        if blob:
            blob = blob.replace("\n", " ").strip()
            if len(blob) > 240:
                blob = blob[:237] + "..."
            parts.append(blob)
        return " | ".join(parts)


class AuthError(SdkError):
    pass


class ApiError(SdkError):
    pass


class ValidationFailed(SdkError):
    pass


class FeatureDisabled(SdkError):
    pass


if __name__ == "__main__":
    fire.Fire()
