"""
Performance regression tests for client operations.

These tests track API call counts and patterns to detect performance regressions.
"""

from contextlib import asynccontextmanager

import pytest

from arraylake import AsyncClient

from tests.test_virtual_chunks import vcap_for_bucket


@asynccontextmanager
async def _noop_cm():
    yield


@pytest.mark.asyncio
class TestGetRepoCallCount:
    """Regression tests: get_repo should make minimal API calls"""

    @pytest.mark.parametrize(
        ("use_vccs", "authorize_vccs_explicitly", "expected_num_calls", "expected_num_sequential_calls"),
        [
            pytest.param(False, False, 1, 1, id="auto_discover_no_vccs"),
            pytest.param(
                True,
                False,
                1,
                1,
                id="auto_discover_vccs",
            ),
            pytest.param(True, True, 3, 3, id="explicit_vccs"),
        ],
    )
    async def test_get_repo(
        self,
        api_call_counter,
        isolated_org,
        default_bucket,
        minio_anon_bucket,
        token,
        use_vccs,
        authorize_vccs_explicitly,
        expected_num_calls,
        expected_num_sequential_calls,
    ):
        repo_bucket = default_bucket()
        virtual_bucket = minio_anon_bucket(prefix="prefix")
        vcc_url_prefix = "s3://" + virtual_bucket.name + "/" + virtual_bucket.prefix + "/"

        authorize_virtual_chunk_access = {vcc_url_prefix: virtual_bucket.nickname}
        async with isolated_org(repo_bucket, virtual_bucket) as (org_name, buckets):
            aclient = AsyncClient(token=token)

            # VCAP required for VCC validation when virtual chunks are used
            vcap_cm = vcap_for_bucket(aclient, org_name, virtual_bucket) if use_vccs else _noop_cm()
            async with vcap_cm:
                # Setup: create repo (not counted)
                name = f"{org_name}/foo"
                await aclient.create_repo(
                    name,
                    bucket_config_nickname=repo_bucket.nickname,
                    authorize_virtual_chunk_access=authorize_virtual_chunk_access if use_vccs else {},
                )

                # Count only get_repo calls
                async with api_call_counter() as counter:
                    await aclient.get_repo(
                        name, authorize_virtual_chunk_access=authorize_virtual_chunk_access if authorize_vccs_explicitly else None
                    )

        assert len(counter.tracked_calls) <= expected_num_calls, counter.call_log()
        assert counter.count_sequential_calls() <= expected_num_sequential_calls, counter.call_log()
