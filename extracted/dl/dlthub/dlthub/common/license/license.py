"""Issue, validate license and manage scopes"""

import time
from datetime import datetime  # noqa: TID251
from uuid import uuid4
from typing import (
    ClassVar,
    Dict,
    Iterable,
    Set,
    Tuple,
    cast,
    Any,
    Literal,
    Optional,
    List,
)

from dlt.common.typing import TypedDict

from dlt.common.configuration.specs import ContainerInjectableContext
from dlt.common.runtime.anon_tracker import get_anonymous_id

from dlthub.common.constants import LICENSE_PUBLIC_KEY
from dlthub.common.license.exceptions import (
    DltLicenseExpiredException,
    DltLicenseFeatureScopeFormatInvalid,
    DltLicenseNotFoundException,
    DltLicenseScopeInvalidException,
    DltLicenseSelfSignedSubInvalid,
    DltLicenseSignatureInvalidException,
    DltPrivateKeyNotFoundException,
    DltUnknownScopeException,
)

SCOPE_ALL = "*"
"""Matches all scopes if present in license"""
KNOWN_SCOPES = {
    SCOPE_ALL: ("All features", ""),
    "dlthub": ("All dltHub features", ""),
    "dlthub.dbt_generator": (
        "Generate dbt packages from dlt pipelines",
        "https://dlthub.com/docs/hub/features/transformations/dbt-transformations",
    ),
    "dlthub.sources.mssql": (
        "Change tracking for MSSQL",
        "https://dlthub.com/docs/hub/ecosystem/ms-sql",
    ),
    "dlthub.project": (
        "Declarative yaml interface for dlt",
        "https://dlthub.com/docs/hub/features/project/",
    ),
    "dlthub.transformation": (
        "Python-first query-agnostic data transformations",
        "https://dlthub.com/docs/hub/features/transformations/",
    ),
    "dlthub.data_quality": (
        "Data quality checks and metrics for datasets",
        "https://dlthub.com/docs/hub/intro",  # TODO add docs
    ),
    "dlthub.destinations.iceberg": (
        "Iceberg destination with full catalog support",
        "https://dlthub.com/docs/hub/ecosystem/iceberg",
    ),
    "dlthub.destinations.snowflake_plus": (
        "Snowflake iceberg extension with Open Catalog",
        "https://dlthub.com/docs/hub/ecosystem/snowflake_plus",
    ),
    "dlthub.runner": (
        "Production pipeline runner and orchestrator support",
        "https://dlthub.com/docs/hub/features/runner",
    ),
}
"""List of known scopes, might be moved to pluggy to be extendable by other packages"""

TLicenseType = Literal["commercial", "trial", "self-issued-trial"]
"""Type of the license"""


class DltLicense(TypedDict, total=False):
    sub: str
    iat: int
    exp: int
    iss: str
    license_type: TLicenseType
    jit: str
    scope: Optional[str]


class LicenseContext(ContainerInjectableContext):
    """Holds current license and cached scopes"""

    global_affinity: ClassVar[bool] = True

    license: DltLicense = None
    _validated_scopes: List[str] = None

    # TODO: consider reloading when providers reload in pluggable run context

    def __init__(self, license: DltLicense = None) -> None:
        if license:
            self._set_license(license)
        else:
            self.reload()

    def reset(self) -> None:
        """Resets validated scopes so they will be reloaded on next access"""
        self._validated_scopes = None

    def validated_scopes(self) -> List[str]:
        """Scopes present in the currently active license"""
        if self._validated_scopes is None:
            self.reload()
        return self._validated_scopes

    def reload(self) -> None:
        """Looks for encoded license in configuration, validates it and caches scopes"""
        license_string = discover_license()
        self._set_license(validate_license(license_string))

    def _set_license(self, license: DltLicense) -> None:
        self.license = license
        # save the scopes that were already extracted from a valid license
        # to avoid validating the license multiple times
        self._validated_scopes = get_scopes(self.license)


