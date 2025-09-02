from argparse import ArgumentParser, Namespace


class Command(object):
    def __init__(self, argument_parser: ArgumentParser) -> None:
        pass

    def __call__(self, args: Namespace) -> int:
        raise NotImplementedError()
