import uuid

import pytest
from pydantic import SecretStr, ValidationError

from arraylake.compute.types import ComputeConfig
from arraylake.types import (
    AWSCustomerManagedRoleAuth,
    AWSRoleAuthPatch,
    Author,
    AzureCredentials,
    BucketModifyRequest,
    BucketResponse,
    DatasetFilter,
    GSCredentials,
    HmacAuth,
    MAX_BUCKET_NAME_LENGTH,
    MAX_BUCKET_PREFIX_LENGTH,
    MAX_REPO_NAME_LENGTH,
    NewBucket,
    NodeFilter,
    RESERVED_REPO_NAMES,
    R2AuthPatch,
    R2CustomerManagedRoleAuth,
    Repo,
    RepoCreateBody,
    RepoKind,
    RepoSubscribeBody,
    S3Credentials,
    TokenAuthenticateBody,
    utc_now,
)


def test_identities_to_author(test_user, test_api_token):
    user_author: Author = test_user.as_author()
    assert isinstance(user_author, Author)
    assert user_author.email == "abc@earthmover.io"
    assert user_author.name == "TestFirst TestFamily"

    api_author: Author = test_api_token.as_author()
    assert isinstance(api_author, Author)
    assert api_author.email == "svc-email@some-earthmover-org.service.earthmover.io"
    assert not api_author.name


@pytest.mark.parametrize(
    "nickname, platform, prefix, name, extra_config",
    [
        ("foo-bar", "s3", "", "my-bucket-on-s3", {"region_name": "us-east-1"}),
        ("foo_bar", "s3-compatible", "foo", "my_bucket_on_s3", {"endpoint_url": "http://localhost:9000"}),
        ("foo-bar", "s3", "", "my-bucket-on-s3", {"region_name": "us-east-1"}),
        ("foo-bar", "s3", "foo/bar/spam", "my-bucket-on-s3", {"region_name": "us-east-1"}),
    ],
)
def test_bucket_name_validation(nickname, platform, prefix, name, extra_config):
    b = NewBucket(
        nickname=nickname, platform=platform, name=name, prefix=prefix, extra_config=extra_config, auth_config={"method": "anonymous"}
    )
    assert b.nickname == nickname
    assert b.platform == platform
    assert b.name == name
    assert b.prefix == prefix


@pytest.mark.parametrize(
    "nickname, platform, prefix, name, extra_config, err_msg",
    [
        ("fo", "s3", "", "my-bucket-on-s3", {"region_name": "us-east-1"}, "Bucket nickname must be at least 3 characters long."),
        ("foo-bar", "s3", "", "b", {"region_name": "us-east-1"}, "Bucket name must be at least 3 characters long."),
        ("foo-bar", "s3-compatible", "", "my bucket", {"endpoint_url": "http://localhost:9000"}, "Bucket name must not contain spaces."),
        (
            "foo-bar",
            "s3-compatible",
            "",
            "s3://my-arraylake-bucket",
            {"endpoint_url": "http://localhost:9000"},
            "Bucket name must not contain schemes.",
        ),
        ("foo-bar", "s3-compatible", "", "my-arraylake-bucket", {}, "S3-compatible buckets require an endpoint_url"),
        ("foo-bar", "s3", "", "my bucket", {"region_name": "us-east-1"}, "Bucket name must not contain spaces."),
        ("foo-bar", "s3", "/foo/", "my-bucket-on-s3", {"region_name": "us-east-1"}, "Bucket prefix must not start or end with a slash."),
        (
            "foo-bar",
            "s3",
            "/foo/bar/",
            "my-bucket-on-s3",
            {"region_name": "us-east-1"},
            "Bucket prefix must not start or end with a slash.",
        ),
        ("foo-bar", "s3", "foo bar", "my-bucket-on-s3", {"region_name": "us-east-1"}, "Bucket prefix must not contain spaces."),
        (
            "foo-bar",
            "s3",
            "NetCDF/s3://other-bucket/NetCDF",
            "my-bucket-on-s3",
            {"region_name": "us-east-1"},
            "Bucket prefix must not contain a scheme",
        ),
        (
            "foo-bar",
            "s3",
            "a" * (MAX_BUCKET_PREFIX_LENGTH + 1),
            "my-bucket-on-s3",
            {"region_name": "us-east-1"},
            f"at most {MAX_BUCKET_PREFIX_LENGTH} characters",
        ),
        (
            "foo-bar",
            "s3",
            "",
            "a" * (MAX_BUCKET_NAME_LENGTH + 1),
            {"region_name": "us-east-1"},
            f"at most {MAX_BUCKET_NAME_LENGTH} characters",
        ),
    ],
)
def test_bucket_name_validation_error(nickname, platform, prefix, name, extra_config, err_msg):
    with pytest.raises(ValueError, match=err_msg):
        b = NewBucket(
            nickname=nickname,
            platform=platform,
            name=name,
            prefix=prefix,
            extra_config=extra_config,
            auth_config={"method": "anonymous"},
        )


