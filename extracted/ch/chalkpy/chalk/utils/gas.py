class GasLimit:
    """
    A way to limit recursive functions.
    """

    def __init__(self, remaining_gas: int, out_of_gas_error: Exception):
        self.remaining_gas = remaining_gas
        self.out_of_gas_error = out_of_gas_error
        super().__init__()

    def consume_gas(self, amount: int = 1) -> None:
        self.remaining_gas -= amount
        if self.remaining_gas <= 0:
            raise self.out_of_gas_error


class OutOfGasError(Exception):
    """A generic sentinel exception for running out of gas."""

    pass
