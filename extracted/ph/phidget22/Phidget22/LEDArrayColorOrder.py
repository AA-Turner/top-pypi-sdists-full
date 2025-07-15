import sys
import ctypes
class LEDArrayColorOrder:
	# Byte order RGB (WS2811)
	LED_COLOR_ORDER_RGB = 1
	# Byte order GRB (WS2812B, SK6812)
	LED_COLOR_ORDER_GRB = 2
	# Byte order RGBW
	LED_COLOR_ORDER_RGBW = 3
	# Byte order GRBW (SK6812RGBW)
	LED_COLOR_ORDER_GRBW = 4

	@classmethod
	def getName(self, val):
		if val == self.LED_COLOR_ORDER_RGB:
			return "LED_COLOR_ORDER_RGB"
		if val == self.LED_COLOR_ORDER_GRB:
			return "LED_COLOR_ORDER_GRB"
		if val == self.LED_COLOR_ORDER_RGBW:
			return "LED_COLOR_ORDER_RGBW"
		if val == self.LED_COLOR_ORDER_GRBW:
			return "LED_COLOR_ORDER_GRBW"
		return "<invalid enumeration value>"
