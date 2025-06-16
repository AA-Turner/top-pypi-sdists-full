from abc import ABC, abstractmethod
from typing import Dict, List, Tuple

try:
    from ragformance.models.corpus import DocModel
    from ragformance.models.answer import AnnotatedQueryModel
except ImportError:
    DocModel = type("DocModel", (), {})
    AnnotatedQueryModel = type("AnnotatedQueryModel", (), {})
    print(
        "Warning: DocModel or AnnotatedQueryModel not found. Using placeholder types."
    )


class RAGformanceGeneratorInterface(ABC):
    """
    Interface for RAGformance data generators.

    Each generator should implement the `run` method, which takes a configuration
    dictionary and returns a tuple containing a list of document models and a
    list of annotated query models.
    """

    @abstractmethod
    def run(self, config: Dict) -> Tuple[List[DocModel], List[AnnotatedQueryModel]]:
        """
        Runs the data generation process.

        Args:
            config: A dictionary containing all necessary configuration parameters
                    for the generator. This can include paths, API keys, model names,
                    generation options, etc.

        Returns:
            A tuple containing two lists:
            1. List[DocModel]: The generated corpus (list of document models).
            2. List[AnnotatedQueryModel]: The generated queries/questions (list of
                                          annotated query models), potentially with
                                          reference answers.
        """
        raise NotImplementedError
