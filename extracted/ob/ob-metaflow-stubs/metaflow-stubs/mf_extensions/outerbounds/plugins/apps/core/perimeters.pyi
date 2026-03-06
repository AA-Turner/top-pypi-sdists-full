######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.20.1+obcheckpoint(0.2.10);<unk>(<unk>);ob(v1)                                     #
# Generated on 2026-03-05T21:57:32.419544                                                            #
######################################################################################################

from __future__ import annotations

import typing

from .utils import safe_requests_wrapper as safe_requests_wrapper
from .exceptions import OuterboundsConfigurationException as OuterboundsConfigurationException

class PerimeterExtractor(object, metaclass=type):
    @classmethod
    def for_ob_cli(cls, config_dir: str, profile: str) -> typing.Union[typing.Tuple[str, str], typing.Tuple[None, None]]:
        """
        This function will be called when we are trying to extract the perimeter
        via the ob cli's execution. We will rely on the following logic:
        1. check environment variables like OB_CURRENT_PERIMETER / OBP_PERIMETER
        2. run init config to extract the perimeter related configurations.
        
        Returns
        -------
            Tuple[str, str] : Tuple containing perimeter name , API server url.
        """
        ...
    @classmethod
    def during_programmatic_access(cls) -> typing.Union[typing.Tuple[str, str], typing.Tuple[None, None]]:
        ...
    @classmethod
    def config_during_programmatic_access(cls) -> dict:
        ...
    ...

