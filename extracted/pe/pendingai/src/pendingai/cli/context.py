#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from typing import TypedDict

from typer import Context as TyperContext

from pendingai.client import PendingAiClient


class PendingAiContext(TyperContext):
    class Object(TypedDict):
        client: PendingAiClient

    obj: Object
