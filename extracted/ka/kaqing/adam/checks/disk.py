import re
from pathlib import Path
import traceback

from adam.checks.check import Check
from adam.checks.check_context import CheckContext
from adam.checks.check_result import CheckResult
from adam.checks.issue import Issue
from adam.config import Config
from adam.utils import Color, log_exc
from adam.utils_context import Context
from adam.utils_k8s.cassandra_nodes import CassandraNodes

class Disk(Check):
    def name(self):
        return 'disk'

    def check(self, ctx: CheckContext) -> CheckResult:
        issues: list[Issue] = []
        result = {}

        try:
            ctx_fg = ctx.copy(background=False, text_color=Color.gray)
            cass_data_path = Config().get('checks.cassandra-data-path', '/c3/cassandra')
            df_result = CassandraNodes.exec(ctx.pod, ctx.namespace, f"df -h | grep -e '{cass_data_path}' -e 'overlay'", ctx=ctx_fg)

            snapshot_size = Config().get('checks.snapshot-size-cmd', "ls /c3/cassandra/data/data/*/*/snapshots | grep snapshots | sed 's/:$//g' | xargs -I {} du -sk {} | awk '{print $1}' | awk '{s+=$1} END {print s}'")
            ss_result = CassandraNodes.exec(ctx.pod, ctx.namespace, snapshot_size, ctx=ctx_fg)

            data_sizes = Config().get('checks.data-size-cmd', "du -sh /c3/cassandra/data/data")
            ds_result = CassandraNodes.exec(ctx.pod, ctx.namespace, data_sizes, ctx=ctx_fg)

            table_sizes = Config().get('checks.table-sizes-cmd', "ls -Al /c3/cassandra/data/data/ | awk '{print $9}' | sed 's/\^r//g' | xargs -I {} du -sk /c3/cassandra/data/data/{}")
            ts_result = CassandraNodes.exec(ctx.pod, ctx.namespace, table_sizes, ctx=ctx_fg)

            result = self.build_details(ctx, df_result.stdout, ss_result.stdout, ds_result.stdout, ts_result.stdout)

            dev = result['devices']['/']
            root_used = float(dev['per'].strip('%'))
            if root_used > Config().get('checks.root-disk-threshold', 50):
                usage = f"{dev['per']}({dev['used']}/{dev['total']})"
                issues.append(Issue(
                    statefulset=ctx.statefulset,
                    namespace=ctx.namespace,
                    pod=ctx.pod,
                    category="disk",
                    desc=f"Root data disk is full: {usage}"
                ))

            if not cass_data_path in result['devices']:
                issues.append(Issue(
                    statefulset=ctx.statefulset,
                    namespace=ctx.namespace,
                    pod=ctx.pod,
                    category="disk",
                    desc=f"Cassandra volume is lost: {cass_data_path}"
                ))

            dev = result['devices'][cass_data_path]
            cass_used = float(dev['per'].strip('%'))
            if cass_used > Config().get('checks.cassandra-disk-threshold', 50):
                usage = f"{dev['per']}({dev['used']}/{dev['total']})"
                issues.append(Issue(
                    statefulset=ctx.statefulset,
                    namespace=ctx.namespace,
                    pod=ctx.pod,
                    category="disk",
                    desc=f"Cassandra data disk is full: {usage}"
                ))
        except Exception as e:
            if ctx.debug:
                traceback.print_exc()

            issues.append(self.issue_from_err(sts_name=ctx.statefulset, ns=ctx.namespace, pod_name=ctx.pod, exception=e))

        return CheckResult(self.name(), result, issues)

    def build_details(self, ctx: CheckContext, df_out: str, ss_out: str, ds_out: str, ts_out: str):
        # overlay                 499.9G     52.4G    447.5G  10% /
        # /dev/nvme2n1           1006.9G      2.6G   1004.2G   0% /c3/cassandra
        devices = {}
        for l in df_out.split('\n'):
            l = l.strip('\r')
            groups = re.match(r'^(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)$', l)
            if groups:
                dev = Disk.clean(groups[1])
                total = Disk.clean(groups[2])
                used = Disk.clean(groups[3])
                free = Disk.clean(groups[4])
                per = Disk.clean(groups[5])
                path = Disk.clean(groups[6])
                device = {'dev': dev, 'total': total, 'used': used, 'free': free, 'per': per, 'path': path}
                devices[path] = device

        ss_size = 0.0
        if ss_out:
            with log_exc():
                ss_size = round(float(ss_out.strip(' \r\n')) / 1024 / 1024, 2)

        def parse_du_out(l: str, default: str = None):
            groups = re.match(r'^(\S+)\s+(\S+)$', l.strip('\r'))
            if groups:
                return {'name': Path(groups[2]).name, 'size': groups[1], 'path': groups[2]}

            return default

        keyspaces = []
        for l in ts_out.split('\n'):
            if s := parse_du_out(l):
                keyspaces.append(s)

        return {
                'name': ctx.pod,
                'namespace': ctx.namespace,
                'statefulset': ctx.statefulset,
                'snapshot': ss_size,
                'devices': devices,
                'data': parse_du_out(ds_out.strip('\r\n '), default='Unknown'),
                'keyspaces': keyspaces}

    def clean(s: str):
        return re.sub(r'[^a-zA-Z0-9/%\.]', '', s)

    def help(self):
        return f'{Disk().name()}: check disk usages with df and du'