# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from ours_privacy import OursPrivacy, AsyncOursPrivacy
from ours_privacy.types import TrackEventResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestTrack:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_event(self, client: OursPrivacy) -> None:
        track = client.track.event(
            token="x",
            event="x",
        )
        assert_matches_type(TrackEventResponse, track, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_event_with_all_params(self, client: OursPrivacy) -> None:
        track = client.track.event(
            token="x",
            event="x",
            default_properties={
                "_ef_transaction_id": "_ef_transaction_id",
                "active_duration": 0,
                "ad_id": "ad_id",
                "admitad_uid": "admitad_uid",
                "adset_id": "adset_id",
                "alart": "alart",
                "aleid": "aleid",
                "axwrt": "axwrt",
                "basis_cid": "basis_cid",
                "beeswax_auction_id": "beeswax_auction_id",
                "browser_language": "browser_language",
                "browser_name": "browser_name",
                "browser_version": "browser_version",
                "campaign_id": "campaign_id",
                "clickid": "clickid",
                "clid": "clid",
                "cpu_architecture": "cpu_architecture",
                "current_url": "current_url",
                "dclid": "dclid",
                "device_model": "device_model",
                "device_type": "device_type",
                "device_vendor": "device_vendor",
                "duration": 0,
                "encoding": "encoding",
                "engine_name": "engine_name",
                "engine_version": "engine_version",
                "epik": "epik",
                "fbc": "fbc",
                "fbclid": "fbclid",
                "fbp": "fbp",
                "fv": True,
                "gad_source": "gad_source",
                "gbraid": "gbraid",
                "gclid": "gclid",
                "host": "host",
                "iframe": True,
                "im_ref": "im_ref",
                "ip": "ip",
                "irclickid": "irclickid",
                "is_bot": "is_bot",
                "li_fat_id": "li_fat_id",
                "msclkid": "msclkid",
                "ndclid": "ndclid",
                "new_s": True,
                "ob_click_id": "ob_click_id",
                "oppref": "oppref",
                "os_name": "os_name",
                "os_version": "os_version",
                "page_hash": 0,
                "pathname": "pathname",
                "qclid": "qclid",
                "rdt_cid": "rdt_cid",
                "received_at": "received_at",
                "referrer": "referrer",
                "referring_domain": "referring_domain",
                "sacid": "sacid",
                "sccid": "sccid",
                "screen_height": 0,
                "screen_width": 0,
                "session_count": 0,
                "sid": "sid",
                "sr": "sr",
                "title": "title",
                "ttclid": "ttclid",
                "twclid": "twclid",
                "uafvl": "uafvl",
                "user_agent": "user_agent",
                "utm_campaign": "utm_campaign",
                "utm_content": "utm_content",
                "utm_medium": "utm_medium",
                "utm_name": "utm_name",
                "utm_source": "utm_source",
                "utm_term": "utm_term",
                "version": "version",
                "viant_click_id": "viant_click_id",
                "viant_impression_id": "viant_impression_id",
                "wbraid": "wbraid",
                "webview": True,
            },
            distinct_id="x",
            email="x",
            event_properties={"foo": "string"},
            external_id="x",
            identity_context={
                "ip": "ip",
                "user_agent": "userAgent",
            },
            time=0,
            user_id="x",
            user_properties={
                "_ef_transaction_id": "_ef_transaction_id",
                "ad_id": "ad_id",
                "admitad_uid": "admitad_uid",
                "adset_id": "adset_id",
                "alart": "alart",
                "aleid": "aleid",
                "axwrt": "axwrt",
                "basis_cid": "basis_cid",
                "beeswax_auction_id": "beeswax_auction_id",
                "campaign_id": "campaign_id",
                "city": "city",
                "clickid": "clickid",
                "clid": "clid",
                "company_name": "company_name",
                "consent": {"foo": "string"},
                "country": "country",
                "custom_properties": {"foo": "string"},
                "date_of_birth": "date_of_birth",
                "dclid": "dclid",
                "email": "email",
                "epik": "epik",
                "external_id": "external_id",
                "fbc": "fbc",
                "fbclid": "fbclid",
                "fbp": "fbp",
                "first_name": "first_name",
                "gad_source": "gad_source",
                "gbraid": "gbraid",
                "gclid": "gclid",
                "gender": "gender",
                "im_ref": "im_ref",
                "ip": "ip",
                "irclickid": "irclickid",
                "is_bot": "is_bot",
                "job_title": "job_title",
                "last_name": "last_name",
                "li_fat_id": "li_fat_id",
                "msclkid": "msclkid",
                "ndclid": "ndclid",
                "ob_click_id": "ob_click_id",
                "oppref": "oppref",
                "phone_number": "phone_number",
                "qclid": "qclid",
                "rdt_cid": "rdt_cid",
                "referrer": "referrer",
                "referring_domain": "referring_domain",
                "sacid": "sacid",
                "sccid": "sccid",
                "sid": "sid",
                "state": "state",
                "ttclid": "ttclid",
                "twclid": "twclid",
                "user_agent": "user_agent",
                "user_agent_full_list": "user_agent_full_list",
                "utm_campaign": "utm_campaign",
                "utm_content": "utm_content",
                "utm_medium": "utm_medium",
                "utm_name": "utm_name",
                "utm_source": "utm_source",
                "utm_term": "utm_term",
                "viant_click_id": "viant_click_id",
                "viant_impression_id": "viant_impression_id",
                "wbraid": "wbraid",
                "zip": "zip",
            },
        )
        assert_matches_type(TrackEventResponse, track, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_event(self, client: OursPrivacy) -> None:
        response = client.track.with_raw_response.event(
            token="x",
            event="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        track = response.parse()
        assert_matches_type(TrackEventResponse, track, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_event(self, client: OursPrivacy) -> None:
        with client.track.with_streaming_response.event(
            token="x",
            event="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            track = response.parse()
            assert_matches_type(TrackEventResponse, track, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncTrack:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_event(self, async_client: AsyncOursPrivacy) -> None:
        track = await async_client.track.event(
            token="x",
            event="x",
        )
        assert_matches_type(TrackEventResponse, track, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_event_with_all_params(self, async_client: AsyncOursPrivacy) -> None:
        track = await async_client.track.event(
            token="x",
            event="x",
            default_properties={
                "_ef_transaction_id": "_ef_transaction_id",
                "active_duration": 0,
                "ad_id": "ad_id",
                "admitad_uid": "admitad_uid",
                "adset_id": "adset_id",
                "alart": "alart",
                "aleid": "aleid",
                "axwrt": "axwrt",
                "basis_cid": "basis_cid",
                "beeswax_auction_id": "beeswax_auction_id",
                "browser_language": "browser_language",
                "browser_name": "browser_name",
                "browser_version": "browser_version",
                "campaign_id": "campaign_id",
                "clickid": "clickid",
                "clid": "clid",
                "cpu_architecture": "cpu_architecture",
                "current_url": "current_url",
                "dclid": "dclid",
                "device_model": "device_model",
                "device_type": "device_type",
                "device_vendor": "device_vendor",
                "duration": 0,
                "encoding": "encoding",
                "engine_name": "engine_name",
                "engine_version": "engine_version",
                "epik": "epik",
                "fbc": "fbc",
                "fbclid": "fbclid",
                "fbp": "fbp",
                "fv": True,
                "gad_source": "gad_source",
                "gbraid": "gbraid",
                "gclid": "gclid",
                "host": "host",
                "iframe": True,
                "im_ref": "im_ref",
                "ip": "ip",
                "irclickid": "irclickid",
                "is_bot": "is_bot",
                "li_fat_id": "li_fat_id",
                "msclkid": "msclkid",
                "ndclid": "ndclid",
                "new_s": True,
                "ob_click_id": "ob_click_id",
                "oppref": "oppref",
                "os_name": "os_name",
                "os_version": "os_version",
                "page_hash": 0,
                "pathname": "pathname",
                "qclid": "qclid",
                "rdt_cid": "rdt_cid",
                "received_at": "received_at",
                "referrer": "referrer",
                "referring_domain": "referring_domain",
                "sacid": "sacid",
                "sccid": "sccid",
                "screen_height": 0,
                "screen_width": 0,
                "session_count": 0,
                "sid": "sid",
                "sr": "sr",
                "title": "title",
                "ttclid": "ttclid",
                "twclid": "twclid",
                "uafvl": "uafvl",
                "user_agent": "user_agent",
                "utm_campaign": "utm_campaign",
                "utm_content": "utm_content",
                "utm_medium": "utm_medium",
                "utm_name": "utm_name",
                "utm_source": "utm_source",
                "utm_term": "utm_term",
                "version": "version",
                "viant_click_id": "viant_click_id",
                "viant_impression_id": "viant_impression_id",
                "wbraid": "wbraid",
                "webview": True,
            },
            distinct_id="x",
            email="x",
            event_properties={"foo": "string"},
            external_id="x",
            identity_context={
                "ip": "ip",
                "user_agent": "userAgent",
            },
            time=0,
            user_id="x",
            user_properties={
                "_ef_transaction_id": "_ef_transaction_id",
                "ad_id": "ad_id",
                "admitad_uid": "admitad_uid",
                "adset_id": "adset_id",
                "alart": "alart",
                "aleid": "aleid",
                "axwrt": "axwrt",
                "basis_cid": "basis_cid",
                "beeswax_auction_id": "beeswax_auction_id",
                "campaign_id": "campaign_id",
                "city": "city",
                "clickid": "clickid",
                "clid": "clid",
                "company_name": "company_name",
                "consent": {"foo": "string"},
                "country": "country",
                "custom_properties": {"foo": "string"},
                "date_of_birth": "date_of_birth",
                "dclid": "dclid",
                "email": "email",
                "epik": "epik",
                "external_id": "external_id",
                "fbc": "fbc",
                "fbclid": "fbclid",
                "fbp": "fbp",
                "first_name": "first_name",
                "gad_source": "gad_source",
                "gbraid": "gbraid",
                "gclid": "gclid",
                "gender": "gender",
                "im_ref": "im_ref",
                "ip": "ip",
                "irclickid": "irclickid",
                "is_bot": "is_bot",
                "job_title": "job_title",
                "last_name": "last_name",
                "li_fat_id": "li_fat_id",
                "msclkid": "msclkid",
                "ndclid": "ndclid",
                "ob_click_id": "ob_click_id",
                "oppref": "oppref",
                "phone_number": "phone_number",
                "qclid": "qclid",
                "rdt_cid": "rdt_cid",
                "referrer": "referrer",
                "referring_domain": "referring_domain",
                "sacid": "sacid",
                "sccid": "sccid",
                "sid": "sid",
                "state": "state",
                "ttclid": "ttclid",
                "twclid": "twclid",
                "user_agent": "user_agent",
                "user_agent_full_list": "user_agent_full_list",
                "utm_campaign": "utm_campaign",
                "utm_content": "utm_content",
                "utm_medium": "utm_medium",
                "utm_name": "utm_name",
                "utm_source": "utm_source",
                "utm_term": "utm_term",
                "viant_click_id": "viant_click_id",
                "viant_impression_id": "viant_impression_id",
                "wbraid": "wbraid",
                "zip": "zip",
            },
        )
        assert_matches_type(TrackEventResponse, track, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_event(self, async_client: AsyncOursPrivacy) -> None:
        response = await async_client.track.with_raw_response.event(
            token="x",
            event="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        track = await response.parse()
        assert_matches_type(TrackEventResponse, track, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_event(self, async_client: AsyncOursPrivacy) -> None:
        async with async_client.track.with_streaming_response.event(
            token="x",
            event="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            track = await response.parse()
            assert_matches_type(TrackEventResponse, track, path=["response"])

        assert cast(Any, response.is_closed) is True
