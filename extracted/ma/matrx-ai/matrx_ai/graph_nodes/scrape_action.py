"""``ai.scrape.web`` — scrape a web page and return structured content."""

from __future__ import annotations

from matrx_graph.actions import register_node
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, failure, success
from pydantic import BaseModel, ConfigDict, Field


class WebScrapeInput(BaseModel):
    model_config = ConfigDict(extra="allow")

    url: str = Field(min_length=1, description="The URL to scrape.")
    max_content_length: int = Field(default=30000)
    channel_out: str | None = Field(
        default=None,
        description="Optional channel to write the results to. Used for gather/fan-in patterns.",
    )


class WebScrapeOutput(BaseModel):
    """Conforms to the ``scraped_page`` platform kind: ``text`` is the
    canonical readable-content field its renderers consume. ``content`` is the
    same value under this node's historical name — live definitions dot-path
    it, so it stays until they migrate.

    ``is_good_scrape`` means "the fetch succeeded AND produced non-empty
    text". It was previously read off a key ``read_page_mcp_quick`` does not
    return, so it was ``False`` on every successful scrape (AD193)."""

    model_config = ConfigDict(extra="forbid")

    url: str
    text: str = ""
    content: str = ""
    is_good_scrape: bool = False


@register_node(
    name="ai.scrape.web",
    display_name="Fetch Page Content",
    description="Fetch a web page and pull out its readable content.",
    category=NodeCategory.TOOL,
    determinism=ActionTier.NON_DETERMINISTIC,
    input_schema=WebScrapeInput,
    output_schema=WebScrapeOutput,
    output_kind="scraped_page",
    icon="globe",
    tags=("ai", "scrape", "web"),
)
async def ai_scrape_web(
    ctx: NodeExecutionContext, inputs: WebScrapeInput
) -> NodeResult[WebScrapeOutput]:
    try:
        from matrx_scraper.features.read_page import read_page_mcp_quick

        result = await read_page_mcp_quick(url=inputs.url)

        if isinstance(result, dict):
            # `read_page_mcp_quick` signals failure with status="error" and puts
            # an apology sentence in `result`. Reading only `result` turned every
            # failed fetch into a node Success carrying "Sorry could not access
            # this page." as page text (AD193). Check the status FIRST.
            if result.get("status") == "error":
                reason = result.get("result") or "read_page returned status=error"
                return failure(
                    "scrape_failed",
                    f"scrape of {inputs.url} failed: {reason}",
                    details={"url": inputs.url, "failure_reason": reason},
                )
            # `text` is the raw extract. `result` is a legacy PROMPT-wrapped
            # string ('Here is the content from page …. Assess if this context
            # fully answers the user's query…') — instructions to a model, not
            # page content, and never what the `scraped_page` kind means.
            content = result.get("text") or ""
        else:
            content = str(result)

        is_good_scrape = bool(content.strip())

        if isinstance(content, str) and len(content) > inputs.max_content_length:
            content = content[: inputs.max_content_length] + "\n...[truncated]"

        output = WebScrapeOutput(
            url=inputs.url,
            text=content,
            content=content,
            is_good_scrape=is_good_scrape,
        )

        if inputs.channel_out:
            ctx.channels.write(inputs.channel_out, output)

        return success(output)

    except Exception as e:
        # Node Result System: failure travels in the envelope — nothing is
        # written to channel_out on failure (fan-in consumers see only real
        # scrapes; use on_item_failure='hole' for explicit failed slots).
        return failure(
            "scrape_failed",
            f"{type(e).__name__}: {e}",
            details={"url": inputs.url},
        )
