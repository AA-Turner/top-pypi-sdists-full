import click

from adam.commands.bash import Bash
from adam.commands.check import Check, CheckCommandHelper
from adam.commands.cp import ClipboardCopy, CopyCommandHelper
from adam.commands.command import Command
from adam.commands.command_helpers import ClusterCommandHelper, ClusterOrPodCommandHelper, PodCommandHelper
from adam.commands.cqlsh import CqlCommandHelper, Cqlsh
from adam.commands.frontend.setup import Setup, SetupCommandHelper
from adam.commands.frontend.teardown import TearDown, TearDownCommandHelper
from adam.commands.issues import Issues
from adam.commands.login import Login
from adam.commands.logs import Logs
from adam.commands.ls import Ls
from adam.commands.medusa.medusa import Medusa
from adam.commands.nodetool import NodeTool, NodeToolCommandHelper
from adam.commands.postgres.postgres import Postgres, PostgresCommandHelper
from adam.commands.preview_table import PreviewTable
from adam.commands.reaper.reaper import Reaper, ReaperCommandHelper
from adam.commands.repair.repair import Repair, RepairCommandHelper
from adam.commands.report import Report
from adam.commands.restart import Restart
from adam.commands.rollout import RollOut
from adam.commands.show.show import Show, ShowCommandHelper
from adam.commands.user_entry import UserEntry
from adam.commands.watch import Watch
from adam.k8s_utils.kube_context import KubeContext
from adam.repl import enter_repl
from adam.repl_state import ReplState
from adam.cli_group import cli

@cli.command(context_settings=dict(ignore_unknown_options=True, allow_extra_args=True), cls=ClusterOrPodCommandHelper, help='Run a single bash command.')
@click.option('--kubeconfig', '-k', required=False, metavar='path', help='path to kubeconfig file')
@click.option('--config', default='params.yaml', metavar='path', help='path to kaqing parameters file')
@click.option('--param', '-v', multiple=True, metavar='<key>=<value>', help='parameter override')
@click.option('--cluster', '-c', required=False, metavar='statefulset', help='Kubernetes statefulset name')
@click.option('--namespace', '-n', required=False, metavar='namespace', help='Kubernetes namespace')
@click.option('--pod', '-p', required=False, metavar='pod', help='Kubernetes pod name')
@click.argument('extra_args', nargs=-1, metavar='<cluster|pod>', type=click.UNPROCESSED)
def bash(kubeconfig: str, config: str, param: list[str], cluster: str, namespace: str, pod: str, extra_args):
    run_command(Bash(), kubeconfig, config, param, cluster, namespace, pod, extra_args)


@cli.command(context_settings=dict(ignore_unknown_options=True, allow_extra_args=True), cls=CheckCommandHelper, help='Run a single check.')
@click.option('--kubeconfig', '-k', required=False, metavar='path', help='path to kubeconfig file')
@click.option('--config', default='params.yaml', metavar='path', help='path to kaqing parameters file')
@click.option('--param', '-v', multiple=True, metavar='<key>=<value>', help='parameter override')
@click.option('--cluster', '-c', required=False, metavar='statefulset', help='Kubernetes statefulset name')
@click.option('--namespace', '-n', required=False, metavar='namespace', help='Kubernetes namespace')
@click.option('--pod', '-p', required=False, metavar='pod', help='Kubernetes pod name')
@click.argument('extra_args', nargs=-1, metavar='<check-name> [cluster|pod]', type=click.UNPROCESSED)
def check(kubeconfig: str, config: str, param: list[str], cluster: str, namespace: str, pod: str, extra_args):
    run_command(Check(), kubeconfig, config, param, cluster, namespace, pod, extra_args)


