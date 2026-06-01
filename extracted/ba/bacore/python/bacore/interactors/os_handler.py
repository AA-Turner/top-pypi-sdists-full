"""OS handling interactors."""
import platform
from bacore.domain.protocols import Exists
from bacore.domain.settings import System


def command_on_path(command: Exists) -> bool:
    """Check if CLI command is on path."""
    return command.exists()


def system_information_os(func_os: callable = platform.system()) -> System:
    """Retrieve system information."""
    information = System(os=func_os)
    return information