def test_name_length_limits():
    with pytest.raises(ValidationError, match="at most"):
        RepoCreateBody(name="a" * (MAX_REPO_NAME_LENGTH + 1), bucket_nickname="my-bucket")
    assert RepoCreateBody(name="a" * MAX_REPO_NAME_LENGTH, bucket_nickname="my-bucket").name == "a" * MAX_REPO_NAME_LENGTH


@pytest.mark.parametrize("name", [*sorted(RESERVED_REPO_NAMES), "Exchange"])
def test_reserved_repo_names(name: str):
    with pytest.raises(ValidationError, match="reserved"):
        RepoCreateBody(name=name, bucket_nickname="my-bucket")
    with pytest.raises(ValidationError, match="reserved"):
        RepoSubscribeBody(name=name, exchange_listing_id="some-listing")
    # Existing repos may already hold a reserved name and must stay readable.
    assert Repo.model_validate({**_repo_payload(RepoKind.Icechunk.value), "name": name}).name == name


def test_anonymous_azure_bucket_requires_storage_account():
    # Anonymous Azure buckets must carry the storage account name (s3/gcs don't need it).
    with pytest.raises(ValidationError, match="Anonymous Azure buckets require a storage_account"):
        NewBucket(
            nickname="public-azure",
            platform="azure",
            name="public-container",
            extra_config={},
            auth_config={"method": "anonymous"},
        )


def test_aws_auth_secret_serialization():
    """Test that AWS auth secrets are obfuscated by default but revealed with context."""
    auth = AWSCustomerManagedRoleAuth(
        method="aws_customer_managed_role",
        external_customer_id="12345678",
        external_role_name="my-role",
        shared_secret=SecretStr("super-secret-value"),
    )

    # Default serialization should obfuscate
    default_dump = auth.model_dump()
    assert default_dump["shared_secret"] == "**********"

    # JSON mode should also obfuscate by default
    json_dump = auth.model_dump(mode="json")
    assert json_dump["shared_secret"] == "**********"

    # With reveal_secrets context, should reveal the secret
    revealed_dump = auth.model_dump(mode="json", context={"reveal_secrets": True})
    assert revealed_dump["shared_secret"] == "super-secret-value"


@pytest.mark.parametrize(
    "shared_secret, is_valid",
    [
        ("valid-external-id", True),
        ("ab", True),
        ("a" * 1224, True),
        ("_+=,.@:/-Aa9", True),
        ("a", False),
        ("a" * 1225, False),
        ("has space", False),
        ("has#hash", False),
        ("bang!", False),
        ("percent%", False),
        ("paren(", False),
        ("unïcode", False),
    ],
)
def test_aws_shared_secret_external_id_validation(shared_secret, is_valid):
    kwargs = dict(
        nickname="foo-bar",
        platform="s3",
        name="my-bucket-on-s3",
        prefix="",
        extra_config={"region_name": "us-east-1"},
        auth_config={
            "method": "aws_customer_managed_role",
            "external_customer_id": "123456789012",
            "external_role_name": "my-role",
            "shared_secret": shared_secret,
        },
    )
    if is_valid:
        b = NewBucket(**kwargs)
        assert isinstance(b.auth_config, AWSCustomerManagedRoleAuth)
        assert b.auth_config.shared_secret is not None
        assert b.auth_config.shared_secret.get_secret_value() == shared_secret
    else:
        with pytest.raises(ValidationError, match="2-1224 characters"):
            NewBucket(**kwargs)


