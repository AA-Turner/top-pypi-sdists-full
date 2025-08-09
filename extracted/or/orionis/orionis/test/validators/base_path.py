from pathlib import Path
from orionis.test.exceptions import OrionisTestValueError

class __ValidBasePath:

    def __call__(self, base_path) -> Path:
        """
        Validates and normalizes a base path.

        Parameters
        ----------
        base_path : str or Path
            The base path to validate. Must be a non-empty string or a Path object.

        Returns
        -------
        Path
            A normalized Path object corresponding to the provided base path.

        Raises
        ------
        OrionisTestValueError
            If `base_path` is not a non-empty string or a valid Path object.
        """

        if isinstance(base_path, str):
            base_path = base_path.strip()
            if not base_path:
                raise OrionisTestValueError(
                    "Invalid base_path: Expected a non-empty string or Path."
                )
            return Path(base_path)

        elif isinstance(base_path, Path):
            if not str(base_path).strip():
                raise OrionisTestValueError(
                    "Invalid base_path: Path cannot be empty."
                )
            return base_path

        else:
            raise OrionisTestValueError(
                f"Invalid base_path: Expected a non-empty string or Path, got '{str(base_path)}' ({type(base_path).__name__})."
            )

# Exported singleton instance
ValidBasePath = __ValidBasePath()
