from pathlib import Path
from orionis.test.exceptions import OrionisTestValueError

class __ValidFolderPath:

    def __call__(self, folder_path: str) -> str:
        """
        Validate and clean a folder path string.

        Parameters
        ----------
        folder_path : str
            The folder path to validate.

        Returns
        -------
        str
            The cleaned folder path string.

        Raises
        ------
        OrionisTestValueError
            If the folder_path is not a non-empty string.
        """

        if not isinstance(folder_path, str) or not folder_path.strip():
            raise OrionisTestValueError(
                f"Invalid folder_path: Expected a non-empty string, got '{str(folder_path)}' ({type(folder_path).__name__})."
            )

        return folder_path.strip()

# Exported singleton instance
ValidFolderPath = __ValidFolderPath()
