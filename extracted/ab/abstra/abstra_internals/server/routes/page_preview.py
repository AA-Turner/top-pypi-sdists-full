from typing import Optional


def _escape_attr(value: str) -> str:
    return value.replace("&", "&amp;").replace('"', "&quot;")


_ABSTRA_BRIDGE_SHIM = """<script>
(function() {
  window.abstra = window.abstra || {};
  window.abstra.login = function() {};
  window.abstra.logout = function() {};
  window.abstra.logged = function() {
    return !!document.querySelector('meta[name="abstra-auth-token"]');
  };
})();
</script>"""


def build_standalone_preview_html(
    body: str,
    *,
    auth_token: Optional[str],
    endpoint: Optional[str],
    execution_id: Optional[str],
) -> str:
    """Prepend the preview scaffolding the frontend normally injects client-side
    (PageStageView.vue) so run_page's headless, direct-navigation render behaves
    like a logged-in player preview: metas drive the generated function-call
    fetch (sdk_pages._build_js_fetch) and window.abstra.logged() (abstraBridge.ts).

    Pure: returns a new string; never mutates `body`. Scoped to the editor
    /_editor/api/pages/<id>/run route — NOT applied on the player /_page path.
    """
    parts = []
    if endpoint:
        parts.append(
            f'<meta name="abstra-page-endpoint" content="{_escape_attr(endpoint)}">'
        )
    if auth_token:
        parts.append(f'<meta name="abstra-auth-token" content="{auth_token}">')
    if execution_id:
        parts.append(f'<meta name="abstra-execution-id" content="{execution_id}">')
    parts.append(_ABSTRA_BRIDGE_SHIM)
    parts.append(body)
    return "\n".join(parts)