@cli.command(context_settings=dict(ignore_unknown_options=True, allow_extra_args=True), cls=CopyCommandHelper, help='Copy a value to clipboard.')
@click.option('--kubeconfig', '-k', required=False, metavar='path', help='path to kubeconfig file')
@click.option('--config', default='params.yaml', metavar='path', help='path to kaqing parameters file')
@click.option('--param', '-v', multiple=True, metavar='<key>=<value>', help='parameter override')
@click.option('--cluster', '-c', required=False, metavar='statefulset', help='Kubernetes statefulset name')
@click.option('--namespace', '-n', required=False, metavar='namespace', help='Kubernetes namespace')
@click.option('--pod', '-p', required=False, metavar='pod', help='Kubernetes pod name')
@click.argument('extra_args', nargs=-1, metavar='<key> <cluster|pod>', type=click.UNPROCESSED)
def copy(kubeconfig: str, config: str, param: list[str], cluster: str, namespace: str, pod: str, extra_args):
    run_command(ClipboardCopy(), kubeconfig, config, param, cluster, namespace, pod, extra_args)


@cli.command(context_settings=dict(ignore_unknown_options=True, allow_extra_args=True), cls=CqlCommandHelper, help='Execute CQL statements.')
@click.option('--kubeconfig', '-k', required=False, metavar='path', help='path to kubeconfig file')
@click.option('--config', default='params.yaml', metavar='path', help='path to kaqing parameters file')
@click.option('--param', '-v', multiple=True, metavar='<key>=<value>', help='parameter override')
@click.option('--cluster', '-c', required=False, metavar='statefulset', help='Kubernetes statefulset name')
@click.option('--namespace', '-n', required=False, metavar='namespace', help='Kubernetes namespace')
@click.option('--pod', '-p', required=False, metavar='pod', help='Kubernetes pod name')
@click.argument('extra_args', nargs=-1, metavar='CQL-STATEMENTS <cluster|pod>', type=click.UNPROCESSED)
def cql(kubeconfig: str, config: str, param: list[str], cluster: str, namespace: str, pod: str, extra_args):
    run_command(Cqlsh(), kubeconfig, config, param, cluster, namespace, pod, extra_args)


@cli.command(context_settings=dict(ignore_unknown_options=True, allow_extra_args=True), cls=ClusterOrPodCommandHelper, help="Print Qing's issues.")
@click.option('--kubeconfig', '-k', required=False, metavar='path', help='path to kubeconfig file')
@click.option('--config', default='params.yaml', metavar='path', help='path to kaqing parameters file')
@click.option('--param', '-v', multiple=True, metavar='<key>=<value>', help='parameter override')
@click.option('--cluster', '-c', required=False, metavar='statefulset', help='Kubernetes statefulset name')
@click.option('--namespace', '-n', required=False, metavar='namespace', help='Kubernetes namespace')
@click.option('--pod', '-p', required=False, metavar='pod', help='Kubernetes pod name')
@click.option('--show', '-s', is_flag=True, help='show output from Cassandra nodes')
@click.argument('extra_args', nargs=-1, metavar='[cluster|pod]', type=click.UNPROCESSED)
def issues(kubeconfig: str, config: str, param: list[str], cluster: str, namespace: str, pod: str, show: bool, extra_args):
    run_command(Issues(), kubeconfig, config, param, cluster, namespace, pod, ('-s',) + extra_args if show else extra_args)


@cli.command(context_settings=dict(ignore_unknown_options=True, allow_extra_args=True), cls=PodCommandHelper, help='Get cassandra log.')
@click.option('--kubeconfig', '-k', required=False, metavar='path', help='path to kubeconfig file')
@click.option('--config', default='params.yaml', metavar='path', help='path to kaqing parameters file')
@click.option('--param', '-v', multiple=True, metavar='<key>=<value>', help='parameter override')
@click.option('--namespace', '-n', required=False, metavar='namespace', help='Kubernetes namespace')
@click.option('--pod', '-p', required=False, metavar='pod', help='Kubernetes pod name')
@click.argument('extra_args', nargs=-1, metavar='<pod>', type=click.UNPROCESSED)
def login(kubeconfig: str, config: str, param: list[str], namespace: str, pod: str, extra_args):
    run_command(Login(), kubeconfig, config, param, None, namespace, pod, extra_args)


