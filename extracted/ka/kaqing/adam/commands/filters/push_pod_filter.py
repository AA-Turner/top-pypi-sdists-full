from typing import Callable
from adam.commands.command_filter import CommandFilter
from adam.repl_state import ReplState

class PushPodFilter(CommandFilter):
    def command(self) -> str:
        return '@<pod-name>'

    def process(self, state: ReplState, cmd: str) -> tuple[Callable[[], None], ReplState, str]:
        state, cmd = targetted(state, cmd)
        return None, state, cmd

    def help(self, state: ReplState) -> str:
        return super().help(state, 'run command on a pod', command='@<pod-name> <command>...')

def targetted(state: ReplState, cmd: str):
    if not (cmd.startswith('@') and len(arry := cmd.split(' ')) > 1):
        return state, cmd

    if state.device == ReplState.A and state.app_app or state.device == ReplState.P:
        state.push(pod_targetted=True)

        state.app_pod = arry[0].strip('@')
        cmd = ' '.join(arry[1:])
    elif state.device == ReplState.P:
        state.push(pod_targetted=True)

        state.app_pod = arry[0].strip('@')
        cmd = ' '.join(arry[1:])
    elif state.sts:
        state.push(pod_targetted=True)

        state.pod = arry[0].strip('@')
        cmd = ' '.join(arry[1:])

    return (state, cmd)