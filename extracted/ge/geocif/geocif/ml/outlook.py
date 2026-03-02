import pickle
from pathlib import Path
from dataclasses import dataclass

import pandas as pd


@dataclass
class Outlook:
    path_outlook_file: Path

    def read_outlook_file(self):
        # path_outlook_file is a pickle, read it and return the dataframe
        with open(self.path_outlook_file, "rb") as pickle_file:
            content = pickle.load(pickle_file)

        return pd.DataFrame(content)

    def process(self, df):
        # Process the outlook file
        pass
