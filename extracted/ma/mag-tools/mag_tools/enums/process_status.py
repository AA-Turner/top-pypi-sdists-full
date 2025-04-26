from mag_tools.enums.base_enum import BaseEnum


class ProcessStatus(BaseEnum):
    UNKNOWN = ("UNKNOWN", "未知")
    TO_BE_CONFIRM = ("TO_BE_CONFIRM", "待确认")
    PENDING = ("PENDING", "待处理")
    PROCESSING = ("PROCESSING", "处理中")
    SUCCESS = ("SUCCESS", "成功")
    FAIL = ("FAIL", "失败")