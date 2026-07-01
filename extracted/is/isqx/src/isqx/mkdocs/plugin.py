"""A `MkDocs` plugin bundling a default `KaTeX` configuration necessary to
render mathematical expressions in the documentation.

[`isqx.mkdocs.extension.IsqxExtension`][] is responsible for injecting
[cross-referenced details][isqx.details.Details] into the docstrings of
attributes and functions. This module also comes with an optional client-side JS
script `detail-highlight.js` that searches for matching symbols within
[`isqx.details.Detail`][] blocks and highlights them.

!!! note

    You must install `isqx` with the `docs` extra optional dependencies
    to use this module.
"""

from __future__ import annotations

from logging import getLogger
from pathlib import Path
from typing import TYPE_CHECKING, Generator

from mkdocs.config import Config
from mkdocs.config.config_options import ExtraScriptValue, Type
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin
from mkdocs.utils import copy_file
from mkdocstrings import MkdocstringsPlugin

from . import PATH_PLUGIN_ASSETS

if TYPE_CHECKING:
    from mkdocs.config.defaults import MkDocsConfig

logger = getLogger(__name__)


class IsqxPluginConfig(Config):  # type: ignore
    definitions = Type(list, default=[])
    """Modules that contain the definitions, e.g. `isqx.iso80000`, `isqx.aerospace`.

    This is used to provide cross-references within the [`isqx.details.Detail`][]
    blocks.

    Note that `griffe` will **dynamically import** these modules.
    To reduce build time, avoid expensive imports like `torch`."""
    details = Type(list, default=[])
    """Paths to the details mapping, e.g. `isqx.details.iso80000.TIME_AND_SPACE`."""
    details_highlight = Type(bool, default=True)
    """Whether to highlight symbols in the details."""
    load_katex = Type(bool, default=True)
    """Whether to load KaTeX javascript and CSS assets."""


PLUGIN_ASSETS_JS = (PATH_PLUGIN_ASSETS / "js" / "detail-highlight.js",)
KATEX_VERSION = "0.16.25"


class IsqxPlugin(BasePlugin[IsqxPluginConfig]):  # type: ignore
    def on_config(self, config: MkDocsConfig) -> MkDocsConfig:
        plugin = config.plugins.get("mkdocstrings")
        assert isinstance(plugin, MkdocstringsPlugin)
        options = (
            plugin.config.setdefault("handlers", {})
            .setdefault("python", {})
            .setdefault("options", [])
        )
        extensions = options.setdefault("extensions", [])
        extensions.append(
            {
                "isqx.mkdocs.extension:IsqxExtension": {
                    "config": self.config,
                    "objects_out_path": f"{config.site_dir}/assets",
                }
            }
        )

        self.extra_css: list[str] = []
        self.extra_scripts: list[ExtraScriptValue | str] = []
        if self.config.details_highlight:
            self.extra_scripts.append(_mjs("js/cmap.mjs"))
            self.extra_scripts.append(_mjs("js/detail-highlight.mjs"))
            self.extra_css.append("css/detail-highlight.css")
        if self.config.load_katex:
            self.extra_scripts.append(_mjs("js/katex.mjs"))
            self.extra_scripts.extend(katex_js(KATEX_VERSION))
            self.extra_css.extend(katex_css(KATEX_VERSION))
        if self.extra_scripts:
            config.extra_javascript[:0] = self.extra_scripts
        if self.extra_css:
            config.extra_css[:0] = self.extra_css
        return config

    def on_post_build(self, *, config: MkDocsConfig) -> None:
        output_path = Path(config.site_dir)
        for script in self.extra_scripts:
            maybe_copy_asset(script, str(output_path))
        for css in self.extra_css:
            maybe_copy_asset(css, str(output_path))


def katex_js(version: str) -> Generator[ExtraScriptValue, None, None]:
    yield _script(
        f"https://cdn.jsdelivr.net/npm/katex@{version}/dist/katex.min.js"
    )
    yield _script(
        f"https://cdn.jsdelivr.net/npm/katex@{version}/dist/contrib/auto-render.min.js"
    )
    yield _script(
        f"https://cdn.jsdelivr.net/npm/katex@{version}/dist/contrib/copy-tex.min.js"
    )


def _script(path: str) -> ExtraScriptValue:
    s: ExtraScriptValue = ExtraScriptValue(path)
    s.defer = True
    return s


def _mjs(path: str) -> ExtraScriptValue:
    s: ExtraScriptValue = ExtraScriptValue(path)
    s.type = "module"
    s.defer = True
    return s


def katex_css(version: str) -> Generator[str, None, None]:
    yield f"https://cdn.jsdelivr.net/npm/katex@{version}/dist/katex.min.css"


def maybe_copy_asset(asset: ExtraScriptValue | str, output_path: str) -> None:
    path = asset.path if isinstance(asset, ExtraScriptValue) else asset
    if path.startswith("js/") or path.startswith("css/"):
        a = PATH_PLUGIN_ASSETS / path
        copy_file(
            str(a),
            str(Path(output_path) / a.relative_to(PATH_PLUGIN_ASSETS)),
        )
