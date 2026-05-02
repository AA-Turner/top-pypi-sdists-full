from typing import Union
from ...parsers import JSONParser, TOMLParser, YAMLParser
from ...exceptions import TaskParseError
from .abstract import AbstractTaskStorage


class MemoryTaskStorage(AbstractTaskStorage):
    """Executing Task from Memory."""
    _name_: str = "Memory"

    def __init__(self, *args, **kwargs):
        super(MemoryTaskStorage, self).__init__(*args, **kwargs)
        self.content = None
        self.filename = ":memory:"

    async def open_task(
        self,
        payload: str = None,
        task: str = None,
        program: str = None,
        **kwargs
    ) -> Union[dict, str]:
        """open_task.
        Open A Task from Memory.
        """
        error = None
        for f in ("json", "yaml", "toml"):
            # check every one:
            try:
                if f == "json":
                    parse = JSONParser(content=payload)
                    return await parse.run()
                elif f == "yaml":
                    parse = YAMLParser(content=payload)
                    return await parse.run()
                elif f == "toml":
                    parse = TOMLParser(content=payload)
                    return await parse.run()
            except TaskParseError as e:
                error = e
                continue
        else:
            raise TaskParseError(
                f"Task Parse Error: {error}"
            )
