from typing import TYPE_CHECKING, Any, Protocol, Set, Type, TypeVar, overload

from chalk.features import Feature
from chalk.features.feature_wrapper import unwrap_feature

T = TypeVar("T")

if TYPE_CHECKING:

    class Last(Protocol[T]):
        @overload
        def __get__(self, instance: None, owner: Any) -> Type[T]:
            ...

        @overload
        def __get__(self, instance: object, owner: Any) -> T:
            ...

        def __set__(self, instance: Any, value: T) -> None:
            ...

        def __delete__(self, instance: Any) -> None:
            ...

else:

    class Last:
        """Marks a feature as the last observed value of a feature.

        Examples
        --------
        >>> from chalk.features import features, online
        >>> @features
        ... class User:
        ...     id: int
        ...     model_score: float
        >>> @online
        ... def get_score(
        ...     s: Last[User.model_score]
        ... ) -> User.model_score:
        ...     return s * 1.2
        """

        registry: Set[Feature]

        def __class_getitem__(cls, item):
            return unwrap_feature(item).as_last()
