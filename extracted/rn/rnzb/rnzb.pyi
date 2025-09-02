from collections.abc import Sequence
from datetime import datetime
from os import PathLike
from typing import Final, final

__all__: Final = ("File", "InvalidNzbError", "Meta", "Nzb", "Segment")

@final
class InvalidNzbError(Exception):
    """Raised when the NZB is invalid."""

@final
class Meta:
    """Optional creator-definable metadata for the contents of the NZB."""

    title: str | None
    """Title."""

    passwords: tuple[str, ...]
    """Passwords."""

    tags: tuple[str, ...]
    """Tags."""

    category: str | None
    """Category."""

    def __new__(
        cls,
        *,
        title: str | None = None,
        passwords: Sequence[str] = (),
        tags: Sequence[str] = (),
        category: str | None = None,
    ) -> Meta:
        """Create a new instance of Meta."""

    def __eq__(self, value: object) -> bool: ...
    def __hash__(self) -> int: ...

@final
class Segment:
    """One part segment of a file."""

    size: int
    """Size of the segment."""
    number: int
    """Number of the segment."""
    message_id: str
    """Message ID of the segment."""

    def __new__(cls, *, size: int, number: int, message_id: str) -> Segment:
        """Create a new instance of Segment."""

    def __eq__(self, value: object) -> bool: ...
    def __hash__(self) -> int: ...

@final
class File:
    """Represents a complete file, consisting of segments that make up a file."""

    poster: str
    """The poster of the file."""

    posted_at: datetime
    """The date and time when the file was posted, in UTC."""

    subject: str
    """The subject of the file."""

    groups: tuple[str, ...]
    """Groups that reference the file."""

    segments: tuple[Segment, ...]
    """Segments that make up the file."""

    def __new__(
        cls,
        *,
        poster: str,
        posted_at: datetime,
        subject: str,
        groups: Sequence[str],
        segments: Sequence[Segment],
    ) -> File:
        """Create a new instance of File."""

    def __eq__(self, value: object) -> bool: ...
    def __hash__(self) -> int: ...
    @property
    def size(self) -> int:
        """Size of the file calculated from the sum of segment sizes."""

    @property
    def name(self) -> str | None:
        """
        Complete name of the file with it's extension extracted from the subject.
        May return `None` if it fails to extract the name.
        """

    @property
    def stem(self) -> str | None:
        """
        Base name of the file without it's extension extracted from the [`File.name`][rnzb.File.name].
        May return `None` if it fails to extract the stem.
        """

    @property
    def extension(self) -> str | None:
        """
        Extension of the file without the leading dot extracted from the [`File.name`][rnzb.File.name].
        May return `None` if it fails to extract the extension.
        """

    def has_extension(self, ext: str, /) -> bool:
        """
        Check if the file has the specified extension.

        This method ensures consistent extension comparison
        by normalizing the extension (removing any leading dot)
        and handling case-folding.

        Parameters
        ----------
        ext : str
            Extension to check for, with or without a leading dot (e.g., `.txt` or `txt`).

        Returns
        -------
        bool
            `True` if the file has the specified extension, `False` otherwise.

        Examples
        --------
        ```python
        >>> file.has_extension('.TXT')  # True for 'file.txt'
        True
        >>> file.has_extension('txt')   # Also True for 'file.txt'
        True
        ```

        """

    def is_par2(self) -> bool:
        """
        Return `True` if the file is a `.par2` file, `False` otherwise.
        """

    def is_rar(self) -> bool:
        """
        Return `True` if the file is a `.rar` file, `False` otherwise.
        """

    def is_obfuscated(self) -> bool:
        """
        Return `True` if the file is obfuscated, `False` otherwise.
        """

