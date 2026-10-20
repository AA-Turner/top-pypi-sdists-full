"""Site icons — each result URL's own icon, for the reader's screen only.

A tool that returns websites (search, research) sets ``ToolResult.site_icons``
to ``{url: icon_url}`` from what its provider reported (Brave's
``meta_url.favicon``). The executor emits the map as ONE ``tool_step`` whose
step is ``SITE_ICONS_STEP`` just before ``tool_completed``; it streams live and
is persisted in ``execution_events``, so the client's cards draw each site's
real icon on both paths. The model's tool result never carries it.
"""

# One string, both repos (``SITE_ICONS_STEP`` in @ai-matrx/chat's readSiteIcons).
SITE_ICONS_STEP = "site_icons"
