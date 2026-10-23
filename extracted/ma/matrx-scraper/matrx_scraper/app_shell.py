"""The ONE definition of a JavaScript app shell — a page whose content is drawn after it loads.

Two readers ask the same question and must never answer it from two marker lists:

* ``read_judge`` — "did this read fail?" (a short page plus an app-shell marker);
* ``seo_audit`` — "is there anything here to audit, or did the crawl see an empty frame?"
  (the ``is_js_shell`` page fact that turns every content check ``n_a`` and raises
  ``content_needs_rendering`` instead).

The markers live here; both import them.

The audit's shell test is OpenSEO's (``page-analyzer.ts`` ``javascriptShell``): an app root
element AND an executable script, with fewer than ``JS_SHELL_WORD_LIMIT_DEFAULT`` words, no headings,
no links and no images. Every one of those must hold: a small real page with three sentences
and a menu is a small page, never a shell.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

#: Element ids the major frameworks mount into (CRA/Vite ``root``, Vue ``app``,
#: Next.js pages router ``__next``, Nuxt ``__nuxt``, Quasar ``q-app``, Gatsby ``___gatsby``).
APP_ROOT_IDS: tuple[str, ...] = ("root", "app", "__next", "__nuxt", "q-app", "___gatsby")
#: Angular's root element.
APP_ROOT_TAG = "app-root"
#: Frameworks that mount into ``<body>`` itself, recognised by a body marker:
#: SvelteKit (``data-sveltekit-preload-data``), Ember (``class="ember-application"``).
APP_BODY_ATTRIBUTES: tuple[str, ...] = ("data-sveltekit-preload-data",)
APP_BODY_CLASSES: tuple[str, ...] = ("ember-application",)
#: Boot scripts of frameworks that draw onto an empty body (Flutter web).
APP_SCRIPT_SRC_MARKERS: tuple[str, ...] = ("flutter_bootstrap.js", "flutter.js", "main.dart.js")
#: Inline boot-script text of an empty-body app (SvelteKit's SPA fallback).
APP_SCRIPT_TEXT_MARKERS: tuple[str, ...] = ("__sveltekit", "_flutter.loader")

#: Raw-HTML markers of an EMPTY mount point (what ``read_judge`` scans for in a read's HTML).
SHELL_HTML_MARKERS: tuple[str, ...] = (
    '<div id="root"></div>',
    "<div id='root'></div>",
    '<div id="app"></div>',
    '<div id="__next"></div>',
    f"<{APP_ROOT_TAG}",
    '<div id="__nuxt"></div>',
    '<div id="q-app"></div>',
    '<div id="___gatsby"></div>',
)

#: Visible-text markers of a page that says it needs JavaScript (the ``<noscript>`` line).
SHELL_TEXT_MARKERS: tuple[str, ...] = (
    "enable javascript",
    "javascript is required",
    "javascript is disabled",
    "requires javascript",
    "turn on javascript",
    "please enable js",
    "you need to enable javascript",
    "this app works best with javascript",
)

#: ``<script type>`` values a browser executes. JSON-LD, templates and JSON data blocks are not.
EXECUTABLE_SCRIPT_TYPES = frozenset(
    {
        "",
        "module",
        "text/javascript",
        "application/javascript",
        "text/ecmascript",
        "application/ecmascript",
        # In-browser Babel (CRA prototypes, CodePen-style apps) runs these too.
        "text/babel",
    }
)

#: KNOB MIRROR: knowledge.scraper.audit.js_shell_word_limit = 20 — a page with FEWER words than
#: this (plus the other shell signals) is an app shell. OpenSEO's ``wordCount < 20``.
JS_SHELL_WORD_LIMIT_DEFAULT = 20
JS_SHELL_WORD_LIMIT_KNOB = "audit.js_shell_word_limit"

#: KNOB MIRROR: knowledge.scraper.audit.js_shell_root_text_words = 3 — words of
#: server-rendered text INSIDE the app root a shell may still carry (a "Loading…"
#: placeholder). More than this is a real server-rendered page, never a shell.
JS_SHELL_ROOT_TEXT_WORDS_DEFAULT = 3
JS_SHELL_ROOT_TEXT_WORDS_KNOB = "audit.js_shell_root_text_words"
#: Root text that is a placeholder, whatever its length (a loading line, a
#: "please enable JavaScript" line) — counted as 0 server-rendered words.
_PLACEHOLDER_TEXT_MARKERS: tuple[str, ...] = ("loading",)

#: Elements whose text a reader never sees — excluded from every word count
#: (`seo_audit._audit_tree` drops them before counting).
NON_VISIBLE_TAGS: tuple[str, ...] = ("script", "style", "template")


@dataclass(frozen=True)
class AppShellSignals:
    """The two markup facts of a shell, read from the fetched HTML at capture time."""

    #: An element with an app-root id (``APP_ROOT_IDS``) or an ``<app-root>`` element.
    app_root: bool
    #: At least one ``<script>`` a browser would run (``EXECUTABLE_SCRIPT_TYPES``).
    executable_script: bool
    #: Words of body text OUTSIDE ``<script>`` / ``<style>`` / ``<template>``. The page's
    #: ``word_count`` counts script text too, so a Next.js shell's ``__NEXT_DATA__`` JSON
    #: would read as prose. Measured only when both markup signals hold (``None`` otherwise).
    visible_words: int | None = None
    #: Words of SERVER-RENDERED text inside the app root (``<noscript>`` and
    #: script text excluded; a loading / enable-JavaScript placeholder counts 0).
    #: Real text here is evidence against a shell. Measured with ``visible_words``.
    root_text_words: int | None = None
    #: A bot wall or interstitial (the fetcher's own challenge classifier,
    #: `scraper.detect_challenge_reasons`) wrapped in app-shell markup. Never a shell:
    #: it is a blocked read. Set by `seo_audit`, which owns the classifier call.
    bot_wall: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "app_root": self.app_root,
            "executable_script": self.executable_script,
            "visible_words": self.visible_words,
            "root_text_words": self.root_text_words,
            "bot_wall": self.bot_wall,
        }


def _words(node: Any, *, skip: tuple[str, ...]) -> int:
    """Words of ``node``'s text, minus the text of its ``skip`` descendants."""
    total = len((node.text(deep=True, separator=" ") or "").split())
    hidden = sum(
        len((child.text(deep=True, separator=" ") or "").split()) for child in node.css(", ".join(skip))
    )
    return max(0, total - hidden)


