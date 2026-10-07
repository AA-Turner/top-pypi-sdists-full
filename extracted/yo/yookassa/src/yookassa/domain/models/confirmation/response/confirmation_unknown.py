# -*- coding: utf-8 -*-
from yookassa.domain.common.confirmation_type import ConfirmationType
from yookassa.domain.models.confirmation.confirmation import Confirmation


class ConfirmationUnknown(Confirmation):
    """
    Неизвестный сценарий подтверждения.
    """  # noqa: E501

    def __init__(self, *args, **kwargs):
        super(ConfirmationUnknown, self).__init__(*args, **kwargs)
        if self.type is None or self.type is not ConfirmationType.UNKNOWN:
            self.type = ConfirmationType.UNKNOWN
