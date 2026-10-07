# -*- coding: utf-8 -*-
from yookassa.domain.common.data_context import DataContext
from yookassa.domain.models.self_employed_data.confirmation import SelfEmployedConfirmationType
from yookassa.domain.models.self_employed_data.request.confirmation_redirect import \
    SelfEmployedConfirmationRedirect as RequestConfirmationRedirect
from yookassa.domain.models.self_employed_data.response.confirmation_redirect import \
    SelfEmployedConfirmationRedirect as ResponseConfirmationRedirect
from yookassa.domain.models.self_employed_data.response.confirmation_unknown import \
    SelfEmployedConfirmationUnknown as ResponseConfirmationUnknown


class SelfEmployedConfirmationClassMap(DataContext):
    """
    Сопоставление классов SelfEmployedConfirmation по типу.
    """  # noqa: E501

    def __init__(self):
        super(SelfEmployedConfirmationClassMap, self).__init__(('request', 'response'))

    @property
    def request(self):
        return {
            SelfEmployedConfirmationType.REDIRECT: RequestConfirmationRedirect,
        }

    @property
    def response(self):
        return {
            SelfEmployedConfirmationType.REDIRECT: ResponseConfirmationRedirect,
            SelfEmployedConfirmationType.UNKNOWN: ResponseConfirmationUnknown,
        }