@cli.command(context_settings=dict(ignore_unknown_options=True, allow_extra_args=True), cls=PodCommandHelper, help='Get cassandra log.')
@click.option('--kubeconfig', '-k', required=False, metavar='path', help='path to kubeconfig file')
@click.option('--config', default='params.yaml', metavar='path', help='path to kaqing parameters file')
@click.option('--param', '-v', multiple=True, metavar='<key>=<value>', help='parameter override')
@click.option('--namespace', '-n', required=False, metavar='namespace', help='Kubernetes namespace')
@click.option('--pod', '-p', required=False, metavar='pod', help='Kubernetes pod name')
@click.argument('extra_args', nargs=-1, metavar='<pod>', type=click.UNPROCESSED)
def logs(kubeconfig: str, config: str, param: list[str], namespace: str, pod: str, extra_args):
    run_command(Logs(), kubeconfig, config, param, None, namespace, pod, extra_args)


@cli.command(context_settings=dict(ignore_unknown_options=True, allow_extra_args=True), cls=ClusterCommandHelper, help='List statefulset or pods.')
@click.option('--kubeconfig', '-k', required=False, metavar='path', help='path to kubeconfig file')
@click.option('--config', default='params.yaml', metavar='path', help='path to kaqing parameters file')
@click.option('--param', '-v', multiple=True, metavar='<key>=<value>', help='parameter override')
@click.option('--cluster', '-c', required=False, metavar='statefulset', help='Kubernetes statefulset name')
@click.option('--namespace', '-n', required=False, metavar='namespace', help='Kubernetes namespace')
@click.argument('extra_args', nargs=-1, metavar='[cluster|..]', type=click.UNPROCESSED)
def ls(kubeconfig: str, config: str, param: list[str], cluster: str, namespace: str, extra_args):
    run_command(Ls(), kubeconfig, config, param, cluster, namespace, None, extra_args)


@cli.command(context_settings=dict(ignore_unknown_options=True, allow_extra_args=True), cls=CopyCommandHelper, help='Execute Cassandr Medusa Backup')
@click.option('--kubeconfig', '-k', required=False, metavar='path', help='path to kubeconfig file')
@click.option('--config', default='params.yaml', metavar='path', help='path to kaqing parameters file')
@click.option('--param', '-v', multiple=True, metavar='<key>=<value>', help='parameter override')
@click.option('--cluster', '-c', required=False, metavar='statefulset', help='Kubernetes statefulset name')
@click.option('--namespace', '-n', required=False, metavar='namespace', help='Kubernetes namespace')
@click.option('--pod', '-p', required=False, metavar='pod', help='Kubernetes pod name')
@click.argument('extra_args', nargs=-1, metavar='<key> <cluster|pod>', type=click.UNPROCESSED)
def medusa(kubeconfig: str, config: str, param: list[str], cluster: str, namespace: str, pod: str, extra_args):
    run_command(Medusa(), kubeconfig, config, param, cluster, namespace, pod, extra_args)


@cli.command(context_settings=dict(ignore_unknown_options=True, allow_extra_args=True), cls=NodeToolCommandHelper, help='Nodetool operations.')
@click.option('--kubeconfig', '-k', required=False, metavar='path', help='path to kubeconfig file')
@click.option('--config', default='params.yaml', metavar='path', help='path to kaqing parameters file')
@click.option('--param', '-v', multiple=True, metavar='<key>=<value>', help='parameter override')
@click.option('--cluster', '-c', required=False, metavar='statefulset', help='Kubernetes statefulset name')
@click.option('--namespace', '-n', required=False, metavar='namespace', help='Kubernetes namespace')
@click.option('--pod', '-p', required=False, metavar='pod', help='Kubernetes pod name')
@click.argument('extra_args', nargs=-1, metavar='SUB-COMMAND <cluster|pod>', type=click.UNPROCESSED)
def nodetool(kubeconfig: str, config: str, param: list[str], cluster: str, namespace: str, pod: str, extra_args):
    run_command(NodeTool(), kubeconfig, config, param, cluster, namespace, pod, extra_args)


