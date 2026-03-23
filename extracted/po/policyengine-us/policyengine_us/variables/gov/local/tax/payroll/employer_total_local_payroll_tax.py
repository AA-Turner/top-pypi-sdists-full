from policyengine_us.model_api import *


class employer_total_local_payroll_tax(Variable):
    value_type = float
    entity = Person
    label = "Employer total local payroll tax"
    documentation = (
        "Employer-level local and regional payroll tax liability from "
        "aggregate employer inputs."
    )
    definition_period = YEAR
    unit = USD
    adds = ["ny_mctmt_total_employer_tax"]
