from policyengine_us.model_api import *


class nj_ccap_countable_income(Variable):
    value_type = float
    entity = SPMUnit
    label = "New Jersey CCAP countable income"
    definition_period = MONTH
    unit = USD
    defined_for = StateCode.NJ
    reference = "https://www.childcarenj.gov/ChildCareNJ/media/media_library/CCDF_State_Plan_for_New_Jersey_FFY25-27.pdf#page=23"

    adds = "gov.states.nj.njdhs.ccap.income.countable_income.sources"
