from enum import Enum


class ErrorCode(str, Enum):
    API_KEY_EXPIRED = "api_key_expired"
    API_KEY_INVALID = "api_key_invalid"
    API_KEY_REVOKED = "api_key_revoked"
    BACKOFFICE_SCOPE_MISSING = "backoffice_scope_missing"
    CAPABILITY_DATAPLANE_MISMATCH = "capability_dataplane_mismatch"
    CAPABILITY_GRANT_MISSING = "capability_grant_missing"
    CAPABILITY_MISSING = "capability_missing"
    CAPABILITY_SCOPE_MISSING = "capability_scope_missing"
    CREDENTIALS_MISSING = "credentials_missing"
    EXTERNAL_ACCESS_DENIED = "external_access_denied"
    INVALID_FILES_MANIFEST = "invalid_files_manifest"
    INVALID_REQUIREMENTS_MANIFEST = "invalid_requirements_manifest"
    INVALID_TARBALL_UPLOAD = "invalid_tarball_upload"
    PERMISSION_DENIED = "permission_denied"
    RESERVED_VARIABLE_NAMES = "reserved_variable_names"
    RUN_PACKAGE_ALREADY_CONSUMED = "run_package_already_consumed"
    SERVICE_SCOPE_MISSING = "service_scope_missing"
    SERVICE_UNAUTHENTICATED = "service_unauthenticated"
    TOKEN_AUDIENCE_INVALID = "token_audience_invalid"
    TOKEN_BINDING_MISMATCH = "token_binding_mismatch"
    TOKEN_CLAIMS_INVALID = "token_claims_invalid"
    TOKEN_DATAPLANE_MISMATCH = "token_dataplane_mismatch"
    TOKEN_EXPIRED = "token_expired"
    TOKEN_MALFORMED = "token_malformed"
    TOKEN_SIGNATURE_INVALID = "token_signature_invalid"
    VARIABLES_CAP_EXCEEDED = "variables_cap_exceeded"
    VARIABLES_SCOPE_LOCKED = "variables_scope_locked"

    def __str__(self) -> str:
        return str(self.value)
