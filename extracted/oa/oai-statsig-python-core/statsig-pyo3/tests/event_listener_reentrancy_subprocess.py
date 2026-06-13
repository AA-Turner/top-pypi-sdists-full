from statsig_python_core import Statsig, StatsigUser


statsig = Statsig("secret-key")


def unsubscribe_from_callback(_event):
    statsig.unsubscribe("gate_evaluated")


statsig.subscribe("gate_evaluated", unsubscribe_from_callback)
statsig.check_gate(StatsigUser("a-user"), "test_gate")
statsig.shutdown().wait(timeout=1)
