"""
================================================================================
Generate Time-Invariant Trajectories with GMR Learned from Multiple Trajectories
================================================================================

TODO
"""
from svgpathtools import svg2paths  # pip install svgpathtools
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chi2
from sklearn.mixture import BayesianGaussianMixture
from gmr import GMM, MVN


paths = svg2paths("examples/viapoints.svg")[0]  # only works if started from gmr's root directory
assert len(paths) == 20
X_train_all = []
for path in paths:
    points = []
    for cb in path:
        for t in np.arange(0, 1, 0.2):
            p = cb.point(t)
            p = [p.real, p.imag]
            points.append(p)
    points = np.array(points)

    dt = 0.01

    X = points[::10]
    X_dot = np.gradient(X, axis=0) / dt

    X_normalized = np.copy(X)

    X_train = np.hstack((X, X_dot))
    X_train_all.append(X_train)


mean_start = np.mean([X[0, :2] for X in X_train_all], axis=0)
mean_goal = np.mean([X[-1, :2] for X in X_train_all], axis=0)


X_train_all_normalized = []
for X_train in X_train_all:
    X = X_train[:, :2]
    X_dot = X_train[:, 2:]

    normalized_time = np.linspace(0, 1, len(X))
    start = X[0]
    goal = X[-1]
    X_normalized = X - (goal[np.newaxis] * normalized_time[:, np.newaxis]
                        - start[np.newaxis] * normalized_time[:, np.newaxis])
    X_normalized = X_normalized + (mean_goal[np.newaxis] * normalized_time[:, np.newaxis]
                                   - mean_start[np.newaxis] * normalized_time[:, np.newaxis])
    X_dot_normalized = np.gradient(X_normalized, axis=0) / dt

    X_train_normalized = np.hstack((X_normalized, X_dot_normalized))
    X_train_all_normalized.append(X_train_normalized)


random_state = np.random.RandomState(0)
n_components = 15

bgmm = BayesianGaussianMixture(
    n_components=n_components, max_iter=500,
    random_state=random_state).fit(np.vstack(X_train_all_normalized))
gmm = GMM(n_components=n_components, priors=bgmm.weights_, means=bgmm.means_,
          covariances=bgmm.covariances_, random_state=random_state)


def safe_sample(self, alpha):
    self._check_initialized()

    # Safe prior sampling
    priors = self.priors.copy()
    priors[priors < 1.0 / self.n_components] = 0.0
    priors /= priors.sum()
    assert abs(priors.sum() - 1.0) < 1e-4, priors.sum()
    mvn_index = self.random_state.choice(self.n_components, size=1, p=priors)[0]

    # Allow only samples from alpha-confidence region
    mvn = MVN(mean=self.means[mvn_index], covariance=self.covariances[mvn_index],
              random_state=self.random_state)
    sample = mvn.sample(1)[0]
    while (mahalanobis_distance(sample, mvn) >
           chi2(len(sample) - 1).ppf(alpha)):
        sample = mvn.sample(1)[0]
    return sample


def mahalanobis_distance(x, mvn):
    d = x - mvn.mean
    return d.dot(np.linalg.inv(mvn.covariance)).dot(d)


plt.figure(figsize=(10, 5))
ax = plt.subplot(121)
ax.scatter(mean_start[0], mean_start[1], c="r", label="Mean start")
ax.scatter(mean_goal[0], mean_goal[1], c="g", label="Mean goal")
for i, X_train in enumerate(X_train_all):
    label = "Training data" if i == 0 else None
    ax.plot(X_train[:, 0], X_train[:, 1], color="y", alpha=0.2, label=label)
for i, X_train in enumerate(X_train_all_normalized):
    label = "Normalized" if i == 0 else None
    ax.plot(X_train[:, 0], X_train[:, 1], color="k", alpha=0.2, label=label)

sampled_paths = []
for sample_idx in range(10):
    x = mean_start.copy()
    sampled_path = [x]
    sampling_dt = 0.01
    for t in range(500):
        cgmm = gmm.condition([0, 1], x)
        # default alpha defines the confidence region (e.g., 0.7 -> 70 %)
        x_dot = safe_sample(cgmm, alpha=0.9)

        # TODO correct stopping criterion: marginalize over velocities
        # https://github.com/AlexanderFabisch/gmr/issues/18
        p_joint_xxd = gmm.to_probability_density(np.hstack((x, x_dot))[np.newaxis])[0]
        p_cond_xdx = cgmm.to_probability_density(x_dot[np.newaxis])
        p_x = p_joint_xxd / p_cond_xdx
        if p_x < 1e-5 or np.linalg.norm(mean_goal - x) < 4.0:
            break
        x = x + sampling_dt * x_dot
        sampled_path.append(x)
    sampled_path = np.array(sampled_path)
    sampled_paths.append(sampled_path)

    label = "Sampled" if sample_idx == 0 else None
    ax.plot(sampled_path[:, 0], sampled_path[:, 1], color="r", label=label)
xlim = ax.get_xlim()
ylim = ax.get_ylim()
ax.legend(loc="best")


def rescale(X, new_start, new_goal):
    normalized_time = np.linspace(0, 1, len(X))
    start = X[0]
    goal = X[-1]
    X_normalized = X - (goal[np.newaxis] * normalized_time[:, np.newaxis]
                        - start[np.newaxis] * normalized_time[:, np.newaxis])
    X_rescaled = X_normalized + (new_goal[np.newaxis] * normalized_time[:, np.newaxis]
                                 - new_start[np.newaxis] * normalized_time[:, np.newaxis])
    return X_rescaled


ax = plt.subplot(122)
ax.set_xlim(xlim)
ax.set_ylim(ylim)
new_goal1 = mean_goal - np.array([50.0, 30.0])
new_goal2 = mean_goal - np.array([20.0, 0.0])
new_goal3 = mean_goal + np.array([10.0, 30.0])
ax.scatter(new_goal1[0], new_goal1[1], c="r")
ax.scatter(new_goal2[0], new_goal2[1], c="g")
ax.scatter(new_goal3[0], new_goal3[1], c="b")
for X in sampled_paths:
    X_rescaled = rescale(X, mean_start, new_goal1)
    ax.plot(X_rescaled[:, 0], X_rescaled[:, 1], color="r", alpha=0.5)
    X_rescaled = rescale(X, mean_start, new_goal2)
    ax.plot(X_rescaled[:, 0], X_rescaled[:, 1], color="g", alpha=0.5)
    X_rescaled = rescale(X, mean_start, new_goal3)
    ax.plot(X_rescaled[:, 0], X_rescaled[:, 1], color="b", alpha=0.5)

plt.show()