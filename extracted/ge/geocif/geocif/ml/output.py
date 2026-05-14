import pickle
import sqlite3

import pandas as pd

from geocif import utils


def make_serializable(hparams):
    # Baseline models (analog, median, last_year) return best_hyperparameters
    # as np.nan from _predict_baseline; non-dict values have no .copy() and
    # no callbacks/terms to sanitize — pass through as-is.
    if not isinstance(hparams, dict):
        return hparams

    serializable = hparams.copy()

    # Convert callbacks to strings
    if 'callbacks' in serializable:
        serializable['callbacks'] = [str(cb) for cb in serializable['callbacks']]

    # Convert terms to string
    if 'terms' in serializable:
        serializable['terms'] = str(serializable['terms'])

    return serializable


def config_to_dict(parser):
    """
    Reads a configuration file and returns the configuration as a nested dictionary.

    :param config_file_path: Path to the configuration file.
    :return: Dictionary with section names as keys and dictionaries of options and values as values.
    """
    # Initialize an empty dictionary to store the configuration
    config_dict = {}

    # Iterate over all sections and options, storing them in the dictionary
    for section in parser.sections():
        # Initialize the section dictionary
        section_dict = {}

        # Iterate over options in the current section
        for option in parser.options(section):
            # Get the value for the current option
            value = parser.get(section, option)
            # Store the option and its value in the section dictionary
            section_dict[option] = value

        # Store the current section in the main configuration dictionary
        config_dict[section] = section_dict

    return config_dict


def pprint_config(dict_config):
    """
    Pretty print the configuration file
    """
    import pprint

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(dict_config)


def config_to_db(db_path, parser, today):
    """
    Store the configuration file in the database
    Args:
        db_path:
        parser:
        today:

    Returns:

    """
    con = sqlite3.connect(db_path)

    # Prepare a list to store section, option, and value
    data = []

    # Iterate through each section and each option within the section
    for section in parser.sections():
        for option in parser.options(section):
            # Append a tuple of section, option, and value to the list
            data.append((section, option, parser.get(section, option, raw=True)))

    # Convert the list of tuples into a DataFrame
    df_parser = pd.DataFrame(data, columns=["Section", "Option", "Value"])
    df_parser.loc[:, "Now"] = today

    # name the index level
    df_parser.index.set_names(["Index"], inplace=True)
    utils.to_db(db_path, f"config_{today}", df_parser)

    con.commit()
    con.close()


def store(db_path, experiment_id, df, model, model_name, *, save_model_blobs=False):
    """Persist results (and optionally a pickled model blob) to SQLite.

    Args:
        db_path: SQLite path.
        experiment_id: Per-task table name for the results frame.
        df: Results DataFrame.
        model: Trained model object (only used when ``save_model_blobs``).
        model_name: Display name of the model.
        save_model_blobs: If True, also write a row into the shared ``models``
            table containing ``pickle.dumps(model)``. Off by default because
            the ``models`` table is the worst SQLite write-lock hot spot
            (every task hammers the same table) and nothing in geocif reads
            it. Flip on via ``[ML] save_model_blobs = True`` in the config
            when the pickled blobs are actually needed downstream.
    """
    # Convert any categorical columns to the values else we get the error
    # Exception: 'Categorical' with dtype category does not support reduction 'all'
    for col in df.columns:
        if isinstance(df[col], pd.CategoricalDtype):
            df[col] = df[col].astype(str)

    # Change all categorical columns to type object
    for col in df.select_dtypes(include=["category"]).columns:
        df[col] = df[col].astype(str)

    # Convert all columns to string
    df['Best Hyperparameters'] = df['Best Hyperparameters'].apply(make_serializable)

    # Output results to database
    try:
        utils.to_db(db_path, experiment_id, df)
    except Exception as e:
        print(f"Error: {e}")

    if not save_model_blobs:
        return

    # Optional: pickle the model and store in the shared `models` table.
    try:
        # Output model pickle as a blob to database
        df_model = pd.DataFrame(
            {
                "Experiment_ID": [experiment_id],
                "Model": [model_name],
                "Model_Blob": [pickle.dumps(model)],
            }
        )
        df_model.index.set_names(["Index"], inplace=True)
        utils.to_db(db_path, "models", df_model)
    except Exception as e:
        print(f"Error: {e}")