def get_known_scopes() -> List[str]:
    """Get list of possible scopes from installed dlt packages.
    Package-level scope: grants access to everything in the package ie. dlthub
    Feature-level scope: grants access to a particular feature ie. dlthub.dbt_generator

    """
    return list(KNOWN_SCOPES.keys())
    # NOTE: the entry point is not used anymore, it does not work with python 3.10
    # scopes: List[str] = [SCOPE_ALL]
    # for info in list_dlt_packages():
    #     if info.license_scopes:
    #         scopes.append(info.module_name)
    #         scopes.extend(f"{info.module_name}.{scope}" for scope in info.license_scopes.split())
    # return scopes


def get_known_features() -> Dict[str, Tuple[str, str]]:
    """Gets mapping from scope to feature description and docs link"""
    return KNOWN_SCOPES


def create_license(
    private_key: str,
    days_valid: int,
    licensee_name: str,
    license_type: TLicenseType,
    scope: str,
    additional_allowed_scopes: Set[str] = None,
    algorithm: str = "RS256",
) -> str:
    """Create and sign a license JWT.

    The license is a signed JWT including standard claims (iat, exp, iss, sub) and
    product-specific claims (license_type, jit, scope). The scope claim is a
    space-delimited string of scopes, for example: "dlthub dlthub.dbt_generator".

    If no scope is provided (an empty string), the scope claim is omitted and the
    license is treated as granting all features (equivalent to the "*" wildcard)
    when evaluated by get_scopes.

    Args:
        private_key (str): PEM-encoded private key used to sign the JWT.
        days_valid (int): Number of days the license should remain valid from issuance.
        licensee_name (str): Value for the "sub" claim; identifies the license holder.
        license_type (TLicenseType): Type of the license (for example, "commercial",
            "trial", or "self-issued-trial").
        scope (str): Space-delimited list of allowed scopes. Use an empty string to grant all
            features. Unknown scopes raise ValueError unless explicitly allowed via
            additional_allowed_scopes.
        additional_allowed_scopes (set[str] | None): Optional extra scopes accepted in addition to
            the built-in known scopes (useful for tests or private features).
        algorithm (str): JWT signing algorithm to use. Defaults to "RS256".

    Returns:
        str: The encoded and signed JWT license.

    Raises:
        ValueError: If the provided scope string includes an unknown scope.
    """
    from jose import jwt  # type: ignore

    private_key_bytes = bytes(private_key, "utf-8")

    # check that provided scopes actually exist
    if scope:
        known_scopes = set(get_known_scopes()) | (additional_allowed_scopes or set())
        scopes = scope.split(" ")
        for s in scopes:
            if s not in known_scopes:
                raise ValueError(f"Unknown scope: {s}, must be one of: {', '.join(known_scopes)}")

    now = int(time.time())
    exp = now + (days_valid * 24 * 60 * 60)

    license: DltLicense = {
        "iat": now,
        "exp": exp,
        "sub": licensee_name,
        "iss": "dltHub Inc.",
        "license_type": license_type,
        "jit": str(uuid4()),
    }
    if scope:
        license["scope"] = scope

    encoded = jwt.encode(cast(Any, license), private_key_bytes, algorithm=algorithm)

    return encoded  # type: ignore


