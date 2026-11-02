from agentic_devtools.cli.issue_template.renderer import _heading_text


class TestHeadingText:
    def test_plain_heading(self):
        assert _heading_text("## Links") == "Links"

    def test_heading_with_closing_hashes(self):
        assert _heading_text("## Links ##") == "Links"

    def test_heading_with_closing_hashes_no_space(self):
        # CommonMark: the closing sequence must be preceded by a space
        # "## Links##" — the closing hashes are part of the text, not a closing sequence
        assert _heading_text("## Links##") == "Links##"

    def test_heading_with_multiple_closing_hashes(self):
        assert _heading_text("## Links ###") == "Links"

    def test_heading_only_hashes_as_text(self):
        # "## ##" — text is "##"; the closing sequence strips it
        assert _heading_text("## ##") == ""

    def test_non_heading_returns_empty(self):
        assert _heading_text("not a heading") == ""

    def test_h1_plain(self):
        assert _heading_text("# Title") == "Title"

    def test_h1_with_closing(self):
        assert _heading_text("# Title #") == "Title"

    def test_leading_spaces_allowed(self):
        assert _heading_text("   ## Section ##") == "Section"

    def test_empty_heading(self):
        assert _heading_text("##") == ""
