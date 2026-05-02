from connector.utils.case_insensitive_dict import CaseInsensitiveDict


class TestCaseInsensitiveDict:
    def test_case_insenstive_dict(self) -> None:
        lookup_map = CaseInsensitiveDict()
        lookup_map["Foo"] = "bar"

        assert lookup_map["foo"] == "bar"
        assert lookup_map["FOO"] == "bar"
        assert lookup_map["fOo"] == "bar"
