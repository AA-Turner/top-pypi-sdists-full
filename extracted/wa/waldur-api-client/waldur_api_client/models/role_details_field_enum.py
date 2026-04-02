from enum import Enum


class RoleDetailsFieldEnum(str, Enum):
    CONTENT_TYPE = "content_type"
    DESCRIPTION = "description"
    DESCRIPTION_AR = "description_ar"
    DESCRIPTION_CS = "description_cs"
    DESCRIPTION_DA = "description_da"
    DESCRIPTION_DE = "description_de"
    DESCRIPTION_EN = "description_en"
    DESCRIPTION_ES = "description_es"
    DESCRIPTION_ET = "description_et"
    DESCRIPTION_FR = "description_fr"
    DESCRIPTION_IT = "description_it"
    DESCRIPTION_LT = "description_lt"
    DESCRIPTION_LV = "description_lv"
    DESCRIPTION_NB = "description_nb"
    DESCRIPTION_RU = "description_ru"
    DESCRIPTION_SV = "description_sv"
    IS_ACTIVE = "is_active"
    IS_SYSTEM_ROLE = "is_system_role"
    NAME = "name"
    PERMISSIONS = "permissions"
    USERS_COUNT = "users_count"
    UUID = "uuid"

    def __str__(self) -> str:
        return str(self.value)
