#!/usr/bin/env python3

from __future__ import annotations

import json
import logging
import shutil
import sys
import typing as t
import uuid
from collections import defaultdict
from json import JSONDecodeError
from pathlib import Path

import click

from globus_identity_mapping.errors import InvalidMappingError
from globus_identity_mapping.loader import load_mappers

from .protocol import IdentityMappingProtocol

logging.basicConfig(format="%(message)s")
logger = logging.getLogger(__name__)

# Not useful for script, but the protocol requires it
_TESTING_SCRIPT_CONNECTOR_ID = str(uuid.UUID("0" * 32))
_TESTING_GATEWAY_ID = str(uuid.UUID("1" * 32))


# Note that the \b is a signal to Click to not line-wrap when possible
# and the Globus CLI terminal link is re-phrased to be at the end of the
# sentence because otherwise line breaks are not calculated correctly by
# the terminal/Click

CLI_USAGE = """
Loads the specified identity mapping configuration and attempts to map the
passed in identity (stdin or --identities).

This command will return a non zero exit code in case of failures: 2 when
the input can't be read and 1 otherwise.

Example invocations:

\b  $ {prog} -c ./new_config.json -i ./test_identity_list.json\n
\b  $ {prog} --config ./another_config.json < /another/identity_list.json

Note that to test different identities, one way of generating a data structure
required for identity mapping can be emitted by `get-identities` using the
\033]8;;https://pypi.org/project/globus-cli/\033\\Globus CLI\033]8;;\033\\

\b  $ globus get-identities user@host -F json | {prog} --config ./some_config.json
"""

ordinals = defaultdict(lambda: "th", {1: "st", 2: "nd", 3: "rd"})


class ValidatingMapper:
    def __init__(self, mappings: t.Iterable[dict]):
        self._identity_mappings: list[IdentityMappingProtocol] = []
        self.identity_mappings = mappings

    @property
    def identity_mappings(self):
        return self._identity_mappings

    @identity_mappings.setter
    def identity_mappings(self, mappings_list: t.Iterable[dict] | None):
        self._identity_mappings = load_mappers(
            mappings_list, _TESTING_SCRIPT_CONNECTOR_ID, _TESTING_GATEWAY_ID
        )

    def map_identity(
        self, identity_set: t.Collection[t.Mapping[str, str]]
    ) -> str | None:
        num_mappers = len(self.identity_mappings)
        num_idents = len(identity_set)
        for m_i, mapper in enumerate(self.identity_mappings, start=1):
            m_ord = ordinals[m_i % 10]
            logger.info(f"Using {m_i}{m_ord} mapper [of {num_mappers}]")
            for id_i, ident_data in enumerate(identity_set, start=1):
                id_ord = ordinals[id_i % 10]
                logger.info(f"  Mapping {id_i}{id_ord} identity [of {num_idents}]")
                try:
                    identity = mapper.map_identity(ident_data)
                except Exception as e:
                    logger.error(f"   Failed to map identity ({type(e).__name__}) {e}")
                    continue
                if identity:
                    return identity
        return None

    def map_identities(self, identity_set: t.Collection[t.Mapping[str, str]]):
        num_mappers = len(self.identity_mappings)
        mapped = []
        for m_i, mapper in enumerate(self.identity_mappings, start=1):
            m_ord = ordinals[m_i % 10]
            logger.info(f"Using {m_i}{m_ord} mapper [of {num_mappers}]")
            try:
                mapped.extend(mapper.map_identities(identity_set))
            except Exception as e:
                logger.error(f"  Failed to map identities -- ({type(e).__name__}) {e}")
                continue
        return mapped


