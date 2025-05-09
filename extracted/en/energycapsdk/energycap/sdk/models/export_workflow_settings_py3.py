# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class ExportWorkflowSettings(Model):
    """ExportWorkflowSettings.

    :param export_mode_enabled:
    :type export_mode_enabled: bool
    :param can_export:
    :type can_export: str
    """

    _attribute_map = {
        'export_mode_enabled': {'key': 'exportModeEnabled', 'type': 'bool'},
        'can_export': {'key': 'canExport', 'type': 'str'},
    }

    def __init__(self, *, export_mode_enabled: bool=None, can_export: str=None, **kwargs) -> None:
        super(ExportWorkflowSettings, self).__init__(**kwargs)
        self.export_mode_enabled = export_mode_enabled
        self.can_export = can_export
