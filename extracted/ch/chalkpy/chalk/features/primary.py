import typing
from collections.abc import Iterable
from typing import TYPE_CHECKING, Any, Protocol, Type, TypeVar, overload

from typing_extensions import Annotated

from chalk.features.feature_field import Feature
from chalk.features.feature_set import Features, is_feature_set_class, is_features_cls
from chalk.features.feature_wrapper import unwrap_feature

T = TypeVar("T")

if TYPE_CHECKING:

    class Primary(Protocol[T]):
        """Marks a feature as the primary feature for a feature class.

        Features named `id` on feature classes without an explicit primary
        feature are declared primary keys by default, and don't need to be
        marked with `Primary`.

        If you have primary key feature with a name other than `id`,
        you can use this marker to indicate the primary key.

        Examples
        --------
        >>> from chalk.features import features
        >>> from chalk import Primary
        >>> @features
        ... class User:
        ...     uid: Primary[int]
        """

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

    class Primary:
        """Marks a feature as the primary feature for a feature class.

        Features named `id` on feature classes without an explicit primary
        feature are declared primary keys by default, and don't need to be
        marked with `Primary`.

        If you have primary key feature with a name other than `id`,
        you can use this marker to indicate the primary key.

        Examples
        --------
        >>> from chalk.features import features
        >>> from chalk import Primary
        >>> @features
        ... class User:
        ...     username: Primary[str]
        """

        def __class_getitem__(cls, item: typing.Union[Type, str, int]):
            """
            Parameters
            ----------
            item
                The type of the feature value.

            Returns
            -------
            Annotated[item, "__chalk_primary__"]
                The type, with a special annotation indicating that it is a
                primary key.

            Examples
            --------
            >>> from chalk.features import features
            >>> from chalk import Primary
            >>> @features
            ... class User:
            ...     username: Primary[str]
            """
            return Annotated[item, "__chalk_primary__"]


def is_primary(f: Any) -> bool:
    """Determine whether a feature is a primary key.

    Parameters
    ----------
    f
        A feature (i.e. `User.email`)

    Raises
    ------
    TypeError
        If `f` is not a feature.

    Returns
    -------
    bool
        `True` if `f` is primary and `False` otherwise.

    Examples
    --------
    >>> from chalk.features import features
    >>> from chalk import Primary
    >>> @features
    ... class User:
    ...     uid: Primary[int]
    ...     email: str
    >>> assert is_primary(User.uid)
    >>> assert not is_primary(User.email)
    """
    return unwrap_feature(f).primary


def get_primary_feature(feature_class: typing.Union[Type[Features], typing.Iterable[Feature]]) -> Feature:
    """Returns the primary key feature of a features class or a set of features.

    Parameters
    ----------
    feature_class
        Either a features class or an iterable containing Chalk feature fields.

    Examples
    --------
    >>> from chalk.features import features
    >>> from chalk import Primary
    >>> @features
    ... class User:
    ...     uid: Primary[int]
    ...     email: str
    ...     first_name: str
    ...     last_name: str
    >>> assert get_primary_feature(User).fqn == "user.uid"
    >>> assert get_primary_feature(User).primary
    >>> assert get_primary_feature(Features[User.uid, User.email]).fqn == "user.uid"
    >>> assert get_primary_feature(Features[User.uid, User.email]).primary

    :param feature_class: Either a features class or an iterable containing Chalk feature fields.
    :return: The primary feature for the given feature class/set. Raises an exception if there is no primary key present.
    """
    if is_feature_set_class(feature_class):
        if feature_class.__chalk_primary__ is not None:
            return feature_class.__chalk_primary__
        raise ValueError(f"Feature set {feature_class} does not contain a primary feature.")
    elif is_features_cls(feature_class):
        for f in feature_class.features:
            if is_primary(f):
                return f
        raise ValueError(f"Feature set {feature_class} does not contain a primary feature.")
    elif isinstance(feature_class, Iterable):
        for f in feature_class:
            if is_primary(unwrap_feature(f)):
                return f
        raise ValueError(f"Feature set {feature_class} does not contain a primary feature.")
    else:
        raise ValueError(f"Object {feature_class} is not a feature set.")
