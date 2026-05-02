
from typing import List, Optional, Union, Callable
import logging
import asyncio
import pandas as pd
from pathlib import Path
from weasyprint import HTML, CSS
from ..exceptions import ComponentError, ConfigError, FileNotFound
from .flow import FlowComponent
from ..interfaces import TemplateSupport
from ..utils import SafeDict


logging.getLogger("weasyprint").setLevel(logging.ERROR)
logging.getLogger("fontTools.ttLib.ttFont").setLevel(logging.ERROR)
logging.getLogger("fontTools.subset.timer").setLevel(logging.ERROR)
logging.getLogger("fontTools.subset").setLevel(logging.ERROR)


class PDFGenerator(TemplateSupport, FlowComponent):
    """
    Generates a PDF document from a DataFrame.

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          PDFGenerator:
          # attributes here
        ```
    """
    _version = "1.0.0"
    use_template: bool = True

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        """Init Method."""
        self.template: str = kwargs.pop("template", None)
        self.config: dict = kwargs.pop("config", {})
        self.output_file: str = kwargs.pop("output_file", "output.pdf")
        self.directory: str = kwargs.pop("directory", ".")
        self.default_stylesheets = kwargs.pop("default_stylesheets", ["css/base.css"])
        template_dir = kwargs.get('template_dir', None)
        self.templates_dir = Path(template_dir) if template_dir else Path.cwd() / "templates"
        super().__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs) -> bool:
        """
        Verify if the component is ready to run.
        """
        if self.previous:
            self.data = self.input
        if not isinstance(self.data, pd.DataFrame):
            raise ComponentError("Data must be a pandas DataFrame.")
        if isinstance(self.directory, str):
            self.directory = Path(self.directory)
        if self.directory.exists() and not self.directory.is_dir():
            raise ConfigError(
                f"Path {self.directory!s} is not a valid directory."
            )
        if not self.directory.exists():
            self.directory.mkdir(parents=True, exist_ok=True)
        if not self.template:
            raise ConfigError("Template must be specified.")
        if not self.use_template:
            raise ConfigError("PDFGenerator requires use_template to be True.")
        if not self._templateparser:
            raise ConfigError("Template parser is not initialized.")
        return True

    def _load_stylesheets(self, stylesheets: Optional[List[str]]) -> List[CSS]:
        """Load CSS stylesheets for PDF generation."""
        css_objects = []

        # Use provided stylesheets or defaults
        css_files = stylesheets or self.default_stylesheets
        for css_file in css_files:
            try:
                css_path = self.templates_dir / 'css' / css_file
                if css_path.exists():
                    css_objects.append(CSS(filename=str(css_path)))
                    self.logger.debug(f"Loaded stylesheet: {css_file}")
                else:
                    self.logger.warning(f"Stylesheet not found: {css_path}")
            except Exception as e:
                self.logger.error(f"Error loading stylesheet {css_file}: {e}")

        # Add base CSS if no stylesheets were loaded
        if not css_objects:
            try:
                base_css_path = self.templates_dir / "css" / "base.css"
                if base_css_path.exists():
                    css_objects.append(CSS(filename=str(base_css_path)))
                    self.logger.info("Added base.css as fallback stylesheet")
            except Exception as e:
                self.logger.error(f"Error loading base stylesheet: {e}")

        return css_objects

    async def close(self):
        """Close the component."""
        pass

    async def run(self):
        """ Run the PDF generation process.
        """
        try:
            filenames = []
            # iterate over the DataFrame and generate PDF:
            for i, row in self.data.iterrows():
                # Prepare the context for the template
                data = row.to_dict()
                context = SafeDict(**data)
                context["row"] = data
                if self.use_template:
                    template = self._templateparser.get_template(self.template)
                    rendered_content = await template.render_async(context)
                else:
                    rendered_content = str(context)
                print(f"Generated content for row {i}: {rendered_content}")
                # Then, Generate the PDF using WeasyPrint:
                html = HTML(string=rendered_content)
                # Load stylesheets
                css_objects = self._load_stylesheets(self.config.get("css", ""))
                filename = self.output_file.format_map(SafeDict(**data))
                pdf_file_path = self.directory / f"{filename}_{i}.pdf"
                html.write_pdf(
                    pdf_file_path,
                    stylesheets=css_objects,
                    presentational_hints=True  # This helps with table rendering
                )
                print(f"PDF generated at {pdf_file_path}")
                filenames.append(pdf_file_path)
            return filenames
        except Exception as e:
            raise ComponentError(f"Error generating PDF: {e}")
