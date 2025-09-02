from adam.commands.app import App
from adam.commands.app_ping import AppPing
from adam.commands.frontend.code_start import CodeStart
from adam.commands.frontend.code_stop import CodeStop
from adam.commands.show.show_app_queues import ShowAppQueues
from adam.commands.cp import ClipboardCopy
from adam.commands.bash import Bash
from adam.commands.cd import Cd
from adam.commands.check import Check
from adam.commands.command import Command
from adam.commands.cqlsh import Cqlsh
from adam.commands.devices import DeviceApp, DeviceCass, DevicePostgres
from adam.commands.exit import Exit
from adam.commands.medusa.medusa import Medusa
from adam.commands.param_get import GetParam
from adam.commands.issues import Issues
from adam.commands.ls import Ls
from adam.commands.nodetool import NodeTool
from adam.commands.postgres.postgres import Postgres
from adam.commands.preview_table import PreviewTable
from adam.commands.pwd import Pwd
from adam.commands.reaper.reaper import Reaper
from adam.commands.repair.repair import Repair
from adam.commands.report import Report
from adam.commands.restart import Restart
from adam.commands.rollout import RollOut
from adam.commands.param_set import SetParam
from adam.commands.show.show import Show
from adam.commands.show.show_app_actions import ShowAppActions
from adam.commands.show.show_app_id import ShowAppId
from adam.commands.show.show_cassandra_status import ShowCassandraStatus
from adam.commands.show.show_cassandra_version import ShowCassandraVersion
from adam.commands.show.show_commands import ShowKubectlCommands
from adam.commands.show.show_login import ShowLogin
from adam.commands.show.show_params import ShowParams
from adam.commands.show.show_processes import ShowProcesses
from adam.commands.show.show_repairs import ShowRepairs
from adam.commands.show.show_storage import ShowStorage
from adam.commands.show.show_adam import ShowAdam
from adam.commands.watch import Watch

class ReplCommands:
    def repl_cmd_list() -> list[Command]:
        cmds: list[Command] = ReplCommands.navigation() + ReplCommands.cassandra_check() + ReplCommands.cassandra_ops() + \
            ReplCommands.tools() + ReplCommands.app() + ReplCommands.exit()

        intermediate_cmds: list[Command] = [Show(), App(), Reaper(), Repair()]
        ic = [c.command() for c in intermediate_cmds]
        # 1. dedup commands
        deduped = []
        cs = set()
        for cmd in cmds:
            if cmd.command() not in cs and cmd.command() not in ic:
                deduped.append(cmd)
                cs.add(cmd.command())
        # 2. intermediate commands must be added to the end
        deduped.extend(intermediate_cmds)

        # Command.print_chain(Command.chain(cmds))

        return deduped

    def navigation() -> list[Command]:
        return [Ls(), PreviewTable(), DeviceApp(), DevicePostgres(), DeviceCass(), Cd(), Pwd(), ClipboardCopy(),
                GetParam(), SetParam(), ShowParams(), ShowKubectlCommands(), ShowLogin(), ShowAdam()]

    def cassandra_check() -> list[Command]:
        return [ShowCassandraStatus(), ShowCassandraVersion(), ShowRepairs(), ShowStorage(), ShowProcesses(), Check(), Issues(), NodeTool(), Report()]

    def cassandra_ops() -> list[Command]:
        return Medusa.cmd_list() + [Restart(), RollOut(), Watch()] + Reaper.cmd_list() + Repair.cmd_list()

    def tools() -> list[Command]:
        return [Cqlsh(), Postgres(), Bash(), CodeStart(), CodeStop()]

    def app() -> list[Command]:
        return [ShowAppActions(), ShowAppId(), ShowAppQueues(), AppPing(), App()]

    def exit() -> list[Command]:
        return [Exit()]