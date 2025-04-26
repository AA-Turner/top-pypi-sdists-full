import argparse
import copy

def define_argument(*args, **kwargs):
    """
    Define an argument for a command
    """
    return dict(args=args, kwargs=kwargs)

def create_parser(arguments, defaults={}):
    """
    Create argparse.ArgumentParser instance from given argument definitions and optional additional defaults.
    """
    prefix_char = '-'
    parser = argparse.ArgumentParser()
    for argument in arguments:
        args = copy.copy(argument['args'])
        kwargs = copy.copy(argument['kwargs'])
        # Create a dummy parser to get info about the arguments
        dummy_parser = argparse.ArgumentParser()
        dummy_action = dummy_parser.add_argument(*args, **kwargs)
        if dummy_action.dest in defaults:
            kwargs['default'] = defaults[dummy_action.dest]
            kwargs['required'] = False
            if not dummy_action.option_strings:
                # Convert positional argument to an optional one
                args = [2 * prefix_char + dummy_action.dest.replace('_', '-')]
                kwargs['dest'] = dummy_action.dest
        parser.add_argument(*args, **kwargs)
    return parser
