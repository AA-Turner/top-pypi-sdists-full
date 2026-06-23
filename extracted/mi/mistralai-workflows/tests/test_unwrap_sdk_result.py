"""Unit tests for _unwrap_sdk_result_wrapping.

This function is only valid at the boundary where we just received a raw
SDK workflow return from Temporal.  The SDK wraps non-BaseModel returns in
``{"result": value}`` via a generated single-field Pydantic model.  This
helper strips that envelope using a heuristic (dict with exactly one
``"result"`` key).  It must NOT be reused outside that specific call site.
"""

from mistralai.workflows.plugins.evaluation._record_workflow import _unwrap_sdk_result_wrapping


class TestUnwrapSdkResultWrapping:
    # -- SDK wrapping (single "result" key) should be stripped --

    def test_unwrap_sdk_wrapped_string(self) -> None:
        """SDK wrapped a str return (-> str)."""
        assert _unwrap_sdk_result_wrapping({"result": "hello"}) == "hello"

    def test_unwrap_sdk_wrapped_int(self) -> None:
        """SDK wrapped an int return (-> int)."""
        assert _unwrap_sdk_result_wrapping({"result": 42}) == 42

    def test_unwrap_sdk_wrapped_dict(self) -> None:
        """SDK wrapped a dict return (-> dict). User returned {"key": "val"}."""
        assert _unwrap_sdk_result_wrapping({"result": {"key": "val"}}) == {"key": "val"}

    def test_unwrap_sdk_wrapped_list(self) -> None:
        """SDK wrapped a list return (-> list)."""
        assert _unwrap_sdk_result_wrapping({"result": [1, 2, 3]}) == [1, 2, 3]

    def test_unwrap_sdk_wrapped_none(self) -> None:
        """SDK wrapped a None return."""
        assert _unwrap_sdk_result_wrapping({"result": None}) is None

    # -- User dict that happens to have a "result" key: only unwrap once --

    def test_unwrap_user_dict_with_result_key(self) -> None:
        """User returned {"result": "foo"} from a -> dict workflow.

        SDK wraps to {"result": {"result": "foo"}}.  One unwrap gives back
        the user's original dict — we must NOT strip a second layer.
        """
        # After SDK wrapping + one unwrap, we'd have {"result": "foo"}.
        # That dict has exactly one key "result", so a naive implementation
        # would strip it again.  But _unwrap_sdk_result_wrapping is called
        # only once, so this is safe — the caller must not call it twice.
        sdk_wrapped = {"result": {"result": "foo"}}
        assert _unwrap_sdk_result_wrapping(sdk_wrapped) == {"result": "foo"}

    # -- BaseModel dumps with "result" + other keys: must NOT unwrap --

    def test_no_unwrap_basemodel_with_result_and_other_fields(self) -> None:
        """BaseModel dump: {"result": "foo", "score": 0.5}.

        Not SDK-wrapped — has multiple keys.  Must be left untouched.
        """
        value = {"result": "foo", "score": 0.5}
        assert _unwrap_sdk_result_wrapping(value) == value

    def test_no_unwrap_basemodel_with_result_and_status(self) -> None:
        """Another BaseModel shape with a "result" field among others."""
        value = {"result": "text", "status": "ok", "metadata": {}}
        assert _unwrap_sdk_result_wrapping(value) == value

    # -- Non-dict inputs: must be returned as-is --

    def test_no_unwrap_string(self) -> None:
        assert _unwrap_sdk_result_wrapping("a string") == "a string"

    def test_no_unwrap_int(self) -> None:
        assert _unwrap_sdk_result_wrapping(42) == 42

    def test_no_unwrap_list(self) -> None:
        assert _unwrap_sdk_result_wrapping([1, 2]) == [1, 2]

    def test_no_unwrap_none(self) -> None:
        assert _unwrap_sdk_result_wrapping(None) is None

    # -- Dict without "result" key: must NOT unwrap --

    def test_no_unwrap_dict_without_result_key(self) -> None:
        value = {"foo": "bar", "baz": 1}
        assert _unwrap_sdk_result_wrapping(value) == value

    def test_no_unwrap_empty_dict(self) -> None:
        assert _unwrap_sdk_result_wrapping({}) == {}
