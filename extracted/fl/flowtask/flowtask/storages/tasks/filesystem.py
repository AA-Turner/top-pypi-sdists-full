from typing import Union
from pathlib import Path, PurePath
from ...exceptions import (
    FlowTaskError,
    TaskNotFound,
    TaskParseError,
    TaskDefinition,
    FileNotFound,
)
from ...parsers import JSONParser, TOMLParser, YAMLParser
from .abstract import AbstractTaskStorage


class FileTaskStorage(AbstractTaskStorage):
    """Saving Tasks on the Filesystem."""
    _name_: str = "Filesystem"

    def __init__(self, path: PurePath, *args, **kwargs):
        super(FileTaskStorage, self).__init__(*args, **kwargs)
        if not path:
            ## Default Task Path
            raise FlowTaskError(
                "Required Task Path for Filesystem Task Storage"
            )
        else:
            self.path = path
            if isinstance(path, str):
                self.path = Path(path)

    async def open_task(
        self, task: str = None, program: str = None, **kwargs
    ) -> Union[dict, str]:
        """open_task.
        Open A Task from FileSystem, support json, yaml and toml formats.
        """
        if not program:
            program = "navigator"
        taskpath = self.path.joinpath(program, "tasks")
        self.logger.notice(f"Program Task Path: {taskpath}")
        if not taskpath.exists():
            raise TaskNotFound(
                f"FlowTask: Task Path not found: {taskpath}"
            )
        ext = None
        for f in (
            "json",
            "yaml",
            "toml",
        ):
            filename = taskpath.joinpath(f"{task}.{f}")
            if filename.exists():
                self.logger.info(f"Task File: {filename}")
                ext = f
                break
        else:
            if ext is None:
                raise TaskNotFound(
                    f"FlowTask: Task {program}.{task} Not Found on file > {filename}"
                )
        try:
            if f == "json":
                parse = JSONParser(file=str(filename))
            elif f == "yaml":
                parse = YAMLParser(file=str(filename))
            elif f == "toml":
                parse = TOMLParser(file=str(filename))
            else:
                raise FlowTaskError(
                    f"Invalid File format for Task: {filename.name}"
                )
            return await parse.run()
        except TaskParseError as err:
            raise TaskParseError(f"Task Parse Error for {filename}: {err}") from err
        except Exception as err:
            raise TaskDefinition(
                f"DI: Error Parsing {f} Task in {task} \
                    for filename: {filename.name}: {err}"
            ) from err

    async def open_hook(self, filename: Union[str, PurePath]) -> Union[dict, str]:
        """open_hook.
        Open A Hook from FileSystem, support json, yaml and toml formats.
        """
        if filename.exists():
            f = filename.suffix
            try:
                if f == ".json":
                    parse = JSONParser(str(filename))
                elif f == ".yaml":
                    parse = YAMLParser(str(filename))
                elif f == ".toml":
                    parse = TOMLParser(str(filename))
                else:
                    raise FlowTaskError(
                        f"Invalid File format for Hook: {filename.name}"
                    )
                self.logger.notice(f"Hook File: {filename}")
                return await parse.run()
            except TaskParseError as err:
                raise TaskParseError(
                    f"Hook Parsing Error for {filename}: {err}"
                ) from err
            except Exception as err:
                raise FlowTaskError(
                    f"Error loading Hook {filename.name}: {err}"
                ) from err
        else:
            raise FileNotFound(f"Hook Not Found on file > {filename}")
