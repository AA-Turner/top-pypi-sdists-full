"""Legacy import path; the implementation moved to xpander_sdk.media.caps (re-exported verbatim)."""

import xpander_sdk.media.caps as _impl

globals().update({k: v for k, v in vars(_impl).items() if not k.startswith("__")})
