from enum import Enum


class IssueOEnum(str, Enum):
    ASSIGNEE_NAME = "assignee_name"
    CALLER_FIRST_NAME = "caller_first_name"
    CALLER_LAST_NAME = "caller_last_name"
    CREATED = "created"
    CUSTOMER_NAME = "customer_name"
    KEY = "key"
    MODIFIED = "modified"
    PRIORITY = "priority"
    PROJECT_NAME = "project_name"
    REMOTE_ID = "remote_id"
    REPORTER_NAME = "reporter_name"
    STATUS = "status"
    SUMMARY = "summary"
    TYPE = "type"
    VALUE_0 = "-assignee_name"
    VALUE_1 = "-caller_first_name"
    VALUE_10 = "-reporter_name"
    VALUE_11 = "-status"
    VALUE_12 = "-summary"
    VALUE_13 = "-type"
    VALUE_2 = "-caller_last_name"
    VALUE_3 = "-created"
    VALUE_4 = "-customer_name"
    VALUE_5 = "-key"
    VALUE_6 = "-modified"
    VALUE_7 = "-priority"
    VALUE_8 = "-project_name"
    VALUE_9 = "-remote_id"

    def __str__(self) -> str:
        return str(self.value)
