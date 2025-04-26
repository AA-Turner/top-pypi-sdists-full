from typing import Optional

import anyscale
from anyscale._private.anyscale_client import AnyscaleClientInterface
from anyscale._private.sdk.base_sdk import BaseSDK
from anyscale._private.sdk.timer import Timer
from anyscale.cli_logger import BlockLogger
from anyscale.llm.model import LLMModelsSDK


class LLMSDK(BaseSDK):
    def __init__(
        self,
        *,
        logger: Optional[BlockLogger] = None,
        client: Optional[AnyscaleClientInterface] = None,
        timer: Optional[Timer] = None,
    ):
        self._model = LLMModelsSDK(logger=logger, client=client, timer=timer)

    @property
    def model(self):
        return self._model

    @property
    def dataset(self):
        return anyscale.llm.dataset
