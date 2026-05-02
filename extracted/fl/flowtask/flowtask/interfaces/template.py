from abc import ABC
from pathlib import PurePath, Path
import aiofiles
from ..exceptions import FileError, FileNotFound
from ..template import getTemplateHandler, TemplateHandler
from ..conf import FILE_STORAGES, TASK_STORAGES, TASK_PATH


class TemplateSupport(ABC):
    """TemplateSupport.

    Adding Support for Jinja2 Template parser on Components.
    """
    use_template: bool = False

    def __init__(self, *args, **kwargs):
        self._filestore = None
        self._taskstorage = None
        # Use Template:
        self.use_template: bool = kwargs.pop(
            'use_template', self.use_template
        )
        self.from_templates_dir: bool = kwargs.pop(
            'from_templates_dir', False
        )
        # Template directory
        template_dir = kwargs.pop('template_dir', None)
        super().__init__(*args, **kwargs)
        # Template Parser:
        self._templateparser: TemplateHandler = None
        if self.use_template is True:
            self._templateparser = getTemplateHandler(
                newdir=template_dir
            )

    def template_exists(self, template: str) -> bool:
        """Check if the template file exists."""
        if self._templateparser.get_template(template):
            return True
        if not self._filestore:
            self._filestore = FILE_STORAGES.get('default')
        if not self._taskstorage:
            self._taskstorage = TASK_STORAGES.get('default')
        if isinstance(template, str):
            template = Path(template)
        if not template.is_absolute():
            # Template is relative to TaskStorage:
            directory = self._taskstorage.get_path().joinpath('templates')
            template = directory.joinpath(template).resolve()
        return template.exists() and template.is_file()

    async def open_templatefile(
        self,
        file: PurePath,
        program: str = None,
        from_templates_dir: bool = False,
        folder: str = 'templates',
        **kwargs
    ) -> str:
        """
        Open a file, replace masks and parse template if needed.
        """
        if not self._filestore:
            # we need to calculate which is the filestore
            self._filestore = FILE_STORAGES.get('default')
        if not self._taskstorage:
            self._taskstorage = TASK_STORAGES.get('default')
        if isinstance(file, str):
            file = Path(file)
        if not file.is_absolute():
            # File is relative to TaskStorage:
            if from_templates_dir is True:
                directory = Path(TASK_PATH).parent.joinpath(folder)
            else:
                # Getting from default Task Storage:
                directory = self._taskstorage.get_path().joinpath(program, folder)
                if not directory.exists():
                    # Get Template From Task Path:
                    directory = Path(TASK_PATH).joinpath(program, folder)
                    if not directory.exists():
                        # Get Templates Dir from FileStore
                        directory = self._filestore.get_directory(folder, program=program)
            file = directory.joinpath(file).resolve()
        if file.exists() and file.is_file():
            content = None
            # open File:
            try:
                async with aiofiles.open(file, "r+") as afp:
                    content = await afp.read()
            except Exception as exc:
                raise FileError(
                    f"{__name__}: Error Opening File: {file}"
                ) from exc
            if self.use_template is True:
                content = self._templateparser.from_string(
                    content,
                    kwargs
                )
            elif hasattr(self, "masks"):
                content = self.mask_replacement(content)
            return content
        else:
            raise FileNotFound(
                f"{__name__}: Missing File: {file}"
            )

    async def open_tmpfile(self, file: PurePath, **kwargs) -> str:
        if file.exists() and file.is_file():
            content = None
            # open File:
            try:
                async with aiofiles.open(file, "r+") as afp:
                    content = await afp.read()
            except Exception as exc:
                raise FileError(
                    f"{self.__name__}: {exc}"
                )
                # check if we need to replace masks
            if hasattr(self, "masks"):
                self._logger.debug(
                    f"TemplateSupport Masks: {self.masks}"
                )
                if "{" in content:
                    content = self.mask_replacement(content)
            if self.use_template is True:
                content = self._templateparser.from_string(content, kwargs)
            return content
        else:
            raise FileNotFound(
                f"{self.__name__}: Missing File: {file}"
            )
