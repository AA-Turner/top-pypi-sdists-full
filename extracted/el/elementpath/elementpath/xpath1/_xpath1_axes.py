#
# Copyright (c), 2018-2021, SISSA (International School for Advanced Studies).
# All rights reserved.
# This file is distributed under the terms of the MIT License.
# See the file 'LICENSE' in the root directory of the present
# distribution, or http://opensource.org/licenses/MIT.
#
# @author Davide Brunato <brunato@sissa.it>
#
"""
XPath 1.0 implementation - part 4 (axes)
"""
from collections.abc import Iterator
from typing import cast

from elementpath.xpath_nodes import ChildNodeType, AttributeNode, ElementNode, \
    NamespaceNode, XPathNode, ParentNodeType
from elementpath.xpath_context import ContextType, ItemType, XPathSchemaContext
from elementpath.xpath_tokens import XPathAxis

from ._xpath1_functions import XPath1Parser


register = XPath1Parser.register
method = XPath1Parser.method
axis = XPath1Parser.axis


@method(register('@', lbp=80, rbp=80, label="attribute reference"))
def nud_attribute_reference(self: XPathAxis) -> XPathAxis:
    self.parser.expected_next(
        '*', '(name)', ':', '{', 'Q{', message="invalid attribute specification")
    self[:] = self.parser.expression(rbp=80),
    return self


@method('@')
@method(axis('attribute'))
def select_attribute_reference_or_axis(self: XPathAxis, context: ContextType = None) \
        -> Iterator[AttributeNode]:
    if context is None:
        raise self.missing_context()

    for _ in context.iter_attributes():
        yield from cast(Iterator[AttributeNode], self[0].select(context))


@method(axis('namespace'))
def select_namespace_axis(self: XPathAxis, context: ContextType = None) \
        -> Iterator[NamespaceNode]:
    if context is None:
        raise self.missing_context()
    elif isinstance(context, XPathSchemaContext):
        return  # deprecated for XP20+ and not needed for schema analysis
    elif isinstance(context.item, ElementNode):
        elem = context.item
        if self[0].symbol != 'namespace-node':
            name = self[0].value
        else:
            name = '*'

        for context.item in elem.namespace_nodes:
            if name == '*' or name == context.item.prefix:
                yield context.item


@method(axis('self'))
def select_self_axis(self: XPathAxis, context: ContextType = None) \
        -> Iterator[ItemType]:
    if context is None:
        raise self.missing_context()
    else:
        for _ in context.iter_self():
            yield from self[0].select(context)


@method(axis('child'))
def select_child_axis(self: XPathAxis, context: ContextType = None) \
        -> Iterator[ItemType]:
    if context is None:
        raise self.missing_context()
    else:
        for _ in context.iter_children_or_self():
            yield from self[0].select(context)


@method(axis('parent', reverse_axis=True))
def select_parent_axis(self: XPathAxis, context: ContextType = None) \
        -> Iterator[ParentNodeType]:
    if context is None:
        raise self.missing_context()
    else:
        for _ in context.iter_parent():
            yield from cast(Iterator[ParentNodeType], self[0].select(context))


@method(axis('following-sibling'))
@method(axis('preceding-sibling', reverse_axis=True))
def select_sibling_axes(self: XPathAxis, context: ContextType = None) \
        -> Iterator[ChildNodeType]:
    if context is None:
        raise self.missing_context()
    else:
        for _ in context.iter_siblings(axis=self.symbol):
            yield from cast(Iterator[ChildNodeType], self[0].select(context))


@method(axis('ancestor', reverse_axis=True))
@method(axis('ancestor-or-self', reverse_axis=True))
def select_ancestor_axes(self: XPathAxis, context: ContextType = None) \
        -> Iterator[ParentNodeType]:
    if context is None:
        raise self.missing_context()
    else:
        for _ in context.iter_ancestors(axis=self.symbol):
            yield from cast(Iterator[ParentNodeType], self[0].select(context))


@method(axis('descendant'))
@method(axis('descendant-or-self'))
def select_descendant_axes(self: XPathAxis, context: ContextType = None) \
        -> Iterator[XPathNode]:
    if context is None:
        raise self.missing_context()
    else:
        for _ in context.iter_descendants(axis=self.symbol):
            yield from cast(Iterator[XPathNode], self[0].select(context))


@method(axis('following'))
def select_following_axis(self: XPathAxis, context: ContextType = None) \
        -> Iterator[ChildNodeType]:
    if context is None:
        raise self.missing_context()
    else:
        for _ in context.iter_followings():
            yield from cast(Iterator[ChildNodeType], self[0].select(context))


@method(axis('preceding', reverse_axis=True))
def select_preceding_axis(self: XPathAxis, context: ContextType = None) \
        -> Iterator[ChildNodeType]:
    if context is None:
        raise self.missing_context()
    else:
        for _ in context.iter_preceding():
            yield from cast(Iterator[ChildNodeType], self[0].select(context))