@cli.command(context_settings=dict(ignore_unknown_options=True, allow_extra_args=True), cls=PostgresCommandHelper, help='Execute Postgres operations.')
@click.option('--kubeconfig', '-k', required=False, metavar='path', help='path to kubeconfig file')
@click.option('--config', default='params.yaml', metavar='path', help='path to kaqing parameters file')
@click.option('--param', '-v', multiple=True, metavar='<key>=<value>', help='parameter override')
@click.option('--cluster', '-c', required=False, metavar='statefulset', help='Kubernetes statefulset name')
@click.option('--namespace', '-n', required=False, metavar='namespace', help='Kubernetes namespace')
@click.argument('extra_args', nargs=-1, metavar='SUB-COMMAND|<sql-statements> <cluster> [pg-name/database]', type=click.UNPROCESSED)
def pg(kubeconfig: str, config: str, param: list[str], cluster: str, namespace: str, extra_args):
    run_command(Postgres(), kubeconfig, config, param, cluster, namespace, None, extra_args)


@cli.command(context_settings=dict(ignore_unknown_options=True, allow_extra_args=True), cls=PodCommandHelper, help='Preview table.')
@click.option('--kubeconfig', '-k', required=False, metavar='path', help='path to kubeconfig file')
@click.option('--config', default='params.yaml', metavar='path', help='path to kaqing parameters file')
@click.option('--param', '-v', multiple=True, metavar='<key>=<value>', help='parameter override')
@click.option('--cluster', '-c', required=False, metavar='statefulset', help='Kubernetes statefulset name')
@click.option('--namespace', '-n', required=False, metavar='namespace', help='Kubernetes namespace')
@click.option('--pod', '-p', required=False, metavar='pod', help='Kubernetes pod name')
@click.argument('extra_args', nargs=-1, metavar='<pod> <table>', type=click.UNPROCESSED)
def preview(kubeconfig: str, config: str, param: list[str], cluster: str, namespace: str, pod: str, extra_args):
    run_command(PreviewTable(), kubeconfig, config, param, cluster, namespace, pod, extra_args)


@cli.command(context_settings=dict(ignore_unknown_options=True, allow_extra_args=True), cls=ReaperCommandHelper, help='Execute Cassandra Reaper operations.')
@click.option('--kubeconfig', '-k', required=False, metavar='path', help='path to kubeconfig file')
@click.option('--config', default='params.yaml', metavar='path', help='path to kaqing parameters file')
@click.option('--param', '-v', multiple=True, metavar='<key>=<value>', help='parameter override')
@click.option('--cluster', '-c', required=False, metavar='statefulset', help='Kubernetes statefulset name')
@click.option('--namespace', '-n', required=False, metavar='namespace', help='Kubernetes namespace')
@click.argument('extra_args', nargs=-1, metavar='SUB-COMMAND <cluster>', type=click.UNPROCESSED)
def reaper(kubeconfig: str, config: str, param: list[str], cluster: str, namespace: str, extra_args):
    run_command(Reaper(), kubeconfig, config, param, cluster, namespace, None, extra_args)


@cli.command(context_settings=dict(ignore_unknown_options=True, allow_extra_args=True), cls=RepairCommandHelper, help='Execute Cassandra repair operations.')
@click.option('--kubeconfig', '-k', required=False, metavar='path', help='path to kubeconfig file')
@click.option('--config', default='params.yaml', metavar='path', help='path to kaqing parameters file')
@click.option('--param', '-v', multiple=True, metavar='<key>=<value>', help='parameter override')
@click.option('--cluster', '-c', required=False, metavar='statefulset', help='Kubernetes statefulset name')
@click.option('--namespace', '-n', required=False, metavar='namespace', help='Kubernetes namespace')
@click.argument('extra_args', nargs=-1, metavar='SUB-COMMAND <cluster>', type=click.UNPROCESSED)
def repair(kubeconfig: str, config: str, param: list[str], cluster: str, namespace: str, extra_args):
    run_command(Repair(), kubeconfig, config, param, cluster, namespace, None, extra_args)


