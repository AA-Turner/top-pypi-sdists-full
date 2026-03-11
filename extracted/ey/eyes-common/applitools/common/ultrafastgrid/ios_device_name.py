# GENERATED FILE #
from enum import Enum

from applitools.common.utils.general_utils import DeprecatedEnumVariant

__all__ = ("IosDeviceName",)


class IosDeviceName(Enum):
    iPad_7 = "iPad (7th generation)"
    iPad_9 = "iPad (9th generation)"
    iPad_10 = "iPad (10th generation)"
    iPad_mini_6 = "iPad mini (6th generation)"
    iPad_Air_4 = "iPad Air (4th generation)"
    iPad_Air_11_inch_M3 = "iPad Air 11-inch (M3)"
    iPad_Air_13_inch_M3 = "iPad Air 13-inch (M3)"
    iPad_A16 = "iPad (A16)"
    iPad_Pro_11_inch_4 = "iPad Pro (11-inch) (4th generation)"
    iPad_Pro_11_inch_M5 = "iPad Pro 11-inch (M5)"
    iPad_Pro_13_inch_M5 = "iPad Pro 13-inch (M5)"
    iPad_Pro_12_9_inch_3 = "iPad Pro (12.9-inch) (3rd generation)"
    iPhone_SE_2 = "iPhone SE (2nd generation)"
    iPhone_SE_3 = "iPhone SE (3rd generation)"
    iPhone_XR = "iPhone XR"
    iPhone_Xs = "iPhone Xs"
    iPhone_11 = "iPhone 11"
    iPhone_11_Pro_Max = "iPhone 11 Pro Max"
    iPhone_11_Pro = "iPhone 11 Pro"
    iPhone_12 = "iPhone 12"
    iPhone_12_mini = "iPhone 12 mini"
    iPhone_12_Pro_Max = "iPhone 12 Pro Max"
    iPhone_12_Pro = "iPhone 12 Pro"
    iPhone_13 = "iPhone 13"
    iPhone_13_mini = "iPhone 13 mini"
    iPhone_13_Pro_Max = "iPhone 13 Pro Max"
    iPhone_13_Pro = "iPhone 13 Pro"
    iPhone_14 = "iPhone 14"
    iPhone_14_Pro_Max = "iPhone 14 Pro Max"
    iPhone_14_Pro = "iPhone 14 Pro"
    iPhone_14_Plus = "iPhone 14 Plus"
    iPhone_15 = "iPhone 15"
    iPhone_15_Pro_Max = "iPhone 15 Pro Max"
    iPhone_15_Pro = "iPhone 15 Pro"
    iPhone_15_Plus = "iPhone 15 Plus"
    iPhone_16 = "iPhone 16"
    iPhone_16_Pro_Max = "iPhone 16 Pro Max"
    iPhone_16_Pro = "iPhone 16 Pro"
    iPhone_16_Plus = "iPhone 16 Plus"
    iPhone_17 = "iPhone 17"
    iPhone_17_Pro = "iPhone 17 Pro"
    iPhone_17_Pro_Max = "iPhone 17 Pro Max"
    iPhone_Air = "iPhone Air"

    @DeprecatedEnumVariant
    def iPad_Pro_3(self):
        """`iPad_Pro_3` is deprecated. Use `iPad_Pro_12_9_inch_3` instead"""
        return self.iPad_Pro_12_9_inch_3

    @DeprecatedEnumVariant
    def iPad_Pro_4(self):
        """`iPad_Pro_4` is deprecated. Use `iPad_Pro_11_inch_4` instead"""
        return self.iPad_Pro_11_inch_4

    @DeprecatedEnumVariant
    def iPhone_XS(self):
        """`iPhone_XS` is deprecated. Use `iPhone_Xs` instead"""
        return self.iPhone_Xs
