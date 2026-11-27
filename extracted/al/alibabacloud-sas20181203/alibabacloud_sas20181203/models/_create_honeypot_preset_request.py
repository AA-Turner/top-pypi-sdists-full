# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from darabonba.model import DaraModel

class CreateHoneypotPresetRequest(DaraModel):
    def __init__(
        self,
        honeypot_image_name: str = None,
        lang: str = None,
        meta: str = None,
        node_id: str = None,
        preset_name: str = None,
    ):
        # The name of the honeypot image.
        # 
        # This parameter is required.
        self.honeypot_image_name = honeypot_image_name
        # The language of the request and response. Default value: **zh**. Valid values:
        # - **zh**: Chinese
        # - **en**: English
        self.lang = lang
        # The custom parameters of the honeypot template. The value is a JSON string that contains the following fields:
        # - **portrait_option**: social tracing
        # - **burp**: Burp countermeasure
        # - **trojan_git**: Git countermeasure
        # 
        # This parameter is required.
        self.meta = meta
        # The unique ID of the honeypot management node.
        # > You can call the [ListHoneypotNode](~~ListHoneypotNode~~) operation to obtain this parameter.
        # 
        # This parameter is required.
        self.node_id = node_id
        # The custom name of the honeypot template.
        # 
        # This parameter is required.
        self.preset_name = preset_name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.honeypot_image_name is not None:
            result['HoneypotImageName'] = self.honeypot_image_name

        if self.lang is not None:
            result['Lang'] = self.lang

        if self.meta is not None:
            result['Meta'] = self.meta

        if self.node_id is not None:
            result['NodeId'] = self.node_id

        if self.preset_name is not None:
            result['PresetName'] = self.preset_name

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('HoneypotImageName') is not None:
            self.honeypot_image_name = m.get('HoneypotImageName')

        if m.get('Lang') is not None:
            self.lang = m.get('Lang')

        if m.get('Meta') is not None:
            self.meta = m.get('Meta')

        if m.get('NodeId') is not None:
            self.node_id = m.get('NodeId')

        if m.get('PresetName') is not None:
            self.preset_name = m.get('PresetName')

        return self

