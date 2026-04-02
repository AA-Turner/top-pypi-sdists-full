from pandas.core.dtypes.common import is_numeric_dtype


class PandasPercentile:
    def __init__(self, quantiles, probabilities=None):
        self.quantiles = quantiles
        self.probabilities = probabilities

        # If probabilities are not provided, assume they're the indices of quantiles
        if self.probabilities is None:
            self.probabilities = [q for q in self.quantiles.index]

    def get_percentile(self, value):
        for i, quantile in enumerate(self.quantiles):
            if value <= quantile:
                # Convert probability to percentile (e.g., 0.8 -> 80)
                return int(self.probabilities[i] * 100)
        return 100

    def __call__(self, *args, **kwargs):
        return self.get_percentile(*args, **kwargs)


def get_zero_value(col):
    if is_numeric_dtype(col):
        return 0
    else:
        return ""
