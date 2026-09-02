import json

import json_merge_patch
import pytest

from ocdsextensionregistry import get_versioned_release_schema
from ocdsextensionregistry.exceptions import VersionedReleaseWarning
from tests import read


def test_get_versioned_release_schema():
    schema = json.loads(read("release-schema.json"))

    actual = get_versioned_release_schema(schema, "1__1__5")

    assert actual == json.loads(read("versioned-release-validation-schema.json"))


def test_items_array():
    schema = get_versioned_release_schema(json.loads(read("release-schema.json")), "1__1__5")

    json_merge_patch.merge(schema, json.loads(read("schema-items-array.json")))

    with pytest.warns(VersionedReleaseWarning) as records:
        get_versioned_release_schema(schema, "1__1__5")

    assert len(records) == 62
