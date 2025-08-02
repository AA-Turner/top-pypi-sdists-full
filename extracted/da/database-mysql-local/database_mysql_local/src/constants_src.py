from enum import Enum

from logger_local.LoggerComponentEnum import LoggerComponentEnum


# TODO Move everything related to sync to separate directory called
#  sync_data_source (preferable with it's own src and tests directories)
class UpdateStatus(Enum):
    UPDATE_DATA_SOURCE = -1
    DONT_UPDATE = 0
    UPDATE_CIRCLEZ = 1  # TODO Don't use CIRCLEZ


class IsTestData(Enum):
    PRODUCTION = 0
    TEST_DATA = 1
    TEMP_DATA = 2


# connector / cursor
DATABASE_MYSQL_PYTHON_PACKAGE_COMPONENT_ID = 112
DATABASE_MYSQL_PYTHON_PACKAGE_COMPONENT_NAME = 'database_mysql_local\\connector'
CONNECTOR_DEVELOPER_EMAIL = 'idan.a@circ.zone'
LOGGER_CONNECTOR_CODE_OBJECT = {
    'component_id': DATABASE_MYSQL_PYTHON_PACKAGE_COMPONENT_ID,
    'component_name': DATABASE_MYSQL_PYTHON_PACKAGE_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': CONNECTOR_DEVELOPER_EMAIL
}

# generic_crud
DATABASE_MYSQL_PYTHON_GENERIC_CRUD_COMPONENT_ID = 206
DATABASE_MYSQL_PYTHON_GENERIC_CRUD_COMPONENT_NAME = 'database_mysql_local\\generic_crud'
GENERIC_CRUD_DEVELOPER_EMAIL = 'akiva.s@circ.zone'
CRUD_MYSQL_CODE_LOGGER_OBJECT = {
    'component_id': DATABASE_MYSQL_PYTHON_GENERIC_CRUD_COMPONENT_ID,
    'component_name': DATABASE_MYSQL_PYTHON_GENERIC_CRUD_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': GENERIC_CRUD_DEVELOPER_EMAIL
}

# generic_crud_ml
DATABASE_MYSQL_GENERIC_CRUD_ML_COMPONENT_ID = 7001
DATABASE_MYSQL_GENERIC_CRUD_ML_COMPONENT_NAME = 'database_mysql_local\\generic_crud_ml'
GENERIC_CRUD_ML_DEVELOPER_EMAIL = 'tal.g@circ.zone'
CRUD_ML_CODE_LOGGER_OBJECT = {
    'component_id': DATABASE_MYSQL_GENERIC_CRUD_ML_COMPONENT_ID,
    'component_name': DATABASE_MYSQL_GENERIC_CRUD_ML_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': GENERIC_CRUD_ML_DEVELOPER_EMAIL
}

# generic_mapping
DATABASE_MYSQL_PYTHON_GENERIC_MAPPING_COMPONENT_ID = 7002
DATABASE_MYSQL_PYTHON_GENERIC_MAPPING_COMPONENT_NAME = 'database_mysql_local\\generic_mapping'
GENERIC_MAPPING_DEVELOPER_EMAIL = 'sahar.g@circ.zone'
MAPPING_CODE_LOGGER_OBJECT = {
    'component_id': DATABASE_MYSQL_PYTHON_GENERIC_MAPPING_COMPONENT_ID,
    'component_name': DATABASE_MYSQL_PYTHON_GENERIC_MAPPING_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': GENERIC_MAPPING_DEVELOPER_EMAIL
}
