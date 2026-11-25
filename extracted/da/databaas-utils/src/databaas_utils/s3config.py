"""botocore settings shared by every S3 client this package builds."""

from __future__ import annotations

# botocore >= 1.36 sends uploads as aws-chunked with a checksum trailer and no
# Content-Length by default; Scaleway and RustFS reject that.
CHECKSUMS = {
    "request_checksum_calculation": "when_required",
    "response_checksum_validation": "when_required",
}