def test_modify_request_role_patch_allows_omitting_only_the_secret():
    modify = BucketModifyRequest(
        auth_config={
            "method": "aws_customer_managed_role",
            "external_customer_id": "123456789012",
            "external_role_name": "a-new-role",
        },
    )
    assert isinstance(modify.auth_config, AWSRoleAuthPatch)
    assert modify.auth_config.external_role_name == "a-new-role"
    assert modify.auth_config.shared_secret is None
    assert "external_role_name" in modify.auth_config.model_fields_set
    assert "shared_secret" not in modify.auth_config.model_fields_set


def test_modify_request_role_patch_allows_role_name_only():
    modify = BucketModifyRequest(
        auth_config={"method": "aws_customer_managed_role", "external_role_name": "a-new-role"},
    )
    assert isinstance(modify.auth_config, AWSRoleAuthPatch)
    assert modify.auth_config.model_fields_set == {"method", "external_role_name"}


def test_modify_request_r2_patch_allows_omitting_the_required_key():
    modify = BucketModifyRequest(
        auth_config={"method": "r2_customer_managed_role", "external_account_id": "acct-2"},
    )
    assert isinstance(modify.auth_config, R2AuthPatch)
    assert modify.auth_config.parent_access_key_id is None
    assert modify.auth_config.model_fields_set == {"method", "external_account_id"}


def test_modify_request_role_patch_still_validates_supplied_shared_secret():
    with pytest.raises(ValidationError, match="2-1224 characters"):
        BucketModifyRequest(
            auth_config={
                "method": "aws_customer_managed_role",
                "external_customer_id": "123456789012",
                "external_role_name": "a-new-role",
                "shared_secret": "has space",
            },
        )


def test_r2_auth_secret_serialization():
    """Test that R2 auth secrets are obfuscated by default but revealed with context."""
    auth = R2CustomerManagedRoleAuth(
        method="r2_customer_managed_role",
        external_account_id="account123",
        account_api_token=SecretStr("api-token-secret"),
        parent_access_key_id=SecretStr("access-key-secret"),
    )

    # Default serialization should obfuscate
    default_dump = auth.model_dump()
    assert default_dump["account_api_token"] == "**********"
    assert default_dump["parent_access_key_id"] == "**********"

    # With reveal_secrets context, should reveal the secrets
    revealed_dump = auth.model_dump(mode="json", context={"reveal_secrets": True})
    assert revealed_dump["account_api_token"] == "api-token-secret"
    assert revealed_dump["parent_access_key_id"] == "access-key-secret"


def test_r2_auth_vending_path_required():
    """R2 auth must carry at least one vending secret; either alone is valid, both is fine, neither errors."""
    common = dict(
        method="r2_customer_managed_role",
        external_account_id="account123",
        parent_access_key_id=SecretStr("access-key-secret"),
    )

    # REST path only: account_api_token set, no parent secret.
    rest_only = R2CustomerManagedRoleAuth(**common, account_api_token=SecretStr("api-token-secret"))
    assert rest_only.parent_secret_access_key is None

    # Local JWT path only: parent secret set, no account_api_token (now optional).
    jwt_only = R2CustomerManagedRoleAuth(**common, parent_secret_access_key=SecretStr("f" * 64))
    assert jwt_only.account_api_token is None

    # Managed buckets store both — still valid.
    both = R2CustomerManagedRoleAuth(
        **common, account_api_token=SecretStr("api-token-secret"), parent_secret_access_key=SecretStr("f" * 64)
    )
    assert both.account_api_token is not None and both.parent_secret_access_key is not None

    # Neither secret is a misconfiguration.
    with pytest.raises(ValidationError, match="either account_api_token or parent_secret_access_key"):
        R2CustomerManagedRoleAuth(**common)


