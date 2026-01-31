from adam.commands.app.app import App
from adam.commands.app.app_ping import AppPing
from adam.commands.app.show_app_actions import ShowAppActions
from adam.commands.app.show_app_id import ShowAppId
from adam.commands.app.show_app_queues import ShowAppQueues
from adam.commands.audit.audit import Audit
from adam.commands.cassandra.restart_cluster import RestartCluster
from adam.commands.cassandra.restart_nodes import RestartNodes
from adam.commands.cassandra.rollout import RollOut
from adam.commands.cassandra.show_cassandra_repairs import ShowCassandraRepairs
from adam.commands.cassandra.show_cassandra_ring import ShowCassandraRing
from adam.commands.cassandra.show_cassandra_status import ShowCassandraStatus
from adam.commands.cassandra.show_node_restartable import ShowNodeRestartable
from adam.commands.cassandra.show_cassandra_version import ShowCassandraVersion
from adam.commands.cassandra.show_processes import ShowProcesses
from adam.commands.cassandra.show_storage import ShowStorage
from adam.commands.cassandra.watch import Watch
from adam.commands.cli.clipboard_copy import ClipboardCopy
from adam.commands.config.param_get import GetParam
from adam.commands.config.param_set import SetParam
from adam.commands.debug.show_offloaded_completes import ShowOffloadedCompletes
from adam.commands.diag.check import Check
from adam.commands.diag.generate_report import GenerateReport
from adam.commands.diag.issues import Issues
from adam.commands.fs.cat import Cat
from adam.commands.code import Code
from adam.commands.cql.alter_tables import AlterTables
from adam.commands.debug.debug import Debug
from adam.commands.cassandra.download_cassandra_log import DownloadCassandraLog
from adam.commands.fs.cat_local import CatLocal
from adam.commands.fs.download_file import DownloadFile
from adam.commands.deploy.code_start import CodeStart
from adam.commands.deploy.code_stop import CodeStop
from adam.commands.deploy.deploy import Deploy
from adam.commands.deploy.deploy_frontend import DeployFrontend
from adam.commands.deploy.deploy_pg_agent import DeployPgAgent
from adam.commands.deploy.deploy_pod import DeployPod
from adam.commands.deploy.undeploy import Undeploy
from adam.commands.deploy.undeploy_frontend import UndeployFrontend
from adam.commands.deploy.undeploy_pg_agent import UndeployPgAgent
from adam.commands.deploy.undeploy_pod import UndeployPod
from adam.commands.devices.device_app import DeviceApp
from adam.commands.devices.device_auit_log import DeviceAuditLog
from adam.commands.devices.device_cass import DeviceCass
from adam.commands.devices.device_export import DeviceExport
from adam.commands.devices.device_postgres import DevicePostgres
from adam.commands.export.download_export_session import DownloadExportSession
from adam.commands.export.drop_export_database import DropExportDatabase
from adam.commands.export.export import ExportTables
from adam.commands.export.import_files import ImportCSVFiles
from adam.commands.export.import_session import ImportSession
from adam.commands.export.clean_up_export_sessions import CleanUpExportSessions
from adam.commands.export.clean_up_all_export_sessions import CleanUpAllExportSessions
from adam.commands.export.drop_export_databases import DropExportDatabases
from adam.commands.export.export_x_select import ExportXSelect
from adam.commands.export.export_use import ExportUse
from adam.commands.export.export_select import ExportSelect
from adam.commands.export.show_column_counts import ShowColumnCounts
from adam.commands.export.show_export_databases import ShowExportDatabases
from adam.commands.export.show_export_session import ShowExportSession
from adam.commands.export.show_export_sessions import ShowExportSessions
from adam.commands.fs.find_files import FindLocalFiles
from adam.commands.fs.find_processes import FindProcesses
from adam.commands.fs.head import Head
from adam.commands.fs.head_local import HeadLocal
from adam.commands.fs.ls_local import LsLocal
from adam.commands.fs.rm import RmLocal
from adam.commands.fs.rm_logs import RmLogs
from adam.commands.fs.show_job_result import ShowJobResults
from adam.commands.fs.show_jobs import ShowJobs
from adam.commands.fs.tail import Tail
from adam.commands.fs.tail_local import TailLocal
from adam.commands.kubectl import Kubectl
from adam.commands.fs.shell import Shell
from adam.commands.bash.bash import Bash
from adam.commands.fs.cd import Cd
from adam.commands.command import Command
from adam.commands.cql.cqlsh import Cqlsh
from adam.commands.exit import Exit
from adam.commands.medusa.medusa import Medusa
from adam.commands.fs.ls import Ls
from adam.commands.nodetool.nodetool import NodeTool
from adam.commands.postgres.postgres import Postgres, PostgresPg
from adam.commands.preview_table import PreviewTable
from adam.commands.fs.pwd import Pwd
from adam.commands.reaper.reaper import Reaper
from adam.commands.repair.repair import Repair
from adam.commands.cli.show_cli_commands import ShowKubectlCommands
from adam.commands.fs.show_host import ShowHost
from adam.commands.app.show_login import ShowLogin
from adam.commands.config.show_params import ShowParams
from adam.commands.fs.show_adam import ShowAdam
from adam.commands.show import Show

