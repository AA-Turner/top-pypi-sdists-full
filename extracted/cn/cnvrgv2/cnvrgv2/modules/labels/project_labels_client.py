from cnvrgv2.modules.labels.dataowner_labels_client import DataownerLabelsClient
from cnvrgv2.modules.labels.utils import LabelKind
from cnvrgv2.context import SCOPE
from cnvrgv2.config import routes


class ProjectLabelsClient(DataownerLabelsClient):
    def __init__(self, project):
        super().__init__(project)
        self.kind = LabelKind.PROJECT
        scope = self._context.get_scope(SCOPE.PROJECT)
        self._route = routes.LABELS_DATAOWNER_BASE.format(scope["organization"], self.kind, project.slug)
