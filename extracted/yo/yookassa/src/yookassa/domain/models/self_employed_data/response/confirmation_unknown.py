# -*- coding: utf-8 -*-
from yookassa.domain.models.self_employed_data.confirmation import SelfEmployedConfirmation, \
    SelfEmployedConfirmationType


class SelfEmployedConfirmationUnknown(SelfEmployedConfirmation):
    """
    Неизвестный сценарий подтверждения самозанятого.
    """  # noqa: E501

    def __init__(self, *args, **kwargs):
        super(SelfEmployedConfirmationUnknown, self).__init__(*args, **kwargs)
        if self.type is None or self.type is not SelfEmployedConfirmationType.UNKNOWN:
            self.type = SelfEmployedConfirmationType.UNKNOWN