@cli.command(context_settings=dict(ignore_unknown_options=True, allow_extra_args=True), cls=ClusterOrPodCommandHelper, help="Generate Qing's report.")
@click.option('--kubeconfig', '-k', required=False, metavar='path', help='path to kubeconfig file')
@click.option('--config', default='params.yaml', metavar='path', help='path to kaqing parameters file')
@click.option('--param', '-v', multiple=True, metavar='<key>=<value>', help='parameter override')
@click.option('--cluster', '-c', required=False, metavar='statefulset', help='Kubernetes statefulset name')
@click.option('--namespace', '-n', required=False, metavar='namespace', help='Kubernetes namespace')
@click.option('--pod', '-p', required=False, metavar='pod', help='Kubernetes pod name')
@click.option('--show', '-s', is_flag=True, help='show output from Cassandra nodes')
@click.argument('extra_args', nargs=-1, metavar='[cluster|pod]', type=click.UNPROCESSED)
def report(kubeconfig: str, config: str, param: list[str], cluster: str, namespace: str, pod: str, show: bool, extra_args):
    run_command(Report(), kubeconfig, config, param, cluster, namespace, pod, ('-s',) + extra_args if show else extra_args)


@cli.command(context_settings=dict(ignore_unknown_options=True, allow_extra_args=True), cls=ClusterOrPodCommandHelper, help='Restart Cassandra Cluster or Node')
@click.option('--kubeconfig', '-k', required=False, metavar='path', help='path to kubeconfig file')
@click.option('--config', default='params.yaml', metavar='path', help='path to kaqing parameters file')
@click.option('--param', '-v', multiple=True, metavar='<key>=<value>', help='parameter override')
@click.option('--cluster', '-c', required=False, metavar='statefulset', help='Kubernetes statefulset name')
@click.option('--namespace', '-n', required=False, metavar='namespace', help='Kubernetes namespace')
@click.option('--pod', '-p', required=False, metavar='pod', help='Kubernetes pod name')
@click.option('--force', is_flag=True, help='need for restarting the whole cluster')
@click.argument('extra_args', nargs=-1, metavar='<cluster|pod>', type=click.UNPROCESSED)
def restart(kubeconfig: str, config: str, param: list[str], cluster: str, namespace: str, pod: str, force: bool, extra_args):
    run_command(Restart(), kubeconfig, config, param, cluster, namespace, pod, ('--force',) + extra_args if force else extra_args)


@cli.command(context_settings=dict(ignore_unknown_options=True, allow_extra_args=True), cls=ClusterOrPodCommandHelper, help='Rolling restart Cassandra Cluster.')
@click.option('--kubeconfig', '-k', required=False, metavar='path', help='path to kubeconfig file')
@click.option('--config', default='params.yaml', metavar='path', help='path to kaqing parameters file')
@click.option('--param', '-v', multiple=True, metavar='<key>=<value>', help='parameter override')
@click.option('--cluster', '-c', required=False, metavar='statefulset', help='Kubernetes statefulset name')
@click.option('--namespace', '-n', required=False, metavar='namespace', help='Kubernetes namespace')
@click.argument('extra_args', nargs=-1, metavar='<cluster>', type=click.UNPROCESSED)
def rollout(kubeconfig: str, config: str, param: list[str], cluster: str, namespace: str, extra_args):
    run_command(RollOut(), kubeconfig, config, param, cluster, namespace, None, extra_args)


@cli.command(context_settings=dict(ignore_unknown_options=True, allow_extra_args=True), cls=SetupCommandHelper, help='Setup.')
@click.option('--kubeconfig', '-k', required=False, metavar='path', help='path to kubeconfig file')
@click.option('--config', default='params.yaml', metavar='path', help='path to kaqing parameters file')
@click.option('--param', '-v', multiple=True, metavar='<key>=<value>', help='parameter override')
@click.option('--namespace', '-n', required=False, metavar='namespace', help='Kubernetes namespace')
@click.argument('extra_args', nargs=-1, metavar='<pod>', type=click.UNPROCESSED)
def setup(kubeconfig: str, config: str, param: list[str], namespace: str, extra_args):
    run_command(Setup(), kubeconfig, config, param, None, namespace, None, extra_args)


