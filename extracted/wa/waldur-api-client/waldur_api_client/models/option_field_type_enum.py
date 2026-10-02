from enum import Enum


class OptionFieldTypeEnum(str, Enum):
    BOOLEAN = "boolean"
    COMPONENT_MULTIPLIER = "component_multiplier"
    CONDITIONAL_CASCADE = "conditional_cascade"
    DATE = "date"
    HTML_TEXT = "html_text"
    INTEGER = "integer"
    MONEY = "money"
    MULTI_DATACENTER_K8S_CONFIG = "multi_datacenter_k8s_config"
    SELECT_MULTIPLE_OPENSTACK_INSTANCES = "select_multiple_openstack_instances"
    SELECT_MULTIPLE_OPENSTACK_TENANTS = "select_multiple_openstack_tenants"
    SELECT_OPENSTACK_INSTANCE = "select_openstack_instance"
    SELECT_OPENSTACK_TENANT = "select_openstack_tenant"
    SELECT_STRING = "select_string"
    SELECT_STRING_MULTI = "select_string_multi"
    SINGLE_DATACENTER_K8S_CONFIG = "single_datacenter_k8s_config"
    STORAGE_FOLDER_MANAGER = "storage_folder_manager"
    STRING = "string"
    TEXT = "text"
    TIME = "time"

    def __str__(self) -> str:
        return str(self.value)
