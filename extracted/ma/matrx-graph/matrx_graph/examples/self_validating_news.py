"""Self-validating news workflow — Phase 4 exit criteria.

Designed as a single-run pass/fail test for the entire stack. The final LLM
is given **no web access and no tools** — its only way to produce a factual
answer about today's top story is if every upstream node delivered correct
state. Decoy summaries ensure it isn't cheating via topology.

The full chain::

    news.search                   (DATA)
    └─ text.extract_field         extract hits.0.title (pure)
       └─ web.brave.search             web search on headline (IO)
          └─ ai.llm.chat           rank top URLs (LLM)
             └─ text.regex_extract parse URL list → matches (pure)
                └─ control.map     Send one scrape per URL
                   └─ scraper.scrape    per-URL (IO), output_channel="scrapes"
                      └─ control.gather drain the committed channel
                         └─ ai.llm.chat     summarize successes (LLM)
                            └─ data.transform  mix real + decoy summaries
                               └─ ai.llm.chat   final answer (LLM, no tools)

Pass condition: final_text mentions facts from the real top story.

Fan-in wiring (the part everyone gets wrong):

- The **worker owns the channel write**: ``scrape_page`` carries
  ``data.output_channel = "scrapes"``, so the scheduler appends its full
  output to the append-reducer channel after each invocation (mocked or
  real). ``control.map`` only dispatches Sends — it never writes state.
- The **gather is edge-triggered BY the worker** (``scrape_page →
  gather_scrapes``), so it fires one super-step after the workers, when
  their channel writes are committed. N parallel worker results routed
  to one target collapse to a single gather invocation (Pregel per-target
  aggregation). An edge from the map node instead would run gather in the
  SAME super-step as the workers, where it reads the pre-step channel
  snapshot and always sees an empty channel.
- Strict input schemas are bridged with edge ``mappings``:
  ``rank_urls → parse_urls`` maps ``final_text`` → ``text`` (regex_extract
  takes exactly one field), and ``parse_urls → fanout`` maps the extracted
  ``matches`` list into ``control.map``'s required ``items`` input.

Every action referenced is registered by either ``matrx_ai.graph_nodes``
or ``aidream.graph_actions`` at app startup. Compilation fails fast with
``NodeRegistryError`` if any piece is missing.
"""

from __future__ import annotations

from matrx_graph.types.channel import ChannelSpec
from matrx_graph.types.definition import (
    Definition,
    EdgeDef,
    NodeDef,
    Position,
    Viewport,
)


