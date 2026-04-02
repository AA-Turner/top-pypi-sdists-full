import json
import re
from json import JSONDecodeError
from typing import Any, Dict, List, Union


class JSONCleaner:
    def __init__(self, max_depth: int = 20):
        self.max_depth = max_depth  # Prevent stack overflow on deep nesting
        # Improved pattern to better match JSON objects, including nested ones
        self.json_pattern = re.compile(
            r'{(?:[^{}]|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|\[(?:[^\[\]]|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\')*\]|{(?:[^{}]|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|\[(?:[^\[\]]|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\')*\])*})*}',
            re.DOTALL | re.MULTILINE,
        )

    def extract_json_candidates(self, text: str) -> List[str]:
        """Extract potential JSON objects from arbitrary text"""
        candidates = []
        decoder = json.JSONDecoder()

        # First try to find complete JSON objects with our regex pattern
        for match in self.json_pattern.finditer(text):
            try:
                start = match.start()
                end = match.end()
                # Validate and get exact end position
                obj, new_end = decoder.raw_decode(text[start:end])
                candidates.append(text[start : start + new_end])
            except JSONDecodeError:
                # If direct parsing fails, add it as a candidate for cleaning
                candidates.append(match.group(0))

        # If no candidates found with regex, try a more aggressive approach
        if not candidates:
            # Look for potential JSON start/end markers
            open_braces = [m.start() for m in re.finditer(r"{", text)]
            close_braces = [m.start() for m in re.finditer(r"}", text)]

            # Try to match opening and closing braces
            if open_braces and close_braces:
                for start in open_braces:
                    for end in sorted(close_braces, reverse=True):
                        if end > start:
                            try:
                                # Try to parse the substring
                                potential_json = text[start : end + 1]
                                cleaned = self.clean_json_string(potential_json)
                                json.loads(cleaned)
                                candidates.append(potential_json)
                                break
                            except (JSONDecodeError, TypeError):
                                # If it fails with one closing brace, try the next one
                                continue

            # If still no candidates, look for code blocks that might contain JSON
            if not candidates:
                code_blocks = re.finditer(r"```(?:json)?(.*?)```", text, re.DOTALL)
                for block in code_blocks:
                    candidates.append(block.group(1).strip())

        return candidates

    def clean_json_string(self, data: str) -> str:
        """Multi-stage cleaning process for JSON strings"""
        # Phase 1: Remove code blocks and markdown formatting
        data = re.sub(r"```(?:json)?|```", "", data)  # Remove code block markers

        # Phase 2: Basic normalization
        data = re.sub(
            r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F-\x9F]", "", data
        )  # Remove control characters but keep tabs and newlines

        # Handle special quotes using Unicode code points
        data = re.sub(
            r"(?<!\\)\u2018|\u2019", "'", data
        )  # Normalize single quotes (left/right)
        data = re.sub(
            r"(?<!\\)\u201C|\u201D", '"', data
        )  # Normalize double quotes (left/right)

        # Phase 3: Structural fixes
        data = re.sub(r",\s*([}\]])", r"\1", data)  # Remove trailing commas

        # Fix unquoted keys (more comprehensive)
        data = re.sub(r"(?<!\\)([{,])\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*:", r'\1"\2":', data)

        # Fix boolean and null values
        data = re.sub(r":\s*True\b", r":true", data, flags=re.IGNORECASE)
        data = re.sub(r":\s*False\b", r":false", data, flags=re.IGNORECASE)
        data = re.sub(r":\s*None\b", r":null", data, flags=re.IGNORECASE)

        # Phase 4: Advanced string processing and whitespace handling
        # Process character by character to handle strings, apostrophes, and whitespace correctly
        in_string = False
        in_single_quoted_string = False
        result = []
        i = 0

        while i < len(data):
            char = data[i]

            # Handle double quotes (start/end of JSON string)
            if char == '"' and (i == 0 or data[i - 1] != "\\"):
                if (
                    not in_single_quoted_string
                ):  # Only toggle if not inside a single-quoted string
                    in_string = not in_string
                result.append(char)

            # Handle single quotes (convert to double quotes for JSON)
            elif char == "'" and (i == 0 or data[i - 1] != "\\"):
                if not in_string:  # Outside a double-quoted string
                    if not in_single_quoted_string:  # Start of a single-quoted string
                        in_single_quoted_string = True
                        result.append(
                            '"'
                        )  # Replace opening single quote with double quote
                    else:  # End of a single-quoted string
                        in_single_quoted_string = False
                        result.append(
                            '"'
                        )  # Replace closing single quote with double quote
                else:  # Inside a double-quoted string, it's an apostrophe
                    result.append("'")  # Leave apostrophe as-is in JSON strings

            # Handle whitespace
            elif not (in_string or in_single_quoted_string) and char.isspace():
                # Collapse consecutive whitespace outside strings
                while i + 1 < len(data) and data[i + 1].isspace():
                    i += 1
                result.append(" ")

            # Handle array literals with single quotes
            elif char == "[" and not (in_string or in_single_quoted_string):
                result.append(char)
                # Look ahead for single-quoted array elements
                j = i + 1
                array_content = []
                while j < len(data) and data[j] != "]":
                    array_content.append(data[j])
                    j += 1
                if j < len(data):  # Found closing bracket
                    array_str = "".join(array_content)
                    # Convert single-quoted array elements to double-quoted
                    array_str = re.sub(r"'([^']*)'", r'"\1"', array_str)
                    result.append(array_str)
                    result.append("]")
                    i = j  # Skip processed array content
                else:
                    result.append(
                        data[i:]
                    )  # Append rest of string if no closing bracket
                    break

            # All other characters
            else:
                result.append(char)

            i += 1

        data = "".join(result)

        return data.strip()

    def safe_parse(self, data: str) -> Any:
        """Attempt parsing with multiple recovery strategies"""
        # First, clean the string to handle common issues
        cleaned_data = self.clean_json_string(data)

        strategies = [
            # Try direct parsing first
            lambda d: json.loads(d),
            # Try with comments removed
            lambda d: json.loads(re.sub(r"/\*.*?\*/", "", d, flags=re.DOTALL)),
            # Try with additional fixes for arrays
            lambda d: json.loads(
                re.sub(r"\[(\s*),", "[", d)
            ),  # Fix empty items in arrays
            # Try with more aggressive cleaning
            lambda d: json.loads(
                re.sub(r'([{,])\s*([^"\s\d{[]+)\s*:', r'\1"\2":', d)
            ),  # Force quote all keys
            # Last resort: try to extract just the valid parts
            lambda d: self._extract_valid_json(d),
        ]

        # Try with original data first
        try:
            return json.loads(data)
        except (JSONDecodeError, TypeError):
            pass

        # Then try with cleaned data
        for strategy in strategies:
            try:
                return strategy(cleaned_data)
            except (JSONDecodeError, TypeError):
                continue

        # If all else fails, try to create a minimal valid JSON
        try:
            # Try to extract key-value pairs and build a valid JSON object
            pattern = r'"([^"]+)"\s*:\s*("[^"]*"|\'[^\']*\'|\d+|true|false|null|\{[^}]*\}|\[[^\]]*\])'
            matches = re.findall(pattern, cleaned_data, re.DOTALL)
            if matches:
                result = {
                    key: json.loads(value.replace("'", '"'))
                    if value.startswith(("'", '"'))
                    else json.loads(value)
                    for key, value in matches
                }
                return result
        except (JSONDecodeError, TypeError, ValueError):
            pass

        raise JSONDecodeError("All parsing strategies failed", data, 0)

    def _extract_valid_json(self, text: str) -> Any:
        """Extract valid JSON from potentially malformed text"""
        # Try to find the largest valid JSON object in the text
        for i in range(len(text)):
            for j in range(len(text), i, -1):
                try:
                    substr = text[i:j]
                    if substr.strip().startswith("{") and substr.strip().endswith("}"):
                        return json.loads(substr)
                except (JSONDecodeError, TypeError):
                    continue
        raise JSONDecodeError("No valid JSON found", text, 0)

    def clean(self, data: Union[str, Dict, List]) -> Any:
        """Main entry point for cleaning and parsing JSON from text

        Args:
            data: Input data that might contain JSON. Can be:
                - A string containing JSON or text with embedded JSON
                - An already parsed dict or list

        Returns:
            Parsed JSON data as Python objects (dict, list, etc.)

        Raises:
            ValueError: If no valid JSON could be extracted or parsed
        """
        # If already a dict or list, return as is
        if isinstance(data, (dict, list)):
            return data

        # If empty or not a string, handle appropriately
        if not data or not isinstance(data, str):
            if data is None or data == "":
                return {}
            try:
                # Try to convert to string if possible
                data = str(data)
            except:
                raise ValueError(f"Cannot process input of type {type(data)}")

        # First try direct parsing of the entire string
        try:
            return json.loads(data)
        except JSONDecodeError:
            pass

        # Try to clean the entire string
        try:
            cleaned_data = self.clean_json_string(data)
            return json.loads(cleaned_data)
        except JSONDecodeError:
            pass

        # Extract JSON candidates from the text
        candidates = self.extract_json_candidates(data)

        # If no candidates found, use the entire text as a last resort
        if not candidates:
            candidates = [data]

        # Try each candidate, starting with the longest ones (likely more complete)
        candidates.sort(key=len, reverse=True)

        last_error = None
        for candidate in candidates:
            try:
                return self.safe_parse(candidate)
            except JSONDecodeError as e:
                last_error = e

        # If all else fails, try one last approach with the entire text
        try:
            # Try to extract any key-value pairs from the text
            pattern = r'"([^"]+)"\s*:\s*("[^"]*"|\'[^\']*\'|\d+|true|false|null|\{[^}]*\}|\[[^\]]*\])'
            matches = re.findall(pattern, data, re.DOTALL)
            if matches:
                result = {}
                for key, value in matches:
                    try:
                        if value.startswith(("'", '"')):
                            result[key] = value[1:-1]  # Strip quotes
                        elif value.lower() in ("true", "false"):
                            result[key] = value.lower() == "true"
                        elif value.lower() == "null":
                            result[key] = None
                        else:
                            try:
                                result[key] = json.loads(value)
                            except:
                                result[key] = value
                    except:
                        result[key] = value
                return result
        except Exception:
            pass

        raise ValueError(f"Failed to parse JSON: {last_error}")
