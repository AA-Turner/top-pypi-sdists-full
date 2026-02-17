from concurrent.futures import ThreadPoolExecutor

from adam.commands.command import Command
from adam.utils_repl.repl_state import ReplState
from adam.utils_concurrent import ThreadPool
from adam.utils_tabulize import tabulize

class ShowThreadPools(Command):
    COMMAND = 'show thread pools'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(ShowThreadPools, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return ShowThreadPools.COMMAND

    def aliases(self):
        return ['stp']

    def run(self, cmd: str, state: ReplState):
        if not self.args(cmd):
            return super().run(cmd, state)

        with self.context() as (_, ctx):
            def line(name: str, pool: ThreadPool):
                exec: ThreadPoolExecutor = pool.executor()
                return f'{name}\t{exec._max_workers}\t{pool.max_concurrency}\t{exec._work_queue.qsize()}\t{pool.dispatched - pool.completed}\t{pool.completed}'

            tabulize([(name, exec) for name, exec in ThreadPool.pools.items()],
                    fn=lambda p: line(p[0], p[1]),
                    header='POOL\tWORKERS\tMAX_CONCURRENCY\tPENDING\tRUNNING\tCOMPLETED',
                    separator='\t',
                    ctx=ctx)

            return state

    def completion(self, state: ReplState):
        return super().completion(state)

    def help(self, state: ReplState):
        return super().help(state, 'show worker thread pools status')