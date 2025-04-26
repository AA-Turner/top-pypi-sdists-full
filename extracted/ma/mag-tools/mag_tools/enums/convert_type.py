from mag_tools.enums.base_enum import BaseEnum


class ConvertType(BaseEnum):
    ROTATE_90 = ('R1', '旋转90度')
    ROTATE_180 = ('R2', '旋转180度')
    ROTATE_270 = ('R3', '旋转270度')
    TRANSPOSE = ('T', '转置')
