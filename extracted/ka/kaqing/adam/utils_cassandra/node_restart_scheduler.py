from copy import copy
from datetime import datetime
import threading
import time

from adam.config import Config
from adam.repl_state import ReplState
from adam.utils_cassandra.cassandra_status import CassandraStatus
from adam.utils_cassandra.node_restartability import NodeRestartability
from adam.utils_context import Context
from adam.utils_k8s.pods import Pods

def ts():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def key(pod: str, namespace: str):
    return f'{pod}@{namespace}'

class NodeRestartScheduler:
    lock = threading.Lock()
    nodes_thread: threading.Thread = None
    # context with the first schedule() invocation is used for the event loop
    _ctx: Context = None

    _queue: dict[tuple[str, str], float] = {}
    _in_restartings: dict[tuple[str, str], float] = {}
    _completed: dict[tuple[str, str], float] = {}
    _waiting_ons: dict[tuple[str, str], str] = {}

    def schedule(state: ReplState, pod: str, ctx: Context):
        NodeRestartScheduler.start(state, ctx)

        NodeRestartScheduler._ctx.log2(f'[{ts()}] Restart requested for {pod}@{state.namespace}.')
        with NodeRestartScheduler.lock:
            NodeRestartScheduler._queue[(pod, state.namespace)] = time.time()

    def start(state: ReplState, ctx: Context):
        with NodeRestartScheduler.lock:
            if not NodeRestartScheduler.nodes_thread:
                ctx = ctx.copy(background=True, bg_init_msg='[{job_id}] Use :?? to get job scheduling status.')

                NodeRestartScheduler._ctx = ctx
                NodeRestartScheduler.nodes_thread = threading.Thread(target=NodeRestartScheduler.loop, args=(state, ctx,), daemon=True)
                NodeRestartScheduler.nodes_thread.start()

    def done(pod: tuple[str, str], ctx: Context):
        ctx.log2(f'[{ts()}] Restarted {pod}.')

        if pod in NodeRestartScheduler._in_restartings:
            del NodeRestartScheduler._in_restartings[pod]
        NodeRestartScheduler._completed[pod] = time.time()

    def pending():
        with NodeRestartScheduler.lock:
            return copy(NodeRestartScheduler._queue)

    def completed():
        with NodeRestartScheduler.lock:
            return copy(NodeRestartScheduler._completed)

    def restart_node(pod: str, namespace: str, ctx: Context):
        with NodeRestartScheduler.lock:
            key = (pod, namespace)
            if key in NodeRestartScheduler._queue:
                del NodeRestartScheduler._queue[key]
            NodeRestartScheduler._in_restartings[key] = time.time()

        Pods.delete(pod, namespace)

    def restartings(timeout: int = 0, ctx: Context = Context.NULL):
        if not timeout:
            timeout = Config().get('cassandra.restart.grace-period-in-seconds', 5 * 60)

        with NodeRestartScheduler.lock:
            for pod, t in list(NodeRestartScheduler._in_restartings.items()):
                if (secs := int(time.time() - t)) >= timeout:
                    NodeRestartScheduler._ctx.log2(f'[{ts()}] {int(secs)} seconds have been passed since restart of {pod[0]}@{pod[1]}. Removing from in_restart queue...')
                    NodeRestartScheduler.done(pod, NodeRestartScheduler._ctx)

            return NodeRestartScheduler._in_restartings

    def waiting_ons():
        return copy(NodeRestartScheduler._waiting_ons)

    # single queue pattern
    def loop(state: ReplState, ctx: Context = Context.NULL):
        while True:
            try:
                while (pods := NodeRestartScheduler.pending().keys()):
                    restarted = 0
                    for pod, namespace in pods:
                        in_restartings = NodeRestartScheduler.restartings(ctx=ctx)
                        ir = ''
                        if in_restartings:
                            ir = f', in_restarting:[{", ".join([f"{r[0]}@{r[1]}" for r in in_restartings])}]'

                        node: NodeRestartability = CassandraStatus.restartable(state.with_namespace(namespace), pod, in_restartings=in_restartings, ctx=ctx.copy(show_out=False, background=False))
                        if node.restartable():
                            ctx.log2(f'[{ts()}] Restarting {pod}@{namespace}{ir}.')
                            NodeRestartScheduler.restart_node(pod, namespace, ctx)

                            restarted += 1

                            with NodeRestartScheduler.lock:
                                if (pod, namespace) in NodeRestartScheduler._waiting_ons:
                                    del NodeRestartScheduler._waiting_ons[(pod, namespace)]
                        else:
                            with NodeRestartScheduler.lock:
                                NodeRestartScheduler._waiting_ons[(pod, namespace)] = node.waiting_on()
                            ctx.log2(f'[{ts()}] {pod}@{namespace} is not restartable{ir}.')

                    if not restarted:
                        # ctx.log2(f'[{ts()}] Did not find any restartable pods.')
                        time.sleep(5)

                # trigger cleaning up of restartings
                NodeRestartScheduler.restartings(ctx=ctx)

                time.sleep(5)
            except:
                # container not found "cassandra"
                # nodetool ring, status or cql queries to get the host ids can fail any moment,
                # ignore the errors and start over in the next loop
                # traceback.print_exc()
                pass