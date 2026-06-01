"""File Upload Examples — built-in Swagger UI plugin."""

from importlib.resources import files

from .._base import SwaggerPluginContribution
from ._body_factory import file_upload_body, unwrap_json_schema
from ._schema_patcher import patch_file_upload_examples

__all__ = [
    "FileUploadExamplesPlugin",
    "file_upload_body",
    "unwrap_json_schema",
]

_PACKAGE = "csrd.versioning.extensions.swagger_ui.file_upload"


class FileUploadExamplesPlugin:
    """Built-in plugin that adds file upload example dropdowns to Swagger UI."""

    name = "file_upload_examples"

    def __init__(self) -> None:
        pkg = files(_PACKAGE)
        self._js = pkg.joinpath("file_upload_plugin.js").read_text(encoding="utf-8")
        css_path = pkg.joinpath("file_upload_plugin.css")
        self._css = css_path.read_text(encoding="utf-8")

    def contribute(self) -> SwaggerPluginContribution:
        return SwaggerPluginContribution(
            extra_css=self._css,
            extra_js=self._js,
            bundle_plugins=("FileUploadExamplesPlugin",),
            schema_patcher=patch_file_upload_examples,
        )
