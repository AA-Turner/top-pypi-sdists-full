from mag_tools.enums.base_enum import BaseEnum


class Symbol(BaseEnum):
    """
    标点符号的枚举

    作者: xlcao
    版本: 1.3
    版权所有: Copyright (c) 2017 by Xiaolong Cao. All rights reserved.
    日期: 2017/7/13
    """
    SEMI_COLON = (";", "分号")
    COMMA = (",", "逗号")
    COLON = (":", "冒号")
    DOT = (".", "句点")
    BLANK = (" ", "空格")
    SINGLE_QUOTATION = ("'", "单引号")
    DOUBLE_QUOTATION = ("\"", "双引号")
    FORWARD_SLASH = ("/", "正斜杠")
    BACK_SLASH = ("\\", "反斜杠")
    UNDER_LINE = ("_", "下划线")
    DOUBLE_UNDER = ("__", "双下划线")
    HYPHEN = ("-", "连字符")
    EQUAL = ("=", "等号")
    QUESTION_MARK = ("?", "问号")
    EXCLAMATION_MARK = ("!", "感叹号")
    AMPERSAND = ("&", "与号")
    ASTERISK = ("*", "星号")
    OPEN_PAREN = ("(", "左圆括号")
    CLOSE_PAREN = (")", "右圆括号")
    OPEN_BRACE = ("{", "左花括号")
    CLOSE_BRACE = ("}", "右花括号")
    OPEN_BRACKET = ("[", "左方括号")
    CLOSE_BRACKET = ("]", "右方括号")
    ACCENT = ("`", "抑音符/反引号")
    TILDE = ("~", "波浪号/颚化号")
    POUND = ("#", "井号")
    DOLLAR = ("$", "美元符")
    AT = ("@", "AT符")
    VERTICAL_BAR = ("|", "分隔符")
    PLUS = ("+", "加号")
    CARET = ("^", "指数运算符")
    PERCENT = ("%", "百分号")
    CHINES_DOT = ("。", "中文句号")
    CHINES_COMMA = ("，", "中文逗号")
    CHINES_COLON = ("：", "中文冒号")
    CHINESE_SINGLE_QUOTATION = ("‘", "中文单引号")
    CHINESE_DOUBLE_QUOTATION = ("“", "中文双引号")
    CHINESE_OPEN_PAREN = ("（", "中文左圆括号")
    CHINESE_CLOSE_PAREN = ("）", "中文右圆括号")
    CHINESE_OPEN_BRACKET = ("【", "中文左方括号")
    CHINESE_CLOSE_BRACKET = ("】", "中文右方括号")
    CHINESE_CAESURA = ("、", "中文顿号")
    CHINESE_QUESTION_MARK = ("？", "中文问号")
    CHINESE_EXCLAMATION_MARK = ("！", "中文感叹号")
    CHINESE_SEMI_COLON = ("；", "中文分号")
    CHINESE_DOLLAR = ("￥", "人民币符")
    PLACE_HOLDER = ("%s", "SQL占位符")

    NONE = ("", "空字符")

    @staticmethod
    def is_symbol(c: str) -> bool:
        return Symbol.of_code(c) is not None