@cli.command(context_settings=dict(ignore_unknown_options=True, allow_extra_args=True), cls=ShowCommandHelper, help='Show configuration or kubectl commands.')
@click.option('--kubeconfig', '-k', required=False, metavar='path', help='path to kubeconfig file')
@click.option('--config', default='params.yaml', metavar='path', help='path to kaqing parameters file')
@click.option('--param', '-v', multiple=True, metavar='<key>=<value>', help='parameter override')
@click.option('--cluster', '-c', required=False, metavar='statefulset', help='Kubernetes statefulset name')
@click.option('--namespace', '-n', required=False, metavar='namespace', help='Kubernetes namespace')
@click.option('--pod', '-p', required=False, metavar='pod', help='Kubernetes pod name')
@click.argument('extra_args', nargs=-1, metavar='CATEGORY <cluster|pod>', type=click.UNPROCESSED)
def show(kubeconfig: str, config: str, param: list[str], cluster: str, namespace: str, pod: str, extra_args):
    run_command(Show(), kubeconfig, config, param, cluster, namespace, pod, extra_args)


@cli.command(context_settings=dict(ignore_unknown_options=True, allow_extra_args=True), cls=TearDownCommandHelper, help='Teardown.')
@click.option('--kubeconfig', '-k', required=False, metavar='path', help='path to kubeconfig file')
@click.option('--config', default='params.yaml', metavar='path', help='path to kaqing parameters file')
@click.option('--param', '-v', multiple=True, metavar='<key>=<value>', help='parameter override')
@click.option('--namespace', '-n', required=False, metavar='namespace', help='Kubernetes namespace')
@click.argument('extra_args', nargs=-1, metavar='<pod>', type=click.UNPROCESSED)
def teardown(kubeconfig: str, config: str, param: list[str], namespace: str, extra_args):
    run_command(TearDown(), kubeconfig, config, param, None, namespace, None, extra_args)


@cli.command(context_settings=dict(ignore_unknown_options=True, allow_extra_args=True), cls=PodCommandHelper, help='Get cassandra log.')
@click.option('--kubeconfig', '-k', required=False, metavar='path', help='path to kubeconfig file')
@click.option('--config', default='params.yaml', metavar='path', help='path to kaqing parameters file')
@click.option('--param', '-v', multiple=True, metavar='<key>=<value>', help='parameter override')
@click.option('--namespace', '-n', required=False, metavar='namespace', help='Kubernetes namespace')
@click.argument('extra_args', nargs=-1, metavar='<pod>', type=click.UNPROCESSED)
def entry(kubeconfig: str, config: str, param: list[str], namespace: str, extra_args):
    run_command(UserEntry(), kubeconfig, config, param, None, namespace, None, extra_args)


@cli.command(context_settings=dict(ignore_unknown_options=True, allow_extra_args=True), cls=ClusterOrPodCommandHelper, help='Watch pods in cluster.')
@click.option('--kubeconfig', '-k', required=False, metavar='path', help='path to kubeconfig file')
@click.option('--config', default='params.yaml', metavar='path', help='path to kaqing parameters file')
@click.option('--param', '-v', multiple=True, metavar='<key>=<value>', help='parameter override')
@click.option('--cluster', '-c', required=False, metavar='statefulset', help='Kubernetes statefulset name')
@click.option('--namespace', '-n', required=False, metavar='namespace', help='Kubernetes namespace')
@click.argument('extra_args', nargs=-1, metavar='<cluster>', type=click.UNPROCESSED)
def watch(kubeconfig: str, config: str, param: list[str], cluster: str, namespace: str, extra_args):
    run_command(Watch(), kubeconfig, config, param, cluster, namespace, None, extra_args)


def run_command(cmd: Command, kubeconfig: str, config: str, params: list[str], cluster:str, namespace: str, pod: str, extra_args):
    is_user_entry = cmd.command() == UserEntry().command()

    KubeContext.init_config(kubeconfig, is_user_entry=is_user_entry)
    if not KubeContext.init_params(config, params, is_user_entry=is_user_entry):
        return

    state = ReplState(ns_sts=cluster, pod=pod, namespace=namespace)
    if cmd.command() == 'pg' and not extra_args:
        state, _ = state.apply_args(extra_args)
        state.device = ReplState.P
        state.in_repl = True
        enter_repl(state)
    else:
        cmd.run(build_cmd(cmd.command(), extra_args), state)

def build_cmd(cmd, extra_args):
    path = ' '.join(list(extra_args))
    if path:
        cmd = f'{cmd} {path}'

    return cmd.strip(' ')