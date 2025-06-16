def palmerpenguins():
    import os

    import pandas

    return pandas.read_csv(os.path.join(os.path.dirname(__file__), "penguins.csv")).drop(columns=["rowid"])


def small_molecule_drugbank():
    import os

    import pandas

    return pandas.read_csv(os.path.join(os.path.dirname(__file__), "small_molecule_drugbank.csv")).drop(columns=["Unnamed: 0"])


def stocks_long():
    import os

    import pandas

    return pandas.read_parquet(os.path.join(os.path.dirname(__file__), "stocks_long.parquet"))
