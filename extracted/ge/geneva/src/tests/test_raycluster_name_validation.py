# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""
Unit tests for RayCluster name validation (RFC 1123 compliance).

Tests the name validation and default name generation for RayCluster instances
to ensure compliance with Kubernetes DNS naming conventions (RFC 1123).
"""

import re
from unittest.mock import Mock, patch

import pytest

from geneva.runners.ray.raycluster import RayCluster, _RayClusterConfig


def test_edge_case_names() -> None:
    """Test edge cases for name validation"""
    mock_config = Mock()
    mock_config.user = "testuser"
    mock_config.namespace = "default"

    # Single character names
    with (
        patch.object(_RayClusterConfig, "get", return_value=mock_config),
        patch.object(RayCluster, "__attrs_post_init__", return_value=None),
    ):
        cluster_a = RayCluster(name="a")
        assert cluster_a.name == "a"

        cluster_1 = RayCluster(name="1")
        assert cluster_1.name == "1"

    # Maximum length name
    max_name = "a" * 63
    with (
        patch.object(_RayClusterConfig, "get", return_value=mock_config),
        patch.object(RayCluster, "__attrs_post_init__", return_value=None),
    ):
        cluster_max = RayCluster(name=max_name)
        assert cluster_max.name == max_name
        assert len(cluster_max.name) == 63


def test_consecutive_hyphens_allowed() -> None:
    """Test that consecutive hyphens are allowed per RFC 1123"""
    names_with_consecutive_hyphens = [
        "a--b",
        "test--cluster",
        "a---b---c",
        "x--y--z",
    ]

    for name in names_with_consecutive_hyphens:
        mock_config = Mock()
        mock_config.user = "testuser"
        mock_config.namespace = "default"

        with (
            patch.object(_RayClusterConfig, "get", return_value=mock_config),
            patch.object(RayCluster, "__attrs_post_init__", return_value=None),
        ):
            cluster = RayCluster(name=name)
            assert cluster.name == name


def test_simple_usernames() -> None:
    """Test default name generation with simple usernames"""
    test_cases = [
        ("user", "geneva-user"),
        ("User", "geneva-user"),  # should be lowercased
        ("user123", "geneva-user123"),
        ("123user", "geneva-123user"),
    ]

    for user, expected_name in test_cases:
        mock_config = Mock()
        mock_config.user = user

        with (
            patch.object(_RayClusterConfig, "get", return_value=mock_config),
            patch.object(RayCluster, "__attrs_post_init__", return_value=None),
        ):
            cluster = RayCluster()
            assert cluster.name == expected_name


def test_username_sanitization() -> None:
    """Test that invalid characters in usernames are sanitized"""
    test_cases = [
        ("user_name", "geneva-user-name"),
        ("user.name", "geneva-user-name"),
        ("user@domain.com", "geneva-user-domain-com"),
        ("user name", "geneva-user-name"),
        ("user!@#$%name", "geneva-user-----name"),
        ("USER_NAME", "geneva-user-name"),
    ]

    for user, expected_name in test_cases:
        mock_config = Mock()
        mock_config.user = user

        with (
            patch.object(_RayClusterConfig, "get", return_value=mock_config),
            patch.object(RayCluster, "__attrs_post_init__", return_value=None),
        ):
            cluster = RayCluster()
            assert cluster.name == expected_name
            # Verify the generated name is valid RFC 1123
            assert re.match(r"^[a-z0-9]([a-z0-9\-]*[a-z0-9])?$", cluster.name)


def test_username_edge_cases() -> None:
    """Test username edge cases that need special handling"""
    edge_cases = [
        ("", "geneva-user"),  # empty username
        ("___", "geneva-user"),  # only invalid characters
        ("-user-", "geneva-user"),  # starts/ends with hyphens
        ("--", "geneva-user"),  # only hyphens
        ("   ", "geneva-user"),  # only spaces
        ("123", "geneva-123"),  # numeric only
    ]

    for user, expected_name in edge_cases:
        mock_config = Mock()
        mock_config.user = user

        with (
            patch.object(_RayClusterConfig, "get", return_value=mock_config),
            patch.object(RayCluster, "__attrs_post_init__", return_value=None),
        ):
            cluster = RayCluster()
            assert cluster.name == expected_name
            # Verify the generated name is valid RFC 1123
            assert re.match(r"^[a-z0-9]([a-z0-9\-]*[a-z0-9])?$", cluster.name)


def test_long_username_truncation() -> None:
    """Test that very long usernames are properly truncated"""
    # Test username that would exceed 63 chars when prefixed with "geneva-"
    very_long_user = (
        "this-is-a-very-very-very-long-username-that-definitely-exceeds-"
        "the-kubernetes-limit"
    )

    mock_config = Mock()
    mock_config.user = very_long_user

    with (
        patch.object(_RayClusterConfig, "get", return_value=mock_config),
        patch.object(RayCluster, "__attrs_post_init__", return_value=None),
    ):
        cluster = RayCluster()

        # Should be truncated to fit within 63 character limit
        assert len(cluster.name) <= 63
        assert cluster.name.startswith("geneva-")

        # Should still be valid RFC 1123
        assert re.match(r"^[a-z0-9]([a-z0-9\-]*[a-z0-9])?$", cluster.name)

        # Should not end with hyphen after truncation
        assert not cluster.name.endswith("-")


def test_truncation_edge_cases() -> None:
    """Test edge cases in truncation logic"""
    # Username that becomes empty after removing trailing hyphens post-truncation
    test_cases = [
        # Username that would be all hyphens at the truncation boundary
        ("a" + "-" * 100, "geneva-a"),
        # Username that ends with many hyphens
        (
            "verylongusernamethatisvalid" + "-" * 50,
            "geneva-verylongusernamethatisvalid",
        ),
    ]

    for user, _expected_prefix in test_cases:
        mock_config = Mock()
        mock_config.user = user

        with (
            patch.object(_RayClusterConfig, "get", return_value=mock_config),
            patch.object(RayCluster, "__attrs_post_init__", return_value=None),
        ):
            cluster = RayCluster()

            assert len(cluster.name) <= 63
            assert cluster.name.startswith("geneva-")
            assert not cluster.name.endswith("-")
            assert re.match(r"^[a-z0-9]([a-z0-9\-]*[a-z0-9])?$", cluster.name)


def test_generated_name_length_limits() -> None:
    """Test that generated names respect the 63 character limit"""
    # Test various username lengths
    for user_length in [10, 20, 30, 50, 60, 80, 100]:
        user = "a" * user_length
        mock_config = Mock()
        mock_config.user = user

        with (
            patch.object(_RayClusterConfig, "get", return_value=mock_config),
            patch.object(RayCluster, "__attrs_post_init__", return_value=None),
        ):
            cluster = RayCluster()

            assert len(cluster.name) <= 63, (
                f"Generated name too long: {cluster.name} ({len(cluster.name)} chars)"
            )
            assert cluster.name.startswith("geneva-")
            assert re.match(r"^[a-z0-9]([a-z0-9\-]*[a-z0-9])?$", cluster.name)


def test_validation_with_explicit_name() -> None:
    """Test that explicit names are validated"""
    mock_config = Mock()
    mock_config.user = "testuser"
    mock_config.namespace = "default"

    with (
        patch.object(_RayClusterConfig, "get", return_value=mock_config),
        patch.object(RayCluster, "__attrs_post_init__", return_value=None),
    ):
        # Valid explicit name
        cluster = RayCluster(name="my-valid-cluster")
        assert cluster.name == "my-valid-cluster"

        # Invalid explicit name should raise error
        with pytest.raises(ValueError, match="cluster name must comply with RFC 1123"):
            RayCluster(name="INVALID_NAME")


def test_validation_with_default_name() -> None:
    """Test that default generated names are automatically valid"""
    mock_config = Mock()
    mock_config.user = "test.user@domain.com"  # Contains invalid chars

    with (
        patch.object(_RayClusterConfig, "get", return_value=mock_config),
        patch.object(RayCluster, "__attrs_post_init__", return_value=None),
    ):
        cluster = RayCluster()  # No explicit name provided

        # Should auto-generate a valid name
        assert cluster.name == "geneva-test-user-domain-com"
        assert re.match(r"^[a-z0-9]([a-z0-9\-]*[a-z0-9])?$", cluster.name)


def test_name_used_in_kubernetes_resources() -> None:
    """Test that the validated name would be suitable for Kubernetes resources"""
    valid_cluster_names = [
        "geneva-user",
        "test-cluster-123",
        "a",
        "production-workload",
    ]

    for cluster_name in valid_cluster_names:
        mock_config = Mock()
        mock_config.user = "testuser"
        mock_config.namespace = "default"

        with (
            patch.object(_RayClusterConfig, "get", return_value=mock_config),
            patch.object(RayCluster, "__attrs_post_init__", return_value=None),
        ):
            cluster = RayCluster(name=cluster_name)

            # The name should be suitable for:
            # 1. Kubernetes resource names (metadata.name)
            assert len(cluster.name) <= 63
            assert re.match(r"^[a-z0-9]([a-z0-9\-]*[a-z0-9])?$", cluster.name)

            # 2. DNS subdomain names (for services, etc.)
            assert cluster.name == cluster.name.lower()
            assert not cluster.name.startswith("-")
            assert not cluster.name.endswith("-")


"""Test the validation logic independently"""


def test_rfc1123_regex_pattern() -> None:
    """Test the RFC 1123 regex pattern directly"""
    pattern = r"^[a-z0-9]([a-z0-9\-]*[a-z0-9])?$"

    # Valid matches
    valid_cases = [
        "a",
        "1",
        "ab",
        "a1",
        "1a",
        "a-b",
        "a--b",
        "a-1-b-2",
        "geneva-user-123",
        "x" * 63,
    ]

    for case in valid_cases:
        assert re.match(pattern, case), f"'{case}' should match RFC 1123 pattern"

    # Invalid matches
    invalid_cases = [
        "",
        "-",
        "a-",
        "-a",
        "A",
        "aB",
        "a_b",
        "a.b",
        "a b",
        "a@b",
        "--",
        "a--",
        "--a",
    ]

    for case in invalid_cases:
        assert not re.match(pattern, case), (
            f"'{case}' should not match RFC 1123 pattern"
        )


def test_length_validation() -> None:
    """Test length validation specifically"""
    # Exactly 63 characters should be valid
    exactly_63 = "a" * 63
    assert len(exactly_63) == 63

    # 64 characters should be invalid
    exactly_64 = "a" * 64
    assert len(exactly_64) == 64

    mock_config = Mock()
    mock_config.user = "testuser"
    mock_config.namespace = "default"

    with (
        patch.object(_RayClusterConfig, "get", return_value=mock_config),
        patch.object(RayCluster, "__attrs_post_init__", return_value=None),
    ):
        # 63 chars should work
        cluster_63 = RayCluster(name=exactly_63)
        assert cluster_63.name == exactly_63

        # 64 chars should fail
        with pytest.raises(
            ValueError, match="cluster name must be 63 characters or less"
        ):
            RayCluster(name=exactly_64)
