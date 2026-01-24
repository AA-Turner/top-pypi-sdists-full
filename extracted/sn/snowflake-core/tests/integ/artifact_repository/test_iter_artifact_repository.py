import pytest

from snowflake.core.artifact_repository import ArtifactRepository
from tests.integ.fixtures.constants import UUID
from tests.integ.utils import random_string


@pytest.fixture(scope="function")
def setup(artifact_repositories, temp_pypi_api_integration):
    """Set up multiple artifact repositories for iteration testing."""
    names = [random_string(10, f"test_artifact_repository_iter_a_{UUID}_")]
    for _ in range(2):
        names.append(random_string(10, f"test_artifact_repository_iter_b_{UUID}_"))
    for _ in range(3):
        names.append(random_string(10, f"test_artifact_repository_iter_c_{UUID}_"))

    try:
        for name in names:
            ar_def = ArtifactRepository(
                name=name,
                type="PIP",
                api_integration=temp_pypi_api_integration,
                comment="created by test_iter setup",
            )
            artifact_repositories.create(ar_def)
        yield
    finally:
        for name in names:
            artifact_repositories[name].drop(if_exists=True)


def test_iter_artifact_repositories(setup, artifact_repositories):
    """Test iterating over artifact repositories."""
    test_repositories = list(artifact_repositories.iter())
    assert len(test_repositories) == 6

    for ar in test_repositories:
        assert ar.name is not None
        assert ar.type == "PIP"
        assert ar.api_integration is not None


def test_iter_artifact_repositories_with_filter(setup, artifact_repositories):
    """Test iterating over artifact repositories with pattern filter."""
    filter_pattern = f"TEST_ARTIFACT_REPOSITORY_ITER_B_{UUID}_%"

    b_pattern_results = list(artifact_repositories.iter(like=filter_pattern))
    assert len(b_pattern_results) == 2

    for ar in b_pattern_results:
        assert f"TEST_ARTIFACT_REPOSITORY_ITER_B_{UUID}_" in ar.name


def test_iter_artifact_repositories_empty_filter(setup, artifact_repositories):
    """Test iterating over artifact repositories with filter that matches nothing."""
    no_match_results = list(artifact_repositories.iter(like="nonexistent_pattern_%"))
    assert len(no_match_results) == 0


def test_iter_artifact_repositories_starts_with(setup, artifact_repositories):
    """Test iterating over artifact repositories with starts_with filter."""
    starts_with_pattern = f"TEST_ARTIFACT_REPOSITORY_ITER_C_{UUID}_"

    c_starts_with_results = list(artifact_repositories.iter(starts_with=starts_with_pattern))
    assert len(c_starts_with_results) == 3

    for ar in c_starts_with_results:
        assert ar.name.startswith(starts_with_pattern)


def test_iter_artifact_repositories_with_limit(setup, artifact_repositories):
    """Test iterating over artifact repositories with limit."""
    limited_results = list(artifact_repositories.iter(limit=3))
    assert len(limited_results) == 3

    filter_pattern = f"TEST_ARTIFACT_REPOSITORY_ITER_C_{UUID}_%"
    limited_filtered_results = list(artifact_repositories.iter(like=filter_pattern, limit=2))
    assert len(limited_filtered_results) == 2

    for ar in limited_filtered_results:
        assert f"TEST_ARTIFACT_REPOSITORY_ITER_C_{UUID}_" in ar.name


def test_iter_artifact_repositories_from_name_pagination(setup, artifact_repositories):
    """Test iterating over artifact repositories with from_name pagination parameter."""
    test_results = list(artifact_repositories.iter())

    test_results.sort(key=lambda x: x.name)
    assert len(test_results) == 6

    second_repo_name = test_results[1].name
    from_second_results = list(artifact_repositories.iter(limit=6, from_name=second_repo_name))

    # FROM clause is inclusive, so we expect 5 repos (from index 1 to 5, inclusive)
    assert len(from_second_results) == 5, (
        f"Expected 5 repos from second repo onwards (inclusive), got {len(from_second_results)}"
    )

    for ar in from_second_results:
        assert ar.name >= second_repo_name, f"Expected {ar.name} >= {second_repo_name} (from_name is inclusive)"

    last_repo_name = test_results[-1].name
    from_last_results = list(artifact_repositories.iter(limit=6, from_name=last_repo_name))

    # FROM clause is inclusive, so we expect 1 repo (the last repo itself)
    assert len(from_last_results) == 1, (
        f"Expected 1 repo starting from last repo (inclusive), got {len(from_last_results)}"
    )

    partial_name = f"TEST_ARTIFACT_REPOSITORY_ITER_B_{UUID}_"
    from_partial_results = list(artifact_repositories.iter(limit=6, from_name=partial_name))

    # Should get both B repositories (2) + all C repositories (3) = 5 total
    # since partial_name matches the first B repository and from_name is inclusive
    assert len(from_partial_results) == 5, (
        f"Expected 5 repos from partial name match (2 B + 3 C), got {len(from_partial_results)}"
    )

    # Count the B and C repositories separately to verify the partial matching worked
    b_repos = [ar for ar in from_partial_results if f"TEST_ARTIFACT_REPOSITORY_ITER_B_{UUID}_" in ar.name]
    c_repos = [ar for ar in from_partial_results if f"TEST_ARTIFACT_REPOSITORY_ITER_C_{UUID}_" in ar.name]

    assert len(b_repos) == 2, f"Expected 2 'B' repos, got {len(b_repos)}"
    assert len(c_repos) == 3, f"Expected 3 'C' repos, got {len(c_repos)}"

    limited_results = list(artifact_repositories.iter(from_name=second_repo_name, limit=2))
    assert len(limited_results) <= 2, "Limited results should respect limit parameter"


def test_iter_artifact_repositories_from_name_with_filter(setup, artifact_repositories):
    """Test from_name pagination combined with like filter."""
    filter_pattern = f"TEST_ARTIFACT_REPOSITORY_ITER_B_{UUID}_%"

    all_b_results = list(artifact_repositories.iter(like=filter_pattern))
    assert len(all_b_results) == 2, "Setup should create exactly 2 'B' pattern repositories"

    all_b_results.sort(key=lambda x: x.name)
    from_name_reference = all_b_results[0].name

    from_name_filtered_results = list(
        artifact_repositories.iter(like=filter_pattern, limit=2, from_name=from_name_reference)
    )

    # FROM clause is inclusive, so we expect both B repositories (starting from first one)
    assert len(from_name_filtered_results) == 2, (
        f"Expected 2 'B' repos starting from first (inclusive), got {len(from_name_filtered_results)}"
    )

    for ar in from_name_filtered_results:
        assert f"TEST_ARTIFACT_REPOSITORY_ITER_B_{UUID}_" in ar.name
        assert ar.name >= from_name_reference, f"Expected {ar.name} >= {from_name_reference} (from_name is inclusive)"

    assert from_name_filtered_results[0].name == all_b_results[0].name, "Should get the first 'B' repository"
    assert from_name_filtered_results[1].name == all_b_results[1].name, "Should get the second 'B' repository"
