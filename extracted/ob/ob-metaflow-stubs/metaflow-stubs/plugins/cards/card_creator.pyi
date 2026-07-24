######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.34.1+obcheckpoint(0.2.10);<unk>(<unk>);ob(v1)                                     #
# Generated on 2026-07-23T20:46:33.337981                                                            #
######################################################################################################

from __future__ import annotations

import typing

from ...metaflow_current import current as current

ASYNC_TIMEOUT: int

class CardProcessManager(object, metaclass=type):
    """
    This class is responsible for managing the card creation processes.
    """
    ...

class CardCreator(object, metaclass=type):
    def __init__(self, top_level_options, should_save_metadata_lambda: typing.Callable[[str], typing.Tuple[bool, typing.Dict]]):
        ...
    def create(self, card_uuid = None, user_set_card_id = None, runtime_card = False, decorator_attributes = None, card_options = None, logger = None, mode = 'render', final = False, sync = False):
        ...
    ...

