from .base import FileBase


class FileDelete(FileBase):
    async def __call__(self, *args, **kwargs):
        self.start()
        for filename in self._filenames:
            if filename.exists() and filename.is_file():
                try:
                    filename.unlink()
                except Exception as e:
                    self._logger.error(f"Error deleting {filename}: {e}")
            else:
                self._logger.warning(
                    f"{filename} does not exist or is not a file."
                )
