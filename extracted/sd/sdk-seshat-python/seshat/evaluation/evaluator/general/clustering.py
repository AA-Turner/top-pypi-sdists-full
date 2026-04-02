from sklearn.metrics import silhouette_score, calinski_harabasz_score

from seshat.evaluation.evaluator import Evaluator


class ClusteringEvaluator(Evaluator):
    def __init__(self, silhouette_metric="cosine", group_keys=None):
        super().__init__(group_keys)
        self.silhouette_metric = silhouette_metric

    def __call__(self, **kwargs):
        return self.evaluate(**kwargs)

    def evaluate(self, vector: object, labels: object):
        return {
            "silhouette score": silhouette_score(
                vector, labels, metric=self.silhouette_metric
            ),
            "calinski harabasz": calinski_harabasz_score(vector, labels),
        }
