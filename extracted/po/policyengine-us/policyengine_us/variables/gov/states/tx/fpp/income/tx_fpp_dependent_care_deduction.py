from policyengine_us.model_api import *


class tx_fpp_dependent_care_deduction(Variable):
    value_type = float
    entity = SPMUnit
    label = "Texas Family Planning Program dependent care deduction"
    unit = USD
    definition_period = YEAR
    reference = (
        "https://www.law.cornell.edu/regulations/texas/1-Tex-Admin-Code-SS-382-109",
        "https://www.hhs.texas.gov/handbooks/family-planning-program-policy-manual/4100-client-eligibility-screening-process",
    )
    defined_for = StateCode.TX

    def formula(spm_unit, period, parameters):
        p = parameters(period).gov.states.tx.fpp.income
        person = spm_unit.members
        expenses = person("pre_subsidy_childcare_expenses", period)
        age = person("age", period)
        # 1 TAC 382.109(2)(A) covers child dependents ($200 per month
        # under age two, $175 per month otherwise); (2)(B) limits the
        # adult deduction to dependent adults with a disability.
        is_child = age < p.child_age_threshold
        eligible_dependent = is_child | person("is_disabled", period)
        monthly_cap = p.dependent_care.calc(age)
        capped_expenses = min_(expenses, monthly_cap * MONTHS_IN_YEAR)
        return spm_unit.sum(capped_expenses * eligible_dependent)
