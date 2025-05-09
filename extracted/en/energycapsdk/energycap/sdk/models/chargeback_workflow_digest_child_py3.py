# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class ChargebackWorkflowDigestChild(Model):
    """This class inherits all of the billing period summary properties for a
    source meter
    and adds a list of billing period summaries for each bill split destination
    meter.

    :param splits: List of billing period summaries for meters that are
     children of a bill split source meter.
     This list will be null for calculated source meters.
    :type splits:
     list[~energycap.sdk.models.ChargebackWorkflowDigestSplitChild]
    :param meter:
    :type meter: ~energycap.sdk.models.MeterChild
    :param current_period:
    :type current_period: ~energycap.sdk.models.BillingPeriodUseCostChild
    :param prior_period:
    :type prior_period: ~energycap.sdk.models.BillingPeriodUseCostDeltaChild
    :param prior_year:
    :type prior_year: ~energycap.sdk.models.BillingPeriodUseCostDeltaChild
    """

    _attribute_map = {
        'splits': {'key': 'splits', 'type': '[ChargebackWorkflowDigestSplitChild]'},
        'meter': {'key': 'meter', 'type': 'MeterChild'},
        'current_period': {'key': 'currentPeriod', 'type': 'BillingPeriodUseCostChild'},
        'prior_period': {'key': 'priorPeriod', 'type': 'BillingPeriodUseCostDeltaChild'},
        'prior_year': {'key': 'priorYear', 'type': 'BillingPeriodUseCostDeltaChild'},
    }

    def __init__(self, *, splits=None, meter=None, current_period=None, prior_period=None, prior_year=None, **kwargs) -> None:
        super(ChargebackWorkflowDigestChild, self).__init__(**kwargs)
        self.splits = splits
        self.meter = meter
        self.current_period = current_period
        self.prior_period = prior_period
        self.prior_year = prior_year
