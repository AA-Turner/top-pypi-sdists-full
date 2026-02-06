import unittest
from kubernetes import config as kconfig
from adam.checks.status import Status as StatusCheck, parse_nodetool_status
from adam.commands.show.show_app_id import ShowAppId
from adam.commands.status import Status
from adam.repl_state import ReplState
from adam.utils_k8s import strip

class TestCommands(unittest.TestCase):
    def test_status_on_a_node(self):
        kconfig.load_kube_config(config_file='gkeops845-sa')

        cmd = Status()
        state = ReplState(sts='cs-d0767a536f-cs-d0767a536f-default-sts',
                          pod = 'cs-d0767a536f-cs-d0767a536f-default-sts-0',
                          namespace = 'gkeops845'
        )
        cmd.run('status', state)

    def test_merge_status(self):
        line1 = strip("""
            --  Address       Load      Tokens  Owns  Host ID                               Rack
            UN  172.20.3.228  1.08 MiB  16      ?     6ebc023e-47fc-487a-9443-b05fbd343b4b  default
            UN  172.20.1.129  1.12 MiB  16      ?     6eb3d978-d20b-4a01-9749-54f9b89388ca  default
            UN  172.20.4.114  1.06 MiB  16      ?     19cce943-6ea7-41cc-b87f-8aed335616c2  default""")
        line2 = strip("""
            --  Address       Load      Tokens  Owns  Host ID                               Rack
            UN  172.20.3.228  1.08 MiB  16      ?     6ebc023e-47fc-487a-9443-b05fbd343b4b  default
            UN  172.20.1.129  1.12 MiB  16      ?     6eb3d978-d20b-4a01-9749-54f9b89388ca  default
            DN  172.20.4.114  1.06 MiB  16      ?     19cce943-6ea7-41cc-b87f-8aed335616c2  default""")

        self.assertEqual('DN*', Status().merge_status([parse_nodetool_status(line1), parse_nodetool_status(line2)])[2]['status'], 3)

    def test_app_id(self):
        kconfig.load_kube_config(config_file='stgawsscpsr')

        cmd = ShowAppId()
        state = ReplState(sts = 'cs-9834d85c68-cs-9834d85c68-default-sts',
                          namespace = 'stgawsscpsr')
        cmd.run('c3app', state)

if __name__ == '__main__':
    unittest.main()