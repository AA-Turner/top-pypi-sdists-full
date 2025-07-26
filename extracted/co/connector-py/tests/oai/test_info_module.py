"""Test cases for ``Integration.info`` function."""

import json

from connector.oai.integration import DescriptionData, Integration
from connector_sdk_types.generated import (
    AppCategory,
    AppInfoRequest,
    AppInfoRequestPayload,
    EntitlementType,
    ResourceType,
    StandardCapabilityName,
)


async def test_app_info_capability_is_active():
    integration = Integration(
        app_id="test",
        version="0.1.0",
        credentials=[],
        description_data=DescriptionData(
            app_vendor_domain="test.com",
            user_friendly_name="Test",
            description="Test description",
            categories=[],
        ),
        exception_handlers=[],
    )

    assert StandardCapabilityName.APP_INFO in integration.capabilities


async def test_app_info_capability_returns_app_info():
    integration = Integration(
        app_id="test",
        version="0.1.0",
        credentials=[],
        description_data=DescriptionData(
            app_vendor_domain="test.com",
            user_friendly_name="Test",
            description="Test description",
            categories=[AppCategory.DEVELOPERS],
        ),
        exception_handlers=[],
        resource_types=[
            ResourceType(
                type_id="test",
                type_label="Test",
            )
        ],
        entitlement_types=[
            EntitlementType(
                type_id="test",
                type_label="Test",
                resource_type_id="test",
                min=1,
                max=10,
            )
        ],
    )

    app_info = await integration.dispatch(
        StandardCapabilityName.APP_INFO,
        AppInfoRequest(
            request=AppInfoRequestPayload(),
            credentials=None,
            settings=None,
        ).model_dump_json(),
    )
    app_info = json.loads(app_info)

    assert app_info["response"]["app_id"] == "test"
    assert isinstance(app_info["response"]["app_schema"], dict)

    oas = app_info["response"]["app_schema"]
    assert oas["openapi"] == "3.0.0"
    assert oas["info"]["title"] == "Test"
    assert oas["info"]["version"] == "0.1.0"
    assert oas["info"]["description"] == "Test description"
    assert oas["info"]["x-app-vendor-domain"] == "test.com"
    assert oas["info"]["x-categories"] == {
        "type": "enum",
        "enum": [AppCategory.DEVELOPERS.value],
    }
    assert oas["info"]["x-entitlement-types"] == [
        {
            "type_id": "test",
            "type_label": "Test",
            "resource_type_id": "test",
            "min": 1,
            "max": 10,
        }
    ]
    assert oas["info"]["x-resource-types"] == [
        {
            "type_id": "test",
            "type_label": "Test",
        }
    ]
