import inspect
import typing as t
from copy import deepcopy

import typing_extensions as te

from dreadnode.core.exceptions import warn_at_user_stacklevel
from dreadnode.core.meta import Component, ConfigInfo, Context

if t.TYPE_CHECKING:
    from dreadnode.generators.chat import Chat

In = te.TypeVar("In", default=t.Any)
Out = te.TypeVar("Out", default=t.Any)
In_contra = te.TypeVar("In_contra", contravariant=True, default=t.Any)
Out_co = te.TypeVar("Out_co", covariant=True, default=t.Any)
OuterIn = te.TypeVar("OuterIn", default=t.Any)
OuterOut = te.TypeVar("OuterOut", default=t.Any)


class TransformWarning(UserWarning):
    """Warning issued for non-critical issues during transformations."""


@t.runtime_checkable
class TransformCallable(t.Protocol, t.Generic[In_contra, Out_co]):
    """
    A callable that takes in one object, and returns another.
    """

    def __call__(
        self, obj: In_contra, /, *args: t.Any, **kwargs: t.Any
    ) -> t.Awaitable[Out_co] | Out_co: ...


Modality = t.Literal["text", "image", "audio", "video"]
"""Supported data modalities for transforms."""


class Transform(Component[te.Concatenate[In, ...], Out], t.Generic[In, Out]):
    """
    Represents a transformation operation that modifies the input data.
    """

    def __init__(
        self,
        func: TransformCallable[In, Out],
        *,
        name: str | None = None,
        catch: bool = False,
        modality: Modality | None = None,
        config: dict[str, ConfigInfo] | None = None,
        context: dict[str, Context] | None = None,
        compliance_tags: dict[str, t.Any] | None = None,
    ):
        super().__init__(
            t.cast("t.Callable[[In], Out]", func), name=name, config=config, context=context
        )

        self.name = self.name
        "The name of the transform, used for reporting and logging."
        self.catch = catch
        """
        If True, catches exceptions during the transform and attempts to return the original,
        unmodified object from the input. If False, exceptions are raised.
        """
        self.modality = modality
        """The data modality this transform operates on (text, image, audio, video)."""
        self.compliance_tags = compliance_tags or {}
        """Compliance framework tags (OWASP, ATLAS, SAIF) for this transform."""

    @classmethod
    def fit(cls, transform: "TransformLike[In, Out]") -> "Transform[In, Out]":
        """Ensures that the provided transform is a Transform instance."""
        if isinstance(transform, Transform):
            return transform
        if callable(transform):
            return Transform(transform)
        raise TypeError("Transform must be a Transform instance or a callable.")

    @classmethod
    def fit_many(cls, transforms: "TransformsLike[In, Out] | None") -> list["Transform[In, Out]"]:
        """
        Convert a collection of transform-like objects into a list of Transform instances.

        This method provides a flexible way to handle different input formats for transforms,
        automatically converting callables to Transform objects and applying consistent naming
        and attributes across all transforms.

        Args:
            transforms: A collection of transform-like objects. Can be:
                - A dictionary mapping names to transform objects or callables
                - A sequence of scorer objects or callables
                - None (returns empty list)

        Returns:
            A list of Scorer instances with consistent configuration.
        """
        if isinstance(transforms, t.Mapping):
            return [  # ty: ignore[invalid-return-type]
                transform.with_(name=name)
                if isinstance(transform, Transform)
                else cls(transform, name=name)
                for name, transform in transforms.items()
            ]

        return [
            transform if isinstance(transform, Transform) else cls(transform)
            for transform in transforms or []
        ]

    def __repr__(self) -> str:
        return f"Transform(name='{self.name}')"

    def __deepcopy__(self, memo: dict[int, t.Any]) -> "Transform[In, Out]":
        return Transform(
            func=self.func,
            name=self.name,
            catch=self.catch,
            modality=self.modality,
            config=deepcopy(self.__dn_param_config__, memo),
            context=deepcopy(self.__dn_context__, memo),
            compliance_tags=deepcopy(self.compliance_tags, memo),
        )

    def clone(self) -> "Transform[In, Out]":
        """Clone the transform."""
        return self.__deepcopy__({})

    def with_(
        self,
        *,
        name: str | None = None,
        catch: bool | None = None,
        modality: Modality | None = None,
        compliance_tags: dict[str, t.Any] | None = None,
    ) -> "Transform[In, Out]":
        """Create a new Transform with updated properties."""
        new = self.clone()
        new.name = name or self.name
        new.catch = catch if catch is not None else self.catch
        new.modality = modality if modality is not None else self.modality
        new.compliance_tags = (
            deepcopy(compliance_tags)
            if compliance_tags is not None
            else deepcopy(self.compliance_tags)
        )
        return new

    def rename(self, new_name: str) -> "Transform[In, Out]":
        """
        Rename the transform.

        Args:
            new_name: The new name for the transform.

        Returns:
            A new Transform with the updated name.
        """
        return self.with_(name=new_name)

    def as_transform(
        self,
        *,
        adapt_in: t.Callable[[OuterIn], In],
        adapt_out: t.Callable[[Out], OuterOut],
        name: str | None = None,
    ) -> "Transform[OuterIn, OuterOut]":
        """Adapt this transform to a different input/output shape."""

        async def adapted(obj: OuterIn, *args: t.Any, **kwargs: t.Any) -> OuterOut:
            transformed = await self.transform(adapt_in(obj), *args, **kwargs)
            return adapt_out(transformed)

        return Transform(  # ty: ignore[invalid-return-type]
            adapted,
            name=name or self.name,
            catch=self.catch,
            modality=self.modality,
            compliance_tags=deepcopy(self.compliance_tags),
        )

    async def transform(self, object: In, *args: t.Any, **kwargs: t.Any) -> Out:
        """
        Perform a transform from In to Out.

        Args:
            object: The input object to transform.

        Returns:
            The transformed output object.
        """

        try:
            bound_args = self._bind_args(object, *args, **kwargs)
            result = t.cast(
                "Out | t.Awaitable[Out]", self.func(*bound_args.args, **bound_args.kwargs)
            )
            if inspect.isawaitable(result):
                result = await result

        except Exception as e:
            if not self.catch:
                raise

            warn_at_user_stacklevel(
                f"Error executing transformation {self.name!r} for object {object!r}: {e}",
                TransformWarning,
            )
            return t.cast("Out", object)

        return result  # ty: ignore[invalid-return-type]

    @te.override
    async def __call__(self, object: In, *args: t.Any, **kwargs: t.Any) -> Out:  # ty: ignore[invalid-method-override]
        return await self.transform(object, *args, **kwargs)


