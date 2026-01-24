from snowflake.core.password_policy import PasswordPolicy


test_password_policy_template = PasswordPolicy(
    name="to_be_set",
    password_min_length=8,
    password_max_length=256,
    password_min_upper_case_chars=1,
    password_min_lower_case_chars=1,
    password_min_numeric_chars=1,
    password_min_special_chars=1,
    password_min_age_days=1,
    password_max_age_days=90,
    password_max_retries=5,
    password_lockout_time_mins=15,
    password_history=24,
    comment="Test password policy",
)

test_password_policy_minimal_template = PasswordPolicy(
    name="to_be_set",
)