def get_input_from(config: str, id_path: str | None = None):
    """
    Given a config str taken to be a Path, read its contents and convert to object.
    Given an id_path, read its contents and convert to an object, or read
      contents from stdin if not present

    :param config:  Path to an identity mapping config file
    :param id_path: Path to a file with a list of identities
    :return:   A pair of objects representing the config and identities.
                 Exception will be raised if the inputs are invalid or empty
    """
    try:
        config_text = Path(config)
        config_obj = json.loads(config_text.read_text())
    except (IsADirectoryError, FileNotFoundError, JSONDecodeError) as e:
        config_err_msg = f"Failed to read config: ({type(e).__name__}) {e}"
        logger.error(config_err_msg)
        raise
    except Exception as e:
        config_err_msg = (
            f"Failed to read mapping configuration from ({config}): "
            f" ({type(e).__name__}) {e}"
        )
        logger.error(config_err_msg)
        # Standardize unknown Exceptions to ValueError
        raise ValueError(config_err_msg)

    try:
        if id_path:
            id_text = Path(id_path).read_text()
        else:
            if not sys.stdin:
                id_err_msg = "Identities Path not provided and stdin is not available"
                logger.error(id_err_msg)
                raise FileNotFoundError(id_err_msg)

            if sys.stdin.isatty():
                logger.info(
                    "Awaiting JSON list of identities; Ctrl+D on empty line when done."
                )

            id_text = sys.stdin.read()
        identities: list | dict = json.loads(id_text)
        if isinstance(identities, dict):
            # A convenience allowing `globus get-identities -F json ... | this_script`
            identities = identities["identities"]
        elif not isinstance(identities, list):
            id_err_msg = f"Expected list of identities, not {type(identities).__name__}"
            logger.error(id_err_msg)
            raise SyntaxError(id_err_msg)
    except KeyboardInterrupt:
        logger.info("User Interrupt, exiting")
        # user requested to quit via Ctrl+C
        raise KeyboardInterrupt("Exiting from user initiated interrupt")
    except (IsADirectoryError, FileNotFoundError, JSONDecodeError) as e:
        config_err_msg = f"Failed to parse identities: ({type(e).__name__}) {e}"
        logger.error(config_err_msg)
        raise
    except Exception as e:
        id_source = id_path if id_path else "stdin"
        id_err_msg = (
            f"Failed to read identities from ({id_source}): "
            f"({type(e).__name__}) {e}"
        )
        logger.error(id_err_msg)
        if isinstance(e, JSONDecodeError):
            raise
        else:
            raise ValueError(id_err_msg)

    return config_obj, identities


def do_validate(config: str, identities: str, verbose: bool, first: bool):
    """
    Currently we return 0 for success or user interrupt, 2 for command line
    issues including missing/mispelled filenames, and 1 for all other errors.

    Some exit codes are commented out, in case we decide to use specific
    pre-defined unique ones instead.
    """
    logger.setLevel(logging.ERROR)
    if verbose:
        logger.setLevel(logging.INFO)

    try:
        mapping_config, id_list = get_input_from(config, identities)
        # Error already logged to stderr in get_input_from() when appropriate
    except KeyboardInterrupt:
        # return 128 + SIGINT  # by convention 128 + signal, but 127+ is iffy
        # according to https://docs.python.org/2/library/sys.html#sys.exit
        return 0
    except (IsADirectoryError, FileNotFoundError):
        # return os.EX_NOINPUT  # 66
        return 2
    except (JSONDecodeError, SyntaxError, ValueError):
        # return os.EX_USAGE  # 64
        return 1
    except Exception:
        # catch all
        return 1

    try:
        id_mapper = ValidatingMapper(mapping_config)
    except InvalidMappingError as e:
        logger.error(f"Failed to load mapping from config -- ({type(e).__name__}) {e}")
        return 1
    except Exception as e:
        # Catch all in case, though this shouldn't occur
        logger.error(f"Unexpected mapping error: ({type(e).__name__}) {e}")
        return 1

    if first:
        result_ids = [id_mapper.map_identity(id_list)]
    else:
        result_ids = id_mapper.map_identities(id_list)

    if not result_ids:
        print("\nNo identity mapped.")
    else:
        if first:
            print(f"\nFirst found mapped identity: {result_ids[0]}")
        else:
            print(f"\nAll mapped identities: \n{json.dumps(result_ids, indent=2)}")

    return 0


@click.command(
    no_args_is_help=True,
    epilog=CLI_USAGE.format(
        prog=sys.argv[0].rsplit("/", 1)[1],
    ),
    context_settings={"max_content_width": shutil.get_terminal_size().columns},
)
@click.help_option("--help", "-h")
@click.option(
    "-c",
    "--config",
    required=True,
    help="path to a JSON identity mapping configuration file",
)
@click.option(
    "-i",
    "--identities",
    required=False,
    help="path to a JSON formatted identities list, or from stdin if not provided",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    default=False,
    required=False,
    help="display verbose validation output",
)
@click.option(
    "--first/--all",
    "-f/-a",
    default=False,
    required=True,
    help="return the first matched identity or all matched identities",
)
def validate(config: str, identities: str, verbose: bool, first: bool):
    # Just a wrapper to simplify testing
    sys.exit(do_validate(config, identities, verbose, first))