@pytest.mark.parametrize(
    "model, secrets",
    [
        (
            HmacAuth(method="hmac", access_key_id="AKIAFAKEKEYID", secret_access_key="fake/secret+access-key"),
            ["AKIAFAKEKEYID", "fake/secret+access-key"],
        ),
        (
            S3Credentials(
                aws_access_key_id="ASIAFAKEKEYID",
                aws_secret_access_key="fake/secret+access-key",
                aws_session_token="fake-session-token",
                expiration=None,
            ),
            ["ASIAFAKEKEYID", "fake/secret+access-key", "fake-session-token"],
        ),
        (
            GSCredentials(access_token="ya29.fake-access-token", principal="svc@my-project.iam.gserviceaccount.com", expiration=None),
            ["ya29.fake-access-token"],
        ),
        (
            AzureCredentials(sas_token="sv=2024-01-01&sig=fakesignature", storage_account="myaccount", expiration=None),
            ["sv=2024-01-01&sig=fakesignature"],
        ),
        (TokenAuthenticateBody(token="ema_fake_api_token"), ["ema_fake_api_token"]),
        # Nested case: BucketResponse must not leak its HmacAuth keys either.
        (
            BucketResponse(
                id=uuid.uuid4(),
                nickname="test-bucket-config",
                platform="s3",
                name="my-bucket",
                extra_config={},
                auth_config={"method": "hmac", "access_key_id": "AKIAFAKEKEYID", "secret_access_key": "fake/secret+access-key"},
                is_default=False,
            ),
            ["AKIAFAKEKEYID", "fake/secret+access-key"],
        ),
        (
            ComputeConfig(
                service_uri="https://compute.earthmover.io",
                domain="earthmover.io",
                env="test",
                container_repository="registry/repo",
                kube_config={"token": "fake-kube-token"},
                openmeter_api_key="om_fake_key",
            ),
            ["fake-kube-token", "om_fake_key"],
        ),
    ],
)
def test_secrets_redacted_in_repr_and_str(model, secrets):
    """Secret-carrying models must not leak credentials via repr()/str().

    This covers tracebacks, logging, and interactive display of these models
    (e.g. pytest printing fixture values on failure), including models nested
    inside others (BucketResponse.auth_config).
    """
    for rendered in (repr(model), str(model)):
        for secret in secrets:
            assert secret not in rendered
        assert "**********" in rendered


def test_redacted_repr_does_not_affect_serialization():
    """Redaction is display-only: attribute access and (JSON) serialization round-trip the real values."""
    auth = HmacAuth(method="hmac", access_key_id="AKIAFAKEKEYID", secret_access_key="fake/secret+access-key")
    assert auth.access_key_id == "AKIAFAKEKEYID"
    assert auth.secret_access_key == "fake/secret+access-key"

    dumped = auth.model_dump()
    assert dumped == {"method": "hmac", "access_key_id": "AKIAFAKEKEYID", "secret_access_key": "fake/secret+access-key"}

    # This is the wire format sent to / received from the server; it must carry the real values.
    json_dumped = auth.model_dump_json(context={"reveal_secrets": True})
    assert HmacAuth.model_validate_json(json_dumped) == auth
    assert auth.model_dump_json() == json_dumped


