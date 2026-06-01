import logging
from uuid import UUID

from beartype import beartype

from picsellia import exceptions
from picsellia.colors import Colors
from picsellia.decorators import exception_handler
from picsellia.sdk.connection import Connection
from picsellia.sdk.dao import Dao
from picsellia.sdk.multi_object import MultiObject
from picsellia.types.schemas import EvaluationSchema

logger = logging.getLogger("picsellia")


class Evaluation(Dao):
    def __init__(self, connexion: Connection, context_id: UUID, data: dict) -> None:
        Dao.__init__(self, connexion, data)
        self._context_id = context_id

    @property
    def asset_id(self) -> UUID:
        """UUID of the (Asset) of this (Evaluation)"""
        return self._asset_id

    @property
    def context_id(self) -> UUID:
        """UUID of the context (it can be an experiment or a model version) of this (Evaluation)"""
        return self._context_id

    def __str__(self):
        return f"{Colors.BLUE}Evaluation of {self.asset_id} from context {self.context_id} {Colors.ENDC} (id: {self.id})"

    @exception_handler
    @beartype
    def sync(self) -> dict:
        r = self.connection.get(f"/api/evaluation/{self.id}").json()
        self.refresh(r)
        return r

    @exception_handler
    @beartype
    def refresh(self, data: dict) -> EvaluationSchema:
        schema = EvaluationSchema(**data)
        self._asset_id = schema.asset_id
        return schema

    @exception_handler
    @beartype
    def delete(self) -> None:
        """Delete this evaluation from the platform.
        All evaluated shapes will be deleted!
        This is a very dangerous move.

        :warning: **DANGER ZONE**: Be very careful here!

        Examples:
            ```python
            one_evaluation.delete()
            ```
        """
        self.connection.delete(f"/api/evaluation/{self.id}")
        logger.info(f"{self} deleted from platform.")


class MultiEvaluation(MultiObject[Evaluation]):
    @beartype
    def __init__(
        self, connexion: Connection, context_id: UUID, items: list[Evaluation]
    ):
        MultiObject.__init__(self, connexion, items)
        self._context_id = context_id

    @property
    def context_id(self) -> UUID:
        return self._context_id

    def __str__(self) -> str:
        return f"{Colors.GREEN}MultiEvaluation for context {self.context_id}{Colors.ENDC}  size: {len(self)}"

    def __getitem__(self, key) -> "Evaluation | MultiEvaluation":
        if isinstance(key, slice):
            indices = range(*key.indices(len(self.items)))
            evaluations = [self.items[i] for i in indices]
            return MultiEvaluation(self.connection, self.context_id, evaluations)
        return self.items[key]

    @beartype
    def __add__(self, other) -> "MultiEvaluation":
        self.assert_same_connection(other)
        items = self.items.copy()
        self._add_other_items_to_items(other, items)
        return MultiEvaluation(self.connection, self.context_id, items)

    @beartype
    def __iadd__(self, other) -> "MultiEvaluation":
        self.assert_same_connection(other)
        self._add_other_items_to_items(other, self.items)
        return self

    def _add_other_items_to_items(self, other, items) -> None:
        if isinstance(other, MultiEvaluation):
            if other.context_id != self.context_id:
                raise exceptions.BadRequestError(
                    "These evaluations does not come from the same context"
                )
            items.extend(other.items.copy())
        elif isinstance(other, Evaluation):
            if other.context_id != self.context_id:
                raise exceptions.BadRequestError(
                    "This evaluation does not come from the same context"
                )
            items.append(other)
        else:
            raise exceptions.BadRequestError("You can't add these two objects")

    def copy(self) -> "MultiEvaluation":
        return MultiEvaluation(self.connection, self.context_id, self.items.copy())
