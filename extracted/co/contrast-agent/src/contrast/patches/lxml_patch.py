# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import sys

from contrast_vendor.wrapt import CallableObjectProxy

from contrast.agent.assess.policy.preshift import Preshift
from contrast.agent.assess.policy.analysis import _analyze
from contrast.agent.policy import patch_manager, registry
from contrast.utils.decorators import fail_quietly
from contrast.utils.patch_utils import (
    build_and_apply_patch,
    unregister_module_patcher,
    wrap_and_watermark,
    register_module_patcher,
)


@fail_quietly("Failed to apply assess xpath-injection")
def apply_assess(location, self, retval, args, kwargs):
    patch_policy = registry.get_policy_by_name(location)
    if patch_policy is None:
        return

    preshift = Preshift(self, args, kwargs)
    _analyze(patch_policy, preshift, self, retval, (self,) + args, kwargs)


def apply_call(class_name, orig_func, self, args, kwargs):
    result = None
    try:
        result = orig_func(*args, **kwargs)
    finally:
        location = f"lxml.etree.{class_name}.__call__"
        apply_assess(location, self, result, args, kwargs)
    return result


class ContrastXPathEvaluatorProxy(CallableObjectProxy):
    """
    Proxy class that wraps instances returned by XPathEvaluator factory

    We instrument the relevant classes directly, but since the factory is implemented
    as a C extension, the instances that it returns are the original type instead of
    our replacement. In order to cover all of our bases, we need both the replacement
    subclass and a proxied class that we return from the instrumented factory.
    """

    def __call__(__cs_self, *args, **kwargs):
        self_obj = __cs_self.__wrapped__
        orig_func = __cs_self.__wrapped__.__call__
        return apply_call(
            self_obj.__class__.__name__, orig_func, self_obj, args, kwargs
        )


def create_instrumented_xpath_element_evaluator(XPathElementEvaluator):
    """
    Generate instrumented subclass of XPathElementEvaluator

    We can't simply declare this at module level since we can't guarantee that lxml
    will be installed. We need to wait until the import hook is fired to know whether
    it's safe to make a reference to the original type.
    """

    class ContrastXPathElementEvaluator(XPathElementEvaluator):
        def __call__(__cs_self, *args, **kwargs):
            orig_func = super().__call__
            return apply_call(
                XPathElementEvaluator.__name__, orig_func, __cs_self, args, kwargs
            )

    return ContrastXPathElementEvaluator


def create_instrumented_xpath_document_evaluator(x_path_document_evaluator):
    """
    Generate instrumented subclass of XPathDocumentEvaluator

    See docstring for create_instrumented_xpath_element_evaluator above.
    """

    class ContrastXPathDocumentEvaluator(x_path_document_evaluator):
        def __call__(__cs_self, *args, **kwargs):
            orig_func = super().__call__
            return apply_call(
                x_path_document_evaluator.__name__, orig_func, __cs_self, args, kwargs
            )

    return ContrastXPathDocumentEvaluator


def create_instrumented_xpath(x_path):
    """
    Generate instrumented subclass of XPath

    We can't simply declare this at module level since we can't guarantee that lxml
    will be installed. We need to wait until the import hook is fired to know whether
    it's safe to make a reference to the original type.
    """

    class ContrastXPath(x_path):
        def __init__(__cs_self, *args, **kwargs):
            try:
                super().__init__(*args, **kwargs)
            except TypeError:
                # See PYT-2364.
                # Calling inheritance in this *bad* way fixes a TypeError raised
                # from lxml.cssselect.CSSSelector.__init__ calling
                # etree.XPath.__init__(self, ...)
                # instead of using super()
                x_path.__init__(__cs_self, *args, **kwargs)
            finally:
                apply_assess("lxml.etree.XPath.__init__", __cs_self, None, args, kwargs)

    return ContrastXPath


def create_instrumented_xml_parser(etree_xml_parser_class):
    """
    Generate a subclass of etree.XMLParser. This subclass will replace etree.XMLParser.

    We need this in order to determine if a given parser is created with the attribute
    `resolve_entities=False`. The FROMSTRING trigger action needs to be able to
    know if the parser used by `etree.fromstring` will resolve entities or not.

    There is no way to determine if a parser is safe simply by inspecting an unmodified
    XMLParser instance, because the attribute we need to check is private (Cython
    private, so we -really- can't access it).
    """

    class ContrastXMLParser(etree_xml_parser_class):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # NOTE: this is not safe by default
            self.resolve_entities = kwargs.get("resolve_entities", True)

    return ContrastXMLParser


def build_x_path_eval_patch(orig_func, _):
    def x_path_evaluator(wrapped, instance, args, kwargs):
        """
        Instrumented version of XPathEvaluator factory
        """
        del instance

        evaluator = wrapped(*args, **kwargs)
        return ContrastXPathEvaluatorProxy(evaluator)

    return wrap_and_watermark(orig_func, x_path_evaluator)


def patch_etree(etree_module):
    build_and_apply_patch(etree_module, "XPathEvaluator", build_x_path_eval_patch)

    new_xpath = create_instrumented_xpath(etree_module.XPath)
    patch_manager.patch(etree_module, "XPath", new_xpath)

    new_element_evaluator = create_instrumented_xpath_element_evaluator(
        etree_module.XPathElementEvaluator
    )
    patch_manager.patch(etree_module, "XPathElementEvaluator", new_element_evaluator)

    new_document_evaluator = create_instrumented_xpath_document_evaluator(
        etree_module.XPathDocumentEvaluator
    )
    patch_manager.patch(etree_module, "XPathDocumentEvaluator", new_document_evaluator)

    new_xml_parser = create_instrumented_xml_parser(etree_module.XMLParser)
    patch_manager.patch(etree_module, "XMLParser", new_xml_parser)


MODULE_NAME = "lxml.etree"


def register_patches():
    register_module_patcher(patch_etree, MODULE_NAME)


def reverse_patches():
    unregister_module_patcher(MODULE_NAME)
    module = sys.modules.get(MODULE_NAME)
    if not module:
        return

    patch_manager.reverse_patches_by_owner(module)