def build_self_validating_news_definition() -> Definition:
    """Return a full-chain ``Definition`` for the self-validating workflow.

    Environments without every configured news source, Brave search, or
    Anthropic will see affected nodes fail gracefully with a
    ``node_failed`` event rather than silent pass.
    """
    nodes: list[NodeDef] = [
        NodeDef(
            id="headlines",
            type="news.search",
            position=Position(x=40, y=80),
            data={
                "label": "Search current US news",
                "config": {},
                "spec_type": "news.search",
                "category": "data",
                "icon": "newspaper",
                "input": {"query": "top US news", "limit": 10},
            },
        ),
        NodeDef(
            id="top_title",
            type="text.extract_field",
            position=Position(x=340, y=80),
            data={
                "label": "Top headline title",
                "config": {},
                "spec_type": "text.extract_field",
                "category": "data",
                "icon": "crosshair",
                "input": {"path": "hits.0.title", "default": ""},
            },
        ),
        NodeDef(
            id="web_search",
            type="web.brave.search",
            position=Position(x=640, y=80),
            data={
                "label": "Web search (Brave)",
                "config": {},
                "spec_type": "web.brave.search",
                "category": "io",
                "icon": "search",
                "input": {"count": 10, "country": "us"},
            },
        ),
        # ai.llm.chat sends `prompt` and NOTHING else — upstream keys that
        # merely land beside it are never seen by the model. So every LLM
        # stage in this chain is fed by an edge that maps real upstream text
        # INTO `prompt`, with the standing instruction moved to
        # `system_instruction`. Without that the model answers from a static
        # string and the "self-validating" property is a fiction.
        NodeDef(
            id="search_text",
            type="data.stringify_json",
            position=Position(x=790, y=80),
            data={
                "label": "Search results as text",
                "config": {"indent": 2},
                "spec_type": "data.stringify_json",
                "category": "data",
                "icon": "braces",
            },
        ),
        NodeDef(
            id="rank_urls",
            type="ai.llm.chat",
            position=Position(x=940, y=80),
            data={
                "label": "Rank URLs (LLM)",
                "config": {},
                "spec_type": "ai.llm.chat",
                "category": "llm",
                "icon": "sparkles",
                "input": {
                    "model": "claude-opus-4-7",
                    "system_instruction": (
                        "You are given the JSON results of a web search. "
                        "Return the 5 most newsworthy URLs in order of "
                        "importance, one per line, with no commentary."
                    ),
                    # Overridden by edge e3b (prompt <- the serialized search
                    # results). Kept non-empty so the node is valid standalone.
                    "prompt": "Rank the search results.",
                },
            },
        ),
        NodeDef(
            id="parse_urls",
            type="text.regex_extract",
            position=Position(x=1240, y=80),
            data={
                "label": "Parse URL list",
                # data.transform can't do this: the sandbox (nodes/_sandbox.py)
                # forbids calls, attribute access, and comprehensions by
                # construction. Line-splitting text is regex work.
                "config": {"pattern": r"https?://\S+"},
                "spec_type": "text.regex_extract",
                "category": "data",
                "icon": "search",
            },
        ),
        NodeDef(
            id="fanout",
            type="control.map",
            position=Position(x=1540, y=80),
            data={
                "label": "Fanout over URLs",
                "config": {"target_node_id": "scrape_page", "payload_key": "url"},
                "spec_type": "control.map",
                "category": "control",
                "icon": "split-square-horizontal",
            },
        ),
        NodeDef(
            id="scrape_page",
            type="scraper.scrape",
            position=Position(x=1540, y=320),
            data={
                "label": "Scrape page",
                "config": {},
                "spec_type": "scraper.scrape",
                "category": "io",
                "icon": "globe",
                # Fan-in half 1: every scrape invocation appends its full
                # output to the "scrapes" channel. Without this binding
                # nothing writes the channel and gather drains nothing.
                "output_channel": "scrapes",
                # Real news sites time out, 403, and rate-limit — a single
                # unreachable URL out of five is WEATHER, not a workflow
                # defect, and the default 'park' policy errors the whole run
                # on it. 'hole' leaves that item empty and gather
                # (only_successful=True) drops it, which is the failure mode
                # this chain was built around.
                "on_item_failure": "hole",
            },
        ),
        NodeDef(
            id="gather_scrapes",
            type="control.gather",
            position=Position(x=1840, y=80),
            data={
                "label": "Gather scrapes",
                "config": {"channel": "scrapes", "only_successful": True},
                "spec_type": "control.gather",
                "category": "control",
                "icon": "layers",
            },
        ),
        NodeDef(
            id="combine_pages",
            type="ai.util.format_scraped_content",
            position=Position(x=1990, y=80),
            data={
                "label": "Combine scraped pages",
                "config": {},
                "spec_type": "ai.util.format_scraped_content",
                "category": "data",
                "icon": "align-left",
                "input": {"max_chars_per_page": 1500},
            },
        ),
        NodeDef(
            id="summarize",
            type="ai.llm.chat",
            position=Position(x=2140, y=80),
            data={
                "label": "Summarize successes",
                "config": {},
                "spec_type": "ai.llm.chat",
                "category": "llm",
                "icon": "sparkles",
                "input": {
                    "model": "claude-opus-4-7",
                    "system_instruction": (
                        "Summarize each of the scraped pages you are given in "
                        "3-4 sentences, preserving key facts and numbers. "
                        "Return one paragraph per page, separated by blank "
                        "lines."
                    ),
                    # Overridden by edge e8 (prompt <- the combined page text).
                    "prompt": "Summarize the pages.",
                },
            },
        ),
        NodeDef(
            id="mix_decoys",
            type="data.transform",
            position=Position(x=2440, y=80),
            data={
                "label": "Mix real + decoy",
                # A dict result is spread flat onto the output root, so this
                # emits `context_text` — one string, because that is what an
                # LLM prompt is. The previous list built the decoys correctly
                # and then had no way to reach the model at all.
                "config": {
                    "expression": (
                        "{'context_text': "
                        "'CONTEXT SUMMARIES (the only source you may use):\\n\\n' "
                        "+ str(inputs['final_text']) + '\\n\\n' "
                        "+ 'The annual migration of monarch butterflies to Mexico.\\n' "
                        "+ 'A review of new noise-cancelling headphones released this month.\\n' "
                        "+ 'Historical analysis of Ming dynasty porcelain exports.\\n' "
                        "+ 'An overview of competitive Rubiks Cube solving techniques.\\n' "
                        "+ 'The rise of urban beekeeping in European capitals.\\n\\n' "
                        "+ 'QUESTION: Based strictly on the context summaries above, "
                        "what is today\\'s top news story and what are its key details? "
                        "Quote specific facts from the summaries.'}"
                    )
                },
                "spec_type": "data.transform",
                "category": "data",
                "icon": "function-square",
            },
        ),
        NodeDef(
            id="final_answer",
            type="ai.llm.chat",
            position=Position(x=2740, y=80),
            data={
                "label": "Final answer (no tools)",
                "config": {},
                "spec_type": "ai.llm.chat",
                "category": "llm",
                "icon": "sparkles",
                "input": {
                    "model": "claude-opus-4-7",
                    "system_instruction": (
                        "You have no web access or tools. Answer only from the "
                        "context provided in the user message. If the context "
                        "doesn't contain the answer, say so explicitly."
                    ),
                    # Overridden by edge e9 (prompt <- context_text, which
                    # carries the real summaries, the decoys, and the
                    # question). Kept non-empty so the node is valid alone.
                    "prompt": "Answer from the provided context.",
                },
            },
        ),
    ]

    edges: list[EdgeDef] = [
        # text.extract_field projects INTO "record" (its other fields are
        # path/default), so the headline payload has to land there whole —
        # a broadcast would drop {"hits": [...]} at the top level and
        # leave record={} , which silently yields value="" / found=False.
        EdgeDef(
            id="e1",
            source="headlines",
            target="top_title",
            type="default",
            data={"kind": "data", "mappings": {"record": "$FULL_PAYLOAD"}},
        ),
        # extract_field emits {"value": ...}; web.brave.search requires
        # "query" — without this link the run dies on a missing-field
        # ValidationError at the search node.
        EdgeDef(
            id="e2",
            source="top_title",
            target="web_search",
            type="default",
            data={"kind": "data", "mappings": {"query": "value"}},
        ),
        # data.stringify_json takes exactly {"value": ...} (extra=forbid), so
        # the search payload is routed as ONE mapped key.
        EdgeDef(
            id="e3",
            source="web_search",
            target="search_text",
            type="default",
            data={"kind": "data", "mappings": {"value": "results"}},
        ),
        # ...and the serialized results become the ranker's prompt.
        EdgeDef(
            id="e3b",
            source="search_text",
            target="rank_urls",
            type="default",
            data={"kind": "data", "mappings": {"prompt": "text"}},
        ),
        # text.regex_extract takes exactly {"text": str} (extra=forbid);
        # the LLM's answer arrives as "final_text" — map it across.
        EdgeDef(
            id="e4",
            source="rank_urls",
            target="parse_urls",
            type="default",
            data={"kind": "data", "mappings": {"text": "final_text"}},
        ),
        # regex_extract emits {"matches": [urls]}; control.map requires
        # "items" — the mapping bridges the two shapes.
        EdgeDef(
            id="e5",
            source="parse_urls",
            target="fanout",
            type="default",
            data={"kind": "data", "mappings": {"items": "matches"}},
        ),
        # Fan-in half 2: gather is triggered BY the workers, one super-step
        # after they run, so the committed "scrapes" channel is visible.
        # NEVER wire fanout → gather: that runs gather in the same step as
        # the workers, where it reads the pre-step snapshot (empty channel).
        EdgeDef(
            id="e6",
            source="scrape_page",
            target="gather_scrapes",
            type="default",
            data={"kind": "control"},
        ),
        # gather emits {"values": [...]} — the exact key
        # ai.util.format_scraped_content reads.
        EdgeDef(
            id="e7",
            source="gather_scrapes",
            target="combine_pages",
            type="default",
            data={"kind": "data", "mappings": {"values": "values"}},
        ),
        EdgeDef(
            id="e7b",
            source="combine_pages",
            target="summarize",
            type="default",
            data={"kind": "data", "mappings": {"prompt": "formatted_text"}},
        ),
        EdgeDef(
            id="e8", source="summarize", target="mix_decoys", type="default", data={"kind": "data"}
        ),
        EdgeDef(
            id="e9",
            source="mix_decoys",
            target="final_answer",
            type="default",
            data={"kind": "data", "mappings": {"prompt": "context_text"}},
        ),
    ]

    return Definition(
        version="1",
        nodes=nodes,
        edges=edges,
        viewport=Viewport(x=0, y=0, zoom=0.7),
        channels=[
            ChannelSpec(
                name="scrapes",
                reducer="append",
                default=[],
                description="Scraped page payloads collected by gather_scrapes.",
            ),
        ],
        entry_nodes=["headlines"],
        metadata={
            "origin": "matrx_graph.examples.self_validating_news",
            "purpose": (
                "Phase 4 self-validating chain. Every stage is required — the "
                "final LLM has no tools, so a correct answer is only possible "
                "if the full scrape → filter → summarize chain produced real "
                "facts in the context."
            ),
            "env_vars_required": [
                "BRAVE_SEARCH_API_KEY_PRO_AI",
                "ANTHROPIC_API_KEY",
            ],
        },
    )
