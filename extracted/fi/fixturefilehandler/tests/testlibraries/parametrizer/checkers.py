"""This module implements checker."""
from abc import abstractmethod
from pathlib import Path


class AbstractChecker:
    """This class implements abstruct checker."""

    def __init__(self, path: Path):
        self.path = path

    @abstractmethod
    def do_assertion(self):
        """This method assert something."""


class NotExistChecker(AbstractChecker):
    """This class implements checker in case when want to check that file not exist."""

    def do_assertion(self):
        assert not self.path.exists()


class ContentChecker(AbstractChecker):
    """This class implements checker in case when want to check that file content is as same as expected."""

    def __init__(self, path: Path, content: str):
        super().__init__(path)
        self.content = content

    def do_assertion(self):
        assert self.path.read_text() == self.content
