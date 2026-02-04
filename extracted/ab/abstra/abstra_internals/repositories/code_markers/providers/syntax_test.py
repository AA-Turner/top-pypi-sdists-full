from abstra_internals.repositories.code_markers.providers.syntax import (
    SyntaxMarkerProvider,
)


class TestSyntaxMarkerProvider:
    def setup_method(self):
        self.provider = SyntaxMarkerProvider()

    def test_name(self):
        assert self.provider.name == "syntax"

    def test_supports_python(self):
        assert self.provider.supports_file_type("python") is True

    def test_does_not_support_json(self):
        assert self.provider.supports_file_type("json") is False

    def test_valid_code_returns_no_markers(self):
        code = """
def hello_world():
    print("Hello, world!")
    return "success"
"""
        markers = self.provider.get_markers(code)
        assert len(markers) == 0

    def test_syntax_error_returns_marker(self):
        code = "if True"  # Missing colon - reliable syntax error
        markers = self.provider.get_markers(code)
        assert len(markers) > 0
        assert markers[0].severity == "error"
        assert markers[0].source == "syntax"

    def test_marker_has_correct_structure(self):
        code = "if True"  # Missing colon
        markers = self.provider.get_markers(code)
        assert len(markers) > 0
        marker = markers[0]
        assert hasattr(marker, "line")
        assert hasattr(marker, "column")
        assert hasattr(marker, "until_line")
        assert hasattr(marker, "until_column")
        assert hasattr(marker, "message")
        assert hasattr(marker, "severity")
        assert hasattr(marker, "source")

    def test_marker_to_dict(self):
        code = "if True"  # Missing colon
        markers = self.provider.get_markers(code)
        assert len(markers) > 0
        marker_dict = markers[0].to_dict()
        assert "line" in marker_dict
        assert "column" in marker_dict
        assert "until_line" in marker_dict
        assert "until_column" in marker_dict
        assert "message" in marker_dict
        assert "severity" in marker_dict
        assert "source" in marker_dict
        assert marker_dict["source"] == "syntax"
