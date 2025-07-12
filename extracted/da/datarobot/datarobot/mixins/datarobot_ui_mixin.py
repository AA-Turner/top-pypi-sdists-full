#
# Copyright 2024-2025 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.

from typing import Any, Dict, Union

from datarobot.utils import camelize_obj


class DatarobotUIMixin:
    """A mixin exposes `_repr_mimebundle_` that is called by ipython kernel for cell results output.
    Expects class to define `_datarobot_ui_mime_type` for mapping UI component for results rendering and
    `_get_datarobot_ui_data` method that provides data for UI component
    """

    # pylint: disable-next=unused-argument
    def _repr_mimebundle_(  # type: ignore[no-untyped-def]
        self, include=None, exclude=None
    ) -> Union[None, Dict[str, Any]]:
        if not hasattr(self, "_datarobot_ui_mime_type") or not hasattr(
            self, "_get_datarobot_ui_data"
        ):
            return None
        return {self._datarobot_ui_mime_type: {"data": camelize_obj(self._get_datarobot_ui_data())}}