def create_self_signed_license(scope: str, additional_allowed_scopes: Set[str] = None) -> str:
    """Create a self-issued trial license bound to this machine and anonymous user.

    This helper derives a deterministic EC256 key pair from a machine identifier and an
    anonymous user id, then issues a short-lived trial license signed with the derived
    private key. The resulting license has type "self-issued-trial", is valid for 30 days,
    uses ES256 for signing, and can only be validated on the same machine and for the same
    anonymous user (see validate_self_signed_license).

    The scope argument is a space-delimited string of scopes (for example,
    "dlthub dlthub.dbt_generator"). If scope is an empty string, the license is treated as
    granting all features.

    Args:
        scope (str): Space-delimited list of allowed scopes for the trial license. An empty
            string grants all features.
        additional_allowed_scopes (set[str] | None): Optional extra scopes accepted in addition to
            the built-in known scopes.

    Returns:
        str: The encoded and signed self-issued trial JWT license.

    Raises:
        ValueError: If the provided scope string includes an unknown scope.
    """
    host_id = _get_host_id()
    anonymous_id = get_anonymous_id()
    sub = f"{host_id}:{anonymous_id}"
    _, pk = compute_self_signed_key_pair(sub)
    return create_license(
        pk,
        30,
        sub,
        "self-issued-trial",
        scope,
        additional_allowed_scopes=additional_allowed_scopes,
        algorithm="ES256",
    )


def validate_license(encoded_license: str) -> DltLicense:
    # decode license type
    encoded = decode_license(encoded_license)
    if encoded["license_type"] == "self-issued-trial":
        return validate_self_signed_license(encoded_license)
    else:
        return validate_license_signature(LICENSE_PUBLIC_KEY, encoded_license)


def validate_license_signature(
    public_key: str, license: str, algorithm: str = "RS256"
) -> DltLicense:
    """Decode a jwt with the public, verify signature using `public_key` and `algorithm` and return
    the decoded license object"""
    from jose import jwt
    from jose.exceptions import ExpiredSignatureError, JWTError  # type: ignore

    if not public_key:
        raise DltLicenseSignatureInvalidException()

    try:
        return cast(
            DltLicense, jwt.decode(license, bytes(public_key, "utf-8"), algorithms=[algorithm])
        )
    except ExpiredSignatureError as e:
        raise DltLicenseExpiredException() from e
    except (ValueError, JWTError) as e:
        raise DltLicenseSignatureInvalidException() from e


def validate_self_signed_license(license: str) -> DltLicense:
    """Validates self-signed license with public key generated out of anonymous user id and host
    id."""
    # decode license just to provide a nice exception if user moves license to other machine
    claims: DltLicense = decode_license(license)
    host_id = _get_host_id()
    anonymous_id = get_anonymous_id()
    expected_sub = f"{host_id}:{anonymous_id}"
    if claims["sub"] != expected_sub:
        raise DltLicenseSelfSignedSubInvalid(claims["sub"], host_id, anonymous_id)

    # NOTE: license decoded without verification is scrapped
    # generate public key for validation
    vk, _ = compute_self_signed_key_pair(expected_sub)
    return validate_license_signature(vk, license, algorithm="ES256")


def get_scopes(license: DltLicense) -> List[str]:
    scopes_string = license.get("scope", None) or SCOPE_ALL
    return scopes_string.split(" ")  # default to all if no scope given


def ensure_scope(available_scopes: Iterable[str], required_scope: str) -> None:
    if required_scope not in get_known_scopes():
        raise DltUnknownScopeException(required_scope)
    if SCOPE_ALL in available_scopes:
        return
    # scope that is validated is always feature scope
    package, _ = required_scope.split(".", 1)
    # license must contains full package or exactly this feature
    if package not in available_scopes and required_scope not in available_scopes:
        raise DltLicenseScopeInvalidException(required_scope, available_scopes)


def ensure_feature_scope(scope: str) -> None:
    fragments = scope.split(".", 1)
    package, feature = "", ""
    if len(fragments) == 2:
        package, feature = fragments
    if package and feature:
        return
    raise DltLicenseFeatureScopeFormatInvalid(scope)


def decode_license(license: str) -> DltLicense:
    """Decode the license without verifying that the signature is valid"""
    from jose import jwt

    return cast(DltLicense, jwt.get_unverified_claims(license))


