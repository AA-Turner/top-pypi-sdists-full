from enum import Enum

class DataSourceSchedule(str, Enum):
    Once = "Once",
    Onemin = "1min",
    Fivemin = "5min",
    OneFivemin = "15min",
    ThreeZeromin = "30min",
    Onehr = "1hr",
    Fourhr = "4hr",
    OneTwohr = "12hr",
    Oneday = "1day",
    Threeday = "3day",
    Sevenday = "7day",
    Monitor = "Monitor",

