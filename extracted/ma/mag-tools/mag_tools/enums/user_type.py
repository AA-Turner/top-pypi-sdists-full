from mag_tools.enums.base_enum import BaseEnum


class UserType(BaseEnum):
    ROOT = ("Root", "超级管理员")
    CLOUD = ("Cloud", "云平台用户")
    TENANT = ("Tenant", "租户用户")
    ORG = ("Org", "机构用户")
    PERSON = ("Person", "个人用户")
    APPLICATION = ("Application", "应用系统用户")
