from types import MappingProxyType

from agentic_devtools.ai_providers.serialization import thaw_json


def test_thaw_json():
    frozen = MappingProxyType(
        {
            "a": tuple([1, 2, MappingProxyType({"b": "c"})]),
            "token": "<redacted>",
            "nested": MappingProxyType({"api_key": "<redacted>", "safe": True}),
        }
    )

    thawed = thaw_json(frozen)
    assert isinstance(thawed, dict)
    assert thawed["token"] == "<redacted>"
    assert isinstance(thawed["a"], list)
    assert thawed["a"][2]["b"] == "c"
