from abc import ABC
from typing import ParamSpec, Any
from pathlib import Path, PurePath
from navconfig.logging import logging
from ..utils import SafeDict, fnExecutor


P = ParamSpec("P")


class MaskSupport(ABC):
    """MaskSupport.

    Processing Masks Support.
    """
    def __init__(
        self,
        *args: P.args,
        **kwargs: P.kwargs
    ):
        self._mask = {}  # masks for function replacing
        masks = kwargs.pop('_masks', {})
        self.logger = logging.getLogger('Flowtask.Mask')
        # filling Masks:
        if "masks" in kwargs:
            self._mask = kwargs.pop('masks')
            object.__setattr__(self, "masks", self._mask)
        for mask, replace in masks.items():
            self._mask[mask] = replace  # override component's masks
        try:
            super().__init__(*args, **kwargs)
        except TypeError:
            super().__init__()

    def _mask_processing(self, variables: dict) -> None:
        try:
            for mask, replace in self._mask.items():
                # first: making replacement of masks based on vars:
                try:
                    if mask in variables:
                        value = variables[mask]
                    else:
                        value = replace.format(**variables)
                except Exception:
                    value = replace
                value = fnExecutor(value)
                self.logger.notice(
                    f":: Set Mask {mask} == {value!s}"
                )
                self._mask[mask] = value
        except Exception as err:
            self.logger.warning(
                f"Mask Error: {err}"
            )

    def mask_replacement(self, obj: Any):
        """mask_replacement.

        Replacing occurrences of Masks into an String.
        Args:
            obj (Any): Any kind of object.

        Returns:
            Any: Object with replaced masks.
        """
        for mask, replace in self._mask.items():
            if mask in self._variables:
                value = self._variables[mask]
                # Using SafeDict instead direct replacement:
                value = str(obj).format_map(SafeDict(**self._variables))
            else:
                if str(obj) == mask and mask.startswith("#"):
                    # full replacement of the mask
                    obj = replace
                    return obj
                else:
                    try:
                        if str(obj) == mask and mask.startswith("{"):
                            value = str(obj).replace(mask, str(replace))
                        elif mask in str(obj) and mask.startswith("{"):
                            try:
                                value = str(obj).replace(mask, str(replace))
                            except (ValueError, TypeError) as exc:
                                # remove the "{" and "}" from the mask
                                mask = mask[1:-1]
                                value = str(obj).format_map(
                                    SafeDict({mask: replace})
                                )
                        else:
                            value = str(obj).format_map(
                                SafeDict({mask: replace})
                            )
                    except (ValueError, TypeError):
                        value = str(obj).replace(mask, str(replace))
            if isinstance(obj, PurePath):
                obj = Path(value).resolve()
            else:
                obj = value
        return obj

    def mask_replacement_recursively(self, obj: Any):
        """
        This function replaces all occurrences of "{key}" in the obj structure
        with the corresponding value from the replacements dictionary, recursively.

        Args:
            obj: an object to process.

        Returns:
            The modified obj structure with curly brace replacements.
        """

        if isinstance(obj, dict):
            # If it's a dictionary, iterate through each key-value pair
            for key, value in obj.copy().items():
                # Recursively replace in the key and value
                obj[key] = self.mask_replacement_recursively(value)

                # Check if the key itself has curly braces
                if isinstance(key, str):
                    # Use f-string for formatted key
                    new_key = self.mask_replacement(key)

                    if new_key != key:
                        obj.pop(key)  # Remove old key and add formatted one
                        obj[new_key] = value  # Add key-value pair with formatted key

        elif isinstance(obj, list):
            # If it's a list, iterate through each element and replace recursively
            for idx, value in enumerate(obj):
                obj[idx] = self.mask_replacement_recursively(value)

        elif isinstance(obj, str):
            # If it's a string, use f-string formatting to replace
            return self.mask_replacement(obj)

        return obj

    def resolve_variables_recursively(self, obj: Any) -> Any:
        """resolve_variables_recursively.

        Resolve ``{variable}`` placeholders in any structure (dict, list, str)
        using ``self._variables``.  Unknown placeholders are left intact thanks
        to ``SafeDict``.

        Args:
            obj: Any object to process.

        Returns:
            The same structure with every ``{variable}`` replaced.
        """
        if not self._variables:
            return obj
        if isinstance(obj, dict):
            return {k: self.resolve_variables_recursively(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [self.resolve_variables_recursively(item) for item in obj]
        if isinstance(obj, str) and '{' in obj:
            try:
                return obj.format_map(SafeDict(**self._variables))
            except (ValueError, TypeError):
                return obj
        return obj

    def mask_start(self, **kwargs):
        # Usable by Hooks
        self._masks: dict = kwargs.pop("masks", {})
        self._variables = kwargs.pop("variables", {})
        self._mask_processing(variables=self._variables)