class ReplCommands:
    def repl_cmd_list() -> list[Command]:
        cmds: list[Command] = ReplCommands.navigation() + ReplCommands.cassandra_ops() + ReplCommands.postgres_ops() + \
            ReplCommands.app_ops() + ReplCommands.audit_ops() + ReplCommands.export_ops() + ReplCommands.tools() + ReplCommands.exit()

        intermediate_cmds: list[Command] = [App(), Audit(), Reaper(), Repair(), Debug(), Deploy(), Show(), Undeploy()]
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
        return [Cd(), Cat(), CatLocal(), ClipboardCopy(),
                DeviceApp(), DevicePostgres(), DeviceCass(), DeviceAuditLog(), DeviceExport(),
                DownloadFile(), FindLocalFiles(), FindProcesses(), GetParam(),
                Head(), HeadLocal(), Ls(), LsLocal(), PreviewTable(), Pwd(), RmLogs(),
                SetParam(), ShowAdam(), ShowHost(), ShowKubectlCommands(), ShowJobResults(),
                ShowLogin(), ShowOffloadedCompletes(), ShowParams(),
                Tail(), TailLocal()] + \
                RmLocal().cmd_list()

    def cassandra_ops() -> list[Command]:
        return [AlterTables(), Bash(), Check(), CleanUpExportSessions(), CleanUpAllExportSessions(), Cqlsh(),
                DownloadCassandraLog(), DropExportDatabase(), DropExportDatabases(), DownloadExportSession(),
                ExportTables(), ExportXSelect(), ExportUse(),
                GenerateReport(), ImportSession(), ImportCSVFiles(), Issues(), NodeTool(),
                RestartNodes(), RestartCluster(), RollOut(),
                ShowCassandraRing(), ShowCassandraStatus(), ShowNodeRestartable(), ShowCassandraVersion(),
                ShowCassandraRepairs(), ShowColumnCounts(), ShowJobs(), ShowStorage(), ShowExportDatabases(),
                ShowExportSessions(), ShowExportSession(), ShowProcesses(),
                Watch()] + \
                Debug().cmd_list() + \
                Medusa().cmd_list() + \
                Reaper().cmd_list() + \
                Repair().cmd_list()

    def postgres_ops() -> list[Command]:
        return [Postgres(), DeployPgAgent(), UndeployPgAgent(), PostgresPg()]

    def app_ops() -> list[Command]:
        return [ShowAppActions(), ShowAppId(), ShowAppQueues(), AppPing(), App()]

    def audit_ops() -> list[Command]:
        return [Audit()] + Audit().cmd_list()

    def export_ops() -> list[Command]:
        return [ExportSelect(), DropExportDatabase(), DropExportDatabases(), ShowColumnCounts()]

    def tools() -> list[Command]:
        return [Shell(), CodeStart(), CodeStop(), DeployFrontend(), UndeployFrontend(), DeployPod(), UndeployPod(), Kubectl(), Code()]

    def exit() -> list[Command]:
        return [Exit()]