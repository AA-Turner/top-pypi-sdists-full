from adam.commands.fs.rm_downloads import RmDownloads
from adam.commands.fs.rm_logs_local import RmLogsLocal
from adam.commands.intermediate_command import IntermediateCommand

class RmLocal(IntermediateCommand):
    COMMAND = ':rm'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(RmLocal, cls).__new__(cls)

        return cls.instance

    def command(self):
        return RmLocal.COMMAND

    def cmd_list(self):
        return [RmDownloads(), RmLogsLocal()]