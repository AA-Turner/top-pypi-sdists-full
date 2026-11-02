"""Base64url must have zero unused bits and no padding."""

import pytest

from agentic_devtools.cli.ci.pipeline.conflict_reconciliation import ReconciliationValidationError, _decode_base64url


def test_canonical_padding_bits():
    assert _decode_base64url("AA") == b"\0"
    with pytest.raises(ReconciliationValidationError, match="invalid_base64url"):
        _decode_base64url("AB")
