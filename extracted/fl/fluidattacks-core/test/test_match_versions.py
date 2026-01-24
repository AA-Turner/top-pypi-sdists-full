import pytest

from fluidattacks_core.semver.match_versions import (
    do_ranges_intersect,
    is_single_version_in_range,
    match_vulnerable_versions,
)

VERSIONS_TESTS: list[list[object]] = [
    ["^1.0.0", "<0.0", False],
    ["^7.0.0", "=6.12.2", False],
    ["^7.0.0", "=6.12.2 || =6.9.1", False],
    ["~2.2.3", ">=3.0.0 <=4.0.0", False],
    ["=2.2", ">=2.3.0 <=2.4.0", False],
    ["~0.8.0", ">=0 <=1.8.6", True],
    ["1.8.0", ">=0 <=0.3.0 || >=1.0.1 <=1.8.6", True],
    ["^2.1.0", ">=0 <11.0.5 || >=11.1.0 <11.1.0", True],
    ["2.1.0", "~2", True],
    ["=2.3.0-pre", ">=2.1.1 <2.3.0", False],
    ["=2.3.0-pre", ">=2.3.0 <2.7.0", False],
    ["=2.2.0-rc1", ">=2.1.1 <2.3.0", True],
    ["=2.1.0-pre", "=2.1.0-pre", True],
    ["=2.1.0-pre", "=2.1.0", False],
    [">2.1.1 <=2.3.0", "<2.1.0||=2.3.0-pre||>=2.4.0 <2.5.0", True],
    [">2.1.1 <2.3.0", "<2.1.0||=2.3.1-pre", False],
    ["1.0.0-beta.8", "<=1.0.0-beta.6", False],
    ["1.0.0-beta.4", "<=1.0.0-beta.6", True],
    ["^1.0.0-rc.10", ">2.0.0 <=4.0.0", False],
    ["^1.0.0-rc.10", ">=1.0.0 <=2.0.0", True],
    ["^7.23.2", ">=0 <7.23.2 || >=8.0.0-alpha.0 <8.0.0-alpha.4", False],
    ["7.23.2", ">=0 <=7.23.2", True],
    ["7.23.2", ">=6.5.1", True],
    ["=7.23.2", ">=6.5.1", True],
    [">=11.1", ">=0 <12.3.3", True],
    ["^1.2.0", ">=0 <1.0.3", False],
    ["2.0.0||^3.0.0", ">=3.0.0", True],
    ["3.*", ">=3.2.0 <4.0.0", True],
    ["4.0", "=3.5.1 || =4.0 || =5.0", True],
    ["4.2.2.RELEASE", ">0 <4.2.16", True],
    ["2.13.14", ">0 <2.13.14-1", False],
    ["8.4", ">=0 <7.6.3 || >=8.0.0 <8.4.0", False],
    ["6.1.5.Final", ">=6.1.2 <6.1.5", False],
    ["6.1.5.Final", ">=6.1.2 <=6.1.5", True],
    ["==3.0.0 || >=4.0.1 <4.0.2 || ==4.0.1", "=3.0.0", True],
    ["1.16.5-x86_64-darwin", "<1.16.5", False],
    ["1.16.5-x86_64-mingw-10", "<1.16.5", False],
    ["1.16.5-aarch64-linux", "<=1.16.5", True],
    ["0.0.0-20221012-56ae", ">=0.0.0 <0.17.0", True],
    ["0.0.0-20221012-56ae", "<0.17.0", True],
    ["=0.10.0-20221012-e7cb96979f69", "<0.10.0", False],
    ["=0.10.0-20221012-e7cb96979f69", "<=0.10.0", True],
    ["${lombokVersion}", ">0", False],
    ["", ">0", False],
    ["0.0.0", None, False],
    ["2.*,<2.3", ">=2.0.1", True],
    ["2.*,<2.3", ">=1.3.0 <2.0.0", False],
    ["1.2.0", ">=1.0.0,<=2.0.0", True],
    ["1.2.0", ">=1.0.0,   <=2.0.0", True],
    ["3.2.0+incompatible", ">1.0.0 <=3.2.0", True],
    [">= 3.1.44 , < 3.2.0", ">=3.1.0", True],
    [">= 3.1.44  < 3.2.0", ">=3.1.0", True],
    ["1.2.3 <=2.0.0", ">=1.0.0", True],
]

