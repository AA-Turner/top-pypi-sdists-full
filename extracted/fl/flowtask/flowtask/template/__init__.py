from typing import Optional
import datetime
from pathlib import Path
from navconfig import config
from jinja2 import (
    BaseLoader,
    Environment,
    FileSystemLoader,
    FileSystemBytecodeCache,
    TemplateError,
    TemplateNotFound,
    StrictUndefined
)
from ..utils.json import json_encoder
from ..conf import TEMPLATE_DIR

jinja_config = {
    "enable_async": True,
    "autoescape": True,
    "extensions": [
        "jinja2.ext.i18n",
        "jinja2.ext.loopcontrols",
        "jinja2_time.TimeExtension",
        "jinja2_iso8601.ISO8601Extension",
        "jinja2.ext.do",
        "jinja2_humanize_extension.HumanizeExtension"
    ],
}

string_config = {
    "autoescape": True,
    "extensions": [
        "jinja2.ext.i18n",
        "jinja2.ext.loopcontrols",
        "jinja2_time.TimeExtension",
        "jinja2_iso8601.ISO8601Extension",
        "jinja2.ext.do",
        "jinja2_humanize_extension.HumanizeExtension"
    ],
}

DEFAULT_TEMPLATE_HANDLER = None


def getTemplateHandler(newdir: str = None):
    global DEFAULT_TEMPLATE_HANDLER
    if newdir:
        return TemplateHandler(directory=newdir)
    else:
        if DEFAULT_TEMPLATE_HANDLER is None:
            DEFAULT_TEMPLATE_HANDLER = TemplateHandler(directory=TEMPLATE_DIR)
        return DEFAULT_TEMPLATE_HANDLER


class TemplateHandler:
    """
    TemplateHandler.

    This is a wrapper for the Jinja2 template engine.
    """

    _prefix: str = "dataintegration"

    def __init__(self, directory: Path, **kwargs):
        self.path = directory.resolve()
        if not self.path.exists():
            raise RuntimeError(
                f"Flowtask: template directory {directory} does not exist"
            )
        if "config" in kwargs:
            self.config = {**jinja_config, **kwargs["config"]}
        else:
            self.config = jinja_config
        template_debug = config.getboolean("TEMPLATE_DEBUG", fallback=False)
        if template_debug is True:
            self.config["extensions"].append("jinja2.ext.debug")
        # creating loader:
        templateLoader = FileSystemLoader(searchpath=[str(self.path)])
        # Bytecode Cache that saves to filesystem
        bcache = FileSystemBytecodeCache(str(self.path), "%s.cache")
        # initialize the environment
        try:
            self.env = Environment(
                loader=templateLoader,
                # bytecode_cache=bcache,
                **self.config
            )
            # compiled_path = str(self.path.joinpath('.compiled'))
            # self.env.compile_templates(
            #     target=compiled_path, zip='deflated'
            # )
            self._strparser = Environment(
                loader=BaseLoader,
                # bytecode_cache=bcache,
                undefined=StrictUndefined,
                **string_config
            )
            ## Adding Filters:
            self.env.filters["jsonify"] = json_encoder
            self._strparser.filters["jsonify"] = json_encoder
            self.env.filters["datetime"] = datetime.datetime.fromtimestamp
            self._strparser.filters["datetime"] = datetime.datetime.fromtimestamp
        except Exception as err:
            raise RuntimeError(
                f"DI: Error loading Template Environment: {err!s}"
            ) from err

    def get_template(self, filename: str):
        """
        Get a template from Template Environment using the Filename.
        """
        try:
            return self.env.get_template(str(filename))
        except TemplateNotFound as ex:
            raise FileNotFoundError(f"Template cannot be found: {filename}") from ex

    def from_string(self, content: str, params: dict):
        try:
            template = self._strparser.from_string(content)
            result = template.render(**params)
            return result
        except Exception as err:
            raise RuntimeError(
                f"DI: Error rendering string Template, error: {err}"
            ) from err

    @property
    def environment(self):
        return self.env

    def render(self, filename: str, params):
        result = None
        try:
            template = self.env.get_template(str(filename))
            result = template.render(**params)
            return result
        except Exception as err:
            raise RuntimeError(
                f"DI: Error rendering template: {filename}, error: {err}"
            ) from err

    async def async_render(self, filename: str, params: Optional[dict] = None) -> str:
        """async_render.

        Renders a Jinja2 template using async-await syntax.
        """
        result = None
        if not params:
            params = {}
        try:
            template = self.env.get_template(str(filename))
            result = await template.render_async(**params)
            return result
        except TemplateError as ex:
            raise ValueError(
                f"Template parsing error, template: {filename}: {ex}"
            ) from ex
        except Exception as err:
            raise RuntimeError(
                f"NAV: Error rendering: {filename}, error: {err}"
            ) from err
