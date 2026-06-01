"""Per-version ReDoc UI route registration."""

from html import escape

from fastapi import FastAPI
from fastapi.responses import HTMLResponse


def _register_redoc_routes(
    app: FastAPI,
    *,
    version_list: list[str],
    default_version: str | None = None,
) -> None:
    """Register per-version ReDoc UI at ``/redoc`` with a version query param.

    Usage::

        /redoc                        → latest (or default) version
        /redoc?version=2025-06-20     → specific version

    Points to existing ``/openapi/{version}.json`` routes registered by
    :func:`_docs._register_openapi_json_routes`.
    """

    _SECURITY_HEADERS = {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
    }

    def _build_redoc_html(version: str, versions: list[str]) -> str:
        title = escape(f"ReDoc - {version}")
        openapi_url = f"/openapi/{version}.json"
        options = "\n".join(
            f'        <option value="{v}"{" selected" if v == version else ""}>{escape(v)}</option>'
            for v in versions
        )
        return f"""<!DOCTYPE html>
<html><head>
<title>{title}</title>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<link href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700"
      rel="stylesheet">
<style>
  body {{ margin: 0; padding: 0; }}
  .version-bar {{
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 8px 16px;
    background: #32329f;
    color: #fff;
    font-family: Montserrat, sans-serif;
    font-size: 14px;
  }}
  .version-bar select {{
    padding: 4px 8px;
    border-radius: 4px;
    border: 1px solid #5757c0;
    background: #fff;
    font-size: 14px;
    cursor: pointer;
  }}
  .version-bar a {{
    color: #ccc;
    text-decoration: none;
    margin-left: auto;
    font-size: 13px;
  }}
  .version-bar a:hover {{ color: #fff; }}
</style>
</head><body>
<div class="version-bar">
  <label for="api-version"><strong>API Version:</strong></label>
  <select id="api-version" onchange="switchVersion(this.value)">
{options}
  </select>
  <a href="/swagger-ui/index.html">← Swagger UI</a>
</div>
<redoc spec-url="{openapi_url}" id="redoc-container"></redoc>
<script src="https://cdn.redoc.ly/redoc/latest/bundles/redoc.standalone.js"></script>
<script>
function switchVersion(v) {{
  const url = new URL(window.location);
  url.searchParams.set('version', v);
  window.location.href = url.toString();
}}
</script>
</body></html>"""

    @app.get("/redoc", include_in_schema=False)
    async def redoc_ui(version: str | None = None) -> HTMLResponse:
        resolved = version or default_version or (version_list[-1] if version_list else "latest")
        return HTMLResponse(
            _build_redoc_html(resolved.lower(), version_list),
            headers=_SECURITY_HEADERS,
        )
