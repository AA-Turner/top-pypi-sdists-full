# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class MeterTemplateResponse(Model):
    """MeterTemplateResponse.

    :param form_template_id: The form template identifier
    :type form_template_id: int
    :param display_order: The meter template display order
    :type display_order: int
    :param begin_date: The begin date for the template on the account meter
    :type begin_date: datetime
    :param end_date: The end date for the template on the account meter
    :type end_date: datetime
    :param template:
    :type template: ~energycap.sdk.models.TemplateChild
    :param account:
    :type account: ~energycap.sdk.models.MeterAccountChild
    """

    _attribute_map = {
        'form_template_id': {'key': 'formTemplateId', 'type': 'int'},
        'display_order': {'key': 'displayOrder', 'type': 'int'},
        'begin_date': {'key': 'beginDate', 'type': 'iso-8601'},
        'end_date': {'key': 'endDate', 'type': 'iso-8601'},
        'template': {'key': 'template', 'type': 'TemplateChild'},
        'account': {'key': 'account', 'type': 'MeterAccountChild'},
    }

    def __init__(self, *, form_template_id: int=None, display_order: int=None, begin_date=None, end_date=None, template=None, account=None, **kwargs) -> None:
        super(MeterTemplateResponse, self).__init__(**kwargs)
        self.form_template_id = form_template_id
        self.display_order = display_order
        self.begin_date = begin_date
        self.end_date = end_date
        self.template = template
        self.account = account
