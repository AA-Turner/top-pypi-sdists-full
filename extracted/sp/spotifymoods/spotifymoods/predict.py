import pickle
import pandas as pd

from spotifymoods.constants import AUDIO_FEATURES


def predict(data, trained_path, scaled_path):
    x = data[AUDIO_FEATURES]

    with open(trained_path, 'rb') as f:
        nn = pickle.load(f)

    with open(scaled_path, 'rb') as f:
        scaler = pickle.load(f)

    transformed = scaler.transform(x)
    y = nn.predict(transformed)
    result = pd.DataFrame(data['id'])
    result[AUDIO_FEATURES] = x
    result['mood'] = y

    return result
