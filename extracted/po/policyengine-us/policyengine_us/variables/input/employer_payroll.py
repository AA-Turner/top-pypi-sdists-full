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


class employer_headcount(Variable):
    value_type = int
    entity = Person
    label = "Employer headcount"
    documentation = (
        "Employer employee count used as a proxy for size-based payroll "
        "contribution rules, including paid leave and similar programs."
    )
    definition_period = YEAR
    default_value = 100


class employer_quarterly_payroll_expense_override(Variable):
    value_type = float
    entity = Person
    label = "Employer quarterly payroll expense override"
    documentation = (
        "Optional override for employer quarterly payroll expense used by "
        "payroll-expense taxes such as New York's MCTMT. Set to a non-negative "
        "amount to replace the model proxy."
    )
    unit = USD
    definition_period = YEAR
    default_value = -1


class employer_total_payroll_tax_gross_wages(Variable):
    value_type = float
    entity = Person
    label = "Employer total payroll tax gross wages"
    documentation = (
        "Aggregate employer payroll-tax wages for employer-only payroll tax "
        "calculations."
    )
    unit = USD
    definition_period = YEAR
    default_value = 0


class employer_total_taxable_earnings_for_social_security(Variable):
    value_type = float
    entity = Person
    label = "Employer total taxable earnings for Social Security"
    documentation = (
        "Aggregate employer taxable earnings under the Social Security wage "
        "base for employer-only payroll tax calculations."
    )
    unit = USD
    definition_period = YEAR
    default_value = 0


class employer_total_taxable_earnings_for_federal_unemployment_tax(Variable):
    value_type = float
    entity = Person
    label = "Employer total taxable earnings for federal unemployment tax"
    documentation = (
        "Aggregate employer taxable earnings for FUTA in employer-only "
        "payroll tax calculations."
    )
    unit = USD
    definition_period = YEAR
    default_value = 0


class employer_total_taxable_earnings_for_state_unemployment_tax(Variable):
    value_type = float
    entity = Person
    label = "Employer total taxable earnings for state unemployment tax"
    documentation = (
        "Aggregate employer taxable earnings for state unemployment taxes and "
        "related employer taxes that share that base."
    )
    unit = USD
    definition_period = YEAR
    default_value = 0


class employer_ny_mctmt_zone_1_quarterly_payroll_expense(Variable):
    value_type = float
    entity = Person
    label = "Employer quarterly MCTMT payroll expense in New York Zone 1"
    documentation = (
        "Aggregate employer quarterly payroll expense in New York MCTMT Zone 1 "
        "for employer-only payroll tax calculations."
    )
    unit = USD
    definition_period = YEAR
    default_value = 0


class employer_ny_mctmt_zone_2_quarterly_payroll_expense(Variable):
    value_type = float
    entity = Person
    label = "Employer quarterly MCTMT payroll expense in New York Zone 2"
    documentation = (
        "Aggregate employer quarterly payroll expense in New York MCTMT Zone 2 "
        "for employer-only payroll tax calculations."
    )
    unit = USD
    definition_period = YEAR
    default_value = 0
