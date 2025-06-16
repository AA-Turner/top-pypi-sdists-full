from enum import Enum


class WebsocketChannelEnum(str, Enum):
    OVER_ALL = "over_all"  # 儀表板
    RECEPTION_CENTER = "reception_center"  # 接待中心
    CAR_MOVEMENT = "car_movement"  # 車輛動態
    USER_BELL_NOTIFICATION = "user_bell_notification"  # 個人小鈴噹
