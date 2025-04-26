from ..utils import console, log_interactions


def exit() -> bool:
    with log_interactions("example-exit"):
        console.print("See you next time :wave:")
    return False
