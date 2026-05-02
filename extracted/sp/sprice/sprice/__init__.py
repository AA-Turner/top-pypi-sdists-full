import pandas as pd
import os

# Function to load a specific dataset
def load_data(filename):
    base_dir = os.path.dirname(__file__)  # Get the directory where the module is located
    data_path = os.path.join(base_dir, 'data', filename)  # Construct full path to the data file
    data = pd.read_hdf(data_path)  # Load the data file using Pandas read_hdf
    return data

# Load both datasets upon import
sprice_data_1 = load_data('sprice_data_1.h5')
sprice_data_2 = load_data('sprice_data_2.h5')