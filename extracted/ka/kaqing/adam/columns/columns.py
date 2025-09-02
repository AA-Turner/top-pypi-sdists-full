from adam.columns.column import Column
from adam.columns.compactions import Compactions
from adam.columns.cpu import Cpu
from adam.columns.dir_data import DataDir
from adam.columns.dir_snapshots import SnapshotsDir
from adam.columns.gossip import Gossip
from adam.columns.host_id import HostId
from adam.columns.memory import Memory
from adam.columns.node_address import NodeAddress
from adam.columns.node_load import NodeLoad
from adam.columns.node_owns import NodeOwns
from adam.columns.node_status import NodeStatus
from adam.columns.node_tokens import NodeTokens
from adam.columns.pod_name import PodName
from adam.columns.volume_cassandra import CassandraVolume
from adam.columns.volume_root import RootVolume

def collect_checks(columns: list[Column]):
    checks = sum([c.checks() for c in columns], [])
    return {cc.name(): cc for cc in checks}.values()

class Columns:
    COLUMNS_BY_NAME = None

    def all_columns():
        return [Compactions(), Cpu(), DataDir(), SnapshotsDir(), Gossip(), HostId(), Memory(),
                NodeAddress(), NodeLoad(), NodeOwns(), NodeStatus(),NodeTokens(), PodName(), CassandraVolume(), RootVolume()]

    def columns_by_name():
        return {c.name(): c.__class__ for c in Columns.all_columns()}

    def create_columns(columns: str):
        if not Columns.COLUMNS_BY_NAME:
            Columns.COLUMNS_BY_NAME = Columns.columns_by_name()

        cols = []
        for name in columns.split(','):
            name = name.strip(' ')
            if not name in Columns.COLUMNS_BY_NAME:
                return None
            cols.append(Columns.COLUMNS_BY_NAME[name]())

        return cols
