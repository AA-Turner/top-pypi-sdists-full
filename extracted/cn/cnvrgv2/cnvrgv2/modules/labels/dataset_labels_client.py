from cnvrgv2.modules.labels.dataowner_labels_client import DataownerLabelsClient
from cnvrgv2.modules.labels.utils import LabelKind
from cnvrgv2.context import SCOPE
from cnvrgv2.config import routes


class DatasetLabelsClient(DataownerLabelsClient):
    def __init__(self, dataset):
        super().__init__(dataset)
        self.kind = LabelKind.DATASET
        scope = self._context.get_scope(SCOPE.DATASET)
        self._route = routes.LABELS_DATAOWNER_BASE.format(scope["organization"], self.kind, dataset.slug)
