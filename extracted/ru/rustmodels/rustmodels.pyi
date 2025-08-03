def fit_linear_regression(formula: str, df: int) -> str:
    """
    Function that performs a linear regression fit.

    Args:
        formula (str): Formula for the regression taking place. This will use the R formula syntax, and will use a 'formula' object.
        df (int): A DataFrame containing the data to fit the model. It will be used in conjunction with the formula.

    Returns:
        str: A 'linreg' object containing the regression results.
    """
