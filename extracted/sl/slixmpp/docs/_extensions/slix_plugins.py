"""
Sphinx extension to auto-discover and document slixmpp plugins.
"""

import importlib
from pathlib import Path

from sphinx.application import Config, Sphinx
from sphinx.util import logging

log = logging.getLogger(__name__)


DIR = Path(__file__).parent
INDEX_TEMPLATE = (DIR / "tpl_index.rst").read_text()
PLUGIN_TEMPLATE = (DIR / "tpl_plugin.rst").read_text()
STANZA_TEMPLATE = (DIR / "tpl_plugin_stanza.rst").read_text()


def discover_plugins(plugin_dir: Path) -> list[str]:
    return sorted(
        [path.stem for path in plugin_dir.glob("*") if path.name.startswith("xep_")]
    )


def generate_plugin_docs(app: Sphinx, config: Config) -> None:
    source_dir = Path(app.srcdir)
    plugin_doc_dir = source_dir / "api" / "plugins"
    plugin_doc_dir.mkdir(parents=True, exist_ok=True)

    slixmpp_plugin_dir = Path(app.config.slixmpp_plugin_path)
    plugins = discover_plugins(slixmpp_plugin_dir)

    for plugin_name in plugins:
        plugin_file = plugin_doc_dir / f"{plugin_name}.rst"
        if plugin_file.exists():
            continue
        content = _generate_plugin_content(plugin_name)
        plugin_file.write_text(content)
        log.info(f"Generated {plugin_file}")

    update_index_rst(plugin_doc_dir, plugins)


def _generate_plugin_content(plugin_name: str) -> str:
    xep_num = plugin_name.removeprefix("xep_")
    title = plugin_name.upper().replace("_", "-")
    module = importlib.import_module(f"slixmpp.plugins.{plugin_name}")
    cls = getattr(module, plugin_name.upper(), None)
    if cls is not None:
        title = cls.description
    title = title + "\n" + len(title) * "="

    base = PLUGIN_TEMPLATE.format(title=title, xep_num=xep_num)

    try:
        module = importlib.import_module(f"slixmpp.plugins.{plugin_name}.stanza")
    except ImportError:
        return base
    else:
        return base + "\n" + STANZA_TEMPLATE.format(xep_num=xep_num)


def update_index_rst(plugin_doc_dir: Path, plugins: list[str]) -> None:
    index_file = plugin_doc_dir / "index.rst"
    content = INDEX_TEMPLATE.format(plugins="\n".join(" " * 4 + x for x in plugins))
    index_file.write_text(content)
    log.info(f"Updated {index_file} with {len(plugins)} plugins")


def setup(app: Sphinx) -> dict[str, object]:
    app.add_config_value(
        "slixmpp_plugin_path", default=None, rebuild="env", types=[str]
    )

    app.connect("config-inited", generate_plugin_docs)

    return {
        "version": "1.0",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
