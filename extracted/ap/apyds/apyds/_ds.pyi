"""Type stubs for the _ds pybind11 extension module.

This module provides the C++ extension interface for the deductive system.
All classes are implemented in C++ using pybind11.
"""

from enum import Enum
from typing import Callable, Optional

class String:
    """C++ binding for ds::string_t."""

    @staticmethod
    def from_string(string: str, capacity: int) -> Optional[String]:
        """Create a String from a string with the given buffer capacity.

        Args:
            string: The string to parse.
            capacity: The buffer size for the operation.

        Returns:
            A String object, or None if parsing fails.
        """
        ...

    @staticmethod
    def to_string(value: String, capacity: int) -> str:
        """Convert a String to a string representation.

        Args:
            value: The String to convert.
            capacity: The buffer size for the operation.

        Returns:
            The string representation.
        """
        ...

    @staticmethod
    def from_binary(binary: memoryview) -> String:
        """Create a String from binary data.

        Args:
            binary: The binary data to read from.

        Returns:
            A String object.
        """
        ...

    @staticmethod
    def to_binary(value: String) -> memoryview:
        """Convert a String to binary data.

        Args:
            value: The String to convert.

        Returns:
            The binary representation as a memoryview.
        """
        ...

    def clone(self) -> String:
        """Create a deep copy of this String.

        Returns:
            A new String object with copied data.
        """
        ...

    def data_size(self) -> int:
        """Get the size of the String data in bytes.

        Returns:
            The data size.
        """
        ...

class Variable:
    """C++ binding for ds::variable_t."""

    @staticmethod
    def from_string(string: str, capacity: int) -> Optional[Variable]:
        """Create a Variable from a string with the given buffer capacity.

        Args:
            string: The string to parse.
            capacity: The buffer size for the operation.

        Returns:
            A Variable object, or None if parsing fails.
        """
        ...

    @staticmethod
    def to_string(value: Variable, capacity: int) -> str:
        """Convert a Variable to a string representation.

        Args:
            value: The Variable to convert.
            capacity: The buffer size for the operation.

        Returns:
            The string representation.
        """
        ...

    @staticmethod
    def from_binary(binary: memoryview) -> Variable:
        """Create a Variable from binary data.

        Args:
            binary: The binary data to read from.

        Returns:
            A Variable object.
        """
        ...

    @staticmethod
    def to_binary(value: Variable) -> memoryview:
        """Convert a Variable to binary data.

        Args:
            value: The Variable to convert.

        Returns:
            The binary representation as a memoryview.
        """
        ...

    def clone(self) -> Variable:
        """Create a deep copy of this Variable.

        Returns:
            A new Variable object with copied data.
        """
        ...

    def data_size(self) -> int:
        """Get the size of the Variable data in bytes.

        Returns:
            The data size.
        """
        ...

    def name(self) -> String:
        """Get the name of this variable.

        Returns:
            The variable name as a String.
        """
        ...

class Item:
    """C++ binding for ds::item_t."""

    @staticmethod
    def from_string(string: str, capacity: int) -> Optional[Item]:
        """Create an Item from a string with the given buffer capacity.

        Args:
            string: The string to parse.
            capacity: The buffer size for the operation.

        Returns:
            An Item object, or None if parsing fails.
        """
        ...

    @staticmethod
    def to_string(value: Item, capacity: int) -> str:
        """Convert an Item to a string representation.

        Args:
            value: The Item to convert.
            capacity: The buffer size for the operation.

        Returns:
            The string representation.
        """
        ...

    @staticmethod
    def from_binary(binary: memoryview) -> Item:
        """Create an Item from binary data.

        Args:
            binary: The binary data to read from.

        Returns:
            An Item object.
        """
        ...

    @staticmethod
    def to_binary(value: Item) -> memoryview:
        """Convert an Item to binary data.

        Args:
            value: The Item to convert.

        Returns:
            The binary representation as a memoryview.
        """
        ...

    def clone(self) -> Item:
        """Create a deep copy of this Item.

        Returns:
            A new Item object with copied data.
        """
        ...

    def data_size(self) -> int:
        """Get the size of the Item data in bytes.

        Returns:
            The data size.
        """
        ...

    def name(self) -> String:
        """Get the name of this item.

        Returns:
            The item name as a String.
        """
        ...

