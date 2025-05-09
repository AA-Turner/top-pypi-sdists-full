# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class BillHeaderUpdate(Model):
    """Bill header values to update.

    All required parameters must be populated in order to send to Azure.

    :param begin_date: Required.
    :type begin_date: ~energycap.sdk.models.BillHeaderUpdateBeginDateChild
    :param end_date: Required.
    :type end_date: ~energycap.sdk.models.BillHeaderUpdateEndDateChild
    :param due_date: Required.
    :type due_date: ~energycap.sdk.models.BillHeaderUpdateDueDateChild
    :param statement_date: Required.
    :type statement_date:
     ~energycap.sdk.models.BillHeaderUpdateStatementDateChild
    :param control_code: Required.
    :type control_code: ~energycap.sdk.models.BillHeaderUpdateControlCodeChild
    :param invoice_number: Required.
    :type invoice_number:
     ~energycap.sdk.models.BillHeaderUpdateInvoiceNumberChild
    :param account_period: Required.
    :type account_period:
     ~energycap.sdk.models.BillHeaderUpdateAccountPeriodChild
    :param billing_period: Required.
    :type billing_period:
     ~energycap.sdk.models.BillHeaderUpdateBillingPeriodChild
    :param estimated: Required.
    :type estimated: ~energycap.sdk.models.BillHeaderUpdateEstimatedChild
    """

    _validation = {
        'begin_date': {'required': True},
        'end_date': {'required': True},
        'due_date': {'required': True},
        'statement_date': {'required': True},
        'control_code': {'required': True},
        'invoice_number': {'required': True},
        'account_period': {'required': True},
        'billing_period': {'required': True},
        'estimated': {'required': True},
    }

    _attribute_map = {
        'begin_date': {'key': 'beginDate', 'type': 'BillHeaderUpdateBeginDateChild'},
        'end_date': {'key': 'endDate', 'type': 'BillHeaderUpdateEndDateChild'},
        'due_date': {'key': 'dueDate', 'type': 'BillHeaderUpdateDueDateChild'},
        'statement_date': {'key': 'statementDate', 'type': 'BillHeaderUpdateStatementDateChild'},
        'control_code': {'key': 'controlCode', 'type': 'BillHeaderUpdateControlCodeChild'},
        'invoice_number': {'key': 'invoiceNumber', 'type': 'BillHeaderUpdateInvoiceNumberChild'},
        'account_period': {'key': 'accountPeriod', 'type': 'BillHeaderUpdateAccountPeriodChild'},
        'billing_period': {'key': 'billingPeriod', 'type': 'BillHeaderUpdateBillingPeriodChild'},
        'estimated': {'key': 'estimated', 'type': 'BillHeaderUpdateEstimatedChild'},
    }

    def __init__(self, *, begin_date, end_date, due_date, statement_date, control_code, invoice_number, account_period, billing_period, estimated, **kwargs) -> None:
        super(BillHeaderUpdate, self).__init__(**kwargs)
        self.begin_date = begin_date
        self.end_date = end_date
        self.due_date = due_date
        self.statement_date = statement_date
        self.control_code = control_code
        self.invoice_number = invoice_number
        self.account_period = account_period
        self.billing_period = billing_period
        self.estimated = estimated
