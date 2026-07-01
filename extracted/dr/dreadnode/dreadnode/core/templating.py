"""Client-side rendering for task instruction templates.

``TaskEnvironment`` returns the task's instruction as a raw mustache-style
template (``{{ var }}`` placeholders). Callers render it themselves with the
env's ``service_urls`` plus their own ``inputs`` — this keeps templating out
of the environments-service surface and lets callers re-render, swap
inputs, or customize the goal.

The helpers here are a client-side port of the logic in
``packages/api/app/tasks/utils.py``. They are intentionally permissive:
unresolved placeholders are left as-is so the caller can see what wasn't
filled in.
"""

import re
import typing as t


def build_template_context_from_service_urls(
    service_urls: dict[str, dict[str, t.Any]] | None,
) -> dict[str, str | int | None]:
    """Build a template context mapping from env service URL metadata.

    The resulting context exposes ``{service}_url``, ``{service}_host``, and
    ``{service}_port`` keys, plus per-port ``{service}_url_{port}`` /
    ``{service}_host_{port}`` / ``{service}_port_{port}`` variants.
    """
    if not service_urls:
        return {}

    context: dict[str, str | int | None] = {}

    def _host_from_url(url: str) -> str:
        if "://" in url:
            return url.split("://", 1)[1]
        return url

    for service, urls_meta in service_urls.items():
        if not isinstance(service, str) or not isinstance(urls_meta, dict):
            continue

        url = urls_meta.get("url")
        host = urls_meta.get("host")
        port = urls_meta.get("port")
        urls = urls_meta.get("urls")

        if isinstance(urls, dict):
            for port_key, port_url in urls.items():
                try:
                    port_num = int(str(port_key))
                except ValueError:
                    continue
                if not isinstance(port_url, str):
                    continue
                context[f"{service}_url_{port_num}"] = port_url
                context[f"{service}_host_{port_num}"] = _host_from_url(port_url)
                context[f"{service}_port_{port_num}"] = str(port_num)

        primary_port: int | None = None
        if isinstance(port, int):
            primary_port = port
        elif isinstance(port, str) and port.isdigit():
            primary_port = int(port)
        elif isinstance(urls, dict):
            for port_key in urls:
                try:
                    primary_port = int(str(port_key))
                except ValueError:
                    continue
                break

        if isinstance(url, str):
            context[f"{service}_url"] = url
        if isinstance(host, str):
            context[f"{service}_host"] = host
        if primary_port is not None:
            context[f"{service}_port"] = str(primary_port)

    return context


def _coerce_input_value(value: t.Any) -> str | int | None:
    if value is None:
        return None
    # bool is a subclass of int in Python — check before the int branch.
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (str, int)):
        return value
    return str(value)


def render_task_instruction(
    template: str | None,
    *,
    service_urls: dict[str, dict[str, t.Any]] | None = None,
    inputs: dict[str, t.Any] | None = None,
) -> str | None:
    """Render a task instruction template.

    Substitutes ``{{ var }}`` placeholders using a context built from the
    environment's ``service_urls`` plus caller-provided ``inputs``. Unknown
    variables are left in place (not raised) so callers can inspect which
    placeholders were not resolved.

    Args:
        template: Raw instruction template (typically ``env.instruction``).
            ``None`` returns ``None``.
        service_urls: Service URL metadata (typically ``env.service_urls``).
        inputs: Caller-provided values for task-specific placeholders.

    Returns:
        The rendered string, or ``None`` if ``template`` was ``None``.
    """
    if not template:
        return template

    context: dict[str, str | int | None] = {}
    context.update(build_template_context_from_service_urls(service_urls))
    if inputs:
        for key, value in inputs.items():
            if not isinstance(key, str):
                continue
            context[key] = _coerce_input_value(value)

    def _replacer(match: "re.Match[str]") -> str:
        key = match.group(1).strip()
        value = context.get(key)
        if value is None:
            return match.group(0)  # leave unresolved placeholders in place
        return str(value)

    return re.sub(r"\{\{\s*(\w+)\s*\}\}", _replacer, template)
