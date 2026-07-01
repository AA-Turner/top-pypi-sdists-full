import re
from abc import ABC, abstractmethod

FILE_PATTERN = re.compile(r"\{\{[^\{\}]+\}\}")


class Messaging(ABC):
    @abstractmethod
    def connect(self):
        pass

    EXIT_CODE_INVALID_CREDENTIALS = 200
    EXIT_CODE_INVALID_INPUT = 201
    EXIT_CODE_RATE_LIMIT = 202
    EXIT_CODE_BAD_REQUEST = 203
    EXIT_CODE_FILE_NOT_FOUND = 204
    EXIT_CODE_UNKNOWN_ERROR = 249

    @classmethod
    def message_content_file_injection(self, message: str) -> str:
        """
        Extracts the contents of a file from a message, if a file pattern is present.
        Message pattern: {{text:file.txt}}

        Args:
            message (str): The message

        Returns:
            str: The message with the file contents injected, if a file pattern is present.

        Raises:
            ExitCodeException: If the file pattern is invalid or the file is not found.
        """

        def _extract_filename(message: str) -> str:
            from shipyard_templates import ExitCodeException

            match = FILE_PATTERN.search(message)
            if not match:
                raise ExitCodeException(
                    "No file pattern found in the message.",
                    self.EXIT_CODE_INVALID_INPUT,
                )
            matched = match.group()[
                2:-2
            ].strip()  # Extract the matched text without the curly braces

            if not matched.startswith("text:"):
                raise ExitCodeException(
                    "When using the file pattern, the parameter needs to be prefixed with 'text:'",
                    self.EXIT_CODE_INVALID_INPUT,
                )
            return matched[5:]  # Remove the 'text:' prefix

        def _read_file(file_path: str, message: str) -> str:
            from shipyard_templates import ExitCodeException

            try:
                with open(file_path.strip(), "r") as f:
                    content = f.read()
            except FileNotFoundError as e:
                raise ExitCodeException(
                    f"Could not load the contents of file {file_path}. Make sure the file exists",
                    Messaging.EXIT_CODE_FILE_NOT_FOUND,
                ) from e
            except OSError as e:
                raise ExitCodeException(
                    f"Error opening file {file_path}.",
                    Messaging.EXIT_CODE_INVALID_INPUT,
                ) from e

            return FILE_PATTERN.sub("", message, count=1) + "\n\n" + content

        if not re.search(FILE_PATTERN, message):
            return message

        file = _extract_filename(message)
        return _read_file(file, message)