@final
class Nzb:
    """Represents a complete NZB file."""

    meta: Meta
    """Optional creator-definable metadata for the contents of the NZB."""

    files: tuple[File, ...]
    """File objects representing the files included in the NZB."""

    def __new__(cls, *, meta: Meta, files: Sequence[File]) -> Nzb:
        """Create a new instance of NZB."""

    def __eq__(self, value: object) -> bool: ...
    def __hash__(self) -> int: ...
    @classmethod
    def from_str(cls, nzb: str, /) -> Nzb:
        """
        Parse the given string into an [`Nzb`][rnzb.Nzb].

        Parameters
        ----------
        nzb : str
            NZB string.

        Returns
        -------
        Nzb
            Object representing the parsed NZB file.

        Raises
        ------
        InvalidNzbError
            Raised if the NZB is invalid.

        """

    @classmethod
    def from_file(cls, nzb: str | PathLike[str], /) -> Nzb:
        """
        Parse the given file into an [`Nzb`][nzb.Nzb].
        Handles both regular and gzipped NZB files.

        Parameters
        ----------
        nzb : str | PathLike[str]
            Path to the NZB file.

        Returns
        -------
        Nzb
            Object representing the parsed NZB file.

        Raises
        ------
        FileNotFoundError
            Raised if the specified file doesn't exist.

        InvalidNzbError
            Raised if the NZB is invalid.

        """

    @classmethod
    def from_json(cls, json: str, /) -> Nzb:
        """
        Deserialize the given JSON string into an [`Nzb`][rnzb.Nzb].

        Parameters
        ----------
        json : str
            JSON string representing the NZB.

        Returns
        -------
        Nzb
            Object representing the parsed NZB file.

        Raises
        ------
        InvalidNzbError
            Raised if the NZB is invalid.

        """

    def to_json(self, *, pretty: bool = False) -> str:
        """
        Serialize the [`Nzb`][rnzb.Nzb] object into a JSON string.

        Parameters
        ----------
        pretty : bool, optional
            Whether to pretty format the JSON string.

        Returns
        -------
        str
            JSON string representing the NZB.

        """

    @property
    def file(self) -> File:
        """
        The main content file (episode, movie, etc) in the NZB.
        This is determined by finding the largest non `par2` file in the NZB
        and may not always be accurate.
        """

    @property
    def size(self) -> int:
        """Total size of all the files in the NZB."""

    @property
    def filenames(self) -> tuple[str, ...]:
        """
        Tuple of unique file names across all the files in the NZB.
        May return an empty tuple if it fails to extract the name for every file.
        """

    @property
    def posters(self) -> tuple[str, ...]:
        """
        Tuple of unique posters across all the files in the NZB.
        """

    @property
    def groups(self) -> tuple[str, ...]:
        """
        Tuple of unique groups across all the files in the NZB.
        """

    @property
    def par2_files(self) -> tuple[File, ...]:
        """
        Tuple of par2 files in the NZB.
        """

    @property
    def par2_size(self) -> int:
        """
        Total size of all the `.par2` files.
        """

    @property
    def par2_percentage(self) -> float:
        """
        Percentage of the size of all the `.par2` files relative to the total size.
        """

    def has_extension(self, ext: str, /) -> bool:
        """
        Check if any file in the NZB has the specified extension.

        This method ensures consistent extension comparison
        by normalizing the extension (removing any leading dot)
        and handling case-folding.

        Parameters
        ----------
        ext : str
            Extension to check for, with or without a leading dot (e.g., `.txt` or `txt`).

        Returns
        -------
        bool
            `True` if any file in the NZB has the specified extension, `False` otherwise.
        ```

        """

    def has_rar(self) -> bool:
        """
        Return `True` if any file in the NZB is a `.rar` file, `False` otherwise.
        """

    def is_rar(self) -> bool:
        """
        Return `True` if all files in the NZB are `.rar` files, `False` otherwise.
        """

    def is_obfuscated(self) -> bool:
        """
        Return `True` if any file in the NZB is obfuscated, `False` otherwise.
        """

    def has_par2(self) -> bool:
        """
        Return `True` if there's at least one `.par2` file in the NZB, `False` otherwise.
        """
