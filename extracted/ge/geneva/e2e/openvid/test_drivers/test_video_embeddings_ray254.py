# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""
Wrapper tests for video embeddings that require Ray 2.54.0.

These tests run the actual video embedding tests via subprocess in the
embedding_vjepa2 UDF environment which has Ray 2.54.0 dependencies.
"""

import pytest

from conftest import assert_subprocess_passed, run_test_in_udf_env


def test_video_embedding_column_added_ray254(openvid_table, request) -> None:
    """Run test_video_embedding_column_added in Ray 2.54.0 environment."""
    # This test doesn't actually need a specific Ray version, but we run it via subprocess
    # to keep the test suite together

    # Pass through pytest command-line arguments to subprocess
    pytest_args = ["-v", "-s"]

    # Get command-line options from parent pytest session
    if hasattr(request.config, "getoption"):
        csp = request.config.getoption("--csp", default="gcp")
        test_slug = request.config.getoption("--test-slug", default=None)
        bucket_path = request.config.getoption("--bucket-path", default=None)
        num_videos = request.config.getoption("--num-videos", default=20)
        batch_size_arg = request.config.getoption("--batch-size", default=4)

        pytest_args.extend(
            [
                f"--csp={csp}",
                f"--num-videos={num_videos}",
                f"--batch-size={batch_size_arg}",
            ]
        )
        if test_slug:
            pytest_args.append(f"--test-slug={test_slug}")
        if bucket_path:
            pytest_args.append(f"--bucket-path={bucket_path}")

    result = run_test_in_udf_env(
        udf_name="embedding_vjepa2",
        test_path="test_drivers/_test_video_embeddings_impl.py::test_video_embedding_column_added",
        pytest_args=pytest_args,
    )

    assert_subprocess_passed(result, "test_video_embedding_column_added")


def test_video_embedding_backfill_ray254(
    openvid_table,
    ray_254_gpu_cluster,
    batch_size,
    skip_gpu,
    request,
) -> None:
    """Run test_video_embedding_backfill in Ray 2.54.0 environment."""
    if skip_gpu:
        pytest.skip("Skipping GPU test (--skip-gpu flag set)")

    # Pass through pytest command-line arguments to subprocess
    # The subprocess needs these to configure fixtures properly
    pytest_args = ["-v", "-s"]

    # Get command-line options from parent pytest session
    if hasattr(request.config, "getoption"):
        # Pass through critical options that affect test behavior
        csp = request.config.getoption("--csp", default="gcp")
        test_slug = request.config.getoption("--test-slug", default=None)
        bucket_path = request.config.getoption("--bucket-path", default=None)
        num_videos = request.config.getoption("--num-videos", default=100)
        batch_size_arg = request.config.getoption("--batch-size", default=10)

        pytest_args.extend(
            [
                f"--csp={csp}",
                f"--num-videos={num_videos}",
                f"--batch-size={batch_size_arg}",
            ]
        )
        if test_slug:
            pytest_args.append(f"--test-slug={test_slug}")
        if bucket_path:
            pytest_args.append(f"--bucket-path={bucket_path}")
        if skip_gpu:
            pytest_args.append("--skip-gpu")

    # Run the actual test via subprocess in Ray 2.54.0 environment
    result = run_test_in_udf_env(
        udf_name="embedding_vjepa2",
        test_path="test_drivers/_test_video_embeddings_impl.py::test_video_embedding_backfill",
        pytest_args=pytest_args,
    )

    assert_subprocess_passed(result, "test_video_embedding_backfill")


@pytest.mark.skip(reason="Skipped in original test file")
def test_video_similarity_search_ray254(
    openvid_table,
    ray_254_gpu_cluster,
    skip_gpu,
    request,
) -> None:
    """Run test_video_similarity_search in Ray 2.54.0 environment."""
    if skip_gpu:
        pytest.skip("Skipping GPU test (--skip-gpu flag set)")

    # Pass through pytest command-line arguments to subprocess
    pytest_args = ["-v", "-s"]

    # Get command-line options from parent pytest session
    if hasattr(request.config, "getoption"):
        csp = request.config.getoption("--csp", default="gcp")
        test_slug = request.config.getoption("--test-slug", default=None)
        bucket_path = request.config.getoption("--bucket-path", default=None)
        num_videos = request.config.getoption("--num-videos", default=20)
        batch_size_arg = request.config.getoption("--batch-size", default=4)

        pytest_args.extend(
            [
                f"--csp={csp}",
                f"--num-videos={num_videos}",
                f"--batch-size={batch_size_arg}",
            ]
        )
        if test_slug:
            pytest_args.append(f"--test-slug={test_slug}")
        if bucket_path:
            pytest_args.append(f"--bucket-path={bucket_path}")
        if skip_gpu:
            pytest_args.append("--skip-gpu")

    result = run_test_in_udf_env(
        udf_name="embedding_vjepa2",
        test_path="test_drivers/_test_video_embeddings_impl.py::test_video_similarity_search",
        pytest_args=pytest_args,
    )

    assert_subprocess_passed(result, "test_video_similarity_search")
