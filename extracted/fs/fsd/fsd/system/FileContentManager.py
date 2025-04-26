import re
import aiofiles
import os
import mimetypes
from typing import List, Tuple, Optional
from fsd.log.logger_config import get_logger
import PyPDF2
import docx
import chardet
import openpyxl
import io
from pathlib import Path
import math
from rapidfuzz import fuzz
import difflib
from difflib import SequenceMatcher
from datetime import datetime

logger = get_logger(__name__)

class FileContentManager:

    def __init__(self, repo):
        self.repo = repo
        
    # Flexible delimiter patterns using regex
    HEAD_PATTERN = r'^<{5,9} SEARCH\s*$'       # Matches <<< SEARCH, <<<< SEARCH, etc.
    DIVIDER_PATTERN = r'^={5,9}\s*$'            # Matches ===, ====, etc.
    UPDATED_PATTERN = r'^>{5,9} REPLACE\s*$'  # Matches >>> REPLACE, >>>>> REPLACE, etc.

    SIMILARITY_THRESHOLD = 80.0  # Configurable threshold for fuzzy matching (0-100)
    AUTOMATIC_REPLACE_SIMILAR = True  # Flag to enable/disable automatic replacement of similar lines

    DEFAULT_FENCE = ("```", "```")  # Not used currently, but kept for potential future enhancements

    # Add error message constants
    HEAD_ERR = "<<<<<<< SEARCH"
    DIVIDER_ERR = "======="
    UPDATED_ERR = ">>>>>>> REPLACE"

    @staticmethod
    async def read_file(file_path: str) -> str:
        """
        Read and return the content of any type of file asynchronously, including special files like PDFs,
        DOCs, XLSX, and all code file types.

        Args:
            file_path (str): Full path to the file.

        Returns:
            str: Content of the file or empty string if file doesn't exist or can't be read.
        """
        file_path = str(Path(file_path))  # Convert to platform-specific path
        
        if not os.path.exists(file_path):
            logger.debug(f"File does not exist: {file_path}")
            return ""

        mime_type, _ = mimetypes.guess_type(file_path)

        try:
            # Handle PDF files
            if mime_type == 'application/pdf':
                async with aiofiles.open(file_path, 'rb') as file:
                    content = await file.read()
                pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
                if pdf_reader.is_encrypted:
                    logger.error(f"Cannot read encrypted PDF: {file_path}")
                    return ""
                text_content = []
                for page in pdf_reader.pages:
                    text = page.extract_text()
                    if text:
                        text_content.append(text)
                return '\n'.join(text_content)

            # Handle DOC and DOCX files
            elif mime_type in [
                'application/msword',
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            ]:
                async with aiofiles.open(file_path, 'rb') as file:
                    content = await file.read()
                doc = docx.Document(io.BytesIO(content))
                return '\n'.join(paragraph.text for paragraph in doc.paragraphs)

            # Handle XLSX (Excel) files
            elif mime_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
                async with aiofiles.open(file_path, 'rb') as file:
                    content = await file.read()
                workbook = openpyxl.load_workbook(io.BytesIO(content), data_only=True)
                sheet = workbook.active  # Read the first sheet
                data = []
                for row in sheet.iter_rows(values_only=True):
                    data.append('\t'.join([str(cell) if cell is not None else "" for cell in row]))
                return '\n'.join(data)

            # Handle text and code files
            else:
                # Attempt to read as UTF-8 first
                try:
                    async with aiofiles.open(file_path, 'r', encoding='utf-8', newline='') as file:
                        return await file.read()
                except UnicodeDecodeError:
                    # If UTF-8 fails, detect encoding
                    async with aiofiles.open(file_path, 'rb') as file:
                        raw_data = await file.read()
                    detected = chardet.detect(raw_data)
                    encoding = detected['encoding'] if detected['encoding'] else 'utf-8'
                    async with aiofiles.open(file_path, 'r', encoding=encoding, errors='replace', newline='') as file:
                        return await file.read()

        except Exception as e:
            error_message = f"Failed to read file {file_path}: {e}"
            logger.exception(error_message)
            
            return ""

    @staticmethod
    async def write_file(file_path: str, content: str):
        """Write content to the file asynchronously."""
        try:
            file_path = str(Path(file_path))  # Convert to platform-specific path
            directory = os.path.dirname(file_path)
            if not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)
                logger.debug(f"#### `SnowX` has created a new directory: `{directory}` for the file: `{file_path}`")

            async with aiofiles.open(file_path, 'w', encoding='utf-8', newline='') as file:
                await file.write(content)

            logger.debug(f"#### `SnowX` has successfully written to the file: `{file_path}`")
        except Exception as e:
            error_message = f"#### `SnowX` encountered an error while writing to file `{file_path}`. Error details: `{e}`"
            logger.error(error_message)
            

    @staticmethod
    def parse_search_replace_blocks(response: str) -> List[Tuple[str, str]]:
        """
        Parses a response string for single or multiple SEARCH/REPLACE blocks,
        returning search and replace content as tuples.

        Args:
            response (str): The string containing SEARCH/REPLACE blocks.

        Returns:
            List[Tuple[str, str]]: A list of tuples where each tuple contains (search, replace).

        Raises:
            ValueError: If no valid SEARCH/REPLACE blocks are found.
        """
        # Updated regex pattern to allow variable delimiters
        pattern = rf'''
            (?P<HEAD>{FileContentManager.HEAD_PATTERN})\s*\n
            (?P<SEARCH>.*?)\n
            (?P<DIVIDER>{FileContentManager.DIVIDER_PATTERN})\s*\n
            (?P<REPLACE>.*?)\n
            (?P<UPDATED>{FileContentManager.UPDATED_PATTERN})
        '''

        # Compile the regex with VERBOSE, MULTILINE, and DOTALL flags
        regex = re.compile(pattern, re.VERBOSE | re.MULTILINE | re.DOTALL)

        matches = regex.finditer(response)

        blocks = []
        for match in matches:
            search = match.group('SEARCH').strip()
            replace = match.group('REPLACE').strip()
            blocks.append((search, replace))

        # Raise an error if no blocks are found
        if not blocks:
            error_message = "No valid SEARCH/REPLACE blocks found in the input."
            logger.debug("No matches found with the updated regex pattern.")
            logger.debug(f"Response Content:\n{response}")
            
            raise ValueError(error_message)

        return blocks

    @classmethod
    def parse_search_replace_blocks_line_by_line(cls, response: str) -> List[Tuple[str, str]]:
        """
        Parses the response for SEARCH/REPLACE blocks using a line-by-line approach,
        allowing for more flexibility in block formatting.

        Args:
            response (str): The string containing SEARCH/REPLACE blocks.

        Returns:
            List[Tuple[str, str]]: A list of tuples where each tuple contains (search, replace).

        Raises:
            ValueError: If no valid SEARCH/REPLACE blocks are found.
        """
        blocks = []
        lines = response.splitlines()
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if re.match(cls.HEAD_PATTERN, line):
                search_content = []
                replace_content = []
                i += 1
                # Collect search content
                while i < len(lines) and not re.match(cls.DIVIDER_PATTERN, lines[i].strip()):
                    search_content.append(lines[i])
                    i += 1
                if i >= len(lines):
                    error_message = "Incomplete SEARCH/REPLACE block: Missing DIVIDER."
                    logger.error("SEARCH block not properly closed with DIVIDER.")
                    
                    raise ValueError(error_message)
                i += 1  # Skip the DIVIDER line
                # Collect replace content
                while i < len(lines) and not re.match(cls.UPDATED_PATTERN, lines[i].strip()):
                    replace_content.append(lines[i])
                    i += 1
                if i >= len(lines):
                    error_message = "Incomplete SEARCH/REPLACE block: Missing UPDATED."
                    logger.error("REPLACE block not properly closed with UPDATED.")
                    
                    raise ValueError(error_message)
                i += 1  # Skip the UPDATED line
                # Append the block
                blocks.append((
                    "\n".join(search_content).strip(),
                    "\n".join(replace_content).strip()
                ))
            else:
                i += 1
        if not blocks:
            error_message = "No valid SEARCH/REPLACE blocks found in the input."
            logger.debug("No valid SEARCH/REPLACE blocks found using line-by-line parser.")
            logger.debug(f"Response Content:\n{response}")
            
            raise ValueError(error_message)
        return blocks

    @staticmethod
    def create_pattern_from_search(search: str) -> str:
        """
        Create a regex pattern from the search string where any whitespace sequences are replaced with \s+.

        Args:
            search (str): The search string.

        Returns:
            str: The regex pattern.
        """
        # Split the search string into parts, separating by whitespace
        parts = re.split(r'(\s+)', search)
        # For each part, if it is whitespace, replace with \s+, else escape it
        pattern = ''.join(
            (r'\s+' if s.isspace() else re.escape(s)) for s in parts
        )
        return pattern

    @classmethod
    async def apply_changes(cls, file_path: str, blocks: List[Tuple[str, str]]) -> str:
        """Apply the changes from SEARCH/REPLACE blocks to the file content."""
        content = await cls.read_file(file_path)
        original_content = content  # Keep a copy of the original content for logging
        successful_blocks = 0
        failed_blocks = 0
        failed_block_details = []  # List to store failed block details

        for search, replace in blocks:
            try:
                if search:
                    new_content = cls.replace_content(content, search, replace)
                    if new_content is None:
                        logger.info(f"#### `SnowX` couldn't find a match for search block in file: `{file_path}`")
                        similar_info = cls.find_similar_lines(search, content)
                        similar_lines = similar_info.get('similar_lines')
                        start_index = similar_info.get('start_index')
                        end_index = similar_info.get('end_index')

                        if similar_lines and cls.AUTOMATIC_REPLACE_SIMILAR:
                            logger.debug(f"Attempting to replace similar lines in `{file_path}`:\n{similar_lines}")
                            content = cls.replace_similar_lines(content, start_index, end_index, replace)
                            logger.info(f"#### `SnowX` has replaced similar lines in file: `{file_path}`")
                            successful_blocks += 1
                        elif similar_lines:
                            logger.debug(f"Did you mean to match these lines in `{file_path}`?\n{similar_lines}")
                            failed_blocks += 1
                            failed_block_details.append({
                                'search': search,
                                'replace': replace,
                                'similar_lines': similar_lines
                            })
                        else:
                            failed_blocks += 1
                            failed_block_details.append({
                                'search': search,
                                'replace': replace,
                                'error': "No similar lines found"
                            })
                    else:
                        content = new_content
                        successful_blocks += 1
                else:
                    content += f"{replace}"
                    successful_blocks += 1
            except Exception as e:
                failed_blocks += 1
                failed_block_details.append({
                    'search': search,
                    'replace': replace,
                    'error': str(e)
                })
                error_message = f"Error processing block: {str(e)}"
                logger.error(error_message)
               
                continue

        logger.info(f"#### Processed {len(blocks)} blocks: {successful_blocks} successful, {failed_blocks} failed")
        
        if content != original_content:
            logger.debug(f"#### `SnowX` has successfully applied changes to the content of file: `{file_path}`")
        else:
            logger.info(f"#### `SnowX` did not make any changes to the file: `{file_path}`")
        return content

    @staticmethod
    def replace_content(content: str, search: str, replace: str) -> Optional[str]:
        """
        Replace the search block with the replace block in the content.
        Now with improved matching capabilities.
        """
        # Attempt exact match first
        if search in content:
            return content.replace(search, replace)

        # Handle empty search (append mode)
        if not search.strip():
            if not content.endswith('\n'):
                content += '\n'
            return content + replace

        # Try handling ... elisions
        try:
            new_content = FileContentManager.try_dotdotdots(content, search, replace)
            if new_content:
                return new_content
        except ValueError:
            pass

        # Try perfect match with whitespace flexibility
        new_content = FileContentManager.perfect_or_whitespace(content, search, replace)
        if new_content:
            return new_content

        return None

    @staticmethod
    def try_dotdotdots(whole: str, part: str, replace: str) -> Optional[str]:
        """
        Handle search/replace blocks that use ... to elide code.
        
        Args:
            whole (str): The complete content
            part (str): The search block
            replace (str): The replace block
            
        Returns:
            Optional[str]: Modified content if successful, None if no ... found
            
        Raises:
            ValueError: If ... patterns don't match or multiple matches found
        """
        try:
            dots_re = re.compile(r"(^\s*\.\.\.\n)", re.MULTILINE | re.DOTALL)
            
            part_pieces = re.split(dots_re, part)
            replace_pieces = re.split(dots_re, replace)
            
            if len(part_pieces) != len(replace_pieces):
                logger.error("Unpaired ... in SEARCH/REPLACE block")
                return None
            
            if len(part_pieces) == 1:
                return None
            
            # Verify ... patterns match
            all_dots_match = all(part_pieces[i] == replace_pieces[i] for i in range(1, len(part_pieces), 2))
            if not all_dots_match:
                logger.error("Unmatched ... in SEARCH/REPLACE block")
                return None
            
            # Get the non-... pieces
            part_pieces = [part_pieces[i] for i in range(0, len(part_pieces), 2)]
            replace_pieces = [replace_pieces[i] for i in range(0, len(replace_pieces), 2)]
            
            # Apply replacements
            for part, replace in zip(part_pieces, replace_pieces):
                if not part and not replace:
                    continue
                
                if not part and replace:
                    if not whole.endswith('\n'):
                        whole += '\n'
                    whole += replace
                    continue
                
                if whole.count(part) == 0:
                    raise ValueError("Part not found in content")
                if whole.count(part) > 1:
                    raise ValueError("Multiple matches found")
                
                whole = whole.replace(part, replace, 1)
            
            return whole
        except Exception as e:
            logger.error(f"Error in try_dotdotdots: {str(e)}")
            return None

    @staticmethod
    def perfect_or_whitespace(content: str, search: str, replace: str) -> Optional[str]:
        """Try perfect match, then try matching with whitespace flexibility."""
        content_lines = content.splitlines(keepends=True)
        search_lines = search.splitlines(keepends=True)
        replace_lines = replace.splitlines(keepends=True)

        # Try perfect match first
        res = FileContentManager.perfect_replace(content_lines, search_lines, replace_lines)
        if res:
            return res

        # Try being flexible about leading whitespace
        res = FileContentManager.replace_part_with_missing_leading_whitespace(
            content_lines, search_lines, replace_lines
        )
        if res:
            return res

        # Try without leading blank line if present
        if len(search_lines) > 2 and not search_lines[0].strip():
            res = FileContentManager.perfect_replace(
                content_lines, search_lines[1:], replace_lines
            )
            if res:
                return res

        return None

    @staticmethod
    def perfect_replace(whole_lines: List[str], part_lines: List[str], replace_lines: List[str]) -> Optional[str]:
        part_tup = tuple(part_lines)
        part_len = len(part_lines)

        for i in range(len(whole_lines) - part_len + 1):
            whole_tup = tuple(whole_lines[i : i + part_len])
            if part_tup == whole_tup:
                return "".join(whole_lines[:i] + replace_lines + whole_lines[i + part_len :])

        return None

    @staticmethod
    def replace_part_with_missing_leading_whitespace(whole_lines: List[str], part_lines: List[str], replace_lines: List[str]) -> Optional[str]:
        # Calculate the minimum leading whitespace to remove
        leading = [len(p) - len(p.lstrip()) for p in part_lines if p.strip()] + [
            len(r) - len(r.lstrip()) for r in replace_lines if r.strip()
        ]

        if leading:
            num_leading = min(leading)
            part_lines = [p[num_leading:] if p.strip() else p for p in part_lines]
            replace_lines = [r[num_leading:] if r.strip() else r for r in replace_lines]

        # Attempt to find and replace with adjusted whitespace
        part_tup = tuple(part_lines)
        part_len = len(part_lines)

        for i in range(len(whole_lines) - part_len + 1):
            whole_tup = tuple(whole_lines[i : i + part_len])
            if part_tup == whole_tup:
                # Determine the leading whitespace from the original content
                leading_whitespace_match = re.match(r'\s*', whole_lines[i])
                leading_whitespace = leading_whitespace_match.group() if leading_whitespace_match else ''
                adjusted_replace = [f"{leading_whitespace}{r.lstrip()}" if r.strip() else r for r in replace_lines]
                return "".join(whole_lines[:i] + adjusted_replace + whole_lines[i + part_len :])

        return None

    @staticmethod
    def fuzzy_replace(content: str, search: str, replace: str, threshold: float = None) -> Optional[str]:
        """Use class-level threshold if none provided"""
        if threshold is None:
            threshold = FileContentManager.SIMILARITY_THRESHOLD
        content_lines = content.splitlines(keepends=True)
        search_lines = search.splitlines(keepends=True)
        replace_lines = replace.splitlines(keepends=True)

        best_ratio = 0
        best_match_start = -1
        best_match_end = -1

        part_len = len(search_lines)
        scale = 0.1
        min_len = max(1, math.floor(part_len * (1 - scale)))
        max_len = math.ceil(part_len * (1 + scale))

        search_text = "".join(search_lines)

        for length in range(min_len, max_len + 1):
            for i in range(len(content_lines) - length + 1):
                chunk = content_lines[i : i + length]
                chunk_text = "".join(chunk)

                similarity = SequenceMatcher(None, chunk_text, search_text).ratio()

                if similarity > best_ratio:
                    best_ratio = similarity
                    best_match_start = i
                    best_match_end = i + length

        if best_ratio >= threshold / 100:
            logger.debug(f"Fuzzy match found with similarity {best_ratio} for search block.")
            new_content = (
                "".join(content_lines[:best_match_start]) +
                "".join(replace_lines) +
                "".join(content_lines[best_match_end:])
            )
            return new_content

        return None

    @classmethod
    def find_similar_lines(cls, search: str, content: str, threshold: float = None) -> dict:
        """Use class-level threshold if none provided"""
        if threshold is None:
            threshold = cls.SIMILARITY_THRESHOLD / 100  # Convert to 0-1 range
        search_lines = search.splitlines()
        content_lines = content.splitlines()

        best_ratio = 0
        best_match = None
        best_match_i = -1

        for i in range(len(content_lines) - len(search_lines) + 1):
            chunk = content_lines[i : i + len(search_lines)]
            ratio = SequenceMatcher(None, search_lines, chunk).ratio()
            if ratio > best_ratio:
                best_ratio = ratio
                best_match = chunk
                best_match_i = i

        if best_ratio < threshold:
            error_message = "No similar lines found"
            
            return {
                'similar_lines': "",
                'start_index': -1,
                'end_index': -1
            }

        # Check if exact match
        if best_match and best_match[0] == search_lines[0] and best_match[-1] == search_lines[-1]:
            return {
                'similar_lines': "\n".join(best_match),
                'start_index': best_match_i,
                'end_index': best_match_i + len(best_match)
            }

        # Add context lines
        N = 5  # Number of context lines
        best_match_end = min(len(content_lines), best_match_i + len(search_lines) + N)
        best_match_i = max(0, best_match_i - N)

        best = content_lines[best_match_i:best_match_end]
        return {
            'similar_lines': "\n".join(best),
            'start_index': best_match_i,
            'end_index': best_match_end
        }

    @staticmethod
    def replace_similar_lines(content: str, start_index: int, end_index: int, replace: str) -> str:
        """
        Replace lines in content from start_index to end_index with the replace string.

        Args:
            content (str): The original content.
            start_index (int): The starting line index for replacement.
            end_index (int): The ending line index for replacement.
            replace (str): The replace string.

        Returns:
            str: The modified content.
        """
        content_lines = content.splitlines(keepends=True)
        replace_lines = replace.splitlines(keepends=True)
        new_content = (
            "".join(content_lines[:start_index]) +
            "".join(replace_lines) +
            "".join(content_lines[end_index:])
        )
        return new_content

    @classmethod
    async def process_coding_agent_response(cls, file_path: str, coding_agent_response: str):
        """Process the coding agent response and automatically apply changes to the file."""
        try:
            # First, try regex-based parsing
            blocks = cls.parse_search_replace_blocks(coding_agent_response)
        except ValueError:
            logger.debug("Regex-based parsing failed. Attempting line-by-line parsing.")
            try:
                # Fallback to line-by-line parsing
                blocks = cls.parse_search_replace_blocks_line_by_line(coding_agent_response)
            except ValueError as e:
                error_message = f"#### `SnowX` found no valid SEARCH/REPLACE blocks in the coding agent response for file: `{file_path}`"
                logger.error(error_message)
                logger.debug(f"Error details: {e}")
                return

        new_content = await cls.apply_changes(file_path, blocks)
        await cls.write_file(file_path, new_content)
        logger.debug(f"#### `SnowX` has automatically applied changes to file: `{file_path}`")

    @classmethod
    async def handle_coding_agent_response(cls, file_path: str, coding_agent_response: str):
        """Main method to handle coding agent responses and automatically manage code changes for a single file."""
        logger.debug("Received coding agent response:")
        logger.debug(coding_agent_response)
        try:
            await cls.process_coding_agent_response(file_path, coding_agent_response)
            logger.debug(f"#### `SnowX` has successfully processed the coding agent response for file: `{file_path}`")
        except Exception as e:
            error_message = f"#### `SnowX` encountered an error while processing the coding agent response for file `{file_path}`. Error details: `{e}`"
            logger.error(error_message)
