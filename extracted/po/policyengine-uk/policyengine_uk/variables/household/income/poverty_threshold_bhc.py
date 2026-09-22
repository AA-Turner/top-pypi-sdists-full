from policyengine_uk.model_api import *


class poverty_threshold_bhc(Variable):
    label = "Poverty threshold (BHC)"
    documentation = (
        "The absolute poverty line before housing costs for a couple with no "
        "children, per year: 60% of the 2010/11 median uprated by CPI. "
        "Compare against equivalised income; poverty_line_bhc is the same "
        "line scaled to the household's equivalisation factor."
    )
    entity = Household
    definition_period = YEAR
    value_type = float
    unit = GBP

    def formula(household, period, parameters):
        return (
            parameters(period).household.poverty.absolute_poverty_threshold_bhc
            * WEEKS_IN_YEAR
        )
