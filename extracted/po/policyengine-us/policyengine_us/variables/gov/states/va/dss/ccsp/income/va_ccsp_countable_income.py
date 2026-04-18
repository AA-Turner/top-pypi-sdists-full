from policyengine_us.model_api import *


class va_ccsp_countable_income(Variable):
    value_type = float
    entity = SPMUnit
    label = "Virginia Child Care Subsidy Program countable income"
    unit = USD
    definition_period = MONTH
    defined_for = StateCode.VA
    reference = (
        "https://law.lis.virginia.gov/admincode/title8/agency20/chapter790/section40/",
        "https://doe.virginia.gov/home/showpublisheddocument/56270#page=63",
    )

    adds = "gov.states.va.dss.ccsp.income.countable_income.sources"
    subtracts = "gov.states.va.dss.ccsp.income.countable_income.subtracts"