class TestNodeFilter:
    """Tests for NodeFilter path validation and model creation."""

    @pytest.mark.parametrize(
        "include_paths,exclude_paths",
        [
            # Root path
            (["/"], []),
            ([], ["/"]),
            # Simple paths
            (["/foo"], []),
            ([], ["/foo"]),
            (["/foo/bar"], []),
            # Multiple paths
            (["/foo", "/bar"], []),
            ([], ["/foo", "/bar"]),
            (["/foo/bar", "/baz/qux"], []),
            # Deep paths
            (["/a/b/c/d/e"], []),
            ([], ["/a/b/c/d/e/f/g"]),
            # Both include and exclude
            (["/temperature"], ["/temperature/max"]),
            (["/foo", "/bar"], ["/foo/secret", "/bar/internal"]),
            # Paths with hyphens and underscores
            (["/foo-bar/baz_qux"], []),
            # Paths with numbers
            (["/data2024"], []),
            (["/v1/api"], []),
        ],
    )
    def test_valid_paths(self, include_paths, exclude_paths):
        """Test that valid paths are accepted."""
        nf = NodeFilter(include_paths=include_paths, exclude_paths=exclude_paths)
        assert nf.include_paths == include_paths
        assert nf.exclude_paths == exclude_paths

    def test_empty_filter_rejected(self):
        """Test that empty filters (both lists empty) are rejected.

        Use None at the DatasetFilter level to represent 'no filtering'.
        """
        with pytest.raises(ValueError, match="must have at least one include or exclude path"):
            NodeFilter()

        with pytest.raises(ValueError, match="must have at least one include or exclude path"):
            NodeFilter(include_paths=[], exclude_paths=[])

        # Test that None values are coerced to empty lists, then rejected
        with pytest.raises(ValueError, match="must have at least one include or exclude path"):
            NodeFilter(include_paths=None, exclude_paths=None)

    @pytest.mark.parametrize(
        "paths",
        [
            ["foo"],
            ["foo/bar"],
            ["./foo"],
            ["../foo"],
            ["temperature"],
            ["temperature/min"],
        ],
    )
    def test_relative_paths_rejected(self, paths):
        """Test that relative paths are rejected."""
        with pytest.raises(ValueError, match="Path must be absolute.*start with single '/'"):
            NodeFilter(include_paths=paths)

        with pytest.raises(ValueError, match="Path must be absolute.*start with single '/'"):
            NodeFilter(exclude_paths=paths)

    @pytest.mark.parametrize(
        "paths,err_match",
        [
            # Leading double slash (network path style)
            (["//foo"], "Path must be absolute.*start with single '/'"),
            (["//foo/bar"], "Path must be absolute.*start with single '/'"),
            # Double slashes in middle
            (["/foo//bar"], "Path must be normalized"),
            (["/foo//bar//baz"], "Path must be normalized"),
            (["/a//b/c"], "Path must be normalized"),
        ],
    )
    def test_double_slashes_rejected(self, paths, err_match):
        """Test that paths with double slashes are rejected."""
        with pytest.raises(ValueError, match=err_match):
            NodeFilter(include_paths=paths)

    @pytest.mark.parametrize(
        "paths",
        [
            ["/foo/"],
            ["/foo/bar/"],
            ["/a/b/c/"],
        ],
    )
    def test_trailing_slashes_rejected(self, paths):
        """Test that paths with trailing slashes are rejected."""
        with pytest.raises(ValueError, match="Path must be normalized"):
            NodeFilter(include_paths=paths)

    @pytest.mark.parametrize(
        "paths,err_match",
        [
            # Parent directory references (..)
            (["/foo/../bar"], "cannot contain '.' or '..' components"),
            (["/foo/.."], "cannot contain '.' or '..' components"),
            (["/../foo"], "cannot contain '.' or '..' components"),
            (["/a/b/../c"], "cannot contain '.' or '..' components"),
            # Current directory references (.) - caught by normalization
            (["/foo/./bar"], "Path must be normalized"),
            (["/./foo"], "Path must be normalized"),
            (["/foo/."], "Path must be normalized"),
            (["/a/./b/./c"], "Path must be normalized"),
        ],
    )
    def test_dot_components_rejected(self, paths, err_match):
        """Test that paths with . or .. components are rejected."""
        with pytest.raises(ValueError, match=err_match):
            NodeFilter(include_paths=paths)

    @pytest.mark.parametrize(
        "paths",
        [
            # Asterisk wildcards
            (["/foo*"],),
            (["/foo/bar*"],),
            (["/foo/*/bar"],),
            (["/*"],),
            (["/foo/**/bar"],),
            # Question mark wildcards
            (["/foo?"],),
            (["/foo/bar?baz"],),
            (["/foo/?/bar"],),
        ],
    )
    def test_wildcards_rejected(self, paths):
        """Test that paths with wildcard characters are rejected."""
        with pytest.raises(ValueError, match=r"cannot contain '\*' or '\?' characters"):
            NodeFilter(include_paths=paths[0])

    @pytest.mark.parametrize(
        "paths",
        [
            ["/foo", "/foo"],
            ["/a", "/b", "/a"],
            ["/temperature", "/humidity", "/temperature"],
            ["/a/b/c", "/a/b/c"],
        ],
    )
    def test_duplicate_paths_rejected(self, paths):
        """Test that duplicate paths are rejected."""
        with pytest.raises(ValueError, match="Duplicate paths not allowed"):
            NodeFilter(include_paths=paths)

        with pytest.raises(ValueError, match="Duplicate paths not allowed"):
            NodeFilter(exclude_paths=paths)

    def test_same_path_in_both_include_and_exclude_allowed(self):
        """Test that the same path can appear in both include and exclude.

        This is semantically valid (exclusion wins), so the model should accept it.
        The filter evaluation logic handles the semantics.
        """
        nf = NodeFilter(include_paths=["/foo"], exclude_paths=["/foo"])
        assert nf.include_paths == ["/foo"]
        assert nf.exclude_paths == ["/foo"]

    def test_root_path_only(self):
        """Test filter with only root path."""
        nf = NodeFilter(include_paths=["/"])
        assert nf.include_paths == ["/"]

    def test_empty_string_path_rejected(self):
        """Test that empty string path is rejected."""
        with pytest.raises(ValueError, match="Path must be absolute"):
            NodeFilter(include_paths=[""])

    def test_whitespace_in_path_preserved(self):
        """Test that whitespace in path names is preserved (valid in some filesystems)."""
        # Paths with spaces should be valid
        nf = NodeFilter(include_paths=["/foo bar"])
        assert nf.include_paths == ["/foo bar"]

    def test_case_sensitivity_preserved(self):
        """Test that path case is preserved (paths are case-sensitive)."""
        nf = NodeFilter(include_paths=["/Foo", "/foo", "/FOO"])
        assert nf.include_paths == ["/Foo", "/foo", "/FOO"]
        assert len(nf.include_paths) == 3  # All three are distinct

    def test_model_serialization_roundtrip(self):
        """Test that NodeFilter serializes and deserializes correctly."""
        original = NodeFilter(
            include_paths=["/temperature", "/humidity"],
            exclude_paths=["/temperature/max"],
        )
        dumped = original.model_dump()
        restored = NodeFilter(**dumped)
        assert restored.include_paths == original.include_paths
        assert restored.exclude_paths == original.exclude_paths

    def test_model_json_serialization(self):
        """Test that NodeFilter serializes to JSON correctly."""
        nf = NodeFilter(
            include_paths=["/foo", "/bar"],
            exclude_paths=["/foo/secret"],
        )
        json_str = nf.model_dump_json()
        restored = NodeFilter.model_validate_json(json_str)
        assert restored.include_paths == nf.include_paths
        assert restored.exclude_paths == nf.exclude_paths


