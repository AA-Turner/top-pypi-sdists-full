"""What a site sees when it looks at the Cloud Browser (CB-013).

The persistent Cloud Browser is a person's browser, driven for them. A site must
see an ordinary desktop Chrome on an ordinary computer — the same one every time
that profile opens. This module owns the pieces of that identity the LAUNCH decides:

* **Binary.** Real Google Chrome when the image ships it (``CHROME_BINARY``);
  Playwright's Chromium-for-testing otherwise (tests, developer machines). Only
  Chrome carries the ``Google Chrome`` client-hint brand and the proprietary
  codecs a real user's browser has; a ``Chromium``-branded UA on Linux is a
  headless-farm tell. The choice is announced in the launch log.
* **Flags.** ``--disable-blink-features=AutomationControlled`` so
  ``navigator.webdriver`` is ``false`` (Playwright already drops
  ``--enable-automation``, but the Blink feature stays on without this flag).
* **Timezone and locale.** Never UTC. A browser whose clock says UTC while its
  address is in a US datacentre is the fingerprint of a server. The run policy may
  name them; when it does not, the worker's environment values apply
  (``BROWSER_WORKER_TIMEZONE`` / ``BROWSER_WORKER_LOCALE``, set in the image).
  When the person's own computer becomes the egress (CB-012) the control plane
  should send that computer's timezone through the policy so the two agree.
* **Graphics identity.** Xvfb has no GPU, so WebGL reports SwiftShader — the
  single best-known "this is a server" string there is. The worker installs one
  init script that answers the two ``WEBGL_debug_renderer_info`` parameters with a
  common desktop GPU instead (defaults below; policy or env override). The patch
  masks its own ``toString`` so the function still reads as native code. Empty
  strings turn the patch off (honest SwiftShader).

The behavioural half (pointer paths, keystroke timing, wheel notches) lives in
``matrx_scraper.ai_browser.humanize`` and is switched by ``LaunchPolicy.humanize_input``.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass

from matrx_scraper.cloud_browser.worker import models as M

# ── environment VALUE names (one value, one name; the image sets them) ──────
TIMEZONE_ENV = "BROWSER_WORKER_TIMEZONE"
LOCALE_ENV = "BROWSER_WORKER_LOCALE"
WEBGL_VENDOR_ENV = "BROWSER_WORKER_WEBGL_VENDOR"
WEBGL_RENDERER_ENV = "BROWSER_WORKER_WEBGL_RENDERER"
CHROME_BINARY_ENV = "BROWSER_WORKER_CHROME_BINARY"

# ── defaults when neither the policy nor the environment says ───────────────
DEFAULT_TIMEZONE = "America/Los_Angeles"
DEFAULT_LOCALE = "en-US"
DEFAULT_WEBGL_VENDOR = "Google Inc. (Intel)"
DEFAULT_WEBGL_RENDERER = "ANGLE (Intel, Mesa Intel(R) UHD Graphics 630 (CFL GT2), OpenGL 4.6)"
DEFAULT_CHROME_BINARY = "/opt/google/chrome/chrome"

# Chromium flags that make the browser stop announcing it is driven.
STEALTH_ARGS: tuple[str, ...] = ("--disable-blink-features=AutomationControlled",)
# Playwright defaults the worker refuses. ``--enable-automation`` turns on the
# automation infobar AND ``navigator.webdriver``.
IGNORED_DEFAULT_ARGS: tuple[str, ...] = ("--enable-automation",)


@dataclass(frozen=True)
class BrowserIdentity:
    timezone_id: str
    locale: str
    webgl_vendor: str
    webgl_renderer: str
    humanize_input: bool
    executable_path: str | None
    binary_kind: str  # "google-chrome" | "playwright-chromium" | "playwright-default"


def _env_or(name: str, default: str) -> str:
    value = os.environ.get(name)
    return default if value is None else value


def resolve_identity(policy: M.LaunchPolicy, *, chromium_fallback: str | None) -> BrowserIdentity:
    """The identity this launch will present. Policy fields win; then the image's
    environment values; then the module defaults. ``chromium_fallback`` is the
    Playwright Chromium binary to use when no Google Chrome is installed."""
    chrome = _env_or(CHROME_BINARY_ENV, DEFAULT_CHROME_BINARY)
    if chrome and os.path.exists(chrome):
        executable, kind = chrome, "google-chrome"
    elif chromium_fallback:
        executable, kind = chromium_fallback, "playwright-chromium"
    else:
        executable, kind = None, "playwright-default"
    return BrowserIdentity(
        timezone_id=policy.timezone_id or _env_or(TIMEZONE_ENV, DEFAULT_TIMEZONE),
        locale=policy.locale or _env_or(LOCALE_ENV, DEFAULT_LOCALE),
        webgl_vendor=(
            policy.webgl_vendor
            if policy.webgl_vendor is not None
            else _env_or(WEBGL_VENDOR_ENV, DEFAULT_WEBGL_VENDOR)
        ),
        webgl_renderer=(
            policy.webgl_renderer
            if policy.webgl_renderer is not None
            else _env_or(WEBGL_RENDERER_ENV, DEFAULT_WEBGL_RENDERER)
        ),
        humanize_input=policy.humanize_input,
        executable_path=executable,
        binary_kind=kind,
    )


# WEBGL_debug_renderer_info constants (the extension object is not needed).
_UNMASKED_VENDOR_WEBGL = 0x9245
_UNMASKED_RENDERER_WEBGL = 0x9246


def webgl_init_script(vendor: str, renderer: str) -> str | None:
    """The init script that answers WebGL's unmasked vendor/renderer with a
    desktop GPU. ``None`` when either string is empty (patch off)."""
    if not vendor or not renderer:
        return None
    v, r = json.dumps(vendor), json.dumps(renderer)
    return f"""(() => {{
  const VENDOR = {v};
  const RENDERER = {r};
  const masked = new WeakMap();
  const nativeToString = Function.prototype.toString;
  const maskedToString = function toString() {{
    if (masked.has(this)) return masked.get(this);
    return nativeToString.call(this);
  }};
  masked.set(maskedToString, 'function toString() {{ [native code] }}');
  Object.defineProperty(Function.prototype, 'toString', {{
    value: maskedToString, writable: true, configurable: true, enumerable: false,
  }});
  const patch = (proto) => {{
    if (!proto || typeof proto.getParameter !== 'function') return;
    const original = proto.getParameter;
    const getParameter = function getParameter(parameter) {{
      if (parameter === {_UNMASKED_VENDOR_WEBGL}) return VENDOR;
      if (parameter === {_UNMASKED_RENDERER_WEBGL}) return RENDERER;
      return original.call(this, parameter);
    }};
    masked.set(getParameter, 'function getParameter() {{ [native code] }}');
    Object.defineProperty(proto, 'getParameter', {{
      value: getParameter, writable: true, configurable: true, enumerable: false,
    }});
  }};
  patch(self.WebGLRenderingContext && self.WebGLRenderingContext.prototype);
  patch(self.WebGL2RenderingContext && self.WebGL2RenderingContext.prototype);
}})();"""
