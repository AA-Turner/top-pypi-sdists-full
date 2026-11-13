"""Lifted verbatim from fitevict/cli/update.py (sha256 9674abefdb70541a): validate_artifact and what they reach in that file.
Written by tools/refactors/core-off-fitevict-20261110/lift.py; the definitions below are the original text."""
from __future__ import annotations

import re
from urllib.parse import urlsplit


def validate_artifact(value):
    if not isinstance(value, dict) or set(value) != {'url', 'sha256'}:
        raise ValueError('Artifact requires url and sha256')
    parts = urlsplit(value['url'])
    if parts.scheme != 'https' or not parts.hostname or parts.username or parts.password:
        raise ValueError('Artifact must be an HTTPS Secure Files share URL')
    if not isinstance(value['sha256'], str) or not re.fullmatch('[a-f0-9]{64}', value['sha256']):
        raise ValueError('Artifact requires a SHA256 digest')
    return dict(value)
