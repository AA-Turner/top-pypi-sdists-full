import numpy as np
import pandas as pd
from sklearn.mixture import BayesianGaussianMixture
from gmr import GMM


df = pd.read_csv("examples/survey_data.csv")
X = df[["ID", "Brand"] + ["X%d" % i for i in range(1, 11)] + ["y"]].to_numpy()

bgmm = BayesianGaussianMixture(
    weight_concentration_prior_type="dirichlet_process", n_components=3,
    random_state=0)
bgmm.fit(X)
gmm = GMM(n_components=3, priors=bgmm.weights_, means=bgmm.means_,
          covariances=bgmm.covariances_, random_state=0)
Y = gmm.predict(np.arange(12), X[:, :12])
print(np.hstack((Y, X[:, -1, np.newaxis])))