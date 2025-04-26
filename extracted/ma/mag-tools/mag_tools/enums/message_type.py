from mag_tools.enums.base_enum import BaseEnum


class MessageType(BaseEnum):
    """
    消息类型枚举
    枚举值为消息类型的名称，如：MessageType.INFO
    """
    INFO = ('info', '信息')  # 信息
    WARNING = ('warning', '警告')  # 警告
    ERROR = ('error', '错误')  # 错误
    DEBUG = ('debug', '调试')  # 调试


if __name__ == '__main__':
    # 示例用法
    print(MessageType.INFO.code)  # 输出: ('info', '信息')
    print(MessageType.WARNING.code)  # 输出: ('warning', '警告')
    print(MessageType.ERROR.code)  # 输出: ('error', '错误')
    print(MessageType.DEBUG.code)  # 输出: ('debug', '调试')
