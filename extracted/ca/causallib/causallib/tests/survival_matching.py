from sklearn.linear_model import LogisticRegression, LinearRegression
from causallib.datasets.data_loader import load_nhefs_survival, load_nhefs
from causallib.estimation import IPW, Standardization
from causallib.estimation import Matching
from causallib.survival import WeightedSurvival
from causallib.evaluation import evaluate
import matplotlib.pyplot as plt

# data = load_nhefs_survival()
#
# matching = Matching(
#     with_replacement=True,
#     n_neighbors=1,
#     matching_mode="control_to_treatment",
# )
# surv_model = WeightedSurvival(matching)
# surv_model.fit(data.X, data.a, data.t, data.y)
# po = surv_model.estimate_population_outcome(data.X, data.a, data.t, data.y)
# print(po[1]-po[0])
#
# result = evaluate(matching, data.X, data.a, data.y)
# result.plot_all()

print("hey")

data = load_nhefs()

# ipw = IPW(LogisticRegression()).fit(data.X, data.a, data.y)
# result = evaluate(ipw, data.X, data.a, data.y, cv="auto")
# result.plot_all()
#
# std = Standardization(LinearRegression()).fit(data.X, data.a, data.y)
# result = evaluate(std, data.X, data.a, data.y)
# result.plot_all()
#
# matching = Matching(
#     with_replacement=True,
#     n_neighbors=1,
#     matching_mode="control_to_treatment",
# ).fit(data.X, data.a, data.y)
# result = evaluate(matching, data.X, data.a, data.y)
# result.plot_all()
#
# print("hey")

fig, axes = plt.subplots(1, 3, figsize=(9, 4))
ipw = IPW(LogisticRegression(max_iter=2)).fit(data.X, data.a, data.y)
result = evaluate(ipw, data.X, data.a, data.y)
result.plot_covariate_balance(kind="love", ax=axes[0])
result.plot_covariate_balance(kind="slope", thresh=0.3, ax=axes[1], plot_semi_grid=True, label_imbalanced=False)
result.plot_covariate_balance(kind="scatter", thresh=0.1, label_imbalanced=False, ax=axes[2])
print("hey")