def _server_rendered_words(root: Any) -> int:
    """Words of real text inside an app root; a placeholder line counts 0."""
    text = " ".join(
        (root.text(deep=True, separator=" ") or "").split()
    ).lower()
    if not text:
        return 0
    if any(marker in text for marker in SHELL_TEXT_MARKERS + _PLACEHOLDER_TEXT_MARKERS):
        return 0
    return _words(root, skip=NON_VISIBLE_TAGS + ("noscript",))


def app_shell_signals(tree: Any) -> AppShellSignals:
    """Read the shell markup facts from a parsed selectolax ``HTMLParser`` tree."""
    body = tree.body
    roots = [node for node in (tree.css_first(APP_ROOT_TAG),) if node is not None]
    roots += [
        node
        for root_id in APP_ROOT_IDS
        if (node := tree.css_first(f'[id="{root_id}"]')) is not None
    ]
    scripts = tree.css("script")
    body_app = body is not None and (
        any(attr in (body.attributes or {}) for attr in APP_BODY_ATTRIBUTES)
        or any(cls in (body.attributes.get("class") or "").split() for cls in APP_BODY_CLASSES)
        or any(
            marker in (node.attributes.get("src") or "") for node in scripts for marker in APP_SCRIPT_SRC_MARKERS
        )
        or any(marker in (node.text() or "") for node in scripts for marker in APP_SCRIPT_TEXT_MARKERS)
    )
    app_root = bool(roots) or bool(body_app)
    executable_script = any(
        (node.attributes.get("type") or "").strip().lower() in EXECUTABLE_SCRIPT_TYPES
        for node in scripts
    )
    visible_words: int | None = None
    root_text_words: int | None = None
    if app_root and executable_script and body is not None:
        visible_words = _words(body, skip=NON_VISIBLE_TAGS)
        # A body-mounted app's root IS the body.
        root_text_words = (
            sum(_server_rendered_words(node) for node in roots) if roots else _server_rendered_words(body)
        )
    return AppShellSignals(
        app_root=app_root,
        executable_script=executable_script,
        visible_words=visible_words,
        root_text_words=root_text_words,
    )


def is_js_shell(
    *,
    app_root: bool | None,
    executable_script: bool | None,
    word_count: int | None,
    heading_count: int | None,
    link_count: int | None,
    image_count: int | None,
    word_limit: int = JS_SHELL_WORD_LIMIT_DEFAULT,
    root_text_words: int | None = None,
    root_text_limit: int = JS_SHELL_ROOT_TEXT_WORDS_DEFAULT,
    bot_wall: bool | None = None,
) -> bool | None:
    """Whether a page is an unrendered app shell; ``None`` when a signal was never captured.

    ``root_text_words`` (server-rendered words inside the app root) is evidence
    AGAINST a shell above ``root_text_limit``; ``None`` (a snapshot older than that
    measurement) leaves the other signals to decide.
    """
    if bot_wall:
        return False  # a wall in app-shell markup is a blocked read, never a shell
    signals = (app_root, executable_script, word_count, heading_count, link_count, image_count)
    if any(signal is None for signal in signals):
        return None
    return bool(
        app_root
        and executable_script
        and int(word_count or 0) < word_limit
        and heading_count == 0
        and link_count == 0
        and image_count == 0
        and (root_text_words is None or root_text_words <= root_text_limit)
    )


__all__ = [
    "APP_ROOT_IDS",
    "APP_ROOT_TAG",
    "AppShellSignals",
    "EXECUTABLE_SCRIPT_TYPES",
    "JS_SHELL_WORD_LIMIT_DEFAULT",
    "JS_SHELL_WORD_LIMIT_KNOB",
    "JS_SHELL_ROOT_TEXT_WORDS_DEFAULT",
    "JS_SHELL_ROOT_TEXT_WORDS_KNOB",
    "NON_VISIBLE_TAGS",
    "SHELL_HTML_MARKERS",
    "SHELL_TEXT_MARKERS",
    "app_shell_signals",
    "is_js_shell",
]
