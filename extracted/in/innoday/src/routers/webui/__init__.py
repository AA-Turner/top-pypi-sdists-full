"""The signed-in browser surface at ``/ui`` -- sign-in, dashboard, CLI tokens.

Server-rendered, in-process, no JavaScript framework and no build step. It reads
the database through the same models the API routers use and **never calls
``/api/v1``**: a browser cannot send the ``X-Team-Secret`` header
``TeamSecretMiddleware`` requires, and handing that shared secret to page
JavaScript would leak it to every visitor.

Temporary by design -- a real UI application will replace it -- so the bar here is
"correct, branded and cheap to delete", not "extensible".

| Module | Owns |
|---|---|
| ``routes`` | The routes, and org/reserved-segment resolution |
| ``session`` | The HttpOnly session cookie, backed by a minted ``CLIToken`` |
| ``data`` | Read queries, plus the derived "last synced" and "next launch" |
| ``render`` | HTML: the app shell, the sign-in card, the dashboard |
| ``workflow`` | HTML: the workflow launcher -- the page ``GET /ui`` opens |
| ``icons`` | Pixel-block layer glyphs and the PixelFuel wordmark |

``workflow`` is a sibling of ``render`` rather than more of it. ``render`` was
already 4,195 lines of markup, CSS and script in one string-per-page module, and
the launcher is the one page here with real client-side behaviour -- a step
engine driven by a JSON spec. Keeping it separate is also what makes it liftable
into the replacement UI as a single file instead of a rewrite.
"""

from src.routers.webui.routes import router

__all__ = ["router"]
