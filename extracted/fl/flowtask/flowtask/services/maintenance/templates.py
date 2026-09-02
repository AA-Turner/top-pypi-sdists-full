"""Jinja2 HTML templates for the status and changelog pages.

Templates are kept inline (as module-level strings) so the package renders
correctly regardless of how it is installed (wheel, editable, zipapp) without
relying on package-data discovery.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from jinja2 import Environment, select_autoescape

if TYPE_CHECKING:  # pragma: no cover - typing only
    from .models import ChangelogEntry, StatusReport

_ENV = Environment(autoescape=select_autoescape(["html", "xml"]))

_BASE_CSS = """
  :root { color-scheme: light dark; }
  * { box-sizing: border-box; }
  body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
         Helvetica, Arial, sans-serif; margin: 0; padding: 0;
         background: #f6f8fa; color: #1f2328; }
  .wrap { max-width: 860px; margin: 0 auto; padding: 32px 20px 64px; }
  h1 { font-size: 1.8rem; margin: 0 0 4px; }
  .muted { color: #656d76; font-size: .9rem; }
  .card { background: #fff; border: 1px solid #d0d7de; border-radius: 10px;
          padding: 20px; margin: 18px 0; }
  .banner { border-radius: 10px; padding: 16px 20px; color: #fff; font-weight: 600; }
  .operational { background: #1a7f37; }
  .degraded { background: #9a6700; }
  .down { background: #cf222e; }
  .maintenance { background: #0969da; }
  ul { margin: 8px 0; padding-left: 20px; }
  li { margin: 4px 0; }
  .check { display: flex; align-items: center; justify-content: space-between;
           padding: 10px 0; border-bottom: 1px solid #eaeef2; }
  .check:last-child { border-bottom: none; }
  .pill { font-size: .78rem; font-weight: 600; padding: 3px 10px; border-radius: 999px; }
  .ok { background: #dafbe1; color: #1a7f37; }
  .bad { background: #ffebe9; color: #cf222e; }
  .win { border-left: 4px solid #0969da; padding: 8px 14px; margin: 10px 0;
         background: #f0f6ff; border-radius: 4px; }
  .sec { font-weight: 600; margin: 14px 0 4px; }
  .ver { display: flex; align-items: baseline; gap: 12px; }
  .ver h2 { margin: 0; font-size: 1.25rem; }
  a { color: #0969da; }
"""

_STATUS_TEMPLATE = _ENV.from_string(
    """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{ report.service }} — Status</title>
  <style>""" + _BASE_CSS + """</style>
</head>
<body>
  <div class="wrap">
    <h1>{{ report.service }} Status</h1>
    <p class="muted">
      version {{ report.version }} · {{ report.environment }} ·
      generated {{ report.generated_at.strftime('%Y-%m-%d %H:%M:%S UTC') }}
      {% if report.uptime_seconds is not none %}· uptime {{ uptime }}{% endif %}
    </p>

    <div class="banner {{ report.overall.value }}">
      {% if report.overall.value == 'operational' %}All systems operational
      {% elif report.overall.value == 'maintenance' %}Under maintenance
      {% elif report.overall.value == 'down' %}Major outage
      {% else %}Partial degradation{% endif %}
    </div>

    <div class="card">
      {% for check in report.checks %}
      <div class="check">
        <span>{{ check.name }}{% if check.detail %} <span class="muted">— {{ check.detail }}</span>{% endif %}</span>
        <span class="pill {{ 'ok' if check.ok else 'bad' }}">{{ 'UP' if check.ok else 'DOWN' }}</span>
      </div>
      {% endfor %}
    </div>

    <div class="card">
      <div class="sec">Scheduled Maintenance</div>
      {% if report.upcoming_windows %}
        {% for w in report.upcoming_windows %}
        <div class="win">
          <strong>{{ w.title }}</strong><br>
          <span class="muted">
            {{ w.day.strftime('%A, %B %d, %Y') }} ·
            {{ w.start_time.strftime('%H:%M') }}–{{ w.end_time.strftime('%H:%M') }}
          </span>
          {% if w.description %}<div>{{ w.description }}</div>{% endif %}
        </div>
        {% endfor %}
      {% else %}
        <p class="muted">No maintenance windows scheduled.</p>
      {% endif %}
    </div>
  </div>
</body>
</html>"""
)

_CHANGELOG_TEMPLATE = _ENV.from_string(
    """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{ title }}</title>
  <style>""" + _BASE_CSS + """</style>
</head>
<body>
  <div class="wrap">
    <h1>{{ title }}</h1>
    <p class="muted">Latest changes and improvements.</p>
    {% if not entries %}
      <div class="card"><p class="muted">No changelog entries available yet.</p></div>
    {% endif %}
    {% for entry in entries %}
    <div class="card">
      <div class="ver">
        <h2>
          {% if entry.url %}<a href="{{ entry.url }}">{{ entry.version }}</a>
          {% else %}{{ entry.version }}{% endif %}
        </h2>
        {% if entry.released_on %}<span class="muted">{{ entry.released_on.strftime('%B %d, %Y') }}</span>{% endif %}
      </div>
      {% if entry.title and entry.title != entry.version %}<p class="muted">{{ entry.title }}</p>{% endif %}
      {% for section, items in entry.sections.items() %}
        {% if items %}
        <div class="sec">{{ section }}</div>
        <ul>{% for item in items %}<li>{{ item }}</li>{% endfor %}</ul>
        {% endif %}
      {% endfor %}
    </div>
    {% endfor %}
  </div>
</body>
</html>"""
)


def _format_uptime(seconds: int) -> str:
    """Render a seconds count as ``Xd Yh Zm``."""
    days, rem = divmod(seconds, 86400)
    hours, rem = divmod(rem, 3600)
    minutes = rem // 60
    parts = []
    if days:
        parts.append(f"{days}d")
    if hours:
        parts.append(f"{hours}h")
    parts.append(f"{minutes}m")
    return " ".join(parts)


def render_status(report: "StatusReport") -> str:
    """Render a :class:`StatusReport` to the status HTML page."""
    uptime = (
        _format_uptime(report.uptime_seconds)
        if report.uptime_seconds is not None
        else ""
    )
    return _STATUS_TEMPLATE.render(report=report, uptime=uptime)


def render_changelog(title: str, entries: "list[ChangelogEntry]") -> str:
    """Render changelog ``entries`` to the "What's New" HTML page."""
    return _CHANGELOG_TEMPLATE.render(title=title, entries=entries)
