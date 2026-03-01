import ast

from wemake_python_styleguide.logic.nodes import get_parent


def unwrap_unary_node(node: ast.AST) -> ast.AST:
    """
    Returns a real unwrapped node from the unary wrapper.

    It recursively unwraps any level of unary operators.
    Returns the node itself if it is not wrapped in unary operator.
    """
    while True:
        if not isinstance(node, ast.UnaryOp):
            return node
        node = node.operand


def get_parent_ignoring_unary(node: ast.AST) -> ast.AST | None:
    """
    Returns real parent ignoring proxy unary parent level.

    What can go wrong?

    1. Number can be negative: ``x = -1``,
       so ``1`` has ``UnaryOp`` as parent, but should return ``Assign``
    2. Some values can be negated: ``x = --some``,
       so ``some`` has ``UnaryOp`` as parent, but should return ``Assign``

    """
    while True:
        parent = get_parent(node)
        if parent is None or not isinstance(parent, ast.UnaryOp):
            return parent
        node = parent


def count_consecutive_unary_operator(
    node: ast.AST,
    operator: type[ast.unaryop],
    counter: int = 0,
    max_counter: int = 0,
) -> int:
    """Counts the maximum number of consecutive identical unary operators."""
    parent = get_parent(node)
    if not isinstance(parent, ast.UnaryOp):
        return max(counter, max_counter)

    if isinstance(parent.op, operator):
        return count_consecutive_unary_operator(
            parent, operator, counter + 1, max_counter
        )
    if counter > max_counter:
        return count_consecutive_unary_operator(parent, operator, 0, counter)
    return count_consecutive_unary_operator(parent, operator, 0, max_counter)


def get_reduced_unary_operators(
    node: ast.AST,
    opchain: list[type[ast.unaryop]] | None = None,
) -> list[type[ast.unaryop]]:
    """Returns a sequence of significant unary operators."""
    if opchain is None:
        opchain = []

    parent = get_parent(node)
    if not isinstance(parent, ast.UnaryOp):
        return opchain

    if not isinstance(parent.op, ast.UAdd):
        lastop = opchain[-1] if opchain else None
        if lastop and isinstance(parent.op, lastop):
            opchain.pop()
        else:
            opchain.append(type(parent.op))

    return get_reduced_unary_operators(parent, opchain)
