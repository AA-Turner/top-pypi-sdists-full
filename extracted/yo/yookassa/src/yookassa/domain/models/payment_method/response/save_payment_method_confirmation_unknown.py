# -*- coding: utf-8 -*-
from yookassa.domain.common import ConfirmationType
from yookassa.domain.models.payment_method import SavePaymentMethodConfirmation


class SavePaymentMethodConfirmationUnknown(SavePaymentMethodConfirmation):
    """
    Неизвестный сценарий подтверждения привязки.
    """  # noqa: E501

    def __init__(self, *args, **kwargs):
        super(SavePaymentMethodConfirmationUnknown, self).__init__(*args, **kwargs)
        if self.type is None or self.type is not ConfirmationType.UNKNOWN:
            self.type = ConfirmationType.UNKNOWN
