"""Docstring parser for Flowtask components.

This module provides the DocstringParser class that extracts structured
documentation from component class docstrings. It handles the table format
used in Flowtask components with `:widths: auto` markers.
"""
import re
from typing import List, Optional
from .models import ComponentDoc, ComponentAttribute


class DocstringParser:
    """Parse component docstrings into structured ComponentDoc format.

    The parser handles the Flowtask docstring format which includes:
    - Component name as the first line
    - Description text before the `:widths: auto` marker
    - Attribute table with columns: name | required | description
    - YAML/JSON example blocks in fenced code blocks

    Example docstring format::

        ComponentName

        Description of the component.

        :widths: auto

        | attribute_name | Yes | Description of the attribute |
        | other_attr     | No  | Another description           |

        Example:

        ```yaml
        ComponentName:
          attribute_name: value
        ```
    """

    # Pattern to match table rows: | name | Yes/No | description |
    # Handles variable spacing and captures the three main columns
    TABLE_ROW_PATTERN = re.compile(
        r'^\s*\|\s*(\w[\w_]*)\s*\|\s*(Yes|No)\s*\|\s*(.+?)\s*\|?\s*$',
        re.IGNORECASE
    )

    # Pattern to match continuation rows: |    | | continued description |
    CONTINUATION_PATTERN = re.compile(
        r'^\s*\|\s*\|\s*\|\s*(.+?)\s*\|?\s*$'
    )

    # Pattern to match fenced code blocks with yaml or json
    EXAMPLE_PATTERN = re.compile(
        r'```(?:yaml|json)\s*\n(.*?)```',
        re.DOTALL | re.IGNORECASE
    )

    # Marker that indicates the start of the attribute table
    TABLE_MARKER = ':widths: auto'

    # Optional dataflow contract markers — captured value must be one of
    # the IOType enum (none|file|dataframe|recordset|iterator|any).
    # Example docstring lines:
    #   :consumes: file
    #   :produces: dataframe
    IO_MARKER_PATTERN = re.compile(
        r'^\s*:(consumes|produces):\s*(none|file|dataframe|recordset|iterator|any)\s*$',
        re.MULTILINE | re.IGNORECASE,
    )

    def parse(self, docstring: str) -> Optional[ComponentDoc]:
        """Parse a docstring into ComponentDoc.

        Args:
            docstring: The raw docstring from a component class.

        Returns:
            ComponentDoc if the docstring contains valid documentation,
            None if the docstring is empty or doesn't contain required markers.
        """
        if not docstring:
            return None

        # Check if this is a documentable docstring
        if self.TABLE_MARKER not in docstring:
            return None

        name = self._extract_name(docstring)
        description = self._extract_description(docstring)
        attributes = self._parse_attributes(docstring)
        examples = self._extract_examples(docstring)
        io_overrides = self._extract_io_markers(docstring)

        doc = ComponentDoc(
            name=name,
            description=description,
            attributes=attributes,
            examples=examples,
        )
        # The cascade resolution (override → category default → "any") lives
        # in the generator; here we only carry the value the docstring
        # declares so downstream code can tell "no override" from "explicit
        # 'any'".
        for field, value in io_overrides.items():
            setattr(doc, field, value)
        return doc

    def _extract_io_markers(self, docstring: str) -> dict:
        """Find ``:consumes:`` / ``:produces:`` markers in the docstring.

        Returns:
            Dict with keys ``consumes`` and/or ``produces`` set to the
            normalised lower-case enum value. Missing markers are omitted so
            the caller can apply a fallback (category default).
        """
        overrides: dict[str, str] = {}
        for match in self.IO_MARKER_PATTERN.finditer(docstring):
            field = match.group(1).lower()
            value = match.group(2).lower()
            overrides[field] = value
        return overrides

    def _extract_name(self, docstring: str) -> str:
        """Extract the component name from the first non-empty line.

        Args:
            docstring: The raw docstring.

        Returns:
            The component name or empty string if not found.
        """
        lines = docstring.strip().split('\n')
        for line in lines:
            line = line.strip()
            if line:
                # First non-empty line should be the component name
                # It should be a single word (class name)
                if re.match(r'^[A-Z][a-zA-Z0-9_]*$', line):
                    return line
                break
        return ""

    def _extract_description(self, docstring: str) -> str:
        """Extract the description text before the :widths: auto marker.

        Args:
            docstring: The raw docstring.

        Returns:
            The description text, cleaned of extra whitespace.
        """
        # Find the position of the table marker
        marker_pos = docstring.find(self.TABLE_MARKER)
        if marker_pos == -1:
            return ""

        # Get text before the marker
        before_marker = docstring[:marker_pos]

        # Split into lines and process
        lines = before_marker.strip().split('\n')

        # Skip the first line (component name) and collect description
        description_lines = []
        skip_first = True
        for line in lines:
            stripped = line.strip()
            if skip_first and stripped:
                skip_first = False
                continue
            if stripped:
                description_lines.append(stripped)

        return ' '.join(description_lines)

    def _parse_attributes(self, docstring: str) -> List[ComponentAttribute]:
        """Parse the attribute table from the docstring.

        Handles multi-line descriptions where continuation rows have empty
        first cells.

        Args:
            docstring: The raw docstring.

        Returns:
            List of ComponentAttribute objects.
        """
        attributes = []
        seen_names = set()  # Track seen names to avoid duplicates

        # Find the table section (after :widths: auto)
        marker_pos = docstring.find(self.TABLE_MARKER)
        if marker_pos == -1:
            return attributes

        table_section = docstring[marker_pos:]
        lines = table_section.split('\n')

        current_attr = None
        current_description = []

        for line in lines:
            # Skip the marker line and empty lines
            if self.TABLE_MARKER in line or not line.strip():
                continue

            # Skip separator rows like |---|---|---|
            if re.match(r'^\s*\|[-\s|]+\|\s*$', line):
                continue

            # Try to match a new attribute row
            match = self.TABLE_ROW_PATTERN.match(line)
            if match:
                # Save previous attribute if exists
                if current_attr and current_attr['name'] not in seen_names:
                    attributes.append(ComponentAttribute(
                        name=current_attr['name'],
                        required=current_attr['required'],
                        description=' '.join(current_description).strip()
                    ))
                    seen_names.add(current_attr['name'])

                # Start new attribute
                name = match.group(1)
                required_str = match.group(2).lower()
                description = match.group(3).strip()

                current_attr = {
                    'name': name,
                    'required': required_str == 'yes'
                }
                current_description = [description] if description else []
                continue

            # Try to match a continuation row
            cont_match = self.CONTINUATION_PATTERN.match(line)
            if cont_match and current_attr:
                current_description.append(cont_match.group(1).strip())
                continue

            # If we hit a non-table line (like "Example:"), stop parsing
            if current_attr and not line.strip().startswith('|'):
                break

        # Don't forget the last attribute
        if current_attr and current_attr['name'] not in seen_names:
            attributes.append(ComponentAttribute(
                name=current_attr['name'],
                required=current_attr['required'],
                description=' '.join(current_description).strip()
            ))

        return attributes

    def _extract_examples(self, docstring: str) -> List[str]:
        """Extract YAML/JSON example blocks from the docstring.

        Args:
            docstring: The raw docstring.

        Returns:
            List of example strings with preserved formatting.
        """
        examples = []
        matches = self.EXAMPLE_PATTERN.findall(docstring)
        for match in matches:
            # Clean up the example but preserve structure
            example = match.strip()
            if example:
                examples.append(example)
        return examples
