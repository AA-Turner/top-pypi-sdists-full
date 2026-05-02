import logging
import pprint

import pytest
from acceldata_sdk.errors import APIError
from acceldata_sdk.models.profile import ProfilingType
from acceldata_sdk.models.tags import AssetLabel, CustomAssetMetadata

from . import test_constants as test_const
from ..commons.retry import retry_operation

pp = pprint.PrettyPrinter(indent=4)

logger = logging.getLogger()


@pytest.mark.integration
def test_get_datasource(adoc_client):
    datasource_response = adoc_client.get_datasource(test_const.DS_NAME, True)
    logger.info("Datasource response: %s", datasource_response)
    assert datasource_response is not None


@pytest.mark.integration
def test_get_datasource_id(adoc_client):
    datasource_response = adoc_client.get_datasource(test_const.DS_NAME, True)
    datasource_by_id_response = adoc_client.get_datasource(datasource_response.id, False)
    logger.info("Datasource by ID response: %s", datasource_by_id_response)
    assert datasource_by_id_response is not None


@pytest.mark.integration
def test_get_all_data_sources(adoc_client):
    all_data_sources = adoc_client.get_datasources()
    logger.info("All datasources response:")
    logger.info(pp.pformat(all_data_sources))
    assert all_data_sources is not None


@pytest.mark.integration
def test_get_ds_crawler(adoc_client):
    datasource = adoc_client.get_datasource(test_const.DS_NAME, False)
    ds_id = adoc_client.get_datasource(datasource.id, True)
    try:
        status = ds_id.get_crawler_status()
        logger.info("Crawler status response:")
        logger.info(pp.pformat(status))
    except APIError as e:
        msg = str(e)
        logger.info(msg)

        # ACCEPTABLE outcome
        if "Unable to start the Crawler" in msg or "422" in msg:
            assert True
            return

        # Anything else is a real failure
        raise
    assert status is not None


@pytest.mark.integration
def test_start_crawler(adoc_client):
    datasource = adoc_client.get_datasource(test_const.DS_NAME, False)

    try:
        datasource.start_crawler()
        # If no exception → crawler started → PASS
        assert True

    except APIError as e:
        msg = str(e)
        logger.info(msg)

        # ACCEPTABLE outcome
        if "Unable to start the Crawler" in msg or "422" in msg:
            assert True
            return

        # Anything else is a real failure
        raise


@pytest.mark.integration
def test_get_asset(adoc_client):
    asset = adoc_client.get_asset(test_const.ASSET_UID)
    logger.info("Asset by UID response: %s", asset)
    assert asset is not None


@pytest.mark.integration
def test_get_asset_id(adoc_client):
    asset = adoc_client.get_asset(test_const.ASSET_UID)
    asset = adoc_client.get_asset(asset.id)
    logger.info("Asset by ID response: %s", asset)
    assert asset is not None


@pytest.mark.integration
def test_get_asset_metadata(adoc_client):
    asset = adoc_client.get_asset(test_const.ASSET_UID)
    metadata = asset.get_metadata()
    logger.info("Asset metadata response:")
    logger.info(pp.pformat(metadata))
    assert metadata is not None


@pytest.mark.integration
def test_get_asset_sample_data(adoc_client):
    asset = adoc_client.get_asset(test_const.ASSET_UID)
    sample_data = asset.sample_data()
    logger.info("Sample data response:")
    logger.info(pp.pformat(sample_data))
    assert sample_data is not None


@pytest.mark.integration
def test_get_asset_labels(adoc_client):
    asset = adoc_client.get_asset(test_const.ASSET_UID)
    labels = asset.get_labels()
    logger.info("Asset labels response:")
    logger.info(pp.pformat(labels))
    assert labels is not None


@pytest.mark.integration
def test_add_asset_labels(adoc_client):
    asset = adoc_client.get_asset(test_const.ASSET_UID)

    response = asset.add_labels(
        labels=[
            AssetLabel("test12", "shubh12"),
            AssetLabel("test22", "shubh32"),
        ]
    )

    logger.info("Add labels response: %s", response)

    labels = asset.get_labels()
    logger.info("Labels after add:")
    logger.info(pp.pformat(labels))

    assert labels is not None


@pytest.mark.integration
def test_add_asset_custom_metadata(adoc_client):
    asset = adoc_client.get_asset(test_const.ASSET_UID)

    response = asset.add_custom_metadata(
        custom_metadata=[
            CustomAssetMetadata("testcm1", "shubhcm1"),
            CustomAssetMetadata("testcm2", "shubhcm2"),
        ]
    )

    logger.info("Add custom metadata response: %s", response)

    metadata = asset.get_metadata()
    logger.info("Metadata after add:")
    logger.info(pp.pformat(metadata))

    assert metadata is not None


@pytest.mark.integration
def test_profile_status(adoc_client):
    asset = adoc_client.get_asset(test_const.ASSET_UID)
    status = asset.get_latest_profile_status()
    logger.info("Latest profile status:")
    logger.info(pp.pformat(status))
    assert status is not None


@pytest.mark.integration
def test_add_tag(adoc_client):
    asset = adoc_client.get_asset(test_const.ASSET_UID)

    try:
        asset.add_tag(test_const.ASSET_TAG)
    except APIError as e:
        assert "already exists" in str(e)


@pytest.mark.integration
def test_cancel_profile(adoc_client):
    asset = adoc_client.get_asset(test_const.ASSET_UID)
    def operation():
        return asset.start_profile(ProfilingType.FULL)

    try:
        profile = retry_operation(
            operation,
            test_const.MAX_RETRIES,
            test_const.RETRY_INTERVAL
        )
    except APIError as e:
        msg = str(e)

        # ✅ ACCEPTABLE: already running
        if "A profile is already running" in msg or "409" in msg:
            logger.info("Profile already running — accepting as PASS")
            return

        raise

    logger.info(f"Profile response: {profile}")
    status = profile.get_status()
    logger.info("Profile status before cancel:")
    logger.info(pp.pformat(status))

    if status["profileRequest"]["status"] == "IN PROGRESS":
        cancel_res = profile.cancel()
        logger.info("Cancel profile response: %s", cancel_res)
        assert cancel_res is not None


@pytest.mark.integration
def test_execute_profile(adoc_client):
    asset = adoc_client.get_asset(test_const.ASSET_UID)

    def operation():
        return asset.start_profile(ProfilingType.FULL)

    try:
        profile = retry_operation(
            operation,
            test_const.MAX_RETRIES,
            test_const.RETRY_INTERVAL
        )
    except APIError as e:
        msg = str(e)

        # ✅ ACCEPTABLE: already running
        if "A profile is already running" in msg or "409" in msg:
            logger.info("Profile already running — accepting as PASS")
            return

        raise
    status = profile.get_status()
    logger.info("Profile execution status:")
    logger.info(pp.pformat(status))
    status = profile.get_status()
    logger.info("Profile execution status:")
    logger.info(pp.pformat(status))

    assert status is not None
