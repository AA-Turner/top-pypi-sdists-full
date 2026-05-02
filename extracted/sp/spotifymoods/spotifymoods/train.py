import os.path
import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier

from spotifymoods.constants import AUDIO_FEATURES


def train(data, trained_output, scaled_output):
    nn = None
    scaler = None

    x = data[AUDIO_FEATURES]
    y = data['mood']

    if os.path.isfile(trained_output) and os.path.isfile(scaled_output):
        with open(trained_output, 'rb') as f:
            nn = pickle.load(f)

        with open(scaled_output, 'rb') as f:
            scaler = pickle.load(f)

        scaled = scaler.partial_fit(x).transform(x)
        nn.partial_fit(scaled, y)
    else:
        scaler = StandardScaler()
        nn = MLPClassifier(hidden_layer_sizes=8, max_iter=15000, alpha=1.0)

        scaled = scaler.fit_transform(x)
        nn.fit(scaled, y)

    with open(trained_output, 'wb') as f:
        pickle.dump(nn, f)

    with open(scaled_output, 'wb') as f:
        pickle.dump(scaler, f)
