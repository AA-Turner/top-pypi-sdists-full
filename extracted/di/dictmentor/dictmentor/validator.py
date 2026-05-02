"""Contains argument validating stuff."""

from functools import partial
from pathlib import Path
from typing import Dict, Any, Callable, Iterable, cast, Union, Optional

ValidationReturn = Union[bool, Dict[str, bool]]


class Validator:
    """
    Provides utility methods to easily validate arguments / variables.
    Per default the methods will return True / False whether the argument obeys the rules or not.
    If raise_ex is set to True instead of returning True / False a meaningful exception will be
    thrown.

    The advantage of this component is to produce consistent validation and error messages in a more
    convenient way that assert or other mechanisms do provide.

    But keep in mind: The most pythonic idiom is to clearly document what the function expects and
    then just try to use whatever gets passed to your function. The validators are only for
    situations were you cannot avoid it.
    """
    @staticmethod
    def __logical_dict_merge(first: Dict[Any, bool], second: Dict[Any, bool]) -> Dict[Any, bool]:
        if second is None or not isinstance(second, dict):
            return first

        res = first.copy()
        for k, val in second.items():
            if k in first:
                res[k] = res[k] and val
            else:
                res[k] = val

        return res

    @staticmethod
    def __test_all(condition: Callable[[str, Any], bool],
                   formatter: Callable[[str, Any], str], raise_ex: bool, summary: bool,
                   validators: Optional[Iterable[Callable[..., ValidationReturn]]] = None,
                   **items: Any) -> ValidationReturn:
        assert callable(condition)
        assert callable(formatter)

        res = {}  # type: Dict[Any, bool]
        if validators is not None:
            for validator in validators:
                # Case 1: raise_ex=True -> We don't have anything to catch
                #   -> just propagate the error
                # Case 2: summary=True
                #   -> We have to short circuit if the result is evaluated to False
                # Case 3: raise_ex=False, summary=False
                #   -> We get a dictionary containing the evaluated conditions
                # -> We need to merge them with the previous output / results
                val_res = validator(raise_ex=raise_ex, summary=summary, **items)
                if summary and not val_res:
                    return False
                res = Validator.__logical_dict_merge(res, cast(Dict[Any, bool], val_res))

        cond_res = {}
        for varname, val in items.items():
            cond_eval = condition(varname, val)
            if raise_ex and not cond_eval:
                # Short-circuit on raise_ex
                raise ValueError(formatter(varname, val))
            if summary and not cond_eval:
                # Short-circuit on summary (at least one item has validated to False -> abort)
                return False
            cond_res[varname] = cond_eval

        res = Validator.__logical_dict_merge(res, cond_res)
        # If summary is True we need to return back only one boolean value.
        return res if not summary else all(res.items())

    @staticmethod
    def instance_of(target_type: Optional[type] = None, raise_ex: bool = False,
                    summary: bool = True, **items: Any) -> ValidationReturn:
        """
        Tests if the given key-value pairs (items) are instances of the given ``target_type``.
        Per default this function yields whether ``True`` or ``False`` depending on the fact if all
        items withstand the validation or not. Per default the validation / evaluation is
        short-circuit and will return as soon an item evaluates to ``False``.

        When ``raise_ex`` is set to ``True`` the function will raise a meaningful error message
        after the first item evaluates to ``False`` (short-circuit).

        When ``summary`` is set to ``False`` a dictionary is returned containing the individual
        evaluation result of each item (non short-circuit).

        Examples:


            >>> Validator.instance_of(my_str='str', my_str2='str2', target_type=str)
            True
            >>> Validator.instance_of(my_str1='str', target_type=int)
            False
            >>> Validator.instance_of(my_str=None, raise_ex=True, target_type=str)
            Traceback (most recent call last):
                ...
            ValueError: 'my_str' (NoneType) is not an instance of type 'str'
            >>> Validator.instance_of(my_str='a', my_str2=1, raise_ex=True, target_type=str)
            Traceback (most recent call last):
                ...
            ValueError: 'my_str2' (int) is not an instance of type 'str'
            >>> (Validator.instance_of(
            ...     my_str='str', my_str2='str2', non_str=5, target_type=str, summary=False
            ... )
            ... == {'my_str': True, 'my_str2': True, 'non_str': False})
            True

        Args:
            raise_ex (bool, optional): If set to ``True`` an exception is raised if at least one
            item is validated to ``False`` (works short-circuit and will abort the validation when
            the first item is evaluated to ``False``).

            summary (bool, optional): If set to ``False`` instead of returning just a single
            `bool` the validation will return a dictionary containing the individual evaluation
            result of each item.

            target_type (type): The target type to test the values against.

        Returns:
            (boolean or dictionary): ``True`` when the value was successfully validated; ``False``
                otherwise.
            If ``summary`` is set to ``False`` a dictionary containing the individual evaluation
            result of each item will be returned.
            If ``raise_ex`` is set to True, instead of returning False a meaningful error will be
            raised.
        """
        if not target_type:
            raise ValueError("Argument 'target_type' is None")

        return Validator.__test_all(
            condition=lambda _, val: isinstance(val, cast(type, target_type)),
            formatter=(
                lambda name, val:
                "'{varname}' ({actual}) is not an instance of type '{ttype}'".format(
                    varname=name,
                    actual=type(val).__name__,
                    ttype=cast(type, target_type).__name__
                )
            ),
            raise_ex=raise_ex,
            summary=summary,
            **items
        )

    @staticmethod
    def is_stream(raise_ex: bool = False, summary: bool = True,
                  **items: Any) -> ValidationReturn:
        """
        Tests if the given key-value pairs (items) are all streams. Basically checks if the item
        provides a read(...) method.
        Per default this function yields whether ``True`` or ``False`` depending on the fact if all
        items withstand the validation or not. Per default the validation / evaluation is
        short-circuit and will return as soon an item evaluates to ``False``.

        When ``raise_ex`` is set to ``True`` the function will raise a meaningful error message
        after the first item evaluates to ``False`` (short-circuit).

        When ``summary`` is set to ``False`` a dictionary is returned containing the individual
        evaluation result of each item (non short-circuit).

        Examples:

            >>> class MyStream():
            ...     def read(self):
            ...         pass
            >>> Validator.is_stream(stream=MyStream())
            True
            >>> Validator.is_stream(nonstream='abc')
            False
            >>> Validator.is_stream(stream=MyStream(), nonstream='abc', summary=True)
            False
            >>> (Validator.is_stream(stream=MyStream(), nonstream='abc', summary=False)
            ... == {'stream': True, 'nonstream': False})
            True
            >>> Validator.is_stream(nonstream='abc', raise_ex=True)
            Traceback (most recent call last):
                ...
            ValueError: 'nonstream' is not a stream

        Args:

            raise_ex (bool, optional): If set to ``True`` an exception is raised if at least one
            item is validated to ``False`` (works short-circuit and will abort the validation when
            the first item is evaluated to ``False``).

            summary (bool, optional): If set to ``False`` instead of returning just a single
            ``bool`` the validation will return a dictionary containing the individual evaluation
            result of each item.

        Returns:
            (boolean or dictionary): ``True`` when the value was successfully validated; ``False``
                otherwise.
            If ``summary`` is set to ``False`` a dictionary containing the individual evaluation
            result of each item will be returned.
            If ``raise_ex`` is set to True, instead of returning False a meaningful error will be
            raised.

        """
        return Validator.__test_all(
            condition=lambda _, val: getattr(val, 'read', None) is not None,
            formatter=lambda name, _: "'{varname}' is not a stream".format(varname=name),
            raise_ex=raise_ex,
            summary=summary,
            **items
        )

    @staticmethod
    def is_file(raise_ex: bool = False, summary: bool = True,
                **items: Any) -> ValidationReturn:
        """
        Tests if the given key-value pairs (items) are physical existent files or links to regular
        files.
        Per default this function yields whether ``True`` or ``False`` depending on the fact if all
        items withstand the validation or not. Per default the validation / evaluation is
        short-circuit and will return as soon an item evaluates to ``False``.

        When ``raise_ex`` is set to ``True`` the function will raise a meaningful error message
        after the first item evaluates to ``False`` (short-circuit).

        When ``summary`` is set to ``False`` a dictionary is returned containing the individual
        evaluation result ofeach item (non short-circuit).

        Examples:

            >>> import tempfile
            >>> tmp = tempfile.NamedTemporaryFile()
            >>> Validator.is_file(file=tmp.name)
            True
            >>> Validator.is_file(nonfile="iamsurethatthisdontexist")
            False
            >>> Validator.is_file(file=tmp.name, nonfile="iamsurethatthisdontexist")
            False
            >>> (Validator.is_file(file=tmp.name, nonfile="iamsurethatthisdontexist", summary=False)
            ... == {'file': True, 'nonfile': False})
            True
            >>> Validator.is_file(file=tmp.name, nonfile="iamsurethatthisdontexist", raise_ex=True)
            Traceback (most recent call last):
                ...
            ValueError: 'nonfile' is not a file
            >>> with open(tmp.name) as fp:
            ...     Validator.is_file(nonfile=fp)
            False


        Args:

            raise_ex (bool, optional): If set to ``True`` an exception is raised if at least one i
            tem is validated to ``False`` (works short-circuit and will abort the validation when
            the first item is evaluated to ``False``).

            summary (bool, optional): If set to ``False`` instead of returning just a single
            ``bool`` the validation will return a dictionary containing the individual evaluation
            result of each item.

        Returns:
            (boolean or dictionary): ``True`` when the value was successfully validated; ``False``
                otherwise.
            If ``summary`` is set to ``False`` a dictionary containing the individual evaluation
            result of each item will be returned.
            If ``raise_ex`` is set to True, instead of returning False a meaningful error will be
            raised.

        """
        return Validator.__test_all(
            condition=lambda _, val: Path(val).is_file(),
            formatter=lambda name, _: "'{varname}' is not a file".format(varname=name),
            validators=[partial(Validator.instance_of, target_type=str)],
            raise_ex=raise_ex,
            summary=summary,
            **items
        )

    @staticmethod
    def is_real_iterable(raise_ex: bool = False, summary: bool = True,
                         **items: Any) -> ValidationReturn:
        """
        Tests if the given items are iterables (collections) but no strings.
        Per default this function yields whether ``True`` or ``False`` depending on the fact if all
        items withstand the validation or not. Per default the validation / evaluation is
        short-circuit and will return as soon an item evaluates to ``False``.

        When ``raise_ex`` is set to ``True`` the function will raise a meaningful error message
        after the first item evaluates to ``False`` (short-circuit).

        When ``summary`` is set to ``False`` a dictionary is returned containing the individual
        evaluation result of each item (non short-circuit).

        Examples:

            >>> l = ['i', 'am', 'an', 'iterable']
            >>> Validator.is_real_iterable(l=l)
            True

            >>> d = {'i': 'am', 'a': 'dict'}
            >>> Validator.is_real_iterable(d=d)
            True

            >>> s = "i am a string"
            >>> Validator.is_real_iterable(s=s)
            False

            >>> Validator.is_real_iterable(raise_ex=True, s=s)
            Traceback (most recent call last):
                ...
            ValueError: 's' is not an iterable

        Args:

            raise_ex (bool, optional): If set to ``True`` an exception is raised if at least one
            item is validated to ``False`` (works short-circuit and will abort the validation when
            the first item is evaluated to ``False``).

            summary (bool, optional): If set to ``False`` instead of returning just a single
            ``bool`` the validation will return a dictionary containing the individual evaluation
            result of each item.

        Returns:
            (boolean or dictionary): ``True`` when the value was successfully validated; ``False``
                otherwise.
            If ``summary`` is set to ``False`` a dictionary containing the individual evaluation
            result of each item will be returned.
            If ``raise_ex`` is set to True, instead of returning False a meaningful error will be
            raised.

        """

        return Validator.__test_all(
            condition=lambda _, val: hasattr(val, '__iter__') and not isinstance(val, str),
            formatter=lambda name, _: "'{varname}' is not an iterable".format(varname=name),
            raise_ex=raise_ex,
            summary=summary,
            **items
        )
