"""
Module for parsing castep styled inputs
inputs may contain oneline


STANDARDISATION
CASTEP input does not destinguish between low and upper case, but python does.
To stardardise data parsed. Output follows the convension
1. all keys will be in lower case
2. all block names will be in lower case
3. case of the values themselves are not affected
4. content of the blocks are not affected
"""
import re
from .common import Block, FormatError

COMMENT_SYMBOLS = ("#", "!")

# RE for separating blocks
block_start = re.compile(r"%block (\w+)", flags=re.IGNORECASE)
block_finish = re.compile(r"%endblock (\w+)", flags=re.IGNORECASE)
kw_split = re.compile(r"[ \t:=]+")


class PlainParser:
    """
    Base parser class
    Does nothing fancy, basic text processing
    """

    def __init__(self, lines):
        """
        Parser for cell/param files for castep.
        May also be useful for OptaDos/CASTEPConv that shares similar
        format.
        Parameters:
        :params lines: A list of the file content or name of a file to be read
        """

        if isinstance(lines, (list, tuple)):
            self._raw_lines = lines  # Raw input lines
        else:
            with open(lines, encoding="utf-8") as fhandle:
                lin = []
                for line in fhandle:
                    lin.append(line.strip())
            self._raw_lines = lin

        self._lines = []  # Processed lines
        self._kwlines = []  # key-value paired lines
        self._blocks = {}  # A dictionary of blocks
        self._keywords = {}  # A dictionary of key value pairs
        self._comments = []

    def parse(self):
        """
        Parse the input file
        """
        self._clean_up_lines()  # Remove comments, blank lines
        self._split_block_kw()  # Extract blocks from the lines
        self._parse_keywords()  # Parse the key, value pair

    @property
    def content(self):
        """A list of lines as inputs for parsing"""
        return self._raw_lines

    @property
    def comments(self):
        if self._comments is None:
            raise RuntimeError("File is not parsed")
        return self._comments

    def _clean_up_lines(self):
        """
        Filter out comments
        Save cleaned lines in self._lines and
        comments in self._comments
        Make everything not comment in lower case
        """

        lines = self.content
        comments = []
        cleaned_lines = []
        for line in lines:
            line = line.strip()  # Get rid of white spaces
            if not line:
                continue  # skip empty lines

            # We first check for comment
            if line[0] in COMMENT_SYMBOLS:
                comments.append(line[1:].strip())
                continue

            # Check if there is any trailing comments
            for symbol in COMMENT_SYMBOLS:
                pos = line.find(symbol)
                if pos != -1:
                    comments.append(line[pos + 1 :].strip())
                    cld_line = line[:pos].strip()  # Remove trailing space
                    break
                cld_line = line
            cleaned_lines.append(cld_line)

        self._lines = cleaned_lines
        self._comments = comments
        return cleaned_lines, comments

    def _split_block_kw(self):
        """
        Split blocks from cleaned_up lines.
        Returns a dictionary of block names and contents
        Save all keyword-value lines in self._kwlines
        """

        if self._lines is None:
            self._clean_up_lines()

        # Extract
        block_indices = {}
        in_block = False
        kwlines = []
        start_name = None
        for i, line in enumerate(self._lines):
            start_match = block_start.match(line)
            if start_match:
                if in_block is True:
                    raise FormatError(f"End of block {start_name}" " is not detected")
                start = i
                in_block = True
                start_name = start_match.group(1).lower()
                continue

            end_match = block_finish.match(line)
            if end_match:
                finish = i
                end_name = end_match.group(1).lower()
                if in_block is False:
                    raise FormatError(f"Start of block {end_name} not" " found")
                if end_name != start_name:
                    raise FormatError(
                        f"Mismatch block names, start: {start_name}" f" finish: {end_name}"
                    )
                # Push the content of the push into the main container
                block_indices[start_name] = (start, finish)
                in_block = False
                continue

            if not in_block:
                kwlines.append(line)

        if in_block is True:
            raise FormatError(f"End of block {start_name}" " not detected")

        # Now extract block contents
        blocks = {}
        for key, index in block_indices.items():
            lines = self._lines[index[0] + 1 : index[1]]
            blocks[key.lower()] = Block(lines)

        self._blocks = blocks
        self._kwlines = kwlines
        return blocks, kwlines

    def _parse_keywords(self):
        """Parse keyword, value pairs"""
        out_dict = {}
        for line in self._kwlines:
            tokens = kw_split.split(line, 1)
            if len(tokens) == 2:
                key, value = tokens
            elif len(tokens) == 1:
                key = tokens[0]
                value = ""  # Empty string for key without values
            else:
                raise FormatError(f"Cannot parse into key-value pair in: {line}")
            if not value:
                value = ""

            out_dict[key.lower()] = value
        self._keywords = out_dict
        return out_dict

    def get_dict(self):
        """
        Get the parsed information in a dictionary in a dictionary.
        This is the main function that will be used.
        """
        if not self._keywords:
            self.parse()
        res = dict(self._keywords)
        res.update(self._blocks)
        return res


class Parser(PlainParser):
    """
    General parser class
    Try to convert data types
    bool >> int >> float >> plain text
    """

    def __init__(self, lines, convert_type=True):
        """
        Initialize the parser by passing either:
        - A list of lines to be parsed
        - A path to the file to be parsed

        :param convert_type: Either try to convert the types or not
        """
        super().__init__(lines)
        self._convert_type = convert_type

    def parse(self):
        """
        Parse the contents
        Also will try to convert the types if requested
        """
        super().parse()
        if self._convert_type is False:
            return self._keywords

        old_keywords = self._keywords

        new_keywords = {}
        for key, value in old_keywords.items():
            new_keywords[key] = convert_type_kw(value, key)

        self._keywords = new_keywords
        return None


class CannotConvertError(ValueError):
    pass


class Converter:
    """
    Class for convert that convert types
    """

    ACCEPTED_ERRORS = (ValueError,)

    def __init__(self, func):
        """
        Initialized by passing the conversion function
        """
        self.convert_func = func

    def convert(self, value):
        """
        Convert a string into python object

        Return a tuple of (success, output)
        """

        assert isinstance(value, str)
        try:
            out = self.convert_func(value)
        except self.ACCEPTED_ERRORS:
            success = False
            out = value
        else:
            success = True

        return success, out


def booltest(value):
    """Test if a string value is a Bool"""
    if value.lower().strip() == "true":
        return True
    if value.lower().strip() == "false":
        return False
    raise CannotConvertError


def emptystrtest(value):
    """Rule for empty string to be empty string"""
    if value == "":
        return value
    raise CannotConvertError


intconv = Converter(int)
floatconv = Converter(float)
intarrayconv = Converter(lambda x: list(map(int, x.split())))
floatarrayconv = Converter(lambda x: list(map(float, x.split())))
boolconv = Converter(booltest)
emptyconv = Converter(emptystrtest)


def convert_type_kw(value, key=None):
    """
    Try to convert type of the value
    """
    # the key argument is not used for now - reserve for per-key treatment
    _ = key

    # Note that the order of which these converters are call matters
    convs = [emptyconv, boolconv, intconv, floatconv, intarrayconv, floatarrayconv]
    for converter in convs:
        success, out = converter.convert(value)
        if success:
            return out
    return value
