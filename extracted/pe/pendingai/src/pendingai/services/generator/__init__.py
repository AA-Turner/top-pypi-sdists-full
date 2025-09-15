#!/usr/bin/env python3
# -*- coding:utf-8 -*-


from pendingai.services.generator.models import ModelInterface
from pendingai.services.generator.samples import SampleInterface
from pendingai.services.service import PendingAiService


class GeneratorService(PendingAiService):
    """
    Pending AI generator service.
    """

    models: ModelInterface
    samples: SampleInterface
