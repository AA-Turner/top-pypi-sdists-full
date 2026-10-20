"""Site icons ride beside a tool result for the screen; the model never pays for them."""

from matrx_ai.tools.models import ToolResult


def test_site_icons_are_excluded_from_every_dump():
    result = ToolResult(success=True, output="text", site_icons={"https://a.com": "https://i/a.png"})
    assert result.site_icons == {"https://a.com": "https://i/a.png"}
    assert "site_icons" not in result.model_dump()
    assert "i/a.png" not in result.model_dump_json()
    assert "i/a.png" not in str(result.to_tool_result_content())
