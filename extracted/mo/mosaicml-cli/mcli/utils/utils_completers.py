""" Argcomplete completer functions for mcli commands
"""
import argparse
from collections import defaultdict
from typing import Optional, Sequence, Set

import argcomplete

from mcli.api.cluster.api_get_clusters import get_clusters
from mcli.api.inference_deployments.api_get_inference_deployments import get_inference_deployments
from mcli.api.runs.api_get_runs import get_runs
from mcli.utils.utils_model import SubmissionType


def get_primary_option(options: Sequence[str]) -> str:
    """ Gets the primary option name from a list of options"""
    main = ''
    for o in options:
        if 'platform' in o:
            continue  # legacy - should never be the main option

        # Otherwise, prefer the longer (more descriptive) option
        if len(o) > len(main):
            main = o
    return main


def get_exclude_from_parser(
    parser: argparse.ArgumentParser,
    prog_to_names: defaultdict,
    exclude: Set[str],
) -> Set[str]:
    """
    Gets the list of options to exclude from argcomplete

    Args:
        parser: The parser to get the exclude list from
        prog_to_names: A dictionary mapping subparser prog names to their aliases
        exclude: The current exclude list

        Note: recursively calls itself to get the exclude list for subparsers

    Returns:
        The updated exclude set
    """
    for arg in parser._actions:  # pylint: disable=protected-access
        if len(arg.option_strings) > 1:
            main = get_primary_option(arg.option_strings)
            for o in arg.option_strings:
                if o != main:
                    exclude.add(o)

        if arg.choices:
            if not isinstance(arg.choices, dict):
                continue

            for key, subparser in arg.choices.items():
                prog_to_names[subparser.prog].append(key)
                # recursively get the exclude list for the subparser
                exclude = get_exclude_from_parser(subparser, prog_to_names, exclude)

    # If there are multiple options for a subparser, exclude all but the main option
    for names in prog_to_names.values():
        if len(names) == 1:
            continue

        main = get_primary_option(names)
        for name in names:
            if name != main:
                exclude.add(name)

    excluded_from_exclude = {
        # Run is a special case: It's both a noun and verb (eg mcli delete runs and mcli run)
        "run",
    }
    return {i for i in exclude if i not in excluded_from_exclude}


def apply_autocomplete(parser: argparse.ArgumentParser) -> None:
    exclude = get_exclude_from_parser(parser, defaultdict(list), set())
    argcomplete.autocomplete(
        parser,
        exclude=exclude,  # type: ignore
        always_complete_options='long',
    )


# NOTE: very important that the init function never makes a mapi request


class ClusterNameCompleter:
    """ Argcomplete completer for cluster names
    """

    def __call__(self, **kwargs):
        return sorted(c.name for c in get_clusters())


class GPUTypeCompleter:
    """ Argcomplete completer for gpu types
    """

    def __call__(self, **kwargs):
        return sorted(i.gpu_type for c in get_clusters() for i in c.cluster_instances)


class InstanceNameCompleter:
    """ Argcomplete completer for instance names
    """

    def __call__(self, **kwargs):
        return sorted(i.name for c in get_clusters() for i in c.cluster_instances)


class NodeNameCompleter:
    """ Argcomplete completer for instance names
    """

    def __call__(self, **kwargs):
        return sorted(j.name for c in get_clusters() for i in c.cluster_instances for j in i.node_details)


class RunStatusCompleter:
    """ Argcomplete completer for run statuses
    """

    def __call__(self, **kwargs):
        return SubmissionType.get_status_options(SubmissionType.TRAINING)


class RunNameCompleter:
    """ Argcomplete completer for run names
    """

    limit: Optional[int] = None

    def __init__(self, limit: Optional[int] = 50):
        self.limit = limit

    def __call__(self, **kwargs):
        return sorted(r.name for r in get_runs(limit=self.limit))


class DeploymentStatusCompleter:
    """ Argcomplete completer for deployment statuses
    """

    def __call__(self, **kwargs):
        return SubmissionType.get_status_options(SubmissionType.INFERENCE)


class DeploymentNameCompleter:
    """ Argcomplete completer for deployment names
    """

    def __init__(self):
        # TODO: implement deployment pagination and limits
        pass

    def __call__(self, **kwargs):
        return sorted(r.name for r in get_inference_deployments())
