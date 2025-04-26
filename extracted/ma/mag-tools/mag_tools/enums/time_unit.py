from mag_tools.enums.base_enum import BaseEnum

class TimeUnit(BaseEnum):
    NANOSECOND = ('NANOSECOND', '纳秒')
    MICROSECOND = ('MICROSECOND', '微秒')
    MILLISECOND = ('MILLISECOND', '毫秒')
    SECOND = ('SECOND', '秒')
    MINUTE = ('MINUTE', '分')
    HOUR = ('HOUR', '时')
    DAY = ('DAY', '天')
    WEEK = ('WEEK', '周')
    MONTH = ('MONTH', '月')
    YEAR = ('YEAR', '年')
