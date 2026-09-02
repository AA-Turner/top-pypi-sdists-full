import shutil
from .base import FileBase


class FileCopy(FileBase):
    def __init__(self, *args, **kwargs):
        self.move = kwargs.pop("move", False)
        super(FileCopy, self).__init__(*args, **kwargs)

    async def __call__(self, *args, **kwargs):
        self.start()
        for src in self._filenames:
            dest = self.destination.joinpath(src.name)
            if self.move:
                shutil.move(src, dest)
                # self._logger.info(
                #     f"Moved file {src} to {dest}"
                # )
            else:
                shutil.copy2(src, dest)
                # self._logger.info(
                #     f"Copied file {src} to {dest}"
                # )
