from qwak.inner.build_logic.interface.step_inteface import Step

from qwak_sdk import __version__ as qwak_sdk_version


class SdkVersionStep(Step):
    def description(self) -> str:
        return "Getting SDK Version"

    def execute(self) -> None:
        self.build_logger.debug(
            "Getting sdk version"
        )
        self.context.qwak_sdk_version = qwak_sdk_version
