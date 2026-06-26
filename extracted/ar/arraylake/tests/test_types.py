import uuid

import pytest
from pydantic import SecretStr, ValidationError

from arraylake.types import (
    AWSCustomerManagedRoleAuth,
    Author,
    DatasetFilter,
    MAX_BUCKET_NAME_LENGTH,
    MAX_BUCKET_PREFIX_LENGTH,
    MAX_REPO_NAME_LENGTH,
    NewBucket,
    NodeFilter,
    R2CustomerManagedRoleAuth,
    RepoCreateBody,
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