class List:
    """C++ binding for ds::list_t."""

    @staticmethod
    def from_string(string: str, capacity: int) -> Optional[List]:
        """Create a List from a string with the given buffer capacity.

        Args:
            string: The string to parse.
            capacity: The buffer size for the operation.

        Returns:
            A List object, or None if parsing fails.
        """
        ...

    @staticmethod
    def to_string(value: List, capacity: int) -> str:
        """Convert a List to a string representation.

        Args:
            value: The List to convert.
            capacity: The buffer size for the operation.

        Returns:
            The string representation.
        """
        ...

    @staticmethod
    def from_binary(binary: memoryview) -> List:
        """Create a List from binary data.

        Args:
            binary: The binary data to read from.

        Returns:
            A List object.
        """
        ...

    @staticmethod
    def to_binary(value: List) -> memoryview:
        """Convert a List to binary data.

        Args:
            value: The List to convert.

        Returns:
            The binary representation as a memoryview.
        """
        ...

    def clone(self) -> List:
        """Create a deep copy of this List.

        Returns:
            A new List object with copied data.
        """
        ...

    def data_size(self) -> int:
        """Get the size of the List data in bytes.

        Returns:
            The data size.
        """
        ...

    def __len__(self) -> int:
        """Get the number of elements in the list.

        Returns:
            The list length.
        """
        ...

    def __getitem__(self, index: int) -> Term:
        """Get an element from the list by index.

        Args:
            index: The zero-based index of the element.

        Returns:
            The term at the specified index.
        """
        ...

class Term:
    """C++ binding for ds::term_t."""

    class Type(Enum):
        """Enum representing the type of a term."""

        Variable = ...
        Item = ...
        List = ...
        Null = ...

    @staticmethod
    def from_string(string: str, capacity: int) -> Optional[Term]:
        """Create a Term from a string with the given buffer capacity.

        Args:
            string: The string to parse.
            capacity: The buffer size for the operation.

        Returns:
            A Term object, or None if parsing fails.
        """
        ...

    @staticmethod
    def to_string(value: Term, capacity: int) -> str:
        """Convert a Term to a string representation.

        Args:
            value: The Term to convert.
            capacity: The buffer size for the operation.

        Returns:
            The string representation.
        """
        ...

    @staticmethod
    def from_binary(binary: memoryview) -> Term:
        """Create a Term from binary data.

        Args:
            binary: The binary data to read from.

        Returns:
            A Term object.
        """
        ...

    @staticmethod
    def to_binary(value: Term) -> memoryview:
        """Convert a Term to binary data.

        Args:
            value: The Term to convert.

        Returns:
            The binary representation as a memoryview.
        """
        ...

    def clone(self) -> Term:
        """Create a deep copy of this Term.

        Returns:
            A new Term object with copied data.
        """
        ...

    def data_size(self) -> int:
        """Get the size of the Term data in bytes.

        Returns:
            The data size.
        """
        ...

    def get_type(self) -> Type:
        """Get the type of this term.

        Returns:
            The term type (Variable, Item, List, or Null).
        """
        ...

    def variable(self) -> Variable:
        """Get this term as a Variable.

        Returns:
            The term as a Variable.

        Note:
            Should only be called if get_type() returns Type.Variable.
        """
        ...

    def item(self) -> Item:
        """Get this term as an Item.

        Returns:
            The term as an Item.

        Note:
            Should only be called if get_type() returns Type.Item.
        """
        ...

    def list(self) -> List:
        """Get this term as a List.

        Returns:
            The term as a List.

        Note:
            Should only be called if get_type() returns Type.List.
        """
        ...

    @staticmethod
    def ground(term: Term, dictionary: Term, scope: Optional[str], length: int) -> Optional[Term]:
        """Ground a term using a dictionary to substitute variables.

        Args:
            term: The term to ground.
            dictionary: A term representing a dictionary (list of pairs).
            scope: Optional scope string for variable scoping.
            length: The buffer size for the result.

        Returns:
            The grounded term, or None if grounding fails.
        """
        ...

    @staticmethod
    def match(term_1: Term, term_2: Term, scope_1: str, scope_2: str, length: int) -> Optional[Term]:
        """Match two terms and return the unification result.

        Args:
            term_1: The first term to match.
            term_2: The second term to match.
            scope_1: The scope for the first term.
            scope_2: The scope for the second term.
            length: The buffer size for the result.

        Returns:
            A term representing the unification dictionary, or None if matching fails.
        """
        ...

    @staticmethod
    def rename(term: Term, prefix_and_suffix: Term, length: int) -> Optional[Term]:
        """Rename all variables in a term by adding prefix and suffix.

        Args:
            term: The term to rename.
            prefix_and_suffix: A term with two inner lists for prefix and suffix.
            length: The buffer size for the result.

        Returns:
            The renamed term, or None if renaming fails.
        """
        ...