def discover_license() -> str:
    """Reads license from config and returns encoded form"""
    import dlt
    from dlt.common.configuration.exceptions import ConfigFieldMissingException

    try:
        if license := dlt.secrets["runtime.license"]:
            return cast(str, license)
        raise DltLicenseNotFoundException()
    except ConfigFieldMissingException as e:
        raise DltLicenseNotFoundException from e


def discover_private_key() -> str:
    import dlt
    from dlt.common.configuration.exceptions import ConfigFieldMissingException

    try:
        return dlt.secrets["runtime.license_private_key"]  # type: ignore[no-any-return]
    except ConfigFieldMissingException as e:
        raise DltPrivateKeyNotFoundException from e


def compute_self_signed_key_pair(sub: str) -> Tuple[str, str]:
    """Compute a deterministic EC256 key pair from `sub` JWT field.

    The key material is deterministically derived from the provided anonymous_id and a
    cross-platform host identifier (hostname) (`sub`), so the same inputs will always yield the
    same key pair. The ecdsa library is used under the hood. Keys are returned in
    PEM format suitable for use with EC256 JWT signing/verification.

    HKDF is used to derive a seed that is then used as exponent for ECDSA

    Args:
        sub: `sub` field of JWT being signed

    Returns:
        Tuple[str, str]: A tuple of (public_key_pem, private_key_pem).
    """
    import hashlib
    from ecdsa import SigningKey, NIST256p

    ikm = sub.encode("utf-8")
    d = _derive_seed(ikm, b"0", length=NIST256p.baselen)
    # NOTE: not a bitcoin curve
    sk = SigningKey.from_string(d, curve=NIST256p, hashfunc=hashlib.sha256)
    vk = sk.get_verifying_key()

    public_pem = vk.to_pem().decode("ascii")
    private_pem = sk.to_pem().decode("ascii")
    return public_pem, private_pem


def _derive_seed(ikm: bytes, account: bytes, length: int) -> bytes:
    """Derive deterministic seed from key material `ikm` of a given `length`. HKDF (copied
    from Wikipedia) is used"""
    import hmac
    import hashlib

    def _hmac_digest(key: bytes, data: bytes) -> bytes:
        return hmac.new(key, data, hashlib.sha256).digest()

    def _hkdf_extract(salt: bytes, ikm: bytes) -> bytes:
        if len(salt) == 0:
            salt = bytes([0] * hashlib.sha256().digest_size)
        return _hmac_digest(salt, ikm)

    def _hkdf_expand(prk: bytes, info: bytes, length_: int) -> bytes:
        t = b""
        okm = b""
        i = 0
        while len(okm) < length_:
            i += 1
            t = _hmac_digest(prk, t + info + bytes([i]))
            okm += t
        return okm[:length_]

    # use random but not secret salt
    prk = _hkdf_extract(b"g1vG1WjVKt8hBGo5oEL6cKLgLK53ceAfruE2VmWOK8gYHpLpceoV56ARLKJpHl5u", ikm)
    # info is typically used for hierarchical deterministic key generation, right now we just
    # need one key per sub (ikm), so account is hardcoded to 0
    return _hkdf_expand(prk, b"self-issued-trial/%b" % account, length)


def _get_host_id() -> str:
    import platform
    import socket

    return platform.node() or socket.gethostname() or "unknown-host"


def _to_pretty_timestamp(ts: int) -> str:
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")


def prettify_license(license: str, with_license: bool = False) -> str:
    license_dict = decode_license(license)

    output = f"""
License Id: {license_dict.get("jit")}
Licensee: {license_dict["sub"]}
Issuer: {license_dict["iss"]}
License Type: {license_dict["license_type"]}
Issued: {_to_pretty_timestamp(license_dict["iat"])}
Scopes: {",".join(get_scopes(license_dict))}
Valid Until: {_to_pretty_timestamp(license_dict["exp"])}"""
    if with_license:
        output += f"""
===
{license}
===
"""

    return output
