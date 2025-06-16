class MarkdownException(Exception):
    """Raised when an exception occurs."""


class Markdown:
    """
    Markdown class.

    Attributes
    ----------
    filename : str
        filename where the markdown will be saved when the write_to_file() function is called
    """

    def __init__(self, filename: str = None):
        self.filename = filename

    @staticmethod
    def __header(n: int, header: str) -> str:
        """
        Returns a formatted header.

        :param n: number of '#' characters to be inserted
        :type n: int
        :param header: the header text
        :type header: str
        :return: the formatted header
        :rtype: str
        """
        return f'{"#" * n} {header}\n\n'

    def h1(self, h1: str) -> str:
        """
        Returns a formatted h1 header.

        :param h1: the header text
        :type h1: str
        :return: the formatted header
        :rtype: str
        """
        return self.__header(1, h1)

    def h2(self, h2: str) -> str:
        """
        Returns a formatted h2 header.

        :param h2: the header text
        :type h2: str
        :return: the formatted header
        :rtype: str
        """
        return self.__header(2, h2)

    def h3(self, h3: str) -> str:
        """
        Returns a formatted h3 header.

        :param h3: the header text
        :type h3: str
        :return: the formatted header
        :rtype: str
        """
        return self.__header(3, h3)

    def h4(self, h4: str) -> str:
        """
        Returns a formatted h4 header.

        :param h4: the header text
        :type h4: str
        :return: the formatted header
        :rtype: str
        """
        return self.__header(4, h4)

    def h5(self, h5: str) -> str:
        """
        Returns a formatted h5 header.

        :param h5: the header text
        :type h5: str
        :return: the formatted header
        :rtype: str
        """
        return self.__header(5, h5)

    def h6(self, h6: str) -> str:
        """
        Returns a formatted h6 header.

        :param h6: the header text
        :type h6: str
        :return: the formatted header
        :rtype: str
        """
        return self.__header(6, h6)

    @staticmethod
    def code_block(text: str, lang: str = '') -> str:
        """
        Returns a formatted code block.

        :param text: the text to be placed in the code block
        :type text: str
        :param lang: the code language
        :type lang: str
        :return: the formatted code block
        :rtype: str
        """
        return text.replace(text, f'```{lang}\n{text}\n```\n\n')

    @staticmethod
    def link(text: str, link: str) -> str:
        """
        Returns a formatted link.

        :param text: the text to be shown for the link
        :type text: str
        :param link: the link
        :type link: str
        :return: the formatted link
        :rtype: str
        """
        return f'[{text}]({link})'

    @staticmethod
    def hr() -> str:
        """
        Returns a horizontal rule.

        :return: a horizontal rule.
        :rtype: str
        """
        return '\n\n---\n'

    @staticmethod
    def blockquotes(text: str) -> str:
        """
        Returns a formatted blockquote.

        :param text: the text to be placed in the blockquote
        :type text: str
        :return: the formatted blockquote
        :rtype: str
        """
        return f'> {text}\n\n'

    def write_to_file(self, text: str, mode: str = 'a+'):
        """
        Writes the text to the file.

        :param text: the text to be written to the file
        :type text: str
        :param mode: the mode used when opening the file
        :type mode: str
        """
        if self.filename:
            with open(self.filename, mode) as f:
                f.write(text)

    @staticmethod
    def __emphasis(text: str, modifier: str, substrs: list = None) -> str:
        """
        Returns a formatted text with the given modifier.

        :param text: the text to be formatted
        :type text: str
        :param modifier: the modifier to be applied to the text
        :type modifier: str
        :param substrs: the list of words or sentences to be formatted, if None, the whole text will be formatted
        :type substrs: list
        :return: the formatted text
        :rtype: str
        """
        if not substrs:
            text = f'{modifier}{text}{modifier}'
        else:
            for sub in substrs:
                text = text.replace(f' {sub} ', f' {modifier}{sub}{modifier} ')
            words = text.split()
            if words[0] in substrs:
                text = text.replace(f'{words[0]} ', f'{modifier}{words[0]}{modifier} ', 1)
            if len(words) > 1 and words[len(words) - 1] in substrs:
                text = f' {modifier}{words[len(words) - 1]}{modifier}'.join(text.rsplit(f' {words[len(words) - 1]}', 1))
        return text

    def italic(self, text: str, substrs: list = None) -> str:
        """
        Returns a formatted text using italic.

        :param text: the text to be formatted
        :type text: str
        :param substrs: the list of words or sentences to be formatted, if None, the whole text will be formatted
        :type substrs: list
        :return: the formatted text
        :rtype: str
        """
        return self.__emphasis(text, '*', substrs)

    def bold(self, text: str, substrs: list = None) -> str:
        """
        Returns a formatted text using bold.

        :param text: the text to be formatted
        :type text: str
        :param substrs: the list of words or sentences to be formatted, if None, the whole text will be formatted
        :type substrs: list
        :return: the formatted text
        :rtype: str
        """
        return self.__emphasis(text, '__', substrs)

    def strikethrough(self, text: str, substrs: list = None) -> str:
        """
        Returns a formatted text using strikethrough.

        :param text: the text to be formatted
        :type text: str
        :param substrs: the list of words or sentences to be formatted, if None, the whole text will be formatted
        :type substrs: list
        :return: the formatted text
        :rtype: str
        """
        return self.__emphasis(text, '~~', substrs)

    def inline_code(self, text: str, substrs: list = None) -> str:
        """
        Returns a formatted text using inline code.

        :param text: the text to be formatted
        :type text: str
        :param substrs: the list of words or sentences to be formatted, if None, the whole text will be formatted
        :type substrs: list
        :return: the formatted text
        :rtype: str
        """
        return self.__emphasis(text, '`', substrs)

    def table_header(self, header: list) -> str:
        """
        Returns a formatted table header.

        :param header: the cells for the table header
        :type header: list
        :return: the formatted table header
        :rtype: str
        """
        return f"{self.table_row(header)}{self.table_row(['---' for _ in header])}"

    @staticmethod
    def table_row(row: list) -> str:
        """
        Returns a formatted table row.

        :param row: the cells for the table row
        :type row: list
        :return: the formatted table row
        :rtype: str
        """
        return f'|{"|".join(row)}|\n'

    def table(self, header: list, rows: list) -> str:
        """
        Returns a formatted table.

        :param header: the header for the table
        :type header: list
        :param rows: the rows for the table
        :type rows: list
        :return: the formatted table
        :rtype: str
        """
        for row in rows:
            if type(row) != list:
                raise MarkdownException('rows should be a list of lists')
            if len(row) != len(header):
                raise MarkdownException('size mismatch between header and rows')
        _header = self.table_header(header)
        _rows = ''
        for row in rows:
            _rows += self.table_row(row)
        return f'{_header}{_rows}'

    def __make_list(self, items: list, list_type: str, tab: int = 0) -> str:
        """
        Returns a formatted list.

        :param items: the list to be formatted
        :type items: list
        :param list_type: the type of the list (unordered, ordered)
        :type list_type: str
        :param tab: number of tab characters to be inserted
        :type tab: int
        :return: str
        :rtype: the formatted list
        """
        text = ''
        for item in items:
            if type(item) == list:
                text += self.__make_list(item, list_type, tab + 1)
            else:
                text += '{}{} {}\n'.format("\t" * tab, list_type, item)
        return text

    def unordered_list(self, items: list) -> str:
        """
        Returns a formatted unordered list.

        :param items: the list to be formatted
        :type items: list
        :return: the formatted list
        :rtype: str
        """
        return f"{self.__make_list(items, '-')}\n"

    def ordered_list(self, items: list) -> str:
        """
        Returns a formatted ordered list.

        :param items: the list to be formatted
        :type items: list
        :return: the formatted list
        :rtype: str
        """
        return f"{self.__make_list(items, '1.')}\n"
