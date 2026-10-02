"""Media injection — replay of an authored media-injection step.

Cloud-only: the LambdaTest hub intercepts the `lambda-image-injection=<id>` /
`lambda-video-injection=<id>` script body and swaps the camera feed (V2 parity:
auteur-utils appium_uiActions.inject_media). There is no local equivalent, and
skipping would silently change test behavior — so off-cloud this raises.
The session must carry enableImageInjection / enableVideoInjection caps
(ride the test-config entry; see _test_config._LT_KEYS)."""

import logging

from testmu_appium import _config
from testmu_appium._vars import var

_log = logging.getLogger("testmu_appium")

_HOOKS = {
    "image": "lambda-image-injection",
    "video": "lambda-video-injection",
}


def inject_media(driver, *, kind: str, media_id: str, description: str = "") -> None:
    suffix = f" — {description}" if description else ""
    if kind not in _HOOKS:
        raise ValueError(
            f"inject_media kind {kind!r} not supported — expected one of "
            f"{sorted(_HOOKS)}"
        )
    resolved_id = str(var(media_id))
    if not resolved_id:
        raise ValueError("inject_media: media_id resolved empty")
    if _config.run_target != "cloud":
        raise RuntimeError(
            "inject_media runs through the LambdaTest media-injection hook and "
            "needs run_target='cloud'"
        )
    driver.execute_script(f"{_HOOKS[kind]}={resolved_id}")
    _log.info("inject_media: %s %s%s", kind, resolved_id, suffix)
