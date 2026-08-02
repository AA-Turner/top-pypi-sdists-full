class UartUtil:

	UART_START_CHAR =       0x7E
	UART_ESCAPE_CHAR =      0x5C
	UART_ESCAPE_FLIP_MASK = 0x40

	@staticmethod
	def uartEscape(val):
		if isinstance(val, list):
			# Escape special chars:
			escapedMsg = []
			for c in val:
				if c == UartUtil.UART_ESCAPE_CHAR or c == UartUtil.UART_START_CHAR:
					escapedMsg.append(UartUtil.UART_ESCAPE_CHAR)
					c = UartUtil.uartEscape(c)
				escapedMsg.append(c)
			return escapedMsg
		else:
			return val ^ UartUtil.UART_ESCAPE_FLIP_MASK

	@staticmethod
	def uartUnescape(val):
		return val ^ UartUtil.UART_ESCAPE_FLIP_MASK