class Rule:
    """C++ binding for ds::rule_t."""

    @staticmethod
    def from_string(string: str, capacity: int) -> Optional[Rule]:
        """Create a Rule from a string with the given buffer capacity.

        Args:
            string: The string to parse.
            capacity: The buffer size for the operation.

        Returns:
            A Rule object, or None if parsing fails.
        """
        ...

    @staticmethod
    def to_string(value: Rule, capacity: int) -> str:
        """Convert a Rule to a string representation.

        Args:
            value: The Rule to convert.
            capacity: The buffer size for the operation.

        Returns:
            The string representation.
        """
        ...

    @staticmethod
    def from_binary(binary: memoryview) -> Rule:
        """Create a Rule from binary data.

        Args:
            binary: The binary data to read from.

        Returns:
            A Rule object.
        """
        ...

    @staticmethod
    def to_binary(value: Rule) -> memoryview:
        """Convert a Rule to binary data.

        Args:
            value: The Rule to convert.

        Returns:
            The binary representation as a memoryview.
        """
        ...

    def clone(self) -> Rule:
        """Create a deep copy of this Rule.

        Returns:
            A new Rule object with copied data.
        """
        ...

    def data_size(self) -> int:
        """Get the size of the Rule data in bytes.

        Returns:
            The data size.
        """
        ...

    def __len__(self) -> int:
        """Get the number of premises in the rule.

        Returns:
            The number of premises.
        """
        ...

    def conclusion(self) -> Term:
        """Get the conclusion of the rule.

        Returns:
            The conclusion term.
        """
        ...

    def __getitem__(self, index: int) -> Term:
        """Get a premise term by index.

        Args:
            index: The zero-based index of the premise.

        Returns:
            The premise term at the specified index.
        """
        ...

    @staticmethod
    def ground(rule: Rule, dictionary: Rule, scope: Optional[str], length: int) -> Optional[Rule]:
        """Ground a rule using a dictionary to substitute variables.

        Args:
            rule: The rule to ground.
            dictionary: A rule representing a dictionary (list of pairs).
            scope: Optional scope string for variable scoping.
            length: The buffer size for the result.

        Returns:
            The grounded rule, or None if grounding fails.
        """
        ...

    @staticmethod
    def match(rule_1: Rule, rule_2: Rule, length: int) -> Optional[Rule]:
        """Match two rules using unification.

        Args:
            rule_1: The first rule to match.
            rule_2: The second rule to match.
            length: The buffer size for the result.

        Returns:
            The matched rule, or None if matching fails.
        """
        ...

    @staticmethod
    def rename(rule: Rule, prefix_and_suffix: Rule, length: int) -> Optional[Rule]:
        """Rename all variables in a rule by adding prefix and suffix.

        Args:
            rule: The rule to rename.
            prefix_and_suffix: A rule with two inner lists for prefix and suffix.
            length: The buffer size for the result.

        Returns:
            The renamed rule, or None if renaming fails.
        """
        ...

class Search:
    """C++ binding for ds::search_t."""

    def __init__(self, limit_size: int, buffer_size: int) -> None:
        """Create a new search engine instance.

        Args:
            limit_size: Size of the buffer for storing final objects.
            buffer_size: Size of the buffer for internal operations.
        """
        ...

    def set_limit_size(self, limit_size: int) -> None:
        """Set the size of the buffer for storing final objects.

        Args:
            limit_size: The new limit size.
        """
        ...

    def set_buffer_size(self, buffer_size: int) -> None:
        """Set the buffer size for internal operations.

        Args:
            buffer_size: The new buffer size.
        """
        ...

    def reset(self) -> None:
        """Reset the search engine, clearing all rules and facts."""
        ...

    def add(self, text: str) -> bool:
        """Add a rule or fact to the knowledge base.

        Args:
            text: The rule or fact as a string.

        Returns:
            True if successfully added, False otherwise.
        """
        ...

    def execute(self, callback: Callable[[Rule], bool]) -> int:
        """Execute the search engine with a callback for each inferred rule.

        Args:
            callback: Function called for each candidate rule.
                     Return False to continue, True to stop.

        Returns:
            The number of rules processed.
        """
        ...