TransformLike = Transform[In, Out] | TransformCallable[In, Out]
"""A transform or compatible callable."""
TransformsLike = t.Sequence[TransformLike[In, Out]] | t.Mapping[str, TransformLike[In, Out]]
"""A sequence of transform-like objects or mapping of name/transform pairs."""


class PostTransformWarning(UserWarning):
    """Warning issued for non-critical issues during post-transformations."""


@t.runtime_checkable
class PostTransformCallable(t.Protocol):
    """
    A callable that takes a Chat and returns a Chat.
    """

    def __call__(
        self, chat: "Chat", /, *args: t.Any, **kwargs: t.Any
    ) -> "t.Awaitable[Chat] | Chat": ...


class PostTransform(Component[te.Concatenate["Chat", ...], "Chat"]):
    """
    Represents a post-transformation operation that modifies a Chat after generation.
    """

    def __init__(
        self,
        func: PostTransformCallable,
        *,
        name: str | None = None,
        catch: bool = False,
        config: dict[str, ConfigInfo] | None = None,
        context: dict[str, Context] | None = None,
    ):
        super().__init__(
            t.cast("t.Callable[[Chat], Chat]", func), name=name, config=config, context=context
        )

        self.name = self.name
        "The name of the post-transform, used for reporting and logging."
        self.catch = catch
        """
        If True, catches exceptions during the transform and attempts to return the original,
        unmodified chat. If False, exceptions are raised.
        """

    @classmethod
    def fit(cls, transform: "PostTransformLike") -> "PostTransform":
        """Ensures that the provided transform is a PostTransform instance."""
        if isinstance(transform, PostTransform):
            return transform
        if callable(transform):
            return PostTransform(transform)
        raise TypeError("PostTransform must be a PostTransform instance or a callable.")

    @classmethod
    def fit_many(cls, transforms: "PostTransformsLike | None") -> list["PostTransform"]:
        """
        Convert a collection of transform-like objects into a list of PostTransform instances.

        Args:
            transforms: A collection of transform-like objects. Can be:
                - A dictionary mapping names to transform objects or callables
                - A sequence of transform objects or callables
                - None (returns empty list)

        Returns:
            A list of PostTransform instances with consistent configuration.
        """
        if isinstance(transforms, t.Mapping):
            return [
                transform.with_(name=name)
                if isinstance(transform, PostTransform)
                else cls(transform, name=name)
                for name, transform in transforms.items()
            ]

        return [
            transform if isinstance(transform, PostTransform) else cls(transform)
            for transform in transforms or []
        ]

    def __repr__(self) -> str:
        return f"PostTransform(name='{self.name}')"

    def __deepcopy__(self, memo: dict[int, t.Any]) -> "PostTransform":
        return PostTransform(
            func=self.func,
            name=self.name,
            catch=self.catch,
            config=deepcopy(self.__dn_param_config__, memo),
            context=deepcopy(self.__dn_context__, memo),
        )

    def clone(self) -> "PostTransform":
        """Clone the post-transform."""
        return self.__deepcopy__({})

    def with_(
        self,
        *,
        name: str | None = None,
        catch: bool | None = None,
    ) -> "PostTransform":
        """
        Create a new PostTransform with updated properties.

        Args:
            name: New name for the transform.
            catch: Catch exceptions in the transform function.

        Returns:
            A new PostTransform with the updated properties
        """
        new = self.clone()
        new.name = name or self.name
        new.catch = catch if catch is not None else self.catch
        return new

    def rename(self, new_name: str) -> "PostTransform":
        """
        Rename the post-transform.

        Args:
            new_name: The new name for the transform.

        Returns:
            A new PostTransform with the updated name.
        """
        return self.with_(name=new_name)

    async def transform(self, chat: "Chat", *args: t.Any, **kwargs: t.Any) -> "Chat":
        """
        Perform a post-transformation on a Chat.

        Args:
            chat: The input Chat to transform.

        Returns:
            The transformed Chat.
        """
        try:
            bound_args = self._bind_args(chat, *args, **kwargs)
            result = t.cast(
                "Chat | t.Awaitable[Chat]", self.func(*bound_args.args, **bound_args.kwargs)
            )
            if inspect.isawaitable(result):
                result = await result

        except Exception as e:
            if not self.catch:
                raise

            warn_at_user_stacklevel(
                f"Error executing post-transformation {self.name!r} for chat: {e}",
                PostTransformWarning,
            )
            return chat

        return result  # ty: ignore[invalid-return-type]

    @te.override
    async def __call__(self, chat: "Chat", *args: t.Any, **kwargs: t.Any) -> "Chat":  # ty: ignore[invalid-method-override]
        return await self.transform(chat, *args, **kwargs)


PostTransformLike = PostTransform | PostTransformCallable
"""A post-transform or compatible callable."""
PostTransformsLike = t.Sequence[PostTransformLike] | t.Mapping[str, PostTransformLike]
"""A sequence of post-transform-like objects or mapping of name/transform pairs."""
