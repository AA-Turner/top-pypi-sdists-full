from abc import ABC, abstractmethod
from typing import Dict, List

from ragformance.models.answer import AnnotatedQueryModel, AnswerModel
from ragformance.models.corpus import DocModel


class RagInterface(ABC):
    @abstractmethod
    def upload_corpus(self, corpus: List[DocModel], config: Dict = {}) -> int:
        raise NotImplementedError

    @abstractmethod
    def ask_queries(
        self, queries: List[AnnotatedQueryModel], config: Dict = {}
    ) -> List[AnswerModel]:
        raise NotImplementedError