# Tests for RPM/Red Hat versions with epoch handling
RPM_EPOCH_TESTS: list[list[object]] = [
    # Specific case that was failing
    ["0:2.35.2-42.el9", "<=0:2.35.2-42.el9", True],
    ["0:2.35.2-63.el9", "<=0:2.35.2-42.el9", False],  # 63 > 42
    ["0:2.35.2-30.el9", "<=0:2.35.2-42.el9", True],  # 30 < 42
    ["0:3.8.3-6.el9", "<0:3.8.3-6.el9_6.2", True],
    # Basic epoch cases
    ["0:1.2.3", "<=0:1.2.3", True],
    ["0:1.2.3", "<0:1.2.3", False],
    ["0:1.2.3", ">=0:1.2.3", True],
    ["0:1.2.3", ">0:1.2.3", False],
    # Comparisons between different epochs
    ["1:2.3.4", "==0:2.3.4", False],  # 1 != 0
    ["0:2.3.4", "==1:2.3.4", False],  # 0 != 1
    # Cases with Red Hat release numbers
    ["0:2.35.2-42.el9", "==0:2.35.2-42.el9", True],
    ["0:2.35.2-42.el9", "==0:2.35.2-63.el9", False],  # 42 != 63
    ["0:2.35.2-63.el9", "==0:2.35.2-42.el9", False],  # 63 != 42
]

# Tests for RHEL major and minor version handling
RHEL_VERSION_TESTS: list[list[object]] = [
    # Core RHEL version comparison cases
    ["0:3.8.3-6.el9", "<0:3.8.3-6.el9_6.2", True],  # RHEL 9.0 < RHEL 9.6.2 (original case)
    ["0:3.8.3-6.el9_3", "<0:3.8.3-6.el9_6", True],  # RHEL 9.3 < RHEL 9.6 (minor versions)
    ["0:3.8.3-6.el9_6", "<0:3.8.3-6.el9_6.2", True],  # RHEL 9.6.0 < RHEL 9.6.2 (patch versions)
    # Different RHEL major versions
    ["0:2.35.2-42.el8_5", "<0:2.35.2-42.el8_8", True],  # RHEL 8.5 < RHEL 8.8
    ["0:1.2.3-4.el7_6", "<0:1.2.3-4.el7_9", True],  # RHEL 7.6 < RHEL 7.9
    # Reverse cases (should be False)
    ["0:3.8.3-6.el9_6", "<0:3.8.3-6.el9", False],  # RHEL 9.6 < RHEL 9.0
    ["0:3.8.3-6.el9_6.2", "<0:3.8.3-6.el9_6", False],  # RHEL 9.6.2 < RHEL 9.6.0
    # Equal cases
    ["0:3.8.3-6.el9_6", "<=0:3.8.3-6.el9_6", True],  # RHEL 9.6 <= RHEL 9.6
]


@pytest.mark.parametrize(("dep_ver", "vuln_ver", "expected"), VERSIONS_TESTS)
def test_match_vulnerable_versions(
    dep_ver: str,
    vuln_ver: str | None,
    expected: bool,  # noqa: FBT001
) -> None:
    is_vulnerable = match_vulnerable_versions(dep_ver, vuln_ver)
    assert is_vulnerable == expected


@pytest.mark.parametrize(("dep_ver", "vuln_ver", "expected"), RPM_EPOCH_TESTS)
def test_match_vulnerable_versions_rpm_epoch(
    dep_ver: str,
    vuln_ver: str | None,
    expected: bool,  # noqa: FBT001
) -> None:
    """Test cases specifically for RPM/Red Hat versions with epoch handling."""
    is_vulnerable = match_vulnerable_versions(dep_ver, vuln_ver)
    assert is_vulnerable == expected


@pytest.mark.parametrize(("dep_ver", "vuln_ver", "expected"), RHEL_VERSION_TESTS)
def test_match_vulnerable_versions_rhel_major_minor(
    dep_ver: str,
    vuln_ver: str | None,
    expected: bool,  # noqa: FBT001
) -> None:
    """Test cases specifically for RHEL major and minor version handling."""
    is_vulnerable = match_vulnerable_versions(dep_ver, vuln_ver)
    assert is_vulnerable == expected


def test_do_ranges_intersect_range_parts_is_not_four(caplog: pytest.LogCaptureFixture) -> None:
    assert do_ranges_intersect(">=", ">= 3.4.0") is False
    assert "Invalid version range: >=. Values cannot be parsed." in caplog.text


def test_is_single_version_in_range_range_parts_is_not_four(
    caplog: pytest.LogCaptureFixture,
) -> None:
    assert is_single_version_in_range("1.0.0", ">") is False
    assert "Invalid version range: >. Values cannot be parsed." in caplog.text
