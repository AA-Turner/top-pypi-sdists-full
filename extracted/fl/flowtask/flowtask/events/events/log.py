from navconfig import DEBUG
from navconfig.logging import logging
from .abstract import AbstractEvent


class LogEvent(AbstractEvent):
    def __init__(self, *args, **kwargs):
        super(LogEvent, self).__init__(*args, **kwargs)
        self.use_notice: bool = kwargs.pop("use_notice", False)
        self._logger = logging.getLogger(
            "FlowTask.LogEvent"
        )

    async def __call__(self, *args, **kwargs):
        msg = kwargs.pop("message", None)
        cls = kwargs.pop("cls", None)
        if not msg:
            msg = getattr(cls, "message", str(cls))
        if DEBUG:
            self.echo(msg, level="WARN")
            self._logger.debug(msg)
        else:
            if self.use_notice is True:
                self._logger.notice(msg)
            else:
                self._logger.info(msg)
