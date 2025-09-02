#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from pendingai.services.retrosynthesis.batches import BatchInterface
from pendingai.services.retrosynthesis.engines import EngineInterface
from pendingai.services.retrosynthesis.jobs import JobInterface
from pendingai.services.retrosynthesis.libraries import LibraryInterface
from pendingai.services.service import PendingAiService


class RetrosynthesisService(PendingAiService):
    """
    Pending AI retrosynthesis service.
    """

    batches: BatchInterface
    engines: EngineInterface
    jobs: JobInterface
    libraries: LibraryInterface
