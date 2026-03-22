from policyengine_us.model_api import *


class employer_state_unemployment_tax_rate_override(Variable):
    value_type = float
    entity = Person
    label = "Employer state unemployment tax rate override"
    documentation = (
        "Optional employer-specific override for the employer-side state "
        "unemployment tax rate. Set to a non-negative rate to replace the "
        "model default."
    )
    unit = "/1"
    definition_period = YEAR
    default_value = -1
