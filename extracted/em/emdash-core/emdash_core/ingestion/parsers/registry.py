"""Registry for language-specific parsers."""

from typing import Dict, Type, Optional, List
from pathlib import Path

from .base_parser import BaseLanguageParser
from ...utils.logger import log


class ParserRegistry:
    """Registry for language-specific parsers.

    Maps file extensions to parser classes and provides
    lookup functionality for multi-language support.
    """

    _parsers: Dict[str, Type[BaseLanguageParser]] = {}

    @classmethod
    def register(cls, parser_class: Type[BaseLanguageParser]):
        """Register a parser for its supported file extensions.

        Args:
            parser_class: Parser class to register
        """
        extensions = parser_class.get_supported_extensions()
        for ext in extensions:
            cls._parsers[ext.lower()] = parser_class
            log.debug(f"Registered {parser_class.__name__} for {ext}")

    @classmethod
    def get_parser(cls, file_path: Path) -> Optional[Type[BaseLanguageParser]]:
        """Get parser class for a file based on extension.

        Args:
            file_path: Path to source file

        Returns:
            Parser class or None if not supported
        """
        ext = file_path.suffix.lower()
        return cls._parsers.get(ext)

    @classmethod
    def get_all_extensions(cls) -> List[str]:
        """Get all supported file extensions.

        Returns:
            List of file extensions (e.g., ['.py', '.ts', '.js'])
        """
        return list(cls._parsers.keys())

    @classmethod
    def is_supported(cls, file_path: Path) -> bool:
        """Check if file extension is supported.

        Args:
            file_path: Path to check

        Returns:
            True if supported, False otherwise
        """
        return file_path.suffix.lower() in cls._parsers

    @classmethod
    def list_parsers(cls) -> Dict[str, str]:
        """List all registered parsers.

        Returns:
            Dictionary mapping extension to parser class name
        """
        return {ext: parser.__name__ for ext, parser in cls._parsers.items()}
