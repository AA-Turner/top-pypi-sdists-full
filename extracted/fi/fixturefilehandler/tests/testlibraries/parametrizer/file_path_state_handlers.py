"""This module implements file state dependencies."""
from abc import abstractmethod
from pathlib import Path

from fixturefilehandler.file_paths import RelativeDeployFilePath
from tests.testlibraries.parametrizer.checkers import ContentChecker, NotExistChecker


class FilePathStateHandler:
    """This class implements abstract file state dependency."""

    FILE_NAME_IN_DIRECTORY: Path = Path("file.txt")

    @classmethod
    @abstractmethod
    def create_checker(cls, path: Path):
        """This method returns checker."""

    @classmethod
    @abstractmethod
    def create_file(cls, file_path: RelativeDeployFilePath):
        """This method returns checker."""

    @classmethod
    @abstractmethod
    def create_directory(cls, file_path: RelativeDeployFilePath):
        """This method returns checker."""

    @classmethod
    def assert_file_state(cls, path: Path):
        """This method checks file state."""
        checker = cls.create_checker(path)
        checker.do_assertion()

    @classmethod
    def assert_directory_state(cls, path: Path):
        """This method checks file state."""
        checker = cls.create_checker(path / cls.FILE_NAME_IN_DIRECTORY)
        checker.do_assertion()


class NoExistHandler(FilePathStateHandler):
    """This class implements abstract file state dependency on case when not exist."""

    @classmethod
    def create_checker(cls, path: Path):
        return NotExistChecker(path)

    @classmethod
    def create_file(cls, file_path: RelativeDeployFilePath):
        pass

    @classmethod
    def create_directory(cls, file_path: RelativeDeployFilePath):
        pass

    @classmethod
    def assert_directory_state(cls, path: Path):
        """This method checks file state."""
        checker = cls.create_checker(path)
        checker.do_assertion()


class ContentExistingHandler(FilePathStateHandler):
    """This class implements abstract file state dependency on case when existing content."""

    CONTENT = "Content in existing file"

    @classmethod
    def create_checker(cls, path: Path):
        return ContentChecker(path, cls.CONTENT)

    @classmethod
    def create_file(cls, file_path: RelativeDeployFilePath):
        file_path.target.write_text(cls.CONTENT)

    @classmethod
    def create_directory(cls, file_path: RelativeDeployFilePath):
        file_path.target.mkdir()
        (file_path.target / cls.FILE_NAME_IN_DIRECTORY).write_text(cls.CONTENT)


class ContentBackupHandler(FilePathStateHandler):
    """This class implements abstract file state dependency on case when backup content."""

    CONTENT = "Content in backup file"

    @classmethod
    def create_checker(cls, path: Path):
        return ContentChecker(path, cls.CONTENT)

    @classmethod
    def create_file(cls, file_path: RelativeDeployFilePath):
        file_path.backup.write_text(cls.CONTENT)

    @classmethod
    def create_directory(cls, file_path: RelativeDeployFilePath):
        file_path.backup.mkdir()
        (file_path.backup / cls.FILE_NAME_IN_DIRECTORY).write_text(cls.CONTENT)


class ContentResourceHandler(FilePathStateHandler):
    """This class implements abstract file state dependency on case when resource content."""

    CONTENT = "Content in resource file"

    @classmethod
    def create_checker(cls, path: Path):
        return ContentChecker(path, cls.CONTENT)

    @classmethod
    def create_file(cls, file_path: RelativeDeployFilePath):
        file_path.resource.write_text(cls.CONTENT)

    @classmethod
    def create_directory(cls, file_path: RelativeDeployFilePath):
        file_path.resource.mkdir()
        (file_path.resource / cls.FILE_NAME_IN_DIRECTORY).write_text(cls.CONTENT)
