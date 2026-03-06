"""Materials Project error classes for ferrox.

The actual API and S3 clients are implemented in Rust
(see ``ferrox.MPRester`` and ``ferrox.MPOpenData``).

All three exception classes are defined in Rust (via pyo3 create_exception)
so that errors raised from the Rust HTTP layer carry the correct type:
- ``MPClientError``: base class for all MP errors (network, missing data, etc.)
- ``MPHTTPError(MPClientError)``: HTTP-level errors (non-200 status codes)
- ``MPDecodeError(MPClientError)``: response parsing errors (XML, JSON)
"""

import ferrox._ferrox as _ferrox

MPClientError = _ferrox.mp.MPClientError
MPHTTPError = _ferrox.mp.MPHTTPError
MPDecodeError = _ferrox.mp.MPDecodeError
