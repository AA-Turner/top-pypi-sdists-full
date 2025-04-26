from sklearn.datasets import load_breast_cancer
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from gmr import GMM, plot_error_ellipses


X, y = load_breast_cancer(return_X_y=True)
X_pca = PCA(n_components=2, whiten=True, random_state=0).fit_transform(X)

gmm = GMM(n_components=2, random_state=1)
gmm.from_samples(X_pca)

plt.figure()
ax = plt.subplot(111)
ax.scatter(X_pca[:, 0], X_pca[:, 1], c=y)
plot_error_ellipses(ax, gmm, alpha=0.1, colors=["r", "g", "b"])
plt.show()