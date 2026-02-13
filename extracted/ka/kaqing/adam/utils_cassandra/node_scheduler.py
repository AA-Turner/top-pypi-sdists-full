from datetime import datetime
import threading
import time
import traceback

from adam.config import Config
from adam.repl_state import ReplState
from adam.utils_cassandra.node_restartability import NodeRestartability
from adam.utils_cassandra.node_schedules import NodeSchedules
from adam.utils_context import NULL, Context
from adam.utils_k8s.pods import Pods, strip_pod_name

def ts():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def key(pod: str, namespace: str):
    return f'{pod}@{namespace}'

class NodeScheduler:
    nodes_thread: threading.Thread = None
    # context with the first schedule() invocation is used for the event loop
    _ctx: Context = None

    def schedule(state: ReplState, pod: str, ctx: Context):
        NodeScheduler.start(state, ctx)

        NodeScheduler._ctx.log2(f'[{ts()}] Restart requested for {strip_pod_name(pod)}@{state.namespace}.')
        with NodeSchedules.lock:
            NodeSchedules._queue[(pod, state.namespace)] = time.time()

    def start(state: ReplState, ctx: Context):
        with NodeSchedules.lock:
            if not NodeScheduler.nodes_thread:
                ctx = ctx.copy(background=True, bg_init_msg='[{job_id}] Use :?? to get node scheduling status.')

                NodeScheduler._ctx = ctx
                NodeScheduler.nodes_thread = threading.Thread(target=NodeScheduler.loop, args=(state, ctx,), daemon=True)
                NodeScheduler.nodes_thread.start()

    def restart_node(pod: str, namespace: str, ctx: Context):
        with NodeSchedules.lock:
            key = (pod, namespace)
            if key in NodeSchedules._queue:
                del NodeSchedules._queue[key]
            NodeSchedules._in_restartings[key] = time.time()

        Pods.delete(pod, namespace)

    def cancel_restarts(state: ReplState, pods: list[str], timeout: int = 0, ctx = NULL):
        canceled: dict[tuple[str, str], float] = {}

        # 1. delete from the pending queue first
        for pod in pods:
            key = (pod, state.namespace)
            with NodeSchedules.lock:
                if key in NodeSchedules._queue:
                    ts = NodeSchedules._queue[key]
                    del NodeSchedules._queue[key]
                    canceled[key] = ts

        # 2. the pod could've been deleted on step 1, however, yet possible to leak into the restarting queue
        # deleting from the restarting is fine as DN condition will kick in
        for pod, ts in NodeSchedules.restartings(timeout, ctx=ctx).copy().items():
            if pod[1] == state.namespace and pod[0] in pods:
                with NodeSchedules.lock:
                    try:
                        NodeSchedules.done(pod, NodeScheduler._ctx)
                        canceled[pod] = ts
                    except:
                        pass

        return canceled

    # single queue pattern
    def loop(state: ReplState, ctx = NULL):
        while True:
            try:
                t0: float = 0
                while (pods := NodeSchedules.pending().keys()):
                    checked = 0
                    restarted = 0
                    for pod, namespace in pods:
                        checked += 1

                        in_restartings = NodeSchedules.restartings(ctx=ctx)
                        ir = ''
                        if in_restartings:
                            ir = f', in_restarting:[{", ".join([f"{r[0]}@{r[1]}" for r in in_restartings])}]'

                        node: NodeRestartability = NodeRestartability.probe(state.with_namespace(namespace), pod, in_restartings=in_restartings, ctx=ctx.copy(show_out=False, background=False))
                        if node.restartable():
                            ctx.log2(f'[{ts()}] Restarting {pod}@{namespace}{ir}.')
                            NodeScheduler.restart_node(pod, namespace, ctx)

                            restarted += 1

                            with NodeSchedules.lock:
                                if (pod, namespace) in NodeSchedules._waiting_ons:
                                    del NodeSchedules._waiting_ons[(pod, namespace)]
                        else:
                            with NodeSchedules.lock:
                                NodeSchedules._waiting_ons[(pod, namespace)] = node.waiting_on()

                    if not restarted:
                        if checked:
                            # log line every 60+ secs
                            if not t0 or time.time() - t0 > 60:
                                t0 = time.time()
                                ctx.log2(f'[{ts()}] No pods are restartable.')
                        else:
                            t0 = 0

                        time.sleep(5)

                # trigger cleaning up of restartings
                NodeSchedules.restartings(ctx=ctx)

                time.sleep(5)
            except:
                if Config().is_debug():
                    traceback.print_exc()
                # container not found "cassandra"
                # nodetool ring, status or cql queries to get the host ids can fail any moment,
                # ignore the errors and start over in the next loop
                # traceback.print_exc()