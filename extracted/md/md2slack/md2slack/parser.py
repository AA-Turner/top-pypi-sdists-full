from .lexer import SlackBlockLexer, SlackInlineLexer
from .renderer import SlackRenderer
import re

class SlackMarkdown:
    """
    Main Markdown parser class that combines lexing, parsing, and rendering.
    This class processes Markdown text and converts it to Slack-compatible formatting.
    """
    
    def __init__(self):
        """
        Initializes the SlackMarkdown parser with block and inline lexers,
        as well as the SlackRenderer for final output formatting.
        """
        self.block_lexer = SlackBlockLexer()
        self.inline_lexer = SlackInlineLexer()
        self.renderer = SlackRenderer()
    
    def __call__(self, text):
        """
        Enables the SlackMarkdown instance to be called directly to parse text.

        Args:
            text (str): The Markdown text to be processed.

        Returns:
            str: The formatted Slack-compatible output.
        """
        return self.parse(text)

    def parse(self, text):
        # Ensure fresh instance each time
        self.block_lexer = SlackBlockLexer()
        self.inline_lexer = SlackInlineLexer()
        self.renderer = SlackRenderer()

        # Continue parsing as usual
        text = self._preprocess(text)
        tokens = self.block_lexer.tokenize(text)

        for token in tokens:
            if not token.get("raw", False):
                token["value"] = self.inline_lexer.parse(token["value"])

        return self.renderer.render(tokens).strip()

    
    @staticmethod
    def _preprocess(text, tab=4):
        """
        Cleans up the input text by normalizing newlines and trimming spaces.

        Args:
            text (str): The input text to preprocess.
            tab (int, optional): The number of spaces per tab. Defaults to 4.

        Returns:
            str: The cleaned-up text.
        """
        text = re.sub(r'\r\n|\r', '\n', text)
        text = text.expandtabs(tab)
        text = re.sub(r'[ \t]+\n', '\n', text)  # Trim spaces at line ends
        return text.strip() + '\n'
