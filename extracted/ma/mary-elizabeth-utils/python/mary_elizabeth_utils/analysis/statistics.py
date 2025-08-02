from pathlib import Path

import matplotlib.pyplot as plt
import polars as pl
import seaborn as sns


def generate_summary_statistics(
    df: pl.LazyFrame,
    group_col: str,
    numeric_cols: list[str],
    categorical_cols: list[str],
) -> pl.DataFrame:
    """
    Generate summary statistics for the given DataFrame.

    Args:
        df (pl.LazyFrame): The input DataFrame.
        group_col (str): The column to group by.
        numeric_cols (List[str]): List of numeric column names.
        categorical_cols (List[str]): List of categorical column names.

    Returns:
        pl.DataFrame: A DataFrame containing summary statistics.
    """
    numeric_summary = df.group_by(group_col).agg(
        [
            *[pl.col(col).mean().alias(f"{col}_mean") for col in numeric_cols],
            *[pl.col(col).median().alias(f"{col}_median") for col in numeric_cols],
            *[pl.col(col).std().alias(f"{col}_std") for col in numeric_cols],
            *[pl.col(col).min().alias(f"{col}_min") for col in numeric_cols],
            *[pl.col(col).max().alias(f"{col}_max") for col in numeric_cols],
        ]
    )

    categorical_summary = df.group_by(group_col).agg(
        [pl.col(col).value_counts().alias(f"{col}_counts") for col in categorical_cols]
    )

    return numeric_summary.join(categorical_summary, on=group_col).collect()


def plot_numeric_comparisons(
    df: pl.DataFrame, group_col: str, numeric_cols: list[str], output_dir: Path
) -> None:
    """
    Create box plots for numeric comparisons.

    Args:
        df (pl.DataFrame): The input DataFrame.
        group_col (str): The column to group by.
        numeric_cols (List[str]): List of numeric column names to plot.
        output_dir (Path): Directory to save the output plot.
    """
    n_cols = 3
    n_rows = (len(numeric_cols) - 1) // n_cols + 1
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5 * n_rows))
    axes = axes.flatten()

    for i, col in enumerate(numeric_cols):
        sns.boxplot(x=group_col, y=col, data=df.to_pandas(), ax=axes[i])
        axes[i].set_title(f"Distribution of {col}")
        axes[i].set_xlabel("")

    for i in range(len(numeric_cols), len(axes)):
        axes[i].remove()

    plt.tight_layout()
    plt.savefig(output_dir / "numeric_comparisons.png")
    plt.close()


def plot_categorical_comparisons(
    df: pl.DataFrame, group_col: str, categorical_cols: list[str], output_dir: Path
) -> None:
    """
    Create stacked bar plots for categorical comparisons.

    Args:
        df (pl.DataFrame): The input DataFrame.
        group_col (str): The column to group by.
        categorical_cols (List[str]): List of categorical column names to plot.
        output_dir (Path): Directory to save the output plot.
    """
    n_cols = 2
    n_rows = (len(categorical_cols) - 1) // n_cols + 1
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5 * n_rows))
    axes = axes.flatten()

    for i, col in enumerate(categorical_cols):
        contingency_table = df.pivot(
            values="count", index=col, on=group_col, aggregate_function="sum"
        ).to_pandas()
        contingency_table.plot(kind="bar", stacked=True, ax=axes[i])
        axes[i].set_title(f"Distribution of {col}")
        axes[i].set_xlabel("")
        axes[i].legend(title=group_col)

    for i in range(len(categorical_cols), len(axes)):
        axes[i].remove()

    plt.tight_layout()
    plt.savefig(output_dir / "categorical_comparisons.png")
    plt.close()
