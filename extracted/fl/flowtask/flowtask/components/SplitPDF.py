import asyncio
from pathlib import Path
from typing import Dict, List, Union, Tuple
from collections.abc import Callable
import fitz  # PyMuPDF

from .flow import FlowComponent
from ..exceptions import ComponentError, DataNotFound, FileNotFound


class SplitPDF(FlowComponent):
    """
    SplitPDF

    **Overview**

        Split PDF files into multiple files based on page ranges using PyMuPDF (fitz).
        Each PDF is split according to a dictionary mapping filename prefixes
        to page ranges. PyMuPDF provides fast and reliable PDF processing.

    **Properties**

       :widths: auto

    | files        |   No*    | List of PDF file paths to process. If not provided,          |
    |              |          | uses output from previous component.                          |
    | split_pattern|   Yes    | Can be either:                                                |
    |              |          | 1) Simple dict: {"contract": [0, 10], "w9": [11, 12]}       |
    |              |          | 2) Nested dict with filename patterns:                        |
    |              |          |    {"HVAC": {"sow": [0, 9], "w9": [10, 15]},                 |
    |              |          |     "ELECTRICAL": {"contract": [0, 5]}}                       |
    |              |          | Page ranges are inclusive [start, end] and zero-based.       |
    | directory    |   Yes    | Directory path (str or Path) where split files will be saved. |
    | overwrite    |   No     | Whether to overwrite existing files (default: True).          |
    | default_pattern | No    | Pattern name to use if filename doesn't match any pattern.   |
    |              |          | Only applies when using nested split_pattern.                 |
    | case_sensitive| No      | Whether filename matching is case-sensitive (default: False). |

    *Either 'files' must be provided or component must follow another component
     that outputs a list of files.

    **Example: Simple Split Pattern**


    **Example: Conditional Split Based on Filename**


    **Example with Previous Component**

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          SplitPDF:
          files:
          - /path/to/document.pdf
          split_pattern:
          contract: [0, 10]
          w9: [11, 12]
          addendum: [13, 15]
          directory: /output/split_pdfs
          overwrite: true
        ```
    """
    _version = "1.0.0"

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        """Initialize the SplitPDF component."""
        self.files: Union[List[str], List[Path], None] = kwargs.pop('files', None)
        self.split_pattern: Dict[str, Union[List[int], Dict[str, List[int]]]] = kwargs.pop('split_pattern', {})
        self.directory: Union[str, Path] = kwargs.pop('directory', None)
        self.overwrite: bool = kwargs.pop('overwrite', True)
        self.default_pattern: str = kwargs.pop('default_pattern', None)
        self.case_sensitive: bool = kwargs.pop('case_sensitive', False)

        # Internal flag to track if using nested patterns
        self._is_nested_pattern: bool = False

        super().__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs) -> bool:
        """Initialize and validate component configuration."""
        await super().start(**kwargs)
        # Get files from previous component if not explicitly provided
        if not self.files and self.previous:
            if isinstance(self.input, (list, tuple)):
                self.files = self.input
            elif isinstance(self.input, dict) and 'filenames' in self.input:
                self.files = self.input['filenames']
            else:
                raise DataNotFound(
                    "No files provided and previous component output is not a list."
                )

        if not self.files:
            raise DataNotFound(
                "No PDF files provided. Specify 'files' parameter or use after a component that outputs files."
            )

        # Validate split_pattern
        if not self.split_pattern:
            raise ComponentError(
                "split_pattern is required. Example: {'contract': [0, 10], 'w9': [11, 12]}"
            )

        if not isinstance(self.split_pattern, dict):
            raise ComponentError(
                "split_pattern must be a dictionary."
            )

        # Detect if using nested patterns (conditional by filename)
        # Check if any value is a dict (nested structure) vs a list (simple structure)
        first_value = next(iter(self.split_pattern.values()))
        self._is_nested_pattern = isinstance(first_value, dict)

        if self._is_nested_pattern:
            # Validate nested pattern structure
            for pattern_name, pattern_dict in self.split_pattern.items():
                if not isinstance(pattern_dict, dict):
                    raise ComponentError(
                        f"In nested split_pattern, '{pattern_name}' must be a dictionary. "
                        f"Example: {{'HVAC': {{'sow': [0, 9], 'w9': [10, 15]}}}}"
                    )
                # Validate each page range in the nested pattern
                for prefix, page_range in pattern_dict.items():
                    self._validate_page_range(prefix, page_range, pattern_name)

            self.logger.info(
                f"Using conditional split patterns: {list(self.split_pattern.keys())}"
            )
            if self.default_pattern and self.default_pattern not in self.split_pattern:
                raise ComponentError(
                    f"default_pattern '{self.default_pattern}' not found in split_pattern keys: "
                    f"{list(self.split_pattern.keys())}"
                )
        else:
            # Validate simple pattern structure
            for prefix, page_range in self.split_pattern.items():
                self._validate_page_range(prefix, page_range)
            self.logger.info("Using simple split pattern for all files")

        # Validate and create directory
        if not self.directory:
            raise ComponentError("directory parameter is required.")

        self.directory = Path(self.directory)

        if not self.directory.exists():
            self.logger.info(f"Creating output directory: {self.directory}")
            self.directory.mkdir(parents=True, exist_ok=True)

        # Convert files to Path objects
        self.files = [Path(f) for f in self.files]

        # Validate that all files exist
        for file_path in self.files:
            if not file_path.exists():
                raise FileNotFound(f"PDF file not found: {file_path}")
            if not file_path.suffix.lower() == '.pdf':
                raise ComponentError(f"File is not a PDF: {file_path}")

        return True

    def _validate_page_range(
        self,
        prefix: str,
        page_range: Union[List[int], tuple],
        parent_pattern: str = None
    ) -> None:
        """Validate a single page range."""
        context = f" in pattern '{parent_pattern}'" if parent_pattern else ""

        if not isinstance(page_range, (list, tuple)) or len(page_range) != 2:
            raise ComponentError(
                f"Invalid page range for '{prefix}'{context}: {page_range}. "
                "Page ranges must be [start, end] format."
            )
        if page_range[0] > page_range[1]:
            raise ComponentError(
                f"Invalid page range for '{prefix}'{context}: start page {page_range[0]} "
                f"is greater than end page {page_range[1]}."
            )

    def _get_pattern_for_file(self, pdf_path: Path) -> Tuple[str, Dict[str, List[int]]]:
        """
        Determine which split pattern to use for a given file.

        Args:
            pdf_path: Path to the PDF file

        Returns:
            Tuple of (pattern_name, pattern_dict) where pattern_dict contains the page ranges

        Raises:
            ComponentError: If no matching pattern found and no default_pattern specified
        """
        if not self._is_nested_pattern:
            # Simple pattern - use for all files
            return ("default", self.split_pattern)

        # Check filename against each pattern
        filename = pdf_path.name
        if not self.case_sensitive:
            filename = filename.lower()

        for pattern_name, pattern_dict in self.split_pattern.items():
            search_pattern = pattern_name if self.case_sensitive else pattern_name.lower()

            if search_pattern in filename:
                self.logger.info(
                    f"File '{pdf_path.name}' matched pattern '{pattern_name}'"
                )
                return (pattern_name, pattern_dict)

        # No match found
        if self.default_pattern:
            self.logger.warning(
                f"File '{pdf_path.name}' did not match any pattern. "
                f"Using default pattern '{self.default_pattern}'"
            )
            return (self.default_pattern, self.split_pattern[self.default_pattern])
        else:
            raise ComponentError(
                f"File '{pdf_path.name}' did not match any pattern in {list(self.split_pattern.keys())} "
                f"and no default_pattern is specified."
            )

    def _split_pdf(self, pdf_path: Path, pattern_dict: Dict[str, List[int]],
                   pattern_name: str = None) -> Dict[str, Path]:
        """
        Split a single PDF file according to the provided pattern.

        Args:
            pdf_path: Path to the PDF file to split
            pattern_dict: Dictionary mapping prefix names to page ranges
            pattern_name: Optional name of the pattern being used (for logging)

        Returns:
            Dictionary mapping prefix names to output file paths
        """
        output_files = {}

        try:
            # Open the PDF with PyMuPDF
            source_doc = fitz.open(str(pdf_path))
            total_pages = source_doc.page_count

            pattern_info = f" using pattern '{pattern_name}'" if pattern_name and pattern_name != "default" else ""
            self.logger.info(
                f"Processing {pdf_path.name} ({total_pages} pages){pattern_info}"
            )

            # Process each split pattern
            for prefix, page_range in pattern_dict.items():
                start_page, end_page = page_range

                # Validate page range against actual PDF pages
                if start_page >= total_pages:
                    self.logger.warning(
                        f"Start page {start_page} exceeds total pages {total_pages} "
                        f"in {pdf_path.name}. Skipping '{prefix}'."
                    )
                    continue

                if end_page >= total_pages:
                    self.logger.warning(
                        f"End page {end_page} exceeds total pages {total_pages} "
                        f"in {pdf_path.name}. Adjusting to {total_pages - 1}."
                    )
                    end_page = total_pages - 1

                # Create output filename
                stem = pdf_path.stem
                output_filename = f"{prefix}_{stem}.pdf"
                output_path = self.directory / output_filename

                # Check if file exists and overwrite setting
                if output_path.exists() and not self.overwrite:
                    self.logger.warning(
                        f"Output file {output_path} already exists. "
                        "Skipping (overwrite=False)."
                    )
                    continue

                # Create new PDF document and insert pages
                output_doc = fitz.open()
                output_doc.insert_pdf(
                    source_doc,
                    from_page=start_page,
                    to_page=end_page,
                    start_at=-1
                )

                # Save output file
                output_doc.save(str(output_path))
                output_doc.close()

                output_files[prefix] = output_path
                self.logger.info(
                    f"Created {output_filename}: pages {start_page}-{end_page} "
                    f"({end_page - start_page + 1} pages)"
                )

            # Close source document
            source_doc.close()

        except Exception as e:
            raise ComponentError(
                f"Error splitting PDF {pdf_path.name}: {str(e)}"
            ) from e

        return output_files

    async def run(self):
        """Execute the PDF splitting process."""
        self._result = {
            'processed_files': [],
            'output_files': [],
            'errors': [],
            'pattern_usage': {}  # Track which patterns were used
        }

        for pdf_path in self.files:
            try:
                self.logger.info(f"Splitting PDF: {pdf_path}")

                # Determine which pattern to use for this file
                pattern_name, pattern_dict = self._get_pattern_for_file(pdf_path)

                # Track pattern usage
                if pattern_name not in self._result['pattern_usage']:
                    self._result['pattern_usage'][pattern_name] = []
                self._result['pattern_usage'][pattern_name].append(str(pdf_path))

                # Split the PDF using the determined pattern
                output_files = self._split_pdf(pdf_path, pattern_dict, pattern_name)

                # Record results
                self._result['processed_files'].append(str(pdf_path))
                self._result['output_files'].extend([str(f) for f in output_files.values()])

                self.logger.info(
                    f"Successfully split {pdf_path.name} into {len(output_files)} files"
                )

            except Exception as e:
                error_msg = f"Failed to process {pdf_path.name}: {str(e)}"
                self.logger.error(error_msg)
                self._result['errors'].append(error_msg)

        # Summary logging
        total_processed = len(self._result['processed_files'])
        total_output = len(self._result['output_files'])
        total_errors = len(self._result['errors'])

        self.add_metric('PROCESSED_PDF_FILES', self._result['processed_files'])

        summary = (
            f"PDF splitting complete: {total_processed} files processed, "
            f"{total_output} output files created, {total_errors} errors"
        )

        if self._is_nested_pattern:
            pattern_summary = ", ".join(
                f"{name}: {len(files)} files"
                for name, files in self._result['pattern_usage'].items()
            )
            summary += f" (Pattern usage: {pattern_summary})"

        self.logger.info(summary)

        # Return list of output files for chaining
        return self._result['output_files']

    async def close(self):
        """Clean up resources."""
        pass