class TestDatasetFilter:
    """Tests for DatasetFilter model creation and validation."""

    def test_invalid_node_filter_rejected(self):
        """Test that invalid NodeFilter paths cause DatasetFilter to fail."""
        with pytest.raises(ValueError, match="Path must be absolute"):
            DatasetFilter(nodes={"include_paths": ["relative/path"]})

    def test_model_serialization_roundtrip(self):
        """Test that DatasetFilter serializes and deserializes correctly."""
        original = DatasetFilter(
            nodes=NodeFilter(
                include_paths=["/a", "/b"],
                exclude_paths=["/a/secret"],
            )
        )
        dumped = original.model_dump()
        restored = DatasetFilter(**dumped)
        assert restored.nodes is not None
        assert restored.nodes.include_paths == original.nodes.include_paths
        assert restored.nodes.exclude_paths == original.nodes.exclude_paths

    def test_model_json_serialization(self):
        """Test that DatasetFilter serializes to JSON correctly."""
        df = DatasetFilter(nodes=NodeFilter(include_paths=["/temperature"], exclude_paths=[]))
        json_str = df.model_dump_json()
        restored = DatasetFilter.model_validate_json(json_str)
        assert restored.nodes is not None
        assert restored.nodes.include_paths == df.nodes.include_paths

    def test_none_filter_serialization(self):
        """Test that DatasetFilter with None nodes serializes correctly."""
        df = DatasetFilter(nodes=None)
        dumped = df.model_dump()
        assert dumped == {"nodes": None}
        restored = DatasetFilter(**dumped)
        assert restored.nodes is None


def _repo_payload(kind: str) -> dict:
    return {
        "id": "6543210987654321fedcba98",
        "org": "some-org",
        "name": "some-repo",
        "updated": utc_now().isoformat(),
        "status": {"mode": "online", "initiated_by": {"system_id": "test"}},
        "prefix": "some/prefix",
        "kind": kind,
    }


@pytest.mark.parametrize("kind", [k.value for k in RepoKind])
def test_repo_response_parses_known_kinds_as_enum(kind: str):
    repo = Repo.model_validate(_repo_payload(kind))
    assert repo.kind is RepoKind(kind)


def test_repo_response_tolerates_unknown_kind():
    """A newer server can name a kind this release has never heard of; parsing must
    keep the raw string rather than failing the whole (possibly bulk) response."""
    repo = Repo.model_validate(_repo_payload("some-future-kind"))
    assert repo.kind == "some-future-kind"
    assert repo.kind != RepoKind.Icechunk
    # still serializable, and still renderable
    assert repo._asdict()["kind"] == "some-future-kind"
    assert "some-future-kind" in repr(repo)


def test_repo_create_body_still_rejects_unknown_kind():
    """Request bodies stay strict: a client can only ask for kinds it can open."""
    with pytest.raises(ValidationError):
        RepoCreateBody(name="some-repo", kind="some-future-kind", create_mode="register")
