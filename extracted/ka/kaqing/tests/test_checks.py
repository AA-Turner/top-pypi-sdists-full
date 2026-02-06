import unittest
from adam.checks.compactionstats import CompactionStats
from adam.checks.memory import Memory
from adam.checks.status import parse_nodetool_status
from adam.utils_k8s.pod_exec_result import PodExecResult
from adam.utils_k8s import get_user_pass, init_config, set_test_pod_exec_outs
from pathlib import Path

class TestChecks(unittest.TestCase):
    def test_memory(self):
        init_config('gkeops845-sa')

        check = Memory()

        try:
            with open(Path(__file__).parent / 'data' / 'system.log', "r") as f:
                stdout = f.read()
                set_test_pod_exec_outs(PodExecResult(stdout, ''))
                _, issues = check.check(statefulset_name='cs-d0767a536f-cs-d0767a536f-default-sts', host_id='xx', pod_name = 'cs-d0767a536f-cs-d0767a536f-default-sts-0', ns = 'gkeops845')
                self.assertEqual([], issues)
        finally:
            set_test_pod_exec_outs(None)

        try:
            with open(Path(__file__).parent / 'data' / 'system.log.not_marking', "r") as f:
                stdout = f.read()
                set_test_pod_exec_outs(PodExecResult(stdout, ''))
                _, issues = check.check(statefulset_name='cs-d0767a536f-cs-d0767a536f-default-sts', host_id='xx', pod_name = 'cs-d0767a536f-cs-d0767a536f-default-sts-0', ns = 'gkeops845')
                self.assertEqual(1, len(issues))
        finally:
            set_test_pod_exec_outs(None)

        # against real pod
        check.check(statefulset_name='cs-d0767a536f-cs-d0767a536f-default-sts', host_id='xx', pod_name = 'cs-d0767a536f-cs-d0767a536f-default-sts-0', ns = 'gkeops845')

    def test_parse_nodetool_status(self):
        # NOTE: Picked up JDK_JAVA_OPTIONS: -Djava.security.properties=/usr/lib/cassandra-reaper/config/java.security
        # Datacenter: cs-d0767a536f
        # =========================
        # Status=Up/Down
        # |/ State=Normal/Leaving/Joining/Moving
        # --  Address       Load      Tokens  Owns  Host ID                               Rack
        # UN  172.20.1.115  1.21 MiB  16      ?     6eb3d978-d20b-4a01-9749-54f9b89388ca  default
        # UN  172.20.3.220  1.2 MiB   16      ?     6ebc023e-47fc-487a-9443-b05fbd343b4b  default
        # DN  172.20.4.13   1.11 MiB  16      ?     19cce943-6ea7-41cc-b87f-8aed335616c2  default
        #
        line = 'UN  172.20.1.115  1.21 MiB  16      ?     6eb3d978-d20b-4a01-9749-54f9b89388ca  default'
        status = parse_nodetool_status(line)
        self.assertEqual('1.21 MiB', status[0]['load'])
        self.assertEqual('default', status[0]['rack'])

    def test_compaction(self):
        init_config('gkeops845-sa')

        check = CompactionStats()

        user, pw = get_user_pass('cs-d0767a536f-cs-d0767a536f-default-sts', 'gkeops845')
        r, i = check.check(statefulset_name='cs-d0767a536f-cs-d0767a536f-default-sts', host_id='xx', pod_name = 'cs-d0767a536f-cs-d0767a536f-default-sts-0', ns = 'gkeops845',
                    user=user, pw=pw)
        print(r)
        self.assertNotEqual('Unknown', r['compactionstats']['compactions'])

if __name__ == '__main__':
    unittest.main()