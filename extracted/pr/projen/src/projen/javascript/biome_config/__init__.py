from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

import typeguard
from importlib.metadata import version as _metadata_package_version
TYPEGUARD_MAJOR_VERSION = int(_metadata_package_version('typeguard').split('.')[0])

def check_type(argname: str, value: object, expected_type: typing.Any) -> typing.Any:
    if TYPEGUARD_MAJOR_VERSION <= 2:
        return typeguard.check_type(argname=argname, value=value, expected_type=expected_type) # type:ignore
    else:
        if isinstance(value, jsii._reference_map.InterfaceDynamicProxy): # pyright: ignore [reportAttributeAccessIssue]
           pass
        else:
            if TYPEGUARD_MAJOR_VERSION == 3:
                typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS # type:ignore
                typeguard.check_type(value=value, expected_type=expected_type) # type:ignore
            else:
                typeguard.check_type(value=value, expected_type=expected_type, collection_check_strategy=typeguard.CollectionCheckStrategy.ALL_ITEMS) # type:ignore

from ..._jsii import *


@jsii.interface(jsii_type="projen.javascript.biome_config.IA11y")
class IA11y(typing_extensions.Protocol):
    '''(experimental) A list of rules that belong to this group.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="all")
    def all(self) -> typing.Optional[builtins.bool]:
        '''(experimental) It enables ALL rules for this group.

        :stability: experimental
        '''
        ...

    @all.setter
    def all(self, value: typing.Optional[builtins.bool]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noAccessKey")
    def no_access_key(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Enforce that the accessKey attribute is not used on any HTML element.

        :stability: experimental
        '''
        ...

    @no_access_key.setter
    def no_access_key(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noAriaHiddenOnFocusable")
    def no_aria_hidden_on_focusable(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Enforce that aria-hidden="true" is not set on focusable elements.

        :stability: experimental
        '''
        ...

    @no_aria_hidden_on_focusable.setter
    def no_aria_hidden_on_focusable(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noAriaUnsupportedElements")
    def no_aria_unsupported_elements(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Enforce that elements that do not support ARIA roles, states, and properties do not have those attributes.

        :stability: experimental
        '''
        ...

    @no_aria_unsupported_elements.setter
    def no_aria_unsupported_elements(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noAutofocus")
    def no_autofocus(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Enforce that autoFocus prop is not used on elements.

        :stability: experimental
        '''
        ...

    @no_autofocus.setter
    def no_autofocus(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noBlankTarget")
    def no_blank_target(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithAllowDomainOptions"]]:
        '''(experimental) Disallow target="_blank" attribute without rel="noreferrer".

        :stability: experimental
        '''
        ...

    @no_blank_target.setter
    def no_blank_target(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithAllowDomainOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noDistractingElements")
    def no_distracting_elements(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Enforces that no distracting elements are used.

        :stability: experimental
        '''
        ...

    @no_distracting_elements.setter
    def no_distracting_elements(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noHeaderScope")
    def no_header_scope(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) The scope prop should be used only on <th> elements.

        :stability: experimental
        '''
        ...

    @no_header_scope.setter
    def no_header_scope(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noInteractiveElementToNoninteractiveRole")
    def no_interactive_element_to_noninteractive_role(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Enforce that non-interactive ARIA roles are not assigned to interactive HTML elements.

        :stability: experimental
        '''
        ...

    @no_interactive_element_to_noninteractive_role.setter
    def no_interactive_element_to_noninteractive_role(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noLabelWithoutControl")
    def no_label_without_control(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoLabelWithoutControlOptions"]]:
        '''(experimental) Enforce that a label element or component has a text label and an associated input.

        :stability: experimental
        '''
        ...

    @no_label_without_control.setter
    def no_label_without_control(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoLabelWithoutControlOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noNoninteractiveElementToInteractiveRole")
    def no_noninteractive_element_to_interactive_role(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Enforce that interactive ARIA roles are not assigned to non-interactive HTML elements.

        :stability: experimental
        '''
        ...

    @no_noninteractive_element_to_interactive_role.setter
    def no_noninteractive_element_to_interactive_role(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noNoninteractiveTabindex")
    def no_noninteractive_tabindex(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Enforce that tabIndex is not assigned to non-interactive HTML elements.

        :stability: experimental
        '''
        ...

    @no_noninteractive_tabindex.setter
    def no_noninteractive_tabindex(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noPositiveTabindex")
    def no_positive_tabindex(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Prevent the usage of positive integers on tabIndex property.

        :stability: experimental
        '''
        ...

    @no_positive_tabindex.setter
    def no_positive_tabindex(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noRedundantAlt")
    def no_redundant_alt(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Enforce img alt prop does not contain the word "image", "picture", or "photo".

        :stability: experimental
        '''
        ...

    @no_redundant_alt.setter
    def no_redundant_alt(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noRedundantRoles")
    def no_redundant_roles(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Enforce explicit role property is not the same as implicit/default role property on an element.

        :stability: experimental
        '''
        ...

    @no_redundant_roles.setter
    def no_redundant_roles(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noSvgWithoutTitle")
    def no_svg_without_title(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Enforces the usage of the title element for the svg element.

        :stability: experimental
        '''
        ...

    @no_svg_without_title.setter
    def no_svg_without_title(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="recommended")
    def recommended(self) -> typing.Optional[builtins.bool]:
        '''(experimental) It enables the recommended rules for this group.

        :stability: experimental
        '''
        ...

    @recommended.setter
    def recommended(self, value: typing.Optional[builtins.bool]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useAltText")
    def use_alt_text(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Enforce that all elements that require alternative text have meaningful information to relay back to the end user.

        :stability: experimental
        '''
        ...

    @use_alt_text.setter
    def use_alt_text(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useAnchorContent")
    def use_anchor_content(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Enforce that anchors have content and that the content is accessible to screen readers.

        :stability: experimental
        '''
        ...

    @use_anchor_content.setter
    def use_anchor_content(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useAriaActivedescendantWithTabindex")
    def use_aria_activedescendant_with_tabindex(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Enforce that tabIndex is assigned to non-interactive HTML elements with aria-activedescendant.

        :stability: experimental
        '''
        ...

    @use_aria_activedescendant_with_tabindex.setter
    def use_aria_activedescendant_with_tabindex(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useAriaPropsForRole")
    def use_aria_props_for_role(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Enforce that elements with ARIA roles must have all required ARIA attributes for that role.

        :stability: experimental
        '''
        ...

    @use_aria_props_for_role.setter
    def use_aria_props_for_role(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useButtonType")
    def use_button_type(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Enforces the usage of the attribute type for the element button.

        :stability: experimental
        '''
        ...

    @use_button_type.setter
    def use_button_type(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useFocusableInteractive")
    def use_focusable_interactive(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Elements with an interactive role and interaction handlers must be focusable.

        :stability: experimental
        '''
        ...

    @use_focusable_interactive.setter
    def use_focusable_interactive(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useGenericFontNames")
    def use_generic_font_names(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow a missing generic family keyword within font families.

        :stability: experimental
        '''
        ...

    @use_generic_font_names.setter
    def use_generic_font_names(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useHeadingContent")
    def use_heading_content(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Enforce that heading elements (h1, h2, etc.) have content and that the content is accessible to screen readers. Accessible means that it is not hidden using the aria-hidden prop.

        :stability: experimental
        '''
        ...

    @use_heading_content.setter
    def use_heading_content(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useHtmlLang")
    def use_html_lang(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Enforce that html element has lang attribute.

        :stability: experimental
        '''
        ...

    @use_html_lang.setter
    def use_html_lang(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useIframeTitle")
    def use_iframe_title(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Enforces the usage of the attribute title for the element iframe.

        :stability: experimental
        '''
        ...

    @use_iframe_title.setter
    def use_iframe_title(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useKeyWithClickEvents")
    def use_key_with_click_events(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Enforce onClick is accompanied by at least one of the following: onKeyUp, onKeyDown, onKeyPress.

        :stability: experimental
        '''
        ...

    @use_key_with_click_events.setter
    def use_key_with_click_events(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useKeyWithMouseEvents")
    def use_key_with_mouse_events(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Enforce onMouseOver / onMouseOut are accompanied by onFocus / onBlur.

        :stability: experimental
        '''
        ...

    @use_key_with_mouse_events.setter
    def use_key_with_mouse_events(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useMediaCaption")
    def use_media_caption(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Enforces that audio and video elements must have a track for captions.

        :stability: experimental
        '''
        ...

    @use_media_caption.setter
    def use_media_caption(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useSemanticElements")
    def use_semantic_elements(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) It detects the use of role attributes in JSX elements and suggests using semantic elements instead.

        :stability: experimental
        '''
        ...

    @use_semantic_elements.setter
    def use_semantic_elements(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useValidAnchor")
    def use_valid_anchor(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Enforce that all anchors are valid, and they are navigable elements.

        :stability: experimental
        '''
        ...

    @use_valid_anchor.setter
    def use_valid_anchor(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useValidAriaProps")
    def use_valid_aria_props(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Ensures that ARIA properties aria-* are all valid.

        :stability: experimental
        '''
        ...

    @use_valid_aria_props.setter
    def use_valid_aria_props(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useValidAriaRole")
    def use_valid_aria_role(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithValidAriaRoleOptions"]]:
        '''(experimental) Elements with ARIA roles must use a valid, non-abstract ARIA role.

        :stability: experimental
        '''
        ...

    @use_valid_aria_role.setter
    def use_valid_aria_role(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithValidAriaRoleOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useValidAriaValues")
    def use_valid_aria_values(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Enforce that ARIA state and property values are valid.

        :stability: experimental
        '''
        ...

    @use_valid_aria_values.setter
    def use_valid_aria_values(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useValidLang")
    def use_valid_lang(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Ensure that the attribute passed to the lang attribute is a correct ISO language and/or country.

        :stability: experimental
        '''
        ...

    @use_valid_lang.setter
    def use_valid_lang(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...


class _IA11yProxy:
    '''(experimental) A list of rules that belong to this group.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.IA11y"

    @builtins.property
    @jsii.member(jsii_name="all")
    def all(self) -> typing.Optional[builtins.bool]:
        '''(experimental) It enables ALL rules for this group.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "all"))

    @all.setter
    def all(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__badd0e51dbf93a35ab5ac2799727503b1860ff7535908d55669e22bf7f9e8930)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "all", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noAccessKey")
    def no_access_key(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Enforce that the accessKey attribute is not used on any HTML element.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]], jsii.get(self, "noAccessKey"))

    @no_access_key.setter
    def no_access_key(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14325cc0c0f6d6714b29a964e2eaaa788931706a7b649effa7be33d156f5bf23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noAccessKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noAriaHiddenOnFocusable")
    def no_aria_hidden_on_focusable(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Enforce that aria-hidden="true" is not set on focusable elements.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]], jsii.get(self, "noAriaHiddenOnFocusable"))

    @no_aria_hidden_on_focusable.setter
    def no_aria_hidden_on_focusable(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__061886d01ca59a946c6cf6b28fc22bcba9d82795c0cac570978cc470187182e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noAriaHiddenOnFocusable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noAriaUnsupportedElements")
    def no_aria_unsupported_elements(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Enforce that elements that do not support ARIA roles, states, and properties do not have those attributes.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]], jsii.get(self, "noAriaUnsupportedElements"))

    @no_aria_unsupported_elements.setter
    def no_aria_unsupported_elements(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da101e3e53bd5c4c2bf4809333ad263149575cef80d5c3ce0902ebc80cc710c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noAriaUnsupportedElements", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noAutofocus")
    def no_autofocus(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Enforce that autoFocus prop is not used on elements.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]], jsii.get(self, "noAutofocus"))

    @no_autofocus.setter
    def no_autofocus(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e949f9a7943b853e59b5d827d16a11ee2d15624f19744abd42ed6cca7fe5df3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noAutofocus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noBlankTarget")
    def no_blank_target(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithAllowDomainOptions"]]:
        '''(experimental) Disallow target="_blank" attribute without rel="noreferrer".

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithAllowDomainOptions"]], jsii.get(self, "noBlankTarget"))

    @no_blank_target.setter
    def no_blank_target(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithAllowDomainOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24d501db6193e9146a62a7650ae4dd49d3cfa3b7d9be9ad6d6f07af4b009d883)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noBlankTarget", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noDistractingElements")
    def no_distracting_elements(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Enforces that no distracting elements are used.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]], jsii.get(self, "noDistractingElements"))

    @no_distracting_elements.setter
    def no_distracting_elements(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bedd0f823335951fa5b71166448bb1558408480fafa30ca579254f0f177f1b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noDistractingElements", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noHeaderScope")
    def no_header_scope(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) The scope prop should be used only on <th> elements.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]], jsii.get(self, "noHeaderScope"))

    @no_header_scope.setter
    def no_header_scope(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3ee003c13279c1d9433519f1560be0f0a582af3e9744ef2988f0b31e334c5bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noHeaderScope", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noInteractiveElementToNoninteractiveRole")
    def no_interactive_element_to_noninteractive_role(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Enforce that non-interactive ARIA roles are not assigned to interactive HTML elements.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]], jsii.get(self, "noInteractiveElementToNoninteractiveRole"))

    @no_interactive_element_to_noninteractive_role.setter
    def no_interactive_element_to_noninteractive_role(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d3565a1863735e0d6d42521ab0700dcee8f51a7f232a3d53d9f82d20e58d0ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noInteractiveElementToNoninteractiveRole", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noLabelWithoutControl")
    def no_label_without_control(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoLabelWithoutControlOptions"]]:
        '''(experimental) Enforce that a label element or component has a text label and an associated input.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoLabelWithoutControlOptions"]], jsii.get(self, "noLabelWithoutControl"))

    @no_label_without_control.setter
    def no_label_without_control(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoLabelWithoutControlOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff0335d183fe2accf83547cb02ee7ef359f7e3ad57b6a60724d3bfd18d1f563a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noLabelWithoutControl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noNoninteractiveElementToInteractiveRole")
    def no_noninteractive_element_to_interactive_role(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Enforce that interactive ARIA roles are not assigned to non-interactive HTML elements.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]], jsii.get(self, "noNoninteractiveElementToInteractiveRole"))

    @no_noninteractive_element_to_interactive_role.setter
    def no_noninteractive_element_to_interactive_role(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a34f454613118b49849da4a32dc57a4eb13e722cf205417b9956d947ce158a10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noNoninteractiveElementToInteractiveRole", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noNoninteractiveTabindex")
    def no_noninteractive_tabindex(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Enforce that tabIndex is not assigned to non-interactive HTML elements.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]], jsii.get(self, "noNoninteractiveTabindex"))

    @no_noninteractive_tabindex.setter
    def no_noninteractive_tabindex(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__207c6c55fe512ab828ea3b4a488b4248792ace501e98d2ea8cbc95d4bde8eca4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noNoninteractiveTabindex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noPositiveTabindex")
    def no_positive_tabindex(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Prevent the usage of positive integers on tabIndex property.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]], jsii.get(self, "noPositiveTabindex"))

    @no_positive_tabindex.setter
    def no_positive_tabindex(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc9d6b18e8e360d8f2117ba10f2b50f59c72449599b4b94270235b690e666ac0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noPositiveTabindex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noRedundantAlt")
    def no_redundant_alt(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Enforce img alt prop does not contain the word "image", "picture", or "photo".

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "noRedundantAlt"))

    @no_redundant_alt.setter
    def no_redundant_alt(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f39142081ca04b6cf2dda83461d68fa7ec1e646044165ad8f8031451478118a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noRedundantAlt", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noRedundantRoles")
    def no_redundant_roles(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Enforce explicit role property is not the same as implicit/default role property on an element.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]], jsii.get(self, "noRedundantRoles"))

    @no_redundant_roles.setter
    def no_redundant_roles(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5815be222cffe8cb14379a35232c28adba7fbb31051392c02fe352aff1cfb686)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noRedundantRoles", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noSvgWithoutTitle")
    def no_svg_without_title(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Enforces the usage of the title element for the svg element.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "noSvgWithoutTitle"))

    @no_svg_without_title.setter
    def no_svg_without_title(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8d0f1756afc844438cc5cce37384f983f9c60a7301d81e45a95b49a78b9dee9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noSvgWithoutTitle", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recommended")
    def recommended(self) -> typing.Optional[builtins.bool]:
        '''(experimental) It enables the recommended rules for this group.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "recommended"))

    @recommended.setter
    def recommended(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25f6269b6b2dceb5b14d206301614fcad8ffc67fbe040dcbe4326a40ddcf69d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recommended", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useAltText")
    def use_alt_text(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Enforce that all elements that require alternative text have meaningful information to relay back to the end user.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "useAltText"))

    @use_alt_text.setter
    def use_alt_text(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5f54a04a64674c2cd5d536d1f50056f6094b9277e9edc723cf5a84eb6dddbc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useAltText", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useAnchorContent")
    def use_anchor_content(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Enforce that anchors have content and that the content is accessible to screen readers.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]], jsii.get(self, "useAnchorContent"))

    @use_anchor_content.setter
    def use_anchor_content(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e5b6769c1a6575d4dc68343057aaf2b1ec0ed7e658f3b5a8c41a04c756b80dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useAnchorContent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useAriaActivedescendantWithTabindex")
    def use_aria_activedescendant_with_tabindex(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Enforce that tabIndex is assigned to non-interactive HTML elements with aria-activedescendant.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]], jsii.get(self, "useAriaActivedescendantWithTabindex"))

    @use_aria_activedescendant_with_tabindex.setter
    def use_aria_activedescendant_with_tabindex(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffe5d8a70d06b3ca42730f78efae5c1d666d322c2239c6b66969ef9791633ede)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useAriaActivedescendantWithTabindex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useAriaPropsForRole")
    def use_aria_props_for_role(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Enforce that elements with ARIA roles must have all required ARIA attributes for that role.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "useAriaPropsForRole"))

    @use_aria_props_for_role.setter
    def use_aria_props_for_role(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a780931a71bdc977a8560b015ba95463cd2074e68bf35fe8824608ce4d8d0874)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useAriaPropsForRole", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useButtonType")
    def use_button_type(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Enforces the usage of the attribute type for the element button.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "useButtonType"))

    @use_button_type.setter
    def use_button_type(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c30b3e7cd99762f7a234f66dbf1031156692943acf0f78c6ecd29cd0f4a531c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useButtonType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useFocusableInteractive")
    def use_focusable_interactive(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Elements with an interactive role and interaction handlers must be focusable.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "useFocusableInteractive"))

    @use_focusable_interactive.setter
    def use_focusable_interactive(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad76142a33de27df66b11df77653ea575209aa20090d9c31910df11a15fd665b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useFocusableInteractive", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useGenericFontNames")
    def use_generic_font_names(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow a missing generic family keyword within font families.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "useGenericFontNames"))

    @use_generic_font_names.setter
    def use_generic_font_names(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__802791d714df1717098027e8c1b74cbc4a0ce31838a80b05a9094b37eef81697)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useGenericFontNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useHeadingContent")
    def use_heading_content(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Enforce that heading elements (h1, h2, etc.) have content and that the content is accessible to screen readers. Accessible means that it is not hidden using the aria-hidden prop.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "useHeadingContent"))

    @use_heading_content.setter
    def use_heading_content(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d08e03b5305db1d1603edf6496435905357608066008d4f93dfa9040e9d3a162)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useHeadingContent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useHtmlLang")
    def use_html_lang(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Enforce that html element has lang attribute.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "useHtmlLang"))

    @use_html_lang.setter
    def use_html_lang(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bba312ea093a85fcd23cfb54f259d00507c55482f5b63f8d1431baf02c101467)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useHtmlLang", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useIframeTitle")
    def use_iframe_title(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Enforces the usage of the attribute title for the element iframe.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "useIframeTitle"))

    @use_iframe_title.setter
    def use_iframe_title(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c73f85d0867aa8ade9a55d9c38cc9a0474f8a8c4253eb9b2e647440b6abb794c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useIframeTitle", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useKeyWithClickEvents")
    def use_key_with_click_events(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Enforce onClick is accompanied by at least one of the following: onKeyUp, onKeyDown, onKeyPress.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "useKeyWithClickEvents"))

    @use_key_with_click_events.setter
    def use_key_with_click_events(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e14ec9fe6539ab57f54d77e106a80fbf0fcee37a71a5af2ecaa97563db1d2112)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useKeyWithClickEvents", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useKeyWithMouseEvents")
    def use_key_with_mouse_events(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Enforce onMouseOver / onMouseOut are accompanied by onFocus / onBlur.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "useKeyWithMouseEvents"))

    @use_key_with_mouse_events.setter
    def use_key_with_mouse_events(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d21718dec8ae4b3a898c8709014c7e31f138c31569f271004f3cf4c54927623a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useKeyWithMouseEvents", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useMediaCaption")
    def use_media_caption(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Enforces that audio and video elements must have a track for captions.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "useMediaCaption"))

    @use_media_caption.setter
    def use_media_caption(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__987aa34178662376da76a1aef3568457e91259b6ff95f286136ffb1ccd2332e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useMediaCaption", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useSemanticElements")
    def use_semantic_elements(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) It detects the use of role attributes in JSX elements and suggests using semantic elements instead.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "useSemanticElements"))

    @use_semantic_elements.setter
    def use_semantic_elements(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__912323bf4fb8d4010cfb94def3b8043dc6d5f231d2ae79b8d2052ec2935a1ec4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useSemanticElements", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useValidAnchor")
    def use_valid_anchor(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Enforce that all anchors are valid, and they are navigable elements.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "useValidAnchor"))

    @use_valid_anchor.setter
    def use_valid_anchor(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec4bbf3ebd038d4d14b1d542988b1bf72a2efc9565669c9dda404128a6720cf3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useValidAnchor", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useValidAriaProps")
    def use_valid_aria_props(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Ensures that ARIA properties aria-* are all valid.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]], jsii.get(self, "useValidAriaProps"))

    @use_valid_aria_props.setter
    def use_valid_aria_props(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b87e8452832653685744a282cfc67f9716a3b402c9f6218609e9d75646d509a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useValidAriaProps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useValidAriaRole")
    def use_valid_aria_role(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithValidAriaRoleOptions"]]:
        '''(experimental) Elements with ARIA roles must use a valid, non-abstract ARIA role.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithValidAriaRoleOptions"]], jsii.get(self, "useValidAriaRole"))

    @use_valid_aria_role.setter
    def use_valid_aria_role(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithValidAriaRoleOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6af18b773668a3a5c1a92becfe381333a2422cc2ae1061ff1482b1faa741421)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useValidAriaRole", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useValidAriaValues")
    def use_valid_aria_values(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Enforce that ARIA state and property values are valid.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "useValidAriaValues"))

    @use_valid_aria_values.setter
    def use_valid_aria_values(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfd213ffe79ee2a02b64001a7daa35f7af0d84203eabddd1a177973fd0c5bb3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useValidAriaValues", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useValidLang")
    def use_valid_lang(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Ensure that the attribute passed to the lang attribute is a correct ISO language and/or country.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "useValidLang"))

    @use_valid_lang.setter
    def use_valid_lang(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac3b29c3dfebd21aaaf1c18856f70485f15f4cb387baf4f49fca690a9c368156)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useValidLang", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IA11y).__jsii_proxy_class__ = lambda : _IA11yProxy


@jsii.interface(jsii_type="projen.javascript.biome_config.IActions")
class IActions(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> typing.Optional["ISource"]:
        '''
        :stability: experimental
        '''
        ...

    @source.setter
    def source(self, value: typing.Optional["ISource"]) -> None:
        ...


class _IActionsProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.IActions"

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> typing.Optional["ISource"]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional["ISource"], jsii.get(self, "source"))

    @source.setter
    def source(self, value: typing.Optional["ISource"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7885b267242ab7487e26e20dc5ccbbace5542c71cc20540d689161aeb01669e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IActions).__jsii_proxy_class__ = lambda : _IActionsProxy


@jsii.interface(jsii_type="projen.javascript.biome_config.IAllowDomainOptions")
class IAllowDomainOptions(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="allowDomains")
    def allow_domains(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) List of domains to allow ``target="_blank"`` without ``rel="noreferrer"``.

        :stability: experimental
        '''
        ...

    @allow_domains.setter
    def allow_domains(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        ...


class _IAllowDomainOptionsProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.IAllowDomainOptions"

    @builtins.property
    @jsii.member(jsii_name="allowDomains")
    def allow_domains(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) List of domains to allow ``target="_blank"`` without ``rel="noreferrer"``.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowDomains"))

    @allow_domains.setter
    def allow_domains(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f9f37ceb9b03ed691283ac31b5562272a16c3ac67044d92300f67175e583fde)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowDomains", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IAllowDomainOptions).__jsii_proxy_class__ = lambda : _IAllowDomainOptionsProxy


@jsii.interface(jsii_type="projen.javascript.biome_config.IAssistsConfiguration")
class IAssistsConfiguration(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="actions")
    def actions(self) -> typing.Optional[IActions]:
        '''(experimental) Whether Biome should fail in CLI if the assists were not applied to the code.

        :stability: experimental
        '''
        ...

    @actions.setter
    def actions(self, value: typing.Optional[IActions]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether Biome should enable assists via LSP.

        :stability: experimental
        '''
        ...

    @enabled.setter
    def enabled(self, value: typing.Optional[builtins.bool]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="ignore")
    def ignore(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of Unix shell style patterns.

        The formatter will ignore files/folders that will match these patterns.

        :stability: experimental
        '''
        ...

    @ignore.setter
    def ignore(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="include")
    def include(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of Unix shell style patterns.

        The formatter will include files/folders that will match these patterns.

        :stability: experimental
        '''
        ...

    @include.setter
    def include(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        ...


class _IAssistsConfigurationProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.IAssistsConfiguration"

    @builtins.property
    @jsii.member(jsii_name="actions")
    def actions(self) -> typing.Optional[IActions]:
        '''(experimental) Whether Biome should fail in CLI if the assists were not applied to the code.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[IActions], jsii.get(self, "actions"))

    @actions.setter
    def actions(self, value: typing.Optional[IActions]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d5d19d5827687684b03d2d0ad966c342b5c2f8d8d0211bdad14038c74d9378a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether Biome should enable assists via LSP.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c10ca9a804f308fc75cca8068b3b767225f4f025aa343064b7f9ec5e9aef0a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ignore")
    def ignore(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of Unix shell style patterns.

        The formatter will ignore files/folders that will match these patterns.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "ignore"))

    @ignore.setter
    def ignore(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__663c56ce895f236cb37ecc605f09dc983b9c83aee27413c477dbe22cdb166cd5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignore", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="include")
    def include(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of Unix shell style patterns.

        The formatter will include files/folders that will match these patterns.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "include"))

    @include.setter
    def include(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a80e8d8404a7a73c83041947870a887bc8696c97ec71a58466cb4abbbdafe27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "include", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IAssistsConfiguration).__jsii_proxy_class__ = lambda : _IAssistsConfigurationProxy


@jsii.interface(jsii_type="projen.javascript.biome_config.IComplexity")
class IComplexity(typing_extensions.Protocol):
    '''(experimental) A list of rules that belong to this group.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="all")
    def all(self) -> typing.Optional[builtins.bool]:
        '''(experimental) It enables ALL rules for this group.

        :stability: experimental
        '''
        ...

    @all.setter
    def all(self, value: typing.Optional[builtins.bool]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noBannedTypes")
    def no_banned_types(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Disallow primitive type aliases and misleading types.

        :stability: experimental
        '''
        ...

    @no_banned_types.setter
    def no_banned_types(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noEmptyTypeParameters")
    def no_empty_type_parameters(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow empty type parameters in type aliases and interfaces.

        :stability: experimental
        '''
        ...

    @no_empty_type_parameters.setter
    def no_empty_type_parameters(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noExcessiveCognitiveComplexity")
    def no_excessive_cognitive_complexity(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithComplexityOptions"]]:
        '''(experimental) Disallow functions that exceed a given Cognitive Complexity score.

        :stability: experimental
        '''
        ...

    @no_excessive_cognitive_complexity.setter
    def no_excessive_cognitive_complexity(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithComplexityOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noExcessiveNestedTestSuites")
    def no_excessive_nested_test_suites(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) This rule enforces a maximum depth to nested describe() in test files.

        :stability: experimental
        '''
        ...

    @no_excessive_nested_test_suites.setter
    def no_excessive_nested_test_suites(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noExtraBooleanCast")
    def no_extra_boolean_cast(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Disallow unnecessary boolean casts.

        :stability: experimental
        '''
        ...

    @no_extra_boolean_cast.setter
    def no_extra_boolean_cast(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noForEach")
    def no_for_each(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Prefer for...of statement instead of Array.forEach.

        :stability: experimental
        '''
        ...

    @no_for_each.setter
    def no_for_each(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noMultipleSpacesInRegularExpressionLiterals")
    def no_multiple_spaces_in_regular_expression_literals(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Disallow unclear usage of consecutive space characters in regular expression literals.

        :stability: experimental
        '''
        ...

    @no_multiple_spaces_in_regular_expression_literals.setter
    def no_multiple_spaces_in_regular_expression_literals(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noStaticOnlyClass")
    def no_static_only_class(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) This rule reports when a class has no non-static members, such as for a class used exclusively as a static namespace.

        :stability: experimental
        '''
        ...

    @no_static_only_class.setter
    def no_static_only_class(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noThisInStatic")
    def no_this_in_static(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Disallow this and super in static contexts.

        :stability: experimental
        '''
        ...

    @no_this_in_static.setter
    def no_this_in_static(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noUselessCatch")
    def no_useless_catch(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Disallow unnecessary catch clauses.

        :stability: experimental
        '''
        ...

    @no_useless_catch.setter
    def no_useless_catch(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noUselessConstructor")
    def no_useless_constructor(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Disallow unnecessary constructors.

        :stability: experimental
        '''
        ...

    @no_useless_constructor.setter
    def no_useless_constructor(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noUselessEmptyExport")
    def no_useless_empty_export(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Disallow empty exports that don't change anything in a module file.

        :stability: experimental
        '''
        ...

    @no_useless_empty_export.setter
    def no_useless_empty_export(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noUselessFragments")
    def no_useless_fragments(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Disallow unnecessary fragments.

        :stability: experimental
        '''
        ...

    @no_useless_fragments.setter
    def no_useless_fragments(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noUselessLabel")
    def no_useless_label(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Disallow unnecessary labels.

        :stability: experimental
        '''
        ...

    @no_useless_label.setter
    def no_useless_label(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noUselessLoneBlockStatements")
    def no_useless_lone_block_statements(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Disallow unnecessary nested block statements.

        :stability: experimental
        '''
        ...

    @no_useless_lone_block_statements.setter
    def no_useless_lone_block_statements(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noUselessRename")
    def no_useless_rename(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Disallow renaming import, export, and destructured assignments to the same name.

        :stability: experimental
        '''
        ...

    @no_useless_rename.setter
    def no_useless_rename(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noUselessStringConcat")
    def no_useless_string_concat(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Disallow unnecessary concatenation of string or template literals.

        :stability: experimental
        '''
        ...

    @no_useless_string_concat.setter
    def no_useless_string_concat(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noUselessSwitchCase")
    def no_useless_switch_case(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Disallow useless case in switch statements.

        :stability: experimental
        '''
        ...

    @no_useless_switch_case.setter
    def no_useless_switch_case(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noUselessTernary")
    def no_useless_ternary(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Disallow ternary operators when simpler alternatives exist.

        :stability: experimental
        '''
        ...

    @no_useless_ternary.setter
    def no_useless_ternary(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noUselessThisAlias")
    def no_useless_this_alias(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Disallow useless this aliasing.

        :stability: experimental
        '''
        ...

    @no_useless_this_alias.setter
    def no_useless_this_alias(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noUselessTypeConstraint")
    def no_useless_type_constraint(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Disallow using any or unknown as type constraint.

        :stability: experimental
        '''
        ...

    @no_useless_type_constraint.setter
    def no_useless_type_constraint(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noUselessUndefinedInitialization")
    def no_useless_undefined_initialization(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Disallow initializing variables to undefined.

        :stability: experimental
        '''
        ...

    @no_useless_undefined_initialization.setter
    def no_useless_undefined_initialization(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noVoid")
    def no_void(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow the use of void operators, which is not a familiar operator.

        :stability: experimental
        '''
        ...

    @no_void.setter
    def no_void(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noWith")
    def no_with(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow with statements in non-strict contexts.

        :stability: experimental
        '''
        ...

    @no_with.setter
    def no_with(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="recommended")
    def recommended(self) -> typing.Optional[builtins.bool]:
        '''(experimental) It enables the recommended rules for this group.

        :stability: experimental
        '''
        ...

    @recommended.setter
    def recommended(self, value: typing.Optional[builtins.bool]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useArrowFunction")
    def use_arrow_function(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Use arrow functions over function expressions.

        :stability: experimental
        '''
        ...

    @use_arrow_function.setter
    def use_arrow_function(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useDateNow")
    def use_date_now(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Use Date.now() to get the number of milliseconds since the Unix Epoch.

        :stability: experimental
        '''
        ...

    @use_date_now.setter
    def use_date_now(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useFlatMap")
    def use_flat_map(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Promotes the use of .flatMap() when map().flat() are used together.

        :stability: experimental
        '''
        ...

    @use_flat_map.setter
    def use_flat_map(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useLiteralKeys")
    def use_literal_keys(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Enforce the usage of a literal access to properties over computed property access.

        :stability: experimental
        '''
        ...

    @use_literal_keys.setter
    def use_literal_keys(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useOptionalChain")
    def use_optional_chain(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Enforce using concise optional chain instead of chained logical expressions.

        :stability: experimental
        '''
        ...

    @use_optional_chain.setter
    def use_optional_chain(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useRegexLiterals")
    def use_regex_literals(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Enforce the use of the regular expression literals instead of the RegExp constructor if possible.

        :stability: experimental
        '''
        ...

    @use_regex_literals.setter
    def use_regex_literals(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useSimpleNumberKeys")
    def use_simple_number_keys(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Disallow number literal object member names which are not base10 or uses underscore as separator.

        :stability: experimental
        '''
        ...

    @use_simple_number_keys.setter
    def use_simple_number_keys(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useSimplifiedLogicExpression")
    def use_simplified_logic_expression(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Discard redundant terms from logical expressions.

        :stability: experimental
        '''
        ...

    @use_simplified_logic_expression.setter
    def use_simplified_logic_expression(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        ...


class _IComplexityProxy:
    '''(experimental) A list of rules that belong to this group.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.IComplexity"

    @builtins.property
    @jsii.member(jsii_name="all")
    def all(self) -> typing.Optional[builtins.bool]:
        '''(experimental) It enables ALL rules for this group.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "all"))

    @all.setter
    def all(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81dfef0a7b76c4b904e218b5571e951565908bb26a6f05e2f24aced76abb928e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "all", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noBannedTypes")
    def no_banned_types(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Disallow primitive type aliases and misleading types.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]], jsii.get(self, "noBannedTypes"))

    @no_banned_types.setter
    def no_banned_types(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac576a2aa458a1f40a9ee1ff3ffd44005031cfa009832850596ba32e418e7bb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noBannedTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noEmptyTypeParameters")
    def no_empty_type_parameters(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow empty type parameters in type aliases and interfaces.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "noEmptyTypeParameters"))

    @no_empty_type_parameters.setter
    def no_empty_type_parameters(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94bcb3eca282dc0819b1b89a8208e80dc2a18f8faeb7732550393f5325101100)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noEmptyTypeParameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noExcessiveCognitiveComplexity")
    def no_excessive_cognitive_complexity(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithComplexityOptions"]]:
        '''(experimental) Disallow functions that exceed a given Cognitive Complexity score.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithComplexityOptions"]], jsii.get(self, "noExcessiveCognitiveComplexity"))

    @no_excessive_cognitive_complexity.setter
    def no_excessive_cognitive_complexity(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithComplexityOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b070a07de17f2ecdc567dad6f4eb140ad07153bfe9bf59ad541f988a4697fc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noExcessiveCognitiveComplexity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noExcessiveNestedTestSuites")
    def no_excessive_nested_test_suites(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) This rule enforces a maximum depth to nested describe() in test files.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "noExcessiveNestedTestSuites"))

    @no_excessive_nested_test_suites.setter
    def no_excessive_nested_test_suites(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77c9921099705c4f0fc7d3b7e042fa4a250061c7729f5c2754ed00f530926531)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noExcessiveNestedTestSuites", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noExtraBooleanCast")
    def no_extra_boolean_cast(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Disallow unnecessary boolean casts.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]], jsii.get(self, "noExtraBooleanCast"))

    @no_extra_boolean_cast.setter
    def no_extra_boolean_cast(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f7cb6920800155702b9b29318f733f20beb02c96450897bbcea97cf0b4d93ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noExtraBooleanCast", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noForEach")
    def no_for_each(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Prefer for...of statement instead of Array.forEach.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "noForEach"))

    @no_for_each.setter
    def no_for_each(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09e155514481252a199e15d99de7ade8733b3ad223a9cb6916243dc0dfd38f05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noForEach", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noMultipleSpacesInRegularExpressionLiterals")
    def no_multiple_spaces_in_regular_expression_literals(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Disallow unclear usage of consecutive space characters in regular expression literals.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]], jsii.get(self, "noMultipleSpacesInRegularExpressionLiterals"))

    @no_multiple_spaces_in_regular_expression_literals.setter
    def no_multiple_spaces_in_regular_expression_literals(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7832220cfe9ec2d7eacfe172b836a0c1c226bb2b818b85e84776bc957af1af07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noMultipleSpacesInRegularExpressionLiterals", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noStaticOnlyClass")
    def no_static_only_class(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) This rule reports when a class has no non-static members, such as for a class used exclusively as a static namespace.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "noStaticOnlyClass"))

    @no_static_only_class.setter
    def no_static_only_class(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be6a363d6ed6f19911d8f3b85f27cbc100b07ff390030266d9e1b18d1064faed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noStaticOnlyClass", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noThisInStatic")
    def no_this_in_static(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Disallow this and super in static contexts.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]], jsii.get(self, "noThisInStatic"))

    @no_this_in_static.setter
    def no_this_in_static(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccc966a14f0ad1c4400be9d31266c4369dd5a66833db9e76773d270a94d51b62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noThisInStatic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noUselessCatch")
    def no_useless_catch(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Disallow unnecessary catch clauses.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]], jsii.get(self, "noUselessCatch"))

    @no_useless_catch.setter
    def no_useless_catch(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__550c13e7ca1d8edaf45954383393d367200faf3491b22d5277c20b29a724a48f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noUselessCatch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noUselessConstructor")
    def no_useless_constructor(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Disallow unnecessary constructors.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]], jsii.get(self, "noUselessConstructor"))

    @no_useless_constructor.setter
    def no_useless_constructor(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48447d97386f6ebd9442fdbfa7cb432263cc029e98391be8da835361e0d56d1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noUselessConstructor", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noUselessEmptyExport")
    def no_useless_empty_export(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Disallow empty exports that don't change anything in a module file.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]], jsii.get(self, "noUselessEmptyExport"))

    @no_useless_empty_export.setter
    def no_useless_empty_export(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__184b8369db2e0361462e0072711a85fc4d8b08be044bf9156a133e20c0fb9129)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noUselessEmptyExport", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noUselessFragments")
    def no_useless_fragments(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Disallow unnecessary fragments.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]], jsii.get(self, "noUselessFragments"))

    @no_useless_fragments.setter
    def no_useless_fragments(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d86d1faf9e93c0047ccca4ab8884a6226cd64a747f2a6c24b475d1e831fdf86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noUselessFragments", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noUselessLabel")
    def no_useless_label(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Disallow unnecessary labels.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]], jsii.get(self, "noUselessLabel"))

    @no_useless_label.setter
    def no_useless_label(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc2d3c1b7d492628dac2404a059b2e2f06c22898abcabfe08525a14b247597b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noUselessLabel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noUselessLoneBlockStatements")
    def no_useless_lone_block_statements(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Disallow unnecessary nested block statements.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]], jsii.get(self, "noUselessLoneBlockStatements"))

    @no_useless_lone_block_statements.setter
    def no_useless_lone_block_statements(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4876b1ebfc889845a2f0115187febf0de5e7099f125673a3cb7301df9aa70538)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noUselessLoneBlockStatements", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noUselessRename")
    def no_useless_rename(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Disallow renaming import, export, and destructured assignments to the same name.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]], jsii.get(self, "noUselessRename"))

    @no_useless_rename.setter
    def no_useless_rename(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b41db8df47a49f96beb38540cb374ed37ce4b75bf7bbd23d58b48f42dacdd84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noUselessRename", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noUselessStringConcat")
    def no_useless_string_concat(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Disallow unnecessary concatenation of string or template literals.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]], jsii.get(self, "noUselessStringConcat"))

    @no_useless_string_concat.setter
    def no_useless_string_concat(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34d5a683406556fab59f9b2c764491e1fd2630c8faeb168fe4fd20507f099a6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noUselessStringConcat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noUselessSwitchCase")
    def no_useless_switch_case(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Disallow useless case in switch statements.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]], jsii.get(self, "noUselessSwitchCase"))

    @no_useless_switch_case.setter
    def no_useless_switch_case(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95aebc0bf4de8bd7e02193b09b628eb724623ee1e26d45b269866d389668ce77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noUselessSwitchCase", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noUselessTernary")
    def no_useless_ternary(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Disallow ternary operators when simpler alternatives exist.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]], jsii.get(self, "noUselessTernary"))

    @no_useless_ternary.setter
    def no_useless_ternary(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2374a8cb9ee2ad78532b33b0a8aa172d6056f524f8ee4df23c832248b8374c1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noUselessTernary", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noUselessThisAlias")
    def no_useless_this_alias(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Disallow useless this aliasing.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]], jsii.get(self, "noUselessThisAlias"))

    @no_useless_this_alias.setter
    def no_useless_this_alias(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__583313ca5c9eecb07d5801862b82b0c8ef656ce978027d6504d33dd48e17248f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noUselessThisAlias", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noUselessTypeConstraint")
    def no_useless_type_constraint(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Disallow using any or unknown as type constraint.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]], jsii.get(self, "noUselessTypeConstraint"))

    @no_useless_type_constraint.setter
    def no_useless_type_constraint(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35716f453cb77c716aacc372b1de5e56b8a1afa0152704a09fa6c79cd67cce6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noUselessTypeConstraint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noUselessUndefinedInitialization")
    def no_useless_undefined_initialization(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Disallow initializing variables to undefined.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]], jsii.get(self, "noUselessUndefinedInitialization"))

    @no_useless_undefined_initialization.setter
    def no_useless_undefined_initialization(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__764c7ead6631aa3a414b418a731061e87636902195aea2e94658c5c26f8b3b07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noUselessUndefinedInitialization", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noVoid")
    def no_void(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow the use of void operators, which is not a familiar operator.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "noVoid"))

    @no_void.setter
    def no_void(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7b46453a7adc35e574d584728a4fe697a4be1f5b41c0ef6b1e1a07d52fe936e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noVoid", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noWith")
    def no_with(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow with statements in non-strict contexts.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "noWith"))

    @no_with.setter
    def no_with(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bddf3faef23a299d0e46750faf56278b1370de31683b6d3b135d0ff44284748)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noWith", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recommended")
    def recommended(self) -> typing.Optional[builtins.bool]:
        '''(experimental) It enables the recommended rules for this group.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "recommended"))

    @recommended.setter
    def recommended(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__691b127b6bb9f45ec578da384ba4d528eb91a94a1197d41539283520ceb90a01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recommended", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useArrowFunction")
    def use_arrow_function(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Use arrow functions over function expressions.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]], jsii.get(self, "useArrowFunction"))

    @use_arrow_function.setter
    def use_arrow_function(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9711b21685ba3a17c03b3884187be7fe6ec8492d4a2d1bb9e5c9bdccb41ef5e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useArrowFunction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useDateNow")
    def use_date_now(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Use Date.now() to get the number of milliseconds since the Unix Epoch.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]], jsii.get(self, "useDateNow"))

    @use_date_now.setter
    def use_date_now(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0147b4a6a0a82fe3d35ce697a262d260a764ee168bb8981ceab9ef258fff034c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useDateNow", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useFlatMap")
    def use_flat_map(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Promotes the use of .flatMap() when map().flat() are used together.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]], jsii.get(self, "useFlatMap"))

    @use_flat_map.setter
    def use_flat_map(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fde1a14e4358262119414b0fb7497a1a1a19752bf4ca8eddefc2a45799e7e769)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useFlatMap", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useLiteralKeys")
    def use_literal_keys(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Enforce the usage of a literal access to properties over computed property access.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]], jsii.get(self, "useLiteralKeys"))

    @use_literal_keys.setter
    def use_literal_keys(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__026f54e5038acbee5473fd1df983a2740554f3f2757b2d20401b67778715e93a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useLiteralKeys", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useOptionalChain")
    def use_optional_chain(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Enforce using concise optional chain instead of chained logical expressions.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]], jsii.get(self, "useOptionalChain"))

    @use_optional_chain.setter
    def use_optional_chain(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__215c792f5bab05c9d5ddcec3b6164a5873049dd88eb9d8f94a4b18ca6b72b53e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useOptionalChain", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useRegexLiterals")
    def use_regex_literals(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Enforce the use of the regular expression literals instead of the RegExp constructor if possible.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]], jsii.get(self, "useRegexLiterals"))

    @use_regex_literals.setter
    def use_regex_literals(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__284b064fd7d479aacc423beff999a1bcf5575783792b4dbe93ccd5c37c348dec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useRegexLiterals", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useSimpleNumberKeys")
    def use_simple_number_keys(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Disallow number literal object member names which are not base10 or uses underscore as separator.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]], jsii.get(self, "useSimpleNumberKeys"))

    @use_simple_number_keys.setter
    def use_simple_number_keys(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9e6b292d2f18b74400ed84d4598817f3c3463a200984c2179b5c80abf7d5724)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useSimpleNumberKeys", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useSimplifiedLogicExpression")
    def use_simplified_logic_expression(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Discard redundant terms from logical expressions.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]], jsii.get(self, "useSimplifiedLogicExpression"))

    @use_simplified_logic_expression.setter
    def use_simplified_logic_expression(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e336b60462abd4ddb48fe9acd9bd5250a7f161179b5cac127cfa51ebc3008f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useSimplifiedLogicExpression", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IComplexity).__jsii_proxy_class__ = lambda : _IComplexityProxy


@jsii.interface(jsii_type="projen.javascript.biome_config.IComplexityOptions")
class IComplexityOptions(typing_extensions.Protocol):
    '''(experimental) Options for the rule ``noExcessiveCognitiveComplexity``.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="maxAllowedComplexity")
    def max_allowed_complexity(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The maximum complexity score that we allow.

        Anything higher is considered excessive.

        :stability: experimental
        '''
        ...

    @max_allowed_complexity.setter
    def max_allowed_complexity(self, value: typing.Optional[jsii.Number]) -> None:
        ...


class _IComplexityOptionsProxy:
    '''(experimental) Options for the rule ``noExcessiveCognitiveComplexity``.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.IComplexityOptions"

    @builtins.property
    @jsii.member(jsii_name="maxAllowedComplexity")
    def max_allowed_complexity(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The maximum complexity score that we allow.

        Anything higher is considered excessive.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxAllowedComplexity"))

    @max_allowed_complexity.setter
    def max_allowed_complexity(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__730cb570896a87fa0abe2fb84c33cf5ffa7bf918511eea7126384a15e7b5cce8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxAllowedComplexity", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IComplexityOptions).__jsii_proxy_class__ = lambda : _IComplexityOptionsProxy


@jsii.interface(jsii_type="projen.javascript.biome_config.IConfiguration")
class IConfiguration(typing_extensions.Protocol):
    '''(experimental) The configuration that is contained inside the file ``biome.json``.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="assists")
    def assists(self) -> typing.Optional[IAssistsConfiguration]:
        '''(experimental) Specific configuration for assists.

        :stability: experimental
        '''
        ...

    @assists.setter
    def assists(self, value: typing.Optional[IAssistsConfiguration]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="css")
    def css(self) -> typing.Optional["ICssConfiguration"]:
        '''(experimental) Specific configuration for the Css language.

        :stability: experimental
        '''
        ...

    @css.setter
    def css(self, value: typing.Optional["ICssConfiguration"]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="extends")
    def extends(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of paths to other JSON files, used to extends the current configuration.

        :stability: experimental
        '''
        ...

    @extends.setter
    def extends(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="files")
    def files(self) -> typing.Optional["IFilesConfiguration"]:
        '''(experimental) The configuration of the filesystem.

        :stability: experimental
        '''
        ...

    @files.setter
    def files(self, value: typing.Optional["IFilesConfiguration"]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="formatter")
    def formatter(self) -> typing.Optional["IFormatterConfiguration"]:
        '''(experimental) The configuration of the formatter.

        :stability: experimental
        '''
        ...

    @formatter.setter
    def formatter(self, value: typing.Optional["IFormatterConfiguration"]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="graphql")
    def graphql(self) -> typing.Optional["IGraphqlConfiguration"]:
        '''(experimental) Specific configuration for the GraphQL language.

        :stability: experimental
        '''
        ...

    @graphql.setter
    def graphql(self, value: typing.Optional["IGraphqlConfiguration"]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="javascript")
    def javascript(self) -> typing.Optional["IJavascriptConfiguration"]:
        '''(experimental) Specific configuration for the JavaScript language.

        :stability: experimental
        '''
        ...

    @javascript.setter
    def javascript(self, value: typing.Optional["IJavascriptConfiguration"]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="json")
    def json(self) -> typing.Optional["IJsonConfiguration"]:
        '''(experimental) Specific configuration for the Json language.

        :stability: experimental
        '''
        ...

    @json.setter
    def json(self, value: typing.Optional["IJsonConfiguration"]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="linter")
    def linter(self) -> typing.Optional["ILinterConfiguration"]:
        '''(experimental) The configuration for the linter.

        :stability: experimental
        '''
        ...

    @linter.setter
    def linter(self, value: typing.Optional["ILinterConfiguration"]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="organizeImports")
    def organize_imports(self) -> typing.Optional["IOrganizeImports"]:
        '''(experimental) The configuration of the import sorting.

        :stability: experimental
        '''
        ...

    @organize_imports.setter
    def organize_imports(self, value: typing.Optional["IOrganizeImports"]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="overrides")
    def overrides(self) -> typing.Optional[typing.List["IOverridePattern"]]:
        '''(experimental) A list of granular patterns that should be applied only to a sub set of files.

        :stability: experimental
        '''
        ...

    @overrides.setter
    def overrides(
        self,
        value: typing.Optional[typing.List["IOverridePattern"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="vcs")
    def vcs(self) -> typing.Optional["IVcsConfiguration"]:
        '''(experimental) The configuration of the VCS integration.

        :stability: experimental
        '''
        ...

    @vcs.setter
    def vcs(self, value: typing.Optional["IVcsConfiguration"]) -> None:
        ...


class _IConfigurationProxy:
    '''(experimental) The configuration that is contained inside the file ``biome.json``.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.IConfiguration"

    @builtins.property
    @jsii.member(jsii_name="assists")
    def assists(self) -> typing.Optional[IAssistsConfiguration]:
        '''(experimental) Specific configuration for assists.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[IAssistsConfiguration], jsii.get(self, "assists"))

    @assists.setter
    def assists(self, value: typing.Optional[IAssistsConfiguration]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19ef59b92890c0302f27732b07d85b3baac8ac9f80a459d269e26941ef5945eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assists", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="css")
    def css(self) -> typing.Optional["ICssConfiguration"]:
        '''(experimental) Specific configuration for the Css language.

        :stability: experimental
        '''
        return typing.cast(typing.Optional["ICssConfiguration"], jsii.get(self, "css"))

    @css.setter
    def css(self, value: typing.Optional["ICssConfiguration"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f56cb36219d0a510ffd5110a47e6977e468d23152c729b5366c456e1c4b76dce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "css", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="extends")
    def extends(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of paths to other JSON files, used to extends the current configuration.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "extends"))

    @extends.setter
    def extends(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72c1543c48b401a114885804899042a3aeab12fe374664b0e0874b8331bd4be4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "extends", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="files")
    def files(self) -> typing.Optional["IFilesConfiguration"]:
        '''(experimental) The configuration of the filesystem.

        :stability: experimental
        '''
        return typing.cast(typing.Optional["IFilesConfiguration"], jsii.get(self, "files"))

    @files.setter
    def files(self, value: typing.Optional["IFilesConfiguration"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbf5888714978c76d93f191fce6fc24afe161b4c2602e9796173392a4710c4d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "files", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="formatter")
    def formatter(self) -> typing.Optional["IFormatterConfiguration"]:
        '''(experimental) The configuration of the formatter.

        :stability: experimental
        '''
        return typing.cast(typing.Optional["IFormatterConfiguration"], jsii.get(self, "formatter"))

    @formatter.setter
    def formatter(self, value: typing.Optional["IFormatterConfiguration"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__685ae26f5d8b96d6c516ce520a72902af5ba20be500f6b269e3a81d9bc2e89d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "formatter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="graphql")
    def graphql(self) -> typing.Optional["IGraphqlConfiguration"]:
        '''(experimental) Specific configuration for the GraphQL language.

        :stability: experimental
        '''
        return typing.cast(typing.Optional["IGraphqlConfiguration"], jsii.get(self, "graphql"))

    @graphql.setter
    def graphql(self, value: typing.Optional["IGraphqlConfiguration"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__893d61135484b0fa3f122454da784dc165143f265ec6daf4dbe60e3808319479)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "graphql", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="javascript")
    def javascript(self) -> typing.Optional["IJavascriptConfiguration"]:
        '''(experimental) Specific configuration for the JavaScript language.

        :stability: experimental
        '''
        return typing.cast(typing.Optional["IJavascriptConfiguration"], jsii.get(self, "javascript"))

    @javascript.setter
    def javascript(self, value: typing.Optional["IJavascriptConfiguration"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c52427e4ea4b41dcf9edaabb1a1d0c5a888f23607671086eaf3a81b4d14464a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "javascript", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="json")
    def json(self) -> typing.Optional["IJsonConfiguration"]:
        '''(experimental) Specific configuration for the Json language.

        :stability: experimental
        '''
        return typing.cast(typing.Optional["IJsonConfiguration"], jsii.get(self, "json"))

    @json.setter
    def json(self, value: typing.Optional["IJsonConfiguration"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e23e007685b010ac2f113fdaa1ef164bb116cc67eb9788b661f5ed56c4f56a70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "json", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="linter")
    def linter(self) -> typing.Optional["ILinterConfiguration"]:
        '''(experimental) The configuration for the linter.

        :stability: experimental
        '''
        return typing.cast(typing.Optional["ILinterConfiguration"], jsii.get(self, "linter"))

    @linter.setter
    def linter(self, value: typing.Optional["ILinterConfiguration"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa0ba6323f05508c77e65eeedff69e17bd8c8012fc7cabd2326aa3297c53b498)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "linter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="organizeImports")
    def organize_imports(self) -> typing.Optional["IOrganizeImports"]:
        '''(experimental) The configuration of the import sorting.

        :stability: experimental
        '''
        return typing.cast(typing.Optional["IOrganizeImports"], jsii.get(self, "organizeImports"))

    @organize_imports.setter
    def organize_imports(self, value: typing.Optional["IOrganizeImports"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__903038f50d558cadf8b887a936ed082600c0fc8b9164a87e7624692825ad778f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "organizeImports", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="overrides")
    def overrides(self) -> typing.Optional[typing.List["IOverridePattern"]]:
        '''(experimental) A list of granular patterns that should be applied only to a sub set of files.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List["IOverridePattern"]], jsii.get(self, "overrides"))

    @overrides.setter
    def overrides(
        self,
        value: typing.Optional[typing.List["IOverridePattern"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f83daa8ef482de67976967829aed7ec68c4dd5e9e51c4dfc2d1f99c6233736e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "overrides", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vcs")
    def vcs(self) -> typing.Optional["IVcsConfiguration"]:
        '''(experimental) The configuration of the VCS integration.

        :stability: experimental
        '''
        return typing.cast(typing.Optional["IVcsConfiguration"], jsii.get(self, "vcs"))

    @vcs.setter
    def vcs(self, value: typing.Optional["IVcsConfiguration"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df9874da1131d438df5b8358df9a526e60e72a39fb6e24552f09845858308fda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vcs", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IConfiguration).__jsii_proxy_class__ = lambda : _IConfigurationProxy


@jsii.interface(jsii_type="projen.javascript.biome_config.IConsistentArrayTypeOptions")
class IConsistentArrayTypeOptions(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="syntax")
    def syntax(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        ...

    @syntax.setter
    def syntax(self, value: typing.Optional[builtins.str]) -> None:
        ...


class _IConsistentArrayTypeOptionsProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.IConsistentArrayTypeOptions"

    @builtins.property
    @jsii.member(jsii_name="syntax")
    def syntax(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "syntax"))

    @syntax.setter
    def syntax(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edd6030218644f5c1ff274094ba2ca482af80aaa06e8d0a5d864c1f1a54d9cca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "syntax", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IConsistentArrayTypeOptions).__jsii_proxy_class__ = lambda : _IConsistentArrayTypeOptionsProxy


@jsii.interface(
    jsii_type="projen.javascript.biome_config.IConsistentMemberAccessibilityOptions"
)
class IConsistentMemberAccessibilityOptions(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="accessibility")
    def accessibility(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        ...

    @accessibility.setter
    def accessibility(self, value: typing.Optional[builtins.str]) -> None:
        ...


class _IConsistentMemberAccessibilityOptionsProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.IConsistentMemberAccessibilityOptions"

    @builtins.property
    @jsii.member(jsii_name="accessibility")
    def accessibility(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessibility"))

    @accessibility.setter
    def accessibility(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fe147a2a903f0a90ded05a021117f5c3f32f21821430cbace964257e1a4ec73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessibility", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IConsistentMemberAccessibilityOptions).__jsii_proxy_class__ = lambda : _IConsistentMemberAccessibilityOptionsProxy


@jsii.interface(jsii_type="projen.javascript.biome_config.IConvention")
class IConvention(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="formats")
    def formats(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) String cases to enforce.

        :stability: experimental
        '''
        ...

    @formats.setter
    def formats(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="match")
    def match(self) -> typing.Optional[builtins.str]:
        '''(experimental) Regular expression to enforce.

        :stability: experimental
        '''
        ...

    @match.setter
    def match(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="selector")
    def selector(self) -> typing.Optional["ISelector"]:
        '''(experimental) Declarations concerned by this convention.

        :stability: experimental
        '''
        ...

    @selector.setter
    def selector(self, value: typing.Optional["ISelector"]) -> None:
        ...


class _IConventionProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.IConvention"

    @builtins.property
    @jsii.member(jsii_name="formats")
    def formats(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) String cases to enforce.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "formats"))

    @formats.setter
    def formats(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d996705432f9a05786fe491b3b9394c2467b88acf03abf2de4573995ff7a2a57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "formats", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="match")
    def match(self) -> typing.Optional[builtins.str]:
        '''(experimental) Regular expression to enforce.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "match"))

    @match.setter
    def match(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54a76e2eecbbbab9ae3f0683bdf2e516348f28e2536a09c7e533297864b8237c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "match", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="selector")
    def selector(self) -> typing.Optional["ISelector"]:
        '''(experimental) Declarations concerned by this convention.

        :stability: experimental
        '''
        return typing.cast(typing.Optional["ISelector"], jsii.get(self, "selector"))

    @selector.setter
    def selector(self, value: typing.Optional["ISelector"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__585fcee8be7ecaa7cfd54dd46e1295851adf353af3939640f9e8dd2d91b00fef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "selector", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IConvention).__jsii_proxy_class__ = lambda : _IConventionProxy


@jsii.interface(jsii_type="projen.javascript.biome_config.ICorrectness")
class ICorrectness(typing_extensions.Protocol):
    '''(experimental) A list of rules that belong to this group.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="all")
    def all(self) -> typing.Optional[builtins.bool]:
        '''(experimental) It enables ALL rules for this group.

        :stability: experimental
        '''
        ...

    @all.setter
    def all(self, value: typing.Optional[builtins.bool]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noChildrenProp")
    def no_children_prop(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Prevent passing of children as props.

        :stability: experimental
        '''
        ...

    @no_children_prop.setter
    def no_children_prop(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noConstantCondition")
    def no_constant_condition(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow constant expressions in conditions.

        :stability: experimental
        '''
        ...

    @no_constant_condition.setter
    def no_constant_condition(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noConstantMathMinMaxClamp")
    def no_constant_math_min_max_clamp(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Disallow the use of Math.min and Math.max to clamp a value where the result itself is constant.

        :stability: experimental
        '''
        ...

    @no_constant_math_min_max_clamp.setter
    def no_constant_math_min_max_clamp(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noConstAssign")
    def no_const_assign(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Prevents from having const variables being re-assigned.

        :stability: experimental
        '''
        ...

    @no_const_assign.setter
    def no_const_assign(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noConstructorReturn")
    def no_constructor_return(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow returning a value from a constructor.

        :stability: experimental
        '''
        ...

    @no_constructor_return.setter
    def no_constructor_return(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noEmptyCharacterClassInRegex")
    def no_empty_character_class_in_regex(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow empty character classes in regular expression literals.

        :stability: experimental
        '''
        ...

    @no_empty_character_class_in_regex.setter
    def no_empty_character_class_in_regex(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noEmptyPattern")
    def no_empty_pattern(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallows empty destructuring patterns.

        :stability: experimental
        '''
        ...

    @no_empty_pattern.setter
    def no_empty_pattern(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noFlatMapIdentity")
    def no_flat_map_identity(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Disallow to use unnecessary callback on flatMap.

        :stability: experimental
        '''
        ...

    @no_flat_map_identity.setter
    def no_flat_map_identity(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noGlobalObjectCalls")
    def no_global_object_calls(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow calling global object properties as functions.

        :stability: experimental
        '''
        ...

    @no_global_object_calls.setter
    def no_global_object_calls(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noInnerDeclarations")
    def no_inner_declarations(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow function and var declarations that are accessible outside their block.

        :stability: experimental
        '''
        ...

    @no_inner_declarations.setter
    def no_inner_declarations(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noInvalidBuiltinInstantiation")
    def no_invalid_builtin_instantiation(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Ensure that builtins are correctly instantiated.

        :stability: experimental
        '''
        ...

    @no_invalid_builtin_instantiation.setter
    def no_invalid_builtin_instantiation(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noInvalidConstructorSuper")
    def no_invalid_constructor_super(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Prevents the incorrect use of super() inside classes.

        It also checks whether a call super() is missing from classes that extends other constructors.

        :stability: experimental
        '''
        ...

    @no_invalid_constructor_super.setter
    def no_invalid_constructor_super(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noInvalidDirectionInLinearGradient")
    def no_invalid_direction_in_linear_gradient(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow non-standard direction values for linear gradient functions.

        :stability: experimental
        '''
        ...

    @no_invalid_direction_in_linear_gradient.setter
    def no_invalid_direction_in_linear_gradient(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noInvalidGridAreas")
    def no_invalid_grid_areas(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallows invalid named grid areas in CSS Grid Layouts.

        :stability: experimental
        '''
        ...

    @no_invalid_grid_areas.setter
    def no_invalid_grid_areas(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noInvalidNewBuiltin")
    def no_invalid_new_builtin(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Disallow new operators with global non-constructor functions.

        :stability: experimental
        '''
        ...

    @no_invalid_new_builtin.setter
    def no_invalid_new_builtin(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noInvalidPositionAtImportRule")
    def no_invalid_position_at_import_rule(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow the use of.

        :stability: experimental
        :import: positions.
        '''
        ...

    @no_invalid_position_at_import_rule.setter
    def no_invalid_position_at_import_rule(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noInvalidUseBeforeDeclaration")
    def no_invalid_use_before_declaration(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow the use of variables and function parameters before their declaration.

        :stability: experimental
        '''
        ...

    @no_invalid_use_before_declaration.setter
    def no_invalid_use_before_declaration(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noNewSymbol")
    def no_new_symbol(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Disallow new operators with the Symbol object.

        :stability: experimental
        '''
        ...

    @no_new_symbol.setter
    def no_new_symbol(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noNodejsModules")
    def no_nodejs_modules(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Forbid the use of Node.js builtin modules.

        :stability: experimental
        '''
        ...

    @no_nodejs_modules.setter
    def no_nodejs_modules(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noNonoctalDecimalEscape")
    def no_nonoctal_decimal_escape(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Disallow \\8 and \\9 escape sequences in string literals.

        :stability: experimental
        '''
        ...

    @no_nonoctal_decimal_escape.setter
    def no_nonoctal_decimal_escape(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noPrecisionLoss")
    def no_precision_loss(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow literal numbers that lose precision.

        :stability: experimental
        '''
        ...

    @no_precision_loss.setter
    def no_precision_loss(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noRenderReturnValue")
    def no_render_return_value(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Prevent the usage of the return value of React.render.

        :stability: experimental
        '''
        ...

    @no_render_return_value.setter
    def no_render_return_value(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noSelfAssign")
    def no_self_assign(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow assignments where both sides are exactly the same.

        :stability: experimental
        '''
        ...

    @no_self_assign.setter
    def no_self_assign(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noSetterReturn")
    def no_setter_return(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow returning a value from a setter.

        :stability: experimental
        '''
        ...

    @no_setter_return.setter
    def no_setter_return(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noStringCaseMismatch")
    def no_string_case_mismatch(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Disallow comparison of expressions modifying the string case with non-compliant value.

        :stability: experimental
        '''
        ...

    @no_string_case_mismatch.setter
    def no_string_case_mismatch(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noSwitchDeclarations")
    def no_switch_declarations(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Disallow lexical declarations in switch clauses.

        :stability: experimental
        '''
        ...

    @no_switch_declarations.setter
    def no_switch_declarations(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noUndeclaredDependencies")
    def no_undeclared_dependencies(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow the use of dependencies that aren't specified in the package.json.

        :stability: experimental
        '''
        ...

    @no_undeclared_dependencies.setter
    def no_undeclared_dependencies(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noUndeclaredVariables")
    def no_undeclared_variables(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Prevents the usage of variables that haven't been declared inside the document.

        :stability: experimental
        '''
        ...

    @no_undeclared_variables.setter
    def no_undeclared_variables(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noUnknownFunction")
    def no_unknown_function(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow unknown CSS value functions.

        :stability: experimental
        '''
        ...

    @no_unknown_function.setter
    def no_unknown_function(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noUnknownMediaFeatureName")
    def no_unknown_media_feature_name(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow unknown media feature names.

        :stability: experimental
        '''
        ...

    @no_unknown_media_feature_name.setter
    def no_unknown_media_feature_name(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noUnknownProperty")
    def no_unknown_property(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow unknown properties.

        :stability: experimental
        '''
        ...

    @no_unknown_property.setter
    def no_unknown_property(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noUnknownUnit")
    def no_unknown_unit(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow unknown CSS units.

        :stability: experimental
        '''
        ...

    @no_unknown_unit.setter
    def no_unknown_unit(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noUnmatchableAnbSelector")
    def no_unmatchable_anb_selector(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow unmatchable An+B selectors.

        :stability: experimental
        '''
        ...

    @no_unmatchable_anb_selector.setter
    def no_unmatchable_anb_selector(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noUnnecessaryContinue")
    def no_unnecessary_continue(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Avoid using unnecessary continue.

        :stability: experimental
        '''
        ...

    @no_unnecessary_continue.setter
    def no_unnecessary_continue(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noUnreachable")
    def no_unreachable(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow unreachable code.

        :stability: experimental
        '''
        ...

    @no_unreachable.setter
    def no_unreachable(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noUnreachableSuper")
    def no_unreachable_super(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Ensures the super() constructor is called exactly once on every code  path in a class constructor before this is accessed if the class has a superclass.

        :stability: experimental
        '''
        ...

    @no_unreachable_super.setter
    def no_unreachable_super(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noUnsafeFinally")
    def no_unsafe_finally(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow control flow statements in finally blocks.

        :stability: experimental
        '''
        ...

    @no_unsafe_finally.setter
    def no_unsafe_finally(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noUnsafeOptionalChaining")
    def no_unsafe_optional_chaining(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow the use of optional chaining in contexts where the undefined value is not allowed.

        :stability: experimental
        '''
        ...

    @no_unsafe_optional_chaining.setter
    def no_unsafe_optional_chaining(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noUnusedFunctionParameters")
    def no_unused_function_parameters(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Disallow unused function parameters.

        :stability: experimental
        '''
        ...

    @no_unused_function_parameters.setter
    def no_unused_function_parameters(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noUnusedImports")
    def no_unused_imports(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Disallow unused imports.

        :stability: experimental
        '''
        ...

    @no_unused_imports.setter
    def no_unused_imports(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noUnusedLabels")
    def no_unused_labels(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Disallow unused labels.

        :stability: experimental
        '''
        ...

    @no_unused_labels.setter
    def no_unused_labels(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noUnusedPrivateClassMembers")
    def no_unused_private_class_members(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Disallow unused private class members.

        :stability: experimental
        '''
        ...

    @no_unused_private_class_members.setter
    def no_unused_private_class_members(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noUnusedVariables")
    def no_unused_variables(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Disallow unused variables.

        :stability: experimental
        '''
        ...

    @no_unused_variables.setter
    def no_unused_variables(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noVoidElementsWithChildren")
    def no_void_elements_with_children(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) This rules prevents void elements (AKA self-closing elements) from having children.

        :stability: experimental
        '''
        ...

    @no_void_elements_with_children.setter
    def no_void_elements_with_children(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noVoidTypeReturn")
    def no_void_type_return(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow returning a value from a function with the return type 'void'.

        :stability: experimental
        '''
        ...

    @no_void_type_return.setter
    def no_void_type_return(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="recommended")
    def recommended(self) -> typing.Optional[builtins.bool]:
        '''(experimental) It enables the recommended rules for this group.

        :stability: experimental
        '''
        ...

    @recommended.setter
    def recommended(self, value: typing.Optional[builtins.bool]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useArrayLiterals")
    def use_array_literals(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Disallow Array constructors.

        :stability: experimental
        '''
        ...

    @use_array_literals.setter
    def use_array_literals(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useExhaustiveDependencies")
    def use_exhaustive_dependencies(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithUseExhaustiveDependenciesOptions"]]:
        '''(experimental) Enforce all dependencies are correctly specified in a React hook.

        :stability: experimental
        '''
        ...

    @use_exhaustive_dependencies.setter
    def use_exhaustive_dependencies(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithUseExhaustiveDependenciesOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useHookAtTopLevel")
    def use_hook_at_top_level(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithDeprecatedHooksOptions"]]:
        '''(experimental) Enforce that all React hooks are being called from the Top Level component functions.

        :stability: experimental
        '''
        ...

    @use_hook_at_top_level.setter
    def use_hook_at_top_level(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithDeprecatedHooksOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useImportExtensions")
    def use_import_extensions(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithUseImportExtensionsOptions"]]:
        '''(experimental) Enforce file extensions for relative imports.

        :stability: experimental
        '''
        ...

    @use_import_extensions.setter
    def use_import_extensions(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithUseImportExtensionsOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useIsNan")
    def use_is_nan(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Require calls to isNaN() when checking for NaN.

        :stability: experimental
        '''
        ...

    @use_is_nan.setter
    def use_is_nan(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useJsxKeyInIterable")
    def use_jsx_key_in_iterable(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow missing key props in iterators/collection literals.

        :stability: experimental
        '''
        ...

    @use_jsx_key_in_iterable.setter
    def use_jsx_key_in_iterable(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useValidForDirection")
    def use_valid_for_direction(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Enforce "for" loop update clause moving the counter in the right direction.

        :stability: experimental
        '''
        ...

    @use_valid_for_direction.setter
    def use_valid_for_direction(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useYield")
    def use_yield(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Require generator functions to contain yield.

        :stability: experimental
        '''
        ...

    @use_yield.setter
    def use_yield(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...


class _ICorrectnessProxy:
    '''(experimental) A list of rules that belong to this group.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.ICorrectness"

    @builtins.property
    @jsii.member(jsii_name="all")
    def all(self) -> typing.Optional[builtins.bool]:
        '''(experimental) It enables ALL rules for this group.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "all"))

    @all.setter
    def all(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__098230eee4022d245f3cf2bb2a023a35049ec26fcffbfbddad44eb9d2a4acc70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "all", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noChildrenProp")
    def no_children_prop(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Prevent passing of children as props.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "noChildrenProp"))

    @no_children_prop.setter
    def no_children_prop(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9994d36d0cac2f96b77ebb93b95d6a18558d3f24a7b92b4b072f6dfadc66ff24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noChildrenProp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noConstantCondition")
    def no_constant_condition(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow constant expressions in conditions.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "noConstantCondition"))

    @no_constant_condition.setter
    def no_constant_condition(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e58b43c3e329e892bfd8b4cbac443acad011b52cb60f2d253790ed7cf4b0e296)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noConstantCondition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noConstantMathMinMaxClamp")
    def no_constant_math_min_max_clamp(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Disallow the use of Math.min and Math.max to clamp a value where the result itself is constant.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]], jsii.get(self, "noConstantMathMinMaxClamp"))

    @no_constant_math_min_max_clamp.setter
    def no_constant_math_min_max_clamp(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af5d59ac5671f7082a94972eafc6e387e9dbcf8a530dd50517afc35f0073138d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noConstantMathMinMaxClamp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noConstAssign")
    def no_const_assign(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Prevents from having const variables being re-assigned.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]], jsii.get(self, "noConstAssign"))

    @no_const_assign.setter
    def no_const_assign(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1eb523d0089eddd593c4a1852f8b89f2413880fa5e6bb8f2de5333cedfe9ea2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noConstAssign", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noConstructorReturn")
    def no_constructor_return(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow returning a value from a constructor.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "noConstructorReturn"))

    @no_constructor_return.setter
    def no_constructor_return(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c237c61f679ecfb3e90060b7b107183e8b8e51a66a07ebacc752ae2206c1fe6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noConstructorReturn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noEmptyCharacterClassInRegex")
    def no_empty_character_class_in_regex(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow empty character classes in regular expression literals.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "noEmptyCharacterClassInRegex"))

    @no_empty_character_class_in_regex.setter
    def no_empty_character_class_in_regex(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__248ad84f845aac5113de595fc6458e474b2f8e913e697cc3a053de9a19dd4328)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noEmptyCharacterClassInRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noEmptyPattern")
    def no_empty_pattern(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallows empty destructuring patterns.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "noEmptyPattern"))

    @no_empty_pattern.setter
    def no_empty_pattern(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c7fcdd1e35aeb89c4e519901c4d6633704213133ab4e0eada6cae68970acf79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noEmptyPattern", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noFlatMapIdentity")
    def no_flat_map_identity(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Disallow to use unnecessary callback on flatMap.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]], jsii.get(self, "noFlatMapIdentity"))

    @no_flat_map_identity.setter
    def no_flat_map_identity(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32dbeb99cc31282c15f50fa58ec5ce565a254f7d8d35e0c0b8013572e7dec8ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noFlatMapIdentity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noGlobalObjectCalls")
    def no_global_object_calls(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow calling global object properties as functions.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "noGlobalObjectCalls"))

    @no_global_object_calls.setter
    def no_global_object_calls(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6221f0b2b950d20bcdab7f59776be8f5bf23777ae1f4ed5a59f8a6a8d49ccb90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noGlobalObjectCalls", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noInnerDeclarations")
    def no_inner_declarations(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow function and var declarations that are accessible outside their block.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "noInnerDeclarations"))

    @no_inner_declarations.setter
    def no_inner_declarations(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__648ad48f3943e91b88cf1a716fa0fa5bd5b5ae6b7667713b3c17756b521e35ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noInnerDeclarations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noInvalidBuiltinInstantiation")
    def no_invalid_builtin_instantiation(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Ensure that builtins are correctly instantiated.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]], jsii.get(self, "noInvalidBuiltinInstantiation"))

    @no_invalid_builtin_instantiation.setter
    def no_invalid_builtin_instantiation(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5496e61b94f465b71b05d8886f3b9eebc5d0bab5b81ec168176d57f239cc0e8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noInvalidBuiltinInstantiation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noInvalidConstructorSuper")
    def no_invalid_constructor_super(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Prevents the incorrect use of super() inside classes.

        It also checks whether a call super() is missing from classes that extends other constructors.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "noInvalidConstructorSuper"))

    @no_invalid_constructor_super.setter
    def no_invalid_constructor_super(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd26ae2195ca9e313642103010ee2747f98b47a7c334e5df48b7298a2272a13e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noInvalidConstructorSuper", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noInvalidDirectionInLinearGradient")
    def no_invalid_direction_in_linear_gradient(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow non-standard direction values for linear gradient functions.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "noInvalidDirectionInLinearGradient"))

    @no_invalid_direction_in_linear_gradient.setter
    def no_invalid_direction_in_linear_gradient(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d64977731ca5df0ed98b5a6385aa2bfa6f337521c99860245971253f9945e07f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noInvalidDirectionInLinearGradient", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noInvalidGridAreas")
    def no_invalid_grid_areas(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallows invalid named grid areas in CSS Grid Layouts.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "noInvalidGridAreas"))

    @no_invalid_grid_areas.setter
    def no_invalid_grid_areas(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f58b68456750cad22457b63a83988d26471a97b09092505ce46080a499c58bb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noInvalidGridAreas", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noInvalidNewBuiltin")
    def no_invalid_new_builtin(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Disallow new operators with global non-constructor functions.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]], jsii.get(self, "noInvalidNewBuiltin"))

    @no_invalid_new_builtin.setter
    def no_invalid_new_builtin(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__966f8ff6be4ad6cab78155ad40f298016b5b2a3db450ba5c03c467056c47063a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noInvalidNewBuiltin", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noInvalidPositionAtImportRule")
    def no_invalid_position_at_import_rule(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow the use of.

        :stability: experimental
        :import: positions.
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "noInvalidPositionAtImportRule"))

    @no_invalid_position_at_import_rule.setter
    def no_invalid_position_at_import_rule(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__735c79874ad28098cb4ef92cf896ec070dcfb87d30cb735663aab1aa1d92d808)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noInvalidPositionAtImportRule", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noInvalidUseBeforeDeclaration")
    def no_invalid_use_before_declaration(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow the use of variables and function parameters before their declaration.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "noInvalidUseBeforeDeclaration"))

    @no_invalid_use_before_declaration.setter
    def no_invalid_use_before_declaration(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64bf88a7f183bc72b0fb7838d36fe2c258fa0bfe992e2f4a0445aafa9437520f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noInvalidUseBeforeDeclaration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noNewSymbol")
    def no_new_symbol(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Disallow new operators with the Symbol object.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]], jsii.get(self, "noNewSymbol"))

    @no_new_symbol.setter
    def no_new_symbol(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee495084e223bf762c6cc58ec2207b353e81a2ee8752a27db98e415258d58977)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noNewSymbol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noNodejsModules")
    def no_nodejs_modules(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Forbid the use of Node.js builtin modules.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "noNodejsModules"))

    @no_nodejs_modules.setter
    def no_nodejs_modules(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e46baedd5ff9617bb340b2b9a27cbeb795297c8687143b49c2535a31cec3d16d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noNodejsModules", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noNonoctalDecimalEscape")
    def no_nonoctal_decimal_escape(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Disallow \\8 and \\9 escape sequences in string literals.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]], jsii.get(self, "noNonoctalDecimalEscape"))

    @no_nonoctal_decimal_escape.setter
    def no_nonoctal_decimal_escape(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e53757c666925710b80a1acb1d8971bb9e95a335a0d8e51872fdde1da02da946)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noNonoctalDecimalEscape", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noPrecisionLoss")
    def no_precision_loss(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow literal numbers that lose precision.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "noPrecisionLoss"))

    @no_precision_loss.setter
    def no_precision_loss(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45bbed23498cc2dfb696e950c1fd5a13c3a72b1a00f71e008eba28bbc15e674a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noPrecisionLoss", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noRenderReturnValue")
    def no_render_return_value(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Prevent the usage of the return value of React.render.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "noRenderReturnValue"))

    @no_render_return_value.setter
    def no_render_return_value(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__786b5cc23f2d599b2c8d8bc34490c9a5c948b2120c2cb7be3a2adc30f958a32e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noRenderReturnValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noSelfAssign")
    def no_self_assign(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow assignments where both sides are exactly the same.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "noSelfAssign"))

    @no_self_assign.setter
    def no_self_assign(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d812ec612c257034c485a76394525f4498c20db85bc2359be30c231b2722955)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noSelfAssign", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noSetterReturn")
    def no_setter_return(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow returning a value from a setter.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "noSetterReturn"))

    @no_setter_return.setter
    def no_setter_return(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5c80e320331b4eab558e1dd2f393d899910904282c8f020d1ec143e65e91215)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noSetterReturn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noStringCaseMismatch")
    def no_string_case_mismatch(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Disallow comparison of expressions modifying the string case with non-compliant value.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]], jsii.get(self, "noStringCaseMismatch"))

    @no_string_case_mismatch.setter
    def no_string_case_mismatch(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25416124d2d33d921fc0eb9cf6b1fd4ab98c09a0df78413f4f4d93347b0d1b6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noStringCaseMismatch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noSwitchDeclarations")
    def no_switch_declarations(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Disallow lexical declarations in switch clauses.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]], jsii.get(self, "noSwitchDeclarations"))

    @no_switch_declarations.setter
    def no_switch_declarations(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7eef9dabb1ebfb0ddc9f826c425e50e097eff52dd84cdbe237b22a89bc034ee4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noSwitchDeclarations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noUndeclaredDependencies")
    def no_undeclared_dependencies(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow the use of dependencies that aren't specified in the package.json.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "noUndeclaredDependencies"))

    @no_undeclared_dependencies.setter
    def no_undeclared_dependencies(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5252c1d86c4de7b7a23c791263b87a8dc6187baab551594b73363786edc3c8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noUndeclaredDependencies", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noUndeclaredVariables")
    def no_undeclared_variables(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Prevents the usage of variables that haven't been declared inside the document.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "noUndeclaredVariables"))

    @no_undeclared_variables.setter
    def no_undeclared_variables(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb812ab715c10d8c124dcfdc50eb757c6274946700344588520bcc0ff07424f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noUndeclaredVariables", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noUnknownFunction")
    def no_unknown_function(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow unknown CSS value functions.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "noUnknownFunction"))

    @no_unknown_function.setter
    def no_unknown_function(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed0e1596f722a38bc32b5bc82b2a83d0154da0633cb247918a5e589946a4efe4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noUnknownFunction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noUnknownMediaFeatureName")
    def no_unknown_media_feature_name(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow unknown media feature names.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "noUnknownMediaFeatureName"))

    @no_unknown_media_feature_name.setter
    def no_unknown_media_feature_name(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aefc6d84ced5f132a0b8e5ebb3996a9ef4658630e1805367789a844bc174072d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noUnknownMediaFeatureName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noUnknownProperty")
    def no_unknown_property(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow unknown properties.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "noUnknownProperty"))

    @no_unknown_property.setter
    def no_unknown_property(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b65d2ca8686e50c4fa233049df307d12f0ddccd09b1b6dab03c7eea371e1ea7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noUnknownProperty", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noUnknownUnit")
    def no_unknown_unit(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow unknown CSS units.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "noUnknownUnit"))

    @no_unknown_unit.setter
    def no_unknown_unit(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df90472b886a92dab37744073838016f7eabdfd8ad51844c65d6141f9b21090b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noUnknownUnit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noUnmatchableAnbSelector")
    def no_unmatchable_anb_selector(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow unmatchable An+B selectors.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "noUnmatchableAnbSelector"))

    @no_unmatchable_anb_selector.setter
    def no_unmatchable_anb_selector(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5676ba70d61e378d9606f48a6a5a02a873127bbbcac52616904b1bf63b216fbd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noUnmatchableAnbSelector", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noUnnecessaryContinue")
    def no_unnecessary_continue(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Avoid using unnecessary continue.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]], jsii.get(self, "noUnnecessaryContinue"))

    @no_unnecessary_continue.setter
    def no_unnecessary_continue(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__975ba6d3bde38f393ccacdf0b728b8d129fb2f4ef652d5bf3fa6b803226863f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noUnnecessaryContinue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noUnreachable")
    def no_unreachable(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow unreachable code.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "noUnreachable"))

    @no_unreachable.setter
    def no_unreachable(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d08ca5501f4738b0174602833040907fca7ac2be552d82d545bd2a9893cc3eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noUnreachable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noUnreachableSuper")
    def no_unreachable_super(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Ensures the super() constructor is called exactly once on every code  path in a class constructor before this is accessed if the class has a superclass.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "noUnreachableSuper"))

    @no_unreachable_super.setter
    def no_unreachable_super(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12db216ac6b0da4d39ed5cb52b9d22216c58ab8ee059289b70092e0441184464)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noUnreachableSuper", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noUnsafeFinally")
    def no_unsafe_finally(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow control flow statements in finally blocks.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "noUnsafeFinally"))

    @no_unsafe_finally.setter
    def no_unsafe_finally(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00221b7246b8671839cfcec7a3de248fa8aa1aaefd968a886a2b5f0d3075bdc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noUnsafeFinally", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noUnsafeOptionalChaining")
    def no_unsafe_optional_chaining(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow the use of optional chaining in contexts where the undefined value is not allowed.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "noUnsafeOptionalChaining"))

    @no_unsafe_optional_chaining.setter
    def no_unsafe_optional_chaining(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1a3e411d74b6af150dbf64c3ba96867b2727be020b2f7c1787702a12ec16330)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noUnsafeOptionalChaining", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noUnusedFunctionParameters")
    def no_unused_function_parameters(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Disallow unused function parameters.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]], jsii.get(self, "noUnusedFunctionParameters"))

    @no_unused_function_parameters.setter
    def no_unused_function_parameters(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a663e86bce2cbfb06c8586c23cc421cfae81b71ee484b37e797dbad496b93497)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noUnusedFunctionParameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noUnusedImports")
    def no_unused_imports(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Disallow unused imports.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]], jsii.get(self, "noUnusedImports"))

    @no_unused_imports.setter
    def no_unused_imports(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa071ffe55968bf4a20383ad675be4d97a93940609e34dd98a49f2a2aa4da824)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noUnusedImports", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noUnusedLabels")
    def no_unused_labels(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Disallow unused labels.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]], jsii.get(self, "noUnusedLabels"))

    @no_unused_labels.setter
    def no_unused_labels(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__269ae961ee14164a9aff745ab26256ff07af998901f286daefb43b46fcabef3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noUnusedLabels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noUnusedPrivateClassMembers")
    def no_unused_private_class_members(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Disallow unused private class members.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]], jsii.get(self, "noUnusedPrivateClassMembers"))

    @no_unused_private_class_members.setter
    def no_unused_private_class_members(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b7c20a2e443261f6b2d5c542f84973461b23c5d9659cc5af45ad00af960c453)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noUnusedPrivateClassMembers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noUnusedVariables")
    def no_unused_variables(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Disallow unused variables.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]], jsii.get(self, "noUnusedVariables"))

    @no_unused_variables.setter
    def no_unused_variables(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__425353e112cebe1433db7a45ffeaa52d70e55b7578d0f24b5bf9cc8ea71b7680)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noUnusedVariables", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noVoidElementsWithChildren")
    def no_void_elements_with_children(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) This rules prevents void elements (AKA self-closing elements) from having children.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]], jsii.get(self, "noVoidElementsWithChildren"))

    @no_void_elements_with_children.setter
    def no_void_elements_with_children(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6a4b1404bf668f26aa98e3a50347e0c979d5b93cb69e083b8fb70fcbea98ce8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noVoidElementsWithChildren", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noVoidTypeReturn")
    def no_void_type_return(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow returning a value from a function with the return type 'void'.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "noVoidTypeReturn"))

    @no_void_type_return.setter
    def no_void_type_return(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c75a8712d097ad5853d2324cf357a357d7ffb436664b608c2a0ef97fb3db20d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noVoidTypeReturn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recommended")
    def recommended(self) -> typing.Optional[builtins.bool]:
        '''(experimental) It enables the recommended rules for this group.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "recommended"))

    @recommended.setter
    def recommended(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3c7bd295b86608b6a9ebba9fd5bdec1596386f11d668ab29b895b4d43bbe50b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recommended", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useArrayLiterals")
    def use_array_literals(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Disallow Array constructors.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]], jsii.get(self, "useArrayLiterals"))

    @use_array_literals.setter
    def use_array_literals(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71e148401b1df5a9a54aa080923801561e6827ecbdcaef0663d6f3de1e04ecec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useArrayLiterals", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useExhaustiveDependencies")
    def use_exhaustive_dependencies(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithUseExhaustiveDependenciesOptions"]]:
        '''(experimental) Enforce all dependencies are correctly specified in a React hook.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithUseExhaustiveDependenciesOptions"]], jsii.get(self, "useExhaustiveDependencies"))

    @use_exhaustive_dependencies.setter
    def use_exhaustive_dependencies(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithUseExhaustiveDependenciesOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cd51788e13cf60e6104d969bc02fd17b611d29051347c74447382c13f997f47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useExhaustiveDependencies", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useHookAtTopLevel")
    def use_hook_at_top_level(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithDeprecatedHooksOptions"]]:
        '''(experimental) Enforce that all React hooks are being called from the Top Level component functions.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithDeprecatedHooksOptions"]], jsii.get(self, "useHookAtTopLevel"))

    @use_hook_at_top_level.setter
    def use_hook_at_top_level(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithDeprecatedHooksOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30d66c3a8a7fbec8bfd33fd02410c78af2751e156a8741062a33881c01dc0639)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useHookAtTopLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useImportExtensions")
    def use_import_extensions(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithUseImportExtensionsOptions"]]:
        '''(experimental) Enforce file extensions for relative imports.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithUseImportExtensionsOptions"]], jsii.get(self, "useImportExtensions"))

    @use_import_extensions.setter
    def use_import_extensions(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithUseImportExtensionsOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__913d910a10af876d6e6755aeaf4a2680e59d9d126c62bde720d3736bb14f507e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useImportExtensions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useIsNan")
    def use_is_nan(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Require calls to isNaN() when checking for NaN.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]], jsii.get(self, "useIsNan"))

    @use_is_nan.setter
    def use_is_nan(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd4a80de3c9ee0f4772368ab9d75b8544676e8a239a3e36895e0b0f6c9bba39b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useIsNan", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useJsxKeyInIterable")
    def use_jsx_key_in_iterable(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow missing key props in iterators/collection literals.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "useJsxKeyInIterable"))

    @use_jsx_key_in_iterable.setter
    def use_jsx_key_in_iterable(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ef40a7236b7c1177932ef2f97d7e7485e347e489b37b26b117e3129a0df147c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useJsxKeyInIterable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useValidForDirection")
    def use_valid_for_direction(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Enforce "for" loop update clause moving the counter in the right direction.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "useValidForDirection"))

    @use_valid_for_direction.setter
    def use_valid_for_direction(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f997c1fcfeefe0ec3614552afc16b1f05575be08e51d6f51b6b2532321384deb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useValidForDirection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useYield")
    def use_yield(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Require generator functions to contain yield.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "useYield"))

    @use_yield.setter
    def use_yield(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__977c3c6c00b3ed0d7cd33a14beefbd8cd0334eba18ef3091a98f04ed5297ebf9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useYield", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ICorrectness).__jsii_proxy_class__ = lambda : _ICorrectnessProxy


@jsii.interface(jsii_type="projen.javascript.biome_config.ICssAssists")
class ICssAssists(typing_extensions.Protocol):
    '''(experimental) Options that changes how the CSS assists behaves.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Control the assists for CSS files.

        :stability: experimental
        '''
        ...

    @enabled.setter
    def enabled(self, value: typing.Optional[builtins.bool]) -> None:
        ...


class _ICssAssistsProxy:
    '''(experimental) Options that changes how the CSS assists behaves.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.ICssAssists"

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Control the assists for CSS files.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9162ac26e13aedac41c42ce0e33b611d2267b8120b2fff01334415e34089327)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ICssAssists).__jsii_proxy_class__ = lambda : _ICssAssistsProxy


@jsii.interface(jsii_type="projen.javascript.biome_config.ICssConfiguration")
class ICssConfiguration(typing_extensions.Protocol):
    '''(experimental) Options applied to CSS files.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="assists")
    def assists(self) -> typing.Optional[ICssAssists]:
        '''(experimental) CSS assists options.

        :stability: experimental
        '''
        ...

    @assists.setter
    def assists(self, value: typing.Optional[ICssAssists]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="formatter")
    def formatter(self) -> typing.Optional["ICssFormatter"]:
        '''(experimental) CSS formatter options.

        :stability: experimental
        '''
        ...

    @formatter.setter
    def formatter(self, value: typing.Optional["ICssFormatter"]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="linter")
    def linter(self) -> typing.Optional["ICssLinter"]:
        '''(experimental) CSS linter options.

        :stability: experimental
        '''
        ...

    @linter.setter
    def linter(self, value: typing.Optional["ICssLinter"]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="parser")
    def parser(self) -> typing.Optional["ICssParser"]:
        '''(experimental) CSS parsing options.

        :stability: experimental
        '''
        ...

    @parser.setter
    def parser(self, value: typing.Optional["ICssParser"]) -> None:
        ...


class _ICssConfigurationProxy:
    '''(experimental) Options applied to CSS files.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.ICssConfiguration"

    @builtins.property
    @jsii.member(jsii_name="assists")
    def assists(self) -> typing.Optional[ICssAssists]:
        '''(experimental) CSS assists options.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[ICssAssists], jsii.get(self, "assists"))

    @assists.setter
    def assists(self, value: typing.Optional[ICssAssists]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__487c70f5b2d664fc2514c6eede115a76cb4ad442396c5cde40ae2f89bd33cd68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assists", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="formatter")
    def formatter(self) -> typing.Optional["ICssFormatter"]:
        '''(experimental) CSS formatter options.

        :stability: experimental
        '''
        return typing.cast(typing.Optional["ICssFormatter"], jsii.get(self, "formatter"))

    @formatter.setter
    def formatter(self, value: typing.Optional["ICssFormatter"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb25e6f8e596223545eddbde666181453deb9b3d041516cfba145e4f1901d8ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "formatter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="linter")
    def linter(self) -> typing.Optional["ICssLinter"]:
        '''(experimental) CSS linter options.

        :stability: experimental
        '''
        return typing.cast(typing.Optional["ICssLinter"], jsii.get(self, "linter"))

    @linter.setter
    def linter(self, value: typing.Optional["ICssLinter"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d76b753d915d1a9b1cb7370b1b921317d51e5dc7c632f314525056f0b3c3ad9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "linter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parser")
    def parser(self) -> typing.Optional["ICssParser"]:
        '''(experimental) CSS parsing options.

        :stability: experimental
        '''
        return typing.cast(typing.Optional["ICssParser"], jsii.get(self, "parser"))

    @parser.setter
    def parser(self, value: typing.Optional["ICssParser"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3b9568cfd2347f24e1f4780a7f81ee8659da36ee2cdd88636adaf6d0d3ffaa6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parser", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ICssConfiguration).__jsii_proxy_class__ = lambda : _ICssConfigurationProxy


@jsii.interface(jsii_type="projen.javascript.biome_config.ICssFormatter")
class ICssFormatter(typing_extensions.Protocol):
    '''(experimental) Options that changes how the CSS formatter behaves.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Control the formatter for CSS (and its super languages) files.

        :stability: experimental
        '''
        ...

    @enabled.setter
    def enabled(self, value: typing.Optional[builtins.bool]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="indentStyle")
    def indent_style(self) -> typing.Optional[builtins.str]:
        '''(experimental) The indent style applied to CSS (and its super languages) files.

        :stability: experimental
        '''
        ...

    @indent_style.setter
    def indent_style(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="indentWidth")
    def indent_width(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The size of the indentation applied to CSS (and its super languages) files.

        Default to 2.

        :stability: experimental
        '''
        ...

    @indent_width.setter
    def indent_width(self, value: typing.Optional[jsii.Number]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="lineEnding")
    def line_ending(self) -> typing.Optional[builtins.str]:
        '''(experimental) The type of line ending applied to CSS (and its super languages) files.

        :stability: experimental
        '''
        ...

    @line_ending.setter
    def line_ending(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="lineWidth")
    def line_width(self) -> typing.Optional[jsii.Number]:
        '''(experimental) What's the max width of a line applied to CSS (and its super languages) files.

        Defaults to 80.

        :stability: experimental
        '''
        ...

    @line_width.setter
    def line_width(self, value: typing.Optional[jsii.Number]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="quoteStyle")
    def quote_style(self) -> typing.Optional[builtins.str]:
        '''(experimental) The type of quotes used in CSS code.

        Defaults to double.

        :stability: experimental
        '''
        ...

    @quote_style.setter
    def quote_style(self, value: typing.Optional[builtins.str]) -> None:
        ...


class _ICssFormatterProxy:
    '''(experimental) Options that changes how the CSS formatter behaves.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.ICssFormatter"

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Control the formatter for CSS (and its super languages) files.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da44ebc43ae17626208347d92527115b6fe58d918f02f99546c6f1a60b170ca8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="indentStyle")
    def indent_style(self) -> typing.Optional[builtins.str]:
        '''(experimental) The indent style applied to CSS (and its super languages) files.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "indentStyle"))

    @indent_style.setter
    def indent_style(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6650589045d9bb4095648ddd4fab08f0213c0f063d64d361945e89d43e10b055)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "indentStyle", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="indentWidth")
    def indent_width(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The size of the indentation applied to CSS (and its super languages) files.

        Default to 2.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "indentWidth"))

    @indent_width.setter
    def indent_width(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6aa855ff702add215c5f6d36015ffb9140e5a7e7efe72544de60ab4f63c6e765)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "indentWidth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lineEnding")
    def line_ending(self) -> typing.Optional[builtins.str]:
        '''(experimental) The type of line ending applied to CSS (and its super languages) files.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lineEnding"))

    @line_ending.setter
    def line_ending(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce3a6673120c30bff3a22cb4c6525841ab58fb2b5776144ed71a33cef73cf451)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lineEnding", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lineWidth")
    def line_width(self) -> typing.Optional[jsii.Number]:
        '''(experimental) What's the max width of a line applied to CSS (and its super languages) files.

        Defaults to 80.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "lineWidth"))

    @line_width.setter
    def line_width(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebeca7bf2c8f499bd285a378b385d51922eb483013ec751d5406d1e0fc1cd04c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lineWidth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="quoteStyle")
    def quote_style(self) -> typing.Optional[builtins.str]:
        '''(experimental) The type of quotes used in CSS code.

        Defaults to double.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "quoteStyle"))

    @quote_style.setter
    def quote_style(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c267c92c158ea788c22709e05c1d726a644977b8b72d4faef17c024a23f27992)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "quoteStyle", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ICssFormatter).__jsii_proxy_class__ = lambda : _ICssFormatterProxy


@jsii.interface(jsii_type="projen.javascript.biome_config.ICssLinter")
class ICssLinter(typing_extensions.Protocol):
    '''(experimental) Options that changes how the CSS linter behaves.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Control the linter for CSS files.

        :stability: experimental
        '''
        ...

    @enabled.setter
    def enabled(self, value: typing.Optional[builtins.bool]) -> None:
        ...


class _ICssLinterProxy:
    '''(experimental) Options that changes how the CSS linter behaves.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.ICssLinter"

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Control the linter for CSS files.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5583a36866f3f1f076f9f203158837ccd46c343586156989718a644e5980afe8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ICssLinter).__jsii_proxy_class__ = lambda : _ICssLinterProxy


@jsii.interface(jsii_type="projen.javascript.biome_config.ICssParser")
class ICssParser(typing_extensions.Protocol):
    '''(experimental) Options that changes how the CSS parser behaves.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="allowWrongLineComments")
    def allow_wrong_line_comments(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Allow comments to appear on incorrect lines in ``.css`` files.

        :stability: experimental
        '''
        ...

    @allow_wrong_line_comments.setter
    def allow_wrong_line_comments(self, value: typing.Optional[builtins.bool]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="cssModules")
    def css_modules(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables parsing of CSS Modules specific features.

        :stability: experimental
        '''
        ...

    @css_modules.setter
    def css_modules(self, value: typing.Optional[builtins.bool]) -> None:
        ...


class _ICssParserProxy:
    '''(experimental) Options that changes how the CSS parser behaves.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.ICssParser"

    @builtins.property
    @jsii.member(jsii_name="allowWrongLineComments")
    def allow_wrong_line_comments(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Allow comments to appear on incorrect lines in ``.css`` files.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "allowWrongLineComments"))

    @allow_wrong_line_comments.setter
    def allow_wrong_line_comments(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f69ffc8bef31249014c76894af04f2eaa4e8991ed39bf656007dcd48f6cc5b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowWrongLineComments", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cssModules")
    def css_modules(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables parsing of CSS Modules specific features.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "cssModules"))

    @css_modules.setter
    def css_modules(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e3eb219f02034287491a4901eaee4a6defdd94eda119e20c513a82862740657)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cssModules", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ICssParser).__jsii_proxy_class__ = lambda : _ICssParserProxy


@jsii.interface(
    jsii_type="projen.javascript.biome_config.ICustomRestrictedTypeOptions"
)
class ICustomRestrictedTypeOptions(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="message")
    def message(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        ...

    @message.setter
    def message(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="use")
    def use(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        ...

    @use.setter
    def use(self, value: typing.Optional[builtins.str]) -> None:
        ...


class _ICustomRestrictedTypeOptionsProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.ICustomRestrictedTypeOptions"

    @builtins.property
    @jsii.member(jsii_name="message")
    def message(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "message"))

    @message.setter
    def message(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bdb089598bfbe59ce11b0286a4ac4e6e74e6dbe60eca9d4b0060e44160bc77d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "message", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="use")
    def use(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "use"))

    @use.setter
    def use(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3188d9cc6adecf012f900ec5cd4bdf4132b6be97b89212e78f0262a3fd7d8d95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "use", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ICustomRestrictedTypeOptions).__jsii_proxy_class__ = lambda : _ICustomRestrictedTypeOptionsProxy


@jsii.interface(jsii_type="projen.javascript.biome_config.IDeprecatedHooksOptions")
class IDeprecatedHooksOptions(typing_extensions.Protocol):
    '''(experimental) Options for the ``useHookAtTopLevel`` rule have been deprecated, since we now use the React hook naming convention to determine whether a function is a hook.

    :stability: experimental
    '''

    pass


class _IDeprecatedHooksOptionsProxy:
    '''(experimental) Options for the ``useHookAtTopLevel`` rule have been deprecated, since we now use the React hook naming convention to determine whether a function is a hook.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.IDeprecatedHooksOptions"
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IDeprecatedHooksOptions).__jsii_proxy_class__ = lambda : _IDeprecatedHooksOptionsProxy


@jsii.interface(
    jsii_type="projen.javascript.biome_config.IFilenamingConventionOptions"
)
class IFilenamingConventionOptions(typing_extensions.Protocol):
    '''(experimental) Rule's options.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="filenameCases")
    def filename_cases(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Allowed cases for file names.

        :stability: experimental
        '''
        ...

    @filename_cases.setter
    def filename_cases(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="requireAscii")
    def require_ascii(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If ``false``, then non-ASCII characters are allowed.

        :stability: experimental
        '''
        ...

    @require_ascii.setter
    def require_ascii(self, value: typing.Optional[builtins.bool]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="strictCase")
    def strict_case(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If ``false``, then consecutive uppercase are allowed in *camel* and *pascal* cases.

        This does not affect other [Case].

        :stability: experimental
        '''
        ...

    @strict_case.setter
    def strict_case(self, value: typing.Optional[builtins.bool]) -> None:
        ...


class _IFilenamingConventionOptionsProxy:
    '''(experimental) Rule's options.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.IFilenamingConventionOptions"

    @builtins.property
    @jsii.member(jsii_name="filenameCases")
    def filename_cases(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Allowed cases for file names.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "filenameCases"))

    @filename_cases.setter
    def filename_cases(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34f451e57c6bca38e791cc9ad0267d95804c1bc3027fd03471fff3289323506e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filenameCases", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requireAscii")
    def require_ascii(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If ``false``, then non-ASCII characters are allowed.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "requireAscii"))

    @require_ascii.setter
    def require_ascii(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb00409d724c1a7e7ed80d0cc68a35a13abd05751c36f583d1374a36153f6cae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requireAscii", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="strictCase")
    def strict_case(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If ``false``, then consecutive uppercase are allowed in *camel* and *pascal* cases.

        This does not affect other [Case].

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "strictCase"))

    @strict_case.setter
    def strict_case(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4406b322dbff8e88493af5dd8879d3794c4e8fb5db5ca25ec60737431b18ef75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "strictCase", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IFilenamingConventionOptions).__jsii_proxy_class__ = lambda : _IFilenamingConventionOptionsProxy


@jsii.interface(jsii_type="projen.javascript.biome_config.IFilesConfiguration")
class IFilesConfiguration(typing_extensions.Protocol):
    '''(experimental) The configuration of the filesystem.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="ignore")
    def ignore(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of Unix shell style patterns.

        Biome will ignore files/folders that will match these patterns.

        :stability: experimental
        '''
        ...

    @ignore.setter
    def ignore(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="ignoreUnknown")
    def ignore_unknown(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Tells Biome to not emit diagnostics when handling files that doesn't know.

        :stability: experimental
        '''
        ...

    @ignore_unknown.setter
    def ignore_unknown(self, value: typing.Optional[builtins.bool]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="include")
    def include(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of Unix shell style patterns.

        Biome will handle only those files/folders that will match these patterns.

        :stability: experimental
        '''
        ...

    @include.setter
    def include(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="maxSize")
    def max_size(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The maximum allowed size for source code files in bytes.

        Files above this limit will be ignored for performance reasons. Defaults to 1 MiB

        :stability: experimental
        '''
        ...

    @max_size.setter
    def max_size(self, value: typing.Optional[jsii.Number]) -> None:
        ...


class _IFilesConfigurationProxy:
    '''(experimental) The configuration of the filesystem.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.IFilesConfiguration"

    @builtins.property
    @jsii.member(jsii_name="ignore")
    def ignore(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of Unix shell style patterns.

        Biome will ignore files/folders that will match these patterns.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "ignore"))

    @ignore.setter
    def ignore(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78032ae2b8140aff1b483509b8f36df2b2dcc90dc5ffb186a4360afc22288339)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignore", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ignoreUnknown")
    def ignore_unknown(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Tells Biome to not emit diagnostics when handling files that doesn't know.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "ignoreUnknown"))

    @ignore_unknown.setter
    def ignore_unknown(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2fad0b2aa22cc3334df1681a006e0f5a11125961cde1b9a8fa71d5a2eef8eed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreUnknown", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="include")
    def include(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of Unix shell style patterns.

        Biome will handle only those files/folders that will match these patterns.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "include"))

    @include.setter
    def include(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e230182b0d61868f918e621eb114d5f7c19b14ee6cb50c5e3a39ce23416df5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "include", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxSize")
    def max_size(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The maximum allowed size for source code files in bytes.

        Files above this limit will be ignored for performance reasons. Defaults to 1 MiB

        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxSize"))

    @max_size.setter
    def max_size(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f911b12dfd866d82d08d9540818d97620d787c8910162b295a80895e06dd1a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxSize", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IFilesConfiguration).__jsii_proxy_class__ = lambda : _IFilesConfigurationProxy


@jsii.interface(jsii_type="projen.javascript.biome_config.IFormatterConfiguration")
class IFormatterConfiguration(typing_extensions.Protocol):
    '''(experimental) Generic options applied to all files.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="attributePosition")
    def attribute_position(self) -> typing.Optional[builtins.str]:
        '''(experimental) The attribute position style in HTMLish languages.

        By default auto.

        :stability: experimental
        '''
        ...

    @attribute_position.setter
    def attribute_position(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="bracketSpacing")
    def bracket_spacing(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to insert spaces around brackets in object literals.

        Defaults to true.

        :stability: experimental
        '''
        ...

    @bracket_spacing.setter
    def bracket_spacing(self, value: typing.Optional[builtins.bool]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        ...

    @enabled.setter
    def enabled(self, value: typing.Optional[builtins.bool]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="formatWithErrors")
    def format_with_errors(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Stores whether formatting should be allowed to proceed if a given file has syntax errors.

        :stability: experimental
        '''
        ...

    @format_with_errors.setter
    def format_with_errors(self, value: typing.Optional[builtins.bool]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="ignore")
    def ignore(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of Unix shell style patterns.

        The formatter will ignore files/folders that will match these patterns.

        :stability: experimental
        '''
        ...

    @ignore.setter
    def ignore(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="include")
    def include(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of Unix shell style patterns.

        The formatter will include files/folders that will match these patterns.

        :stability: experimental
        '''
        ...

    @include.setter
    def include(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="indentSize")
    def indent_size(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The size of the indentation, 2 by default (deprecated, use ``indent-width``).

        :stability: experimental
        '''
        ...

    @indent_size.setter
    def indent_size(self, value: typing.Optional[jsii.Number]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="indentStyle")
    def indent_style(self) -> typing.Optional[builtins.str]:
        '''(experimental) The indent style.

        :stability: experimental
        '''
        ...

    @indent_style.setter
    def indent_style(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="indentWidth")
    def indent_width(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The size of the indentation, 2 by default.

        :stability: experimental
        '''
        ...

    @indent_width.setter
    def indent_width(self, value: typing.Optional[jsii.Number]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="lineEnding")
    def line_ending(self) -> typing.Optional[builtins.str]:
        '''(experimental) The type of line ending.

        :stability: experimental
        '''
        ...

    @line_ending.setter
    def line_ending(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="lineWidth")
    def line_width(self) -> typing.Optional[jsii.Number]:
        '''(experimental) What's the max width of a line.

        Defaults to 80.

        :stability: experimental
        '''
        ...

    @line_width.setter
    def line_width(self, value: typing.Optional[jsii.Number]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useEditorconfig")
    def use_editorconfig(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Use any ``.editorconfig`` files to configure the formatter. Configuration in ``biome.json`` will override ``.editorconfig`` configuration. Default: false.

        :stability: experimental
        '''
        ...

    @use_editorconfig.setter
    def use_editorconfig(self, value: typing.Optional[builtins.bool]) -> None:
        ...


class _IFormatterConfigurationProxy:
    '''(experimental) Generic options applied to all files.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.IFormatterConfiguration"

    @builtins.property
    @jsii.member(jsii_name="attributePosition")
    def attribute_position(self) -> typing.Optional[builtins.str]:
        '''(experimental) The attribute position style in HTMLish languages.

        By default auto.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "attributePosition"))

    @attribute_position.setter
    def attribute_position(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b659e962598791441d86cf45aa838464b033269eb39aad84ef15bf47c945a1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "attributePosition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bracketSpacing")
    def bracket_spacing(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to insert spaces around brackets in object literals.

        Defaults to true.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "bracketSpacing"))

    @bracket_spacing.setter
    def bracket_spacing(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35f886619dcca81c7a317b9ac18a44e01c61eed84cd3341caa8476189efd80d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bracketSpacing", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31daa0e8ca08bb67818df018db531931bf807f8464ee1ae2c263498c22b79a23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="formatWithErrors")
    def format_with_errors(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Stores whether formatting should be allowed to proceed if a given file has syntax errors.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "formatWithErrors"))

    @format_with_errors.setter
    def format_with_errors(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce7b00e72be79d8bbe2f42799c64bc1e8ef9dd2f895325c053d7d4fe3f2f3cee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "formatWithErrors", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ignore")
    def ignore(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of Unix shell style patterns.

        The formatter will ignore files/folders that will match these patterns.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "ignore"))

    @ignore.setter
    def ignore(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d6b05c80808795fdb4766e749ce9c7a7f617f8432472888d14aed7770577e99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignore", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="include")
    def include(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of Unix shell style patterns.

        The formatter will include files/folders that will match these patterns.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "include"))

    @include.setter
    def include(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6874bcbeec6dbf3a3da150a223ad430c9a917857d947fbd18eb808bdb599a737)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "include", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="indentSize")
    def indent_size(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The size of the indentation, 2 by default (deprecated, use ``indent-width``).

        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "indentSize"))

    @indent_size.setter
    def indent_size(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5eb6db758c67cacb60ccc18d54f4a52e75430de65d98b4baa45d4cb69e784d57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "indentSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="indentStyle")
    def indent_style(self) -> typing.Optional[builtins.str]:
        '''(experimental) The indent style.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "indentStyle"))

    @indent_style.setter
    def indent_style(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ce4ee77a7e83ab1cb8761745da8e25852d39e64b9b13e60e0e406a5ec50820c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "indentStyle", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="indentWidth")
    def indent_width(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The size of the indentation, 2 by default.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "indentWidth"))

    @indent_width.setter
    def indent_width(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07b3f4f8ea47774e96dd2e80d16d8e224c90c984ad0049c17861dcf27c7417f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "indentWidth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lineEnding")
    def line_ending(self) -> typing.Optional[builtins.str]:
        '''(experimental) The type of line ending.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lineEnding"))

    @line_ending.setter
    def line_ending(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__299ff1fdcd6f0e8c367b9b997b902a3ef995a7e399f216da199d338bada65aae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lineEnding", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lineWidth")
    def line_width(self) -> typing.Optional[jsii.Number]:
        '''(experimental) What's the max width of a line.

        Defaults to 80.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "lineWidth"))

    @line_width.setter
    def line_width(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6aaa599169edfb63c965be53d5006d75f3561c5f6dad52b9841b0ceddadeab01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lineWidth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useEditorconfig")
    def use_editorconfig(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Use any ``.editorconfig`` files to configure the formatter. Configuration in ``biome.json`` will override ``.editorconfig`` configuration. Default: false.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "useEditorconfig"))

    @use_editorconfig.setter
    def use_editorconfig(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcc775927c735486dcacbf59adf19bef48422bb2dc6dfc672b3a751f931ebc68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useEditorconfig", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IFormatterConfiguration).__jsii_proxy_class__ = lambda : _IFormatterConfigurationProxy


@jsii.interface(jsii_type="projen.javascript.biome_config.IGraphqlConfiguration")
class IGraphqlConfiguration(typing_extensions.Protocol):
    '''(experimental) Options applied to GraphQL files.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="formatter")
    def formatter(self) -> typing.Optional["IGraphqlFormatter"]:
        '''(experimental) GraphQL formatter options.

        :stability: experimental
        '''
        ...

    @formatter.setter
    def formatter(self, value: typing.Optional["IGraphqlFormatter"]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="linter")
    def linter(self) -> typing.Optional["IGraphqlLinter"]:
        '''
        :stability: experimental
        '''
        ...

    @linter.setter
    def linter(self, value: typing.Optional["IGraphqlLinter"]) -> None:
        ...


class _IGraphqlConfigurationProxy:
    '''(experimental) Options applied to GraphQL files.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.IGraphqlConfiguration"

    @builtins.property
    @jsii.member(jsii_name="formatter")
    def formatter(self) -> typing.Optional["IGraphqlFormatter"]:
        '''(experimental) GraphQL formatter options.

        :stability: experimental
        '''
        return typing.cast(typing.Optional["IGraphqlFormatter"], jsii.get(self, "formatter"))

    @formatter.setter
    def formatter(self, value: typing.Optional["IGraphqlFormatter"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea6ed61a12ed032e550a7325f3e520e15f49dddd7761bbdee2a7bb7e22475ff5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "formatter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="linter")
    def linter(self) -> typing.Optional["IGraphqlLinter"]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional["IGraphqlLinter"], jsii.get(self, "linter"))

    @linter.setter
    def linter(self, value: typing.Optional["IGraphqlLinter"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97f5b7dde3d54d91c19d7a20ecc9ab2c9b0d3e4014e6c91ca2c84f16391b9210)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "linter", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IGraphqlConfiguration).__jsii_proxy_class__ = lambda : _IGraphqlConfigurationProxy


@jsii.interface(jsii_type="projen.javascript.biome_config.IGraphqlFormatter")
class IGraphqlFormatter(typing_extensions.Protocol):
    '''(experimental) Options that changes how the GraphQL formatter behaves.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="bracketSpacing")
    def bracket_spacing(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to insert spaces around brackets in object literals.

        Defaults to true.

        :stability: experimental
        '''
        ...

    @bracket_spacing.setter
    def bracket_spacing(self, value: typing.Optional[builtins.bool]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Control the formatter for GraphQL files.

        :stability: experimental
        '''
        ...

    @enabled.setter
    def enabled(self, value: typing.Optional[builtins.bool]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="indentStyle")
    def indent_style(self) -> typing.Optional[builtins.str]:
        '''(experimental) The indent style applied to GraphQL files.

        :stability: experimental
        '''
        ...

    @indent_style.setter
    def indent_style(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="indentWidth")
    def indent_width(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The size of the indentation applied to GraphQL files.

        Default to 2.

        :stability: experimental
        '''
        ...

    @indent_width.setter
    def indent_width(self, value: typing.Optional[jsii.Number]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="lineEnding")
    def line_ending(self) -> typing.Optional[builtins.str]:
        '''(experimental) The type of line ending applied to GraphQL files.

        :stability: experimental
        '''
        ...

    @line_ending.setter
    def line_ending(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="lineWidth")
    def line_width(self) -> typing.Optional[jsii.Number]:
        '''(experimental) What's the max width of a line applied to GraphQL files.

        Defaults to 80.

        :stability: experimental
        '''
        ...

    @line_width.setter
    def line_width(self, value: typing.Optional[jsii.Number]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="quoteStyle")
    def quote_style(self) -> typing.Optional[builtins.str]:
        '''(experimental) The type of quotes used in GraphQL code.

        Defaults to double.

        :stability: experimental
        '''
        ...

    @quote_style.setter
    def quote_style(self, value: typing.Optional[builtins.str]) -> None:
        ...


class _IGraphqlFormatterProxy:
    '''(experimental) Options that changes how the GraphQL formatter behaves.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.IGraphqlFormatter"

    @builtins.property
    @jsii.member(jsii_name="bracketSpacing")
    def bracket_spacing(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to insert spaces around brackets in object literals.

        Defaults to true.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "bracketSpacing"))

    @bracket_spacing.setter
    def bracket_spacing(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99b3e53fce7d0a506392529be98ce0a33e011ee2377f82cc006c8a96da9f205d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bracketSpacing", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Control the formatter for GraphQL files.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__873478ced7f5372e2483dcec81f2062819d7afddbd6cad4c2d900bbe7f0da81e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="indentStyle")
    def indent_style(self) -> typing.Optional[builtins.str]:
        '''(experimental) The indent style applied to GraphQL files.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "indentStyle"))

    @indent_style.setter
    def indent_style(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee042c564f228d57470975db311ffe0676385f1a6cc3a010be8170f08ae2626d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "indentStyle", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="indentWidth")
    def indent_width(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The size of the indentation applied to GraphQL files.

        Default to 2.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "indentWidth"))

    @indent_width.setter
    def indent_width(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d004e786d8dd735d54009dede2edb69b34b592fec0d0390cee3bc0a317381d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "indentWidth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lineEnding")
    def line_ending(self) -> typing.Optional[builtins.str]:
        '''(experimental) The type of line ending applied to GraphQL files.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lineEnding"))

    @line_ending.setter
    def line_ending(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d736bf8ca577846f23a09409db240dd3ae393286196a082c622f12ec4873c1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lineEnding", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lineWidth")
    def line_width(self) -> typing.Optional[jsii.Number]:
        '''(experimental) What's the max width of a line applied to GraphQL files.

        Defaults to 80.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "lineWidth"))

    @line_width.setter
    def line_width(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__843d929ef1c01009114e6ebf8c2041c926aa89d2d22cf8f5544fdba0d9cbb77a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lineWidth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="quoteStyle")
    def quote_style(self) -> typing.Optional[builtins.str]:
        '''(experimental) The type of quotes used in GraphQL code.

        Defaults to double.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "quoteStyle"))

    @quote_style.setter
    def quote_style(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54aa923e26579938ecae34290cf4c0e2d9b754da8493b2e37e44d3daa0f9fad9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "quoteStyle", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IGraphqlFormatter).__jsii_proxy_class__ = lambda : _IGraphqlFormatterProxy


@jsii.interface(jsii_type="projen.javascript.biome_config.IGraphqlLinter")
class IGraphqlLinter(typing_extensions.Protocol):
    '''(experimental) Options that changes how the GraphQL linter behaves.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Control the formatter for GraphQL files.

        :stability: experimental
        '''
        ...

    @enabled.setter
    def enabled(self, value: typing.Optional[builtins.bool]) -> None:
        ...


class _IGraphqlLinterProxy:
    '''(experimental) Options that changes how the GraphQL linter behaves.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.IGraphqlLinter"

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Control the formatter for GraphQL files.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bde9aa9118e52045889d9bd7b2391615f8f2bbe7b0efba43b236e98fce4727a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IGraphqlLinter).__jsii_proxy_class__ = lambda : _IGraphqlLinterProxy


@jsii.interface(jsii_type="projen.javascript.biome_config.IHook")
class IHook(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="closureIndex")
    def closure_index(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The "position" of the closure function, starting from zero.

        For example, for React's ``useEffect()`` hook, the closure index is 0.

        :stability: experimental
        '''
        ...

    @closure_index.setter
    def closure_index(self, value: typing.Optional[jsii.Number]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="dependenciesIndex")
    def dependencies_index(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The "position" of the array of dependencies, starting from zero.

        For example, for React's ``useEffect()`` hook, the dependencies index is 1.

        :stability: experimental
        '''
        ...

    @dependencies_index.setter
    def dependencies_index(self, value: typing.Optional[jsii.Number]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the hook.

        :stability: experimental
        '''
        ...

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="stableResult")
    def stable_result(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, typing.List[jsii.Number]]]:
        '''(experimental) Whether the result of the hook is stable.

        Set to ``true`` to mark the identity of the hook's return value as stable, or use a number/an array of numbers to mark the "positions" in the return array as stable.

        For example, for React's ``useRef()`` hook the value would be ``true``, while for ``useState()`` it would be ``[1]``.

        :stability: experimental
        '''
        ...

    @stable_result.setter
    def stable_result(
        self,
        value: typing.Optional[typing.Union[builtins.bool, typing.List[jsii.Number]]],
    ) -> None:
        ...


class _IHookProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.IHook"

    @builtins.property
    @jsii.member(jsii_name="closureIndex")
    def closure_index(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The "position" of the closure function, starting from zero.

        For example, for React's ``useEffect()`` hook, the closure index is 0.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "closureIndex"))

    @closure_index.setter
    def closure_index(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b23204701303e2bbf936eff96bc0476cd451078bca7cc49b0e9a98eb6d07b972)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "closureIndex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dependenciesIndex")
    def dependencies_index(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The "position" of the array of dependencies, starting from zero.

        For example, for React's ``useEffect()`` hook, the dependencies index is 1.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dependenciesIndex"))

    @dependencies_index.setter
    def dependencies_index(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2038e99f6017f032f2a39137b6391b37e426c1c3f2ee17a1014b7561978468a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dependenciesIndex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the hook.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c40013ce6f8ef554264029ad597e25158a7076f4bb026fc38c0428cc83c169b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stableResult")
    def stable_result(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, typing.List[jsii.Number]]]:
        '''(experimental) Whether the result of the hook is stable.

        Set to ``true`` to mark the identity of the hook's return value as stable, or use a number/an array of numbers to mark the "positions" in the return array as stable.

        For example, for React's ``useRef()`` hook the value would be ``true``, while for ``useState()`` it would be ``[1]``.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, typing.List[jsii.Number]]], jsii.get(self, "stableResult"))

    @stable_result.setter
    def stable_result(
        self,
        value: typing.Optional[typing.Union[builtins.bool, typing.List[jsii.Number]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ffa991e90af0407fa545c66b2c49cbbec83808e4c82b9b0e89d9c60448ede05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stableResult", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IHook).__jsii_proxy_class__ = lambda : _IHookProxy


@jsii.interface(jsii_type="projen.javascript.biome_config.IJavascriptAssists")
class IJavascriptAssists(typing_extensions.Protocol):
    '''(experimental) Linter options specific to the JavaScript linter.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Control the linter for JavaScript (and its super languages) files.

        :stability: experimental
        '''
        ...

    @enabled.setter
    def enabled(self, value: typing.Optional[builtins.bool]) -> None:
        ...


class _IJavascriptAssistsProxy:
    '''(experimental) Linter options specific to the JavaScript linter.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.IJavascriptAssists"

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Control the linter for JavaScript (and its super languages) files.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9e8bd2a6062d2431a84fa40c0f5fec47c1e6dfc4b76651d376a40412f802f72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IJavascriptAssists).__jsii_proxy_class__ = lambda : _IJavascriptAssistsProxy


@jsii.interface(jsii_type="projen.javascript.biome_config.IJavascriptConfiguration")
class IJavascriptConfiguration(typing_extensions.Protocol):
    '''(experimental) A set of options applied to the JavaScript files.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="assists")
    def assists(self) -> typing.Optional[IJavascriptAssists]:
        '''(experimental) Assists options.

        :stability: experimental
        '''
        ...

    @assists.setter
    def assists(self, value: typing.Optional[IJavascriptAssists]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="formatter")
    def formatter(self) -> typing.Optional["IJavascriptFormatter"]:
        '''(experimental) Formatting options.

        :stability: experimental
        '''
        ...

    @formatter.setter
    def formatter(self, value: typing.Optional["IJavascriptFormatter"]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="globals")
    def globals(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of global bindings that should be ignored by the analyzers.

        If defined here, they should not emit diagnostics.

        :stability: experimental
        '''
        ...

    @globals.setter
    def globals(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="jsxRuntime")
    def jsx_runtime(self) -> typing.Optional[builtins.str]:
        '''(experimental) Indicates the type of runtime or transformation used for interpreting JSX.

        :stability: experimental
        '''
        ...

    @jsx_runtime.setter
    def jsx_runtime(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="linter")
    def linter(self) -> typing.Optional["IJavascriptLinter"]:
        '''(experimental) Linter options.

        :stability: experimental
        '''
        ...

    @linter.setter
    def linter(self, value: typing.Optional["IJavascriptLinter"]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="organizeImports")
    def organize_imports(self) -> typing.Optional["IJavascriptOrganizeImports"]:
        '''
        :stability: experimental
        '''
        ...

    @organize_imports.setter
    def organize_imports(
        self,
        value: typing.Optional["IJavascriptOrganizeImports"],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="parser")
    def parser(self) -> typing.Optional["IJavascriptParser"]:
        '''(experimental) Parsing options.

        :stability: experimental
        '''
        ...

    @parser.setter
    def parser(self, value: typing.Optional["IJavascriptParser"]) -> None:
        ...


class _IJavascriptConfigurationProxy:
    '''(experimental) A set of options applied to the JavaScript files.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.IJavascriptConfiguration"

    @builtins.property
    @jsii.member(jsii_name="assists")
    def assists(self) -> typing.Optional[IJavascriptAssists]:
        '''(experimental) Assists options.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[IJavascriptAssists], jsii.get(self, "assists"))

    @assists.setter
    def assists(self, value: typing.Optional[IJavascriptAssists]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df7775e52cecc3d9e508cfd21ad8c5f20ac8b041c2ec5173ac619773f18f0041)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assists", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="formatter")
    def formatter(self) -> typing.Optional["IJavascriptFormatter"]:
        '''(experimental) Formatting options.

        :stability: experimental
        '''
        return typing.cast(typing.Optional["IJavascriptFormatter"], jsii.get(self, "formatter"))

    @formatter.setter
    def formatter(self, value: typing.Optional["IJavascriptFormatter"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d6a6596e673ae8a28a21f90d71a18f1db2dfa6a675f0e4ec0059010f6ff1178)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "formatter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="globals")
    def globals(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of global bindings that should be ignored by the analyzers.

        If defined here, they should not emit diagnostics.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "globals"))

    @globals.setter
    def globals(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eafbd538d9f407787a059d9a833b689afd039cde5689eaaef5471954c0c11902)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "globals", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jsxRuntime")
    def jsx_runtime(self) -> typing.Optional[builtins.str]:
        '''(experimental) Indicates the type of runtime or transformation used for interpreting JSX.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "jsxRuntime"))

    @jsx_runtime.setter
    def jsx_runtime(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acfaa9c56a2c25659e2e9aeb5348aa58e11ea5edb8b53854a57f3e382d996422)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jsxRuntime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="linter")
    def linter(self) -> typing.Optional["IJavascriptLinter"]:
        '''(experimental) Linter options.

        :stability: experimental
        '''
        return typing.cast(typing.Optional["IJavascriptLinter"], jsii.get(self, "linter"))

    @linter.setter
    def linter(self, value: typing.Optional["IJavascriptLinter"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__830e7fa8c182d2b1cdf2f33ea8b432be2fce658716588754fa65ea4d93e82a99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "linter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="organizeImports")
    def organize_imports(self) -> typing.Optional["IJavascriptOrganizeImports"]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional["IJavascriptOrganizeImports"], jsii.get(self, "organizeImports"))

    @organize_imports.setter
    def organize_imports(
        self,
        value: typing.Optional["IJavascriptOrganizeImports"],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca952e37b38f4f82ff37dfa6599ed597e58286b38c7803860170876f7c10d53b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "organizeImports", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parser")
    def parser(self) -> typing.Optional["IJavascriptParser"]:
        '''(experimental) Parsing options.

        :stability: experimental
        '''
        return typing.cast(typing.Optional["IJavascriptParser"], jsii.get(self, "parser"))

    @parser.setter
    def parser(self, value: typing.Optional["IJavascriptParser"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15f2169a77f15045edcc320552ca364d5c1a5345761f3fed02785ec92426d589)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parser", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IJavascriptConfiguration).__jsii_proxy_class__ = lambda : _IJavascriptConfigurationProxy


@jsii.interface(jsii_type="projen.javascript.biome_config.IJavascriptFormatter")
class IJavascriptFormatter(typing_extensions.Protocol):
    '''(experimental) Formatting options specific to the JavaScript files.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="arrowParentheses")
    def arrow_parentheses(self) -> typing.Optional[builtins.str]:
        '''(experimental) Whether to add non-necessary parentheses to arrow functions.

        Defaults to "always".

        :stability: experimental
        '''
        ...

    @arrow_parentheses.setter
    def arrow_parentheses(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="attributePosition")
    def attribute_position(self) -> typing.Optional[builtins.str]:
        '''(experimental) The attribute position style in jsx elements.

        Defaults to auto.

        :stability: experimental
        '''
        ...

    @attribute_position.setter
    def attribute_position(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="bracketSameLine")
    def bracket_same_line(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to hug the closing bracket of multiline HTML/JSX tags to the end of the last line, rather than being alone on the following line.

        Defaults to false.

        :stability: experimental
        '''
        ...

    @bracket_same_line.setter
    def bracket_same_line(self, value: typing.Optional[builtins.bool]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="bracketSpacing")
    def bracket_spacing(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to insert spaces around brackets in object literals.

        Defaults to true.

        :stability: experimental
        '''
        ...

    @bracket_spacing.setter
    def bracket_spacing(self, value: typing.Optional[builtins.bool]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Control the formatter for JavaScript (and its super languages) files.

        :stability: experimental
        '''
        ...

    @enabled.setter
    def enabled(self, value: typing.Optional[builtins.bool]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="indentSize")
    def indent_size(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The size of the indentation applied to JavaScript (and its super languages) files.

        Default to 2.

        :stability: experimental
        '''
        ...

    @indent_size.setter
    def indent_size(self, value: typing.Optional[jsii.Number]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="indentStyle")
    def indent_style(self) -> typing.Optional[builtins.str]:
        '''(experimental) The indent style applied to JavaScript (and its super languages) files.

        :stability: experimental
        '''
        ...

    @indent_style.setter
    def indent_style(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="indentWidth")
    def indent_width(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The size of the indentation applied to JavaScript (and its super languages) files.

        Default to 2.

        :stability: experimental
        '''
        ...

    @indent_width.setter
    def indent_width(self, value: typing.Optional[jsii.Number]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="jsxQuoteStyle")
    def jsx_quote_style(self) -> typing.Optional[builtins.str]:
        '''(experimental) The type of quotes used in JSX.

        Defaults to double.

        :stability: experimental
        '''
        ...

    @jsx_quote_style.setter
    def jsx_quote_style(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="lineEnding")
    def line_ending(self) -> typing.Optional[builtins.str]:
        '''(experimental) The type of line ending applied to JavaScript (and its super languages) files.

        :stability: experimental
        '''
        ...

    @line_ending.setter
    def line_ending(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="lineWidth")
    def line_width(self) -> typing.Optional[jsii.Number]:
        '''(experimental) What's the max width of a line applied to JavaScript (and its super languages) files.

        Defaults to 80.

        :stability: experimental
        '''
        ...

    @line_width.setter
    def line_width(self, value: typing.Optional[jsii.Number]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="quoteProperties")
    def quote_properties(self) -> typing.Optional[builtins.str]:
        '''(experimental) When properties in objects are quoted.

        Defaults to asNeeded.

        :stability: experimental
        '''
        ...

    @quote_properties.setter
    def quote_properties(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="quoteStyle")
    def quote_style(self) -> typing.Optional[builtins.str]:
        '''(experimental) The type of quotes used in JavaScript code.

        Defaults to double.

        :stability: experimental
        '''
        ...

    @quote_style.setter
    def quote_style(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="semicolons")
    def semicolons(self) -> typing.Optional[builtins.str]:
        '''(experimental) Whether the formatter prints semicolons for all statements or only in for statements where it is necessary because of ASI.

        :stability: experimental
        '''
        ...

    @semicolons.setter
    def semicolons(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="trailingComma")
    def trailing_comma(self) -> typing.Optional[builtins.str]:
        '''(experimental) Print trailing commas wherever possible in multi-line comma-separated syntactic structures.

        Defaults to "all".

        :stability: experimental
        '''
        ...

    @trailing_comma.setter
    def trailing_comma(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="trailingCommas")
    def trailing_commas(self) -> typing.Optional[builtins.str]:
        '''(experimental) Print trailing commas wherever possible in multi-line comma-separated syntactic structures.

        Defaults to "all".

        :stability: experimental
        '''
        ...

    @trailing_commas.setter
    def trailing_commas(self, value: typing.Optional[builtins.str]) -> None:
        ...


class _IJavascriptFormatterProxy:
    '''(experimental) Formatting options specific to the JavaScript files.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.IJavascriptFormatter"

    @builtins.property
    @jsii.member(jsii_name="arrowParentheses")
    def arrow_parentheses(self) -> typing.Optional[builtins.str]:
        '''(experimental) Whether to add non-necessary parentheses to arrow functions.

        Defaults to "always".

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "arrowParentheses"))

    @arrow_parentheses.setter
    def arrow_parentheses(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4c33f8f8df506e572000450c81891aefaf38f973c634134f849aeac9a946f5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "arrowParentheses", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="attributePosition")
    def attribute_position(self) -> typing.Optional[builtins.str]:
        '''(experimental) The attribute position style in jsx elements.

        Defaults to auto.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "attributePosition"))

    @attribute_position.setter
    def attribute_position(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a86e37c5f0be9c78c3145f033cbd7eef9862dbc1cee5fb382e133c9c4e54ce1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "attributePosition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bracketSameLine")
    def bracket_same_line(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to hug the closing bracket of multiline HTML/JSX tags to the end of the last line, rather than being alone on the following line.

        Defaults to false.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "bracketSameLine"))

    @bracket_same_line.setter
    def bracket_same_line(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a7ca7714b3ecf7f5ca32352785cc1ae2340c49510bf30887356d06697298538)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bracketSameLine", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bracketSpacing")
    def bracket_spacing(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to insert spaces around brackets in object literals.

        Defaults to true.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "bracketSpacing"))

    @bracket_spacing.setter
    def bracket_spacing(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9895d6a9398ad6f77d0d9c93fe871de803d95267102a4f5c5b8c7555a4dae912)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bracketSpacing", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Control the formatter for JavaScript (and its super languages) files.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64200bff30eafe842e3c02f48d3dd9fc700cf115408d2c6298b137ee0d22e00a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="indentSize")
    def indent_size(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The size of the indentation applied to JavaScript (and its super languages) files.

        Default to 2.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "indentSize"))

    @indent_size.setter
    def indent_size(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__970e4c04ca22cd11930ae9df06700b76d659cd3d90b4b9366cb4053555e246ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "indentSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="indentStyle")
    def indent_style(self) -> typing.Optional[builtins.str]:
        '''(experimental) The indent style applied to JavaScript (and its super languages) files.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "indentStyle"))

    @indent_style.setter
    def indent_style(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abcb7803a33213fed04a1025c761826134ecb6ceaff4ff490403d2fed4f171d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "indentStyle", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="indentWidth")
    def indent_width(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The size of the indentation applied to JavaScript (and its super languages) files.

        Default to 2.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "indentWidth"))

    @indent_width.setter
    def indent_width(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfd5ba625ca78c4d990a31597284f8a50537b36db5d4e349cb42f6bdcf9fdfd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "indentWidth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jsxQuoteStyle")
    def jsx_quote_style(self) -> typing.Optional[builtins.str]:
        '''(experimental) The type of quotes used in JSX.

        Defaults to double.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "jsxQuoteStyle"))

    @jsx_quote_style.setter
    def jsx_quote_style(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__879ff32a863ced9e892e8894793cb3543bac036cf5c6aa14cfbd39e68db61c1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jsxQuoteStyle", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lineEnding")
    def line_ending(self) -> typing.Optional[builtins.str]:
        '''(experimental) The type of line ending applied to JavaScript (and its super languages) files.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lineEnding"))

    @line_ending.setter
    def line_ending(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3967fa3bc2612d47cb8da54af2554566d7e76704708a215418ad794c665b926b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lineEnding", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lineWidth")
    def line_width(self) -> typing.Optional[jsii.Number]:
        '''(experimental) What's the max width of a line applied to JavaScript (and its super languages) files.

        Defaults to 80.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "lineWidth"))

    @line_width.setter
    def line_width(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06889dab4ea04f2d6376e2d5899aa9369e4eb73efa3bee44215d65696505c5d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lineWidth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="quoteProperties")
    def quote_properties(self) -> typing.Optional[builtins.str]:
        '''(experimental) When properties in objects are quoted.

        Defaults to asNeeded.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "quoteProperties"))

    @quote_properties.setter
    def quote_properties(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8d9f95731cdb26d51251fe149b0354fc7b67912ac089fb52a49d7b668beee0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "quoteProperties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="quoteStyle")
    def quote_style(self) -> typing.Optional[builtins.str]:
        '''(experimental) The type of quotes used in JavaScript code.

        Defaults to double.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "quoteStyle"))

    @quote_style.setter
    def quote_style(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b216b77c09f6555266f0bedcdc8f98b19dc174b8252eaea234367e7882527ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "quoteStyle", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="semicolons")
    def semicolons(self) -> typing.Optional[builtins.str]:
        '''(experimental) Whether the formatter prints semicolons for all statements or only in for statements where it is necessary because of ASI.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "semicolons"))

    @semicolons.setter
    def semicolons(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a496627366d4cc1fe8d8c4c4e7659ac71eb94aa06609b36ad8cedb7c0433e8f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "semicolons", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="trailingComma")
    def trailing_comma(self) -> typing.Optional[builtins.str]:
        '''(experimental) Print trailing commas wherever possible in multi-line comma-separated syntactic structures.

        Defaults to "all".

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "trailingComma"))

    @trailing_comma.setter
    def trailing_comma(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46dffee5b48aa02a568a9d75ccb86bf239814830b3d0e49fadfed8475d6a66d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trailingComma", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="trailingCommas")
    def trailing_commas(self) -> typing.Optional[builtins.str]:
        '''(experimental) Print trailing commas wherever possible in multi-line comma-separated syntactic structures.

        Defaults to "all".

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "trailingCommas"))

    @trailing_commas.setter
    def trailing_commas(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__681fd9027b5be8a4772dedbfab97e9699a9b9a08096af47f5dad4127e9246d1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trailingCommas", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IJavascriptFormatter).__jsii_proxy_class__ = lambda : _IJavascriptFormatterProxy


@jsii.interface(jsii_type="projen.javascript.biome_config.IJavascriptLinter")
class IJavascriptLinter(typing_extensions.Protocol):
    '''(experimental) Linter options specific to the JavaScript linter.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Control the linter for JavaScript (and its super languages) files.

        :stability: experimental
        '''
        ...

    @enabled.setter
    def enabled(self, value: typing.Optional[builtins.bool]) -> None:
        ...


class _IJavascriptLinterProxy:
    '''(experimental) Linter options specific to the JavaScript linter.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.IJavascriptLinter"

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Control the linter for JavaScript (and its super languages) files.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54c636b732eb87081fc3dd273bb28c9c652183c34c20bd1c2da7ef30257ae3ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IJavascriptLinter).__jsii_proxy_class__ = lambda : _IJavascriptLinterProxy


@jsii.interface(jsii_type="projen.javascript.biome_config.IJavascriptOrganizeImports")
class IJavascriptOrganizeImports(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    pass


class _IJavascriptOrganizeImportsProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.IJavascriptOrganizeImports"
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IJavascriptOrganizeImports).__jsii_proxy_class__ = lambda : _IJavascriptOrganizeImportsProxy


@jsii.interface(jsii_type="projen.javascript.biome_config.IJavascriptParser")
class IJavascriptParser(typing_extensions.Protocol):
    '''(experimental) Options that changes how the JavaScript parser behaves.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="unsafeParameterDecoratorsEnabled")
    def unsafe_parameter_decorators_enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) It enables the experimental and unsafe parsing of parameter decorators.

        These decorators belong to an old proposal, and they are subject to change.

        :stability: experimental
        '''
        ...

    @unsafe_parameter_decorators_enabled.setter
    def unsafe_parameter_decorators_enabled(
        self,
        value: typing.Optional[builtins.bool],
    ) -> None:
        ...


class _IJavascriptParserProxy:
    '''(experimental) Options that changes how the JavaScript parser behaves.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.IJavascriptParser"

    @builtins.property
    @jsii.member(jsii_name="unsafeParameterDecoratorsEnabled")
    def unsafe_parameter_decorators_enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) It enables the experimental and unsafe parsing of parameter decorators.

        These decorators belong to an old proposal, and they are subject to change.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "unsafeParameterDecoratorsEnabled"))

    @unsafe_parameter_decorators_enabled.setter
    def unsafe_parameter_decorators_enabled(
        self,
        value: typing.Optional[builtins.bool],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a6f7e985439173c7ce7031153f14d2c2238d2918c2aec9a1bda56cc4424a40a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unsafeParameterDecoratorsEnabled", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IJavascriptParser).__jsii_proxy_class__ = lambda : _IJavascriptParserProxy


@jsii.interface(jsii_type="projen.javascript.biome_config.IJsonAssists")
class IJsonAssists(typing_extensions.Protocol):
    '''(experimental) Linter options specific to the JSON linter.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Control the linter for JSON (and its super languages) files.

        :stability: experimental
        '''
        ...

    @enabled.setter
    def enabled(self, value: typing.Optional[builtins.bool]) -> None:
        ...


class _IJsonAssistsProxy:
    '''(experimental) Linter options specific to the JSON linter.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.IJsonAssists"

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Control the linter for JSON (and its super languages) files.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__109184c22bfabae10e4a9b60c7d597c20a87973859f63e32cef299a3ac43bb3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IJsonAssists).__jsii_proxy_class__ = lambda : _IJsonAssistsProxy


@jsii.interface(jsii_type="projen.javascript.biome_config.IJsonConfiguration")
class IJsonConfiguration(typing_extensions.Protocol):
    '''(experimental) Options applied to JSON files.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="assists")
    def assists(self) -> typing.Optional[IJsonAssists]:
        '''(experimental) Assists options.

        :stability: experimental
        '''
        ...

    @assists.setter
    def assists(self, value: typing.Optional[IJsonAssists]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="formatter")
    def formatter(self) -> typing.Optional["IJsonFormatter"]:
        '''(experimental) Formatting options.

        :stability: experimental
        '''
        ...

    @formatter.setter
    def formatter(self, value: typing.Optional["IJsonFormatter"]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="linter")
    def linter(self) -> typing.Optional["IJsonLinter"]:
        '''(experimental) Linting options.

        :stability: experimental
        '''
        ...

    @linter.setter
    def linter(self, value: typing.Optional["IJsonLinter"]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="parser")
    def parser(self) -> typing.Optional["IJsonParser"]:
        '''(experimental) Parsing options.

        :stability: experimental
        '''
        ...

    @parser.setter
    def parser(self, value: typing.Optional["IJsonParser"]) -> None:
        ...


class _IJsonConfigurationProxy:
    '''(experimental) Options applied to JSON files.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.IJsonConfiguration"

    @builtins.property
    @jsii.member(jsii_name="assists")
    def assists(self) -> typing.Optional[IJsonAssists]:
        '''(experimental) Assists options.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[IJsonAssists], jsii.get(self, "assists"))

    @assists.setter
    def assists(self, value: typing.Optional[IJsonAssists]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9262983ef9235ff89fe84a67e2b7217da4e2128324cc1af72877f0ae3f459b0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assists", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="formatter")
    def formatter(self) -> typing.Optional["IJsonFormatter"]:
        '''(experimental) Formatting options.

        :stability: experimental
        '''
        return typing.cast(typing.Optional["IJsonFormatter"], jsii.get(self, "formatter"))

    @formatter.setter
    def formatter(self, value: typing.Optional["IJsonFormatter"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d9d6087f2ed0c337b4109f90f755e6eb2414005be8ceab97d94db0cc08ccfd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "formatter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="linter")
    def linter(self) -> typing.Optional["IJsonLinter"]:
        '''(experimental) Linting options.

        :stability: experimental
        '''
        return typing.cast(typing.Optional["IJsonLinter"], jsii.get(self, "linter"))

    @linter.setter
    def linter(self, value: typing.Optional["IJsonLinter"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd91aa4e2dccd85b13872682abff82b5fac37c4be5825024f62f067d17ab3fd7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "linter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parser")
    def parser(self) -> typing.Optional["IJsonParser"]:
        '''(experimental) Parsing options.

        :stability: experimental
        '''
        return typing.cast(typing.Optional["IJsonParser"], jsii.get(self, "parser"))

    @parser.setter
    def parser(self, value: typing.Optional["IJsonParser"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__822d0bffc62744cc1e6d209ee489744b4ea65d4bcb2bdcc867a60f49a937ce0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parser", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IJsonConfiguration).__jsii_proxy_class__ = lambda : _IJsonConfigurationProxy


@jsii.interface(jsii_type="projen.javascript.biome_config.IJsonFormatter")
class IJsonFormatter(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Control the formatter for JSON (and its super languages) files.

        :stability: experimental
        '''
        ...

    @enabled.setter
    def enabled(self, value: typing.Optional[builtins.bool]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="indentSize")
    def indent_size(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The size of the indentation applied to JSON (and its super languages) files.

        Default to 2.

        :stability: experimental
        '''
        ...

    @indent_size.setter
    def indent_size(self, value: typing.Optional[jsii.Number]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="indentStyle")
    def indent_style(self) -> typing.Optional[builtins.str]:
        '''(experimental) The indent style applied to JSON (and its super languages) files.

        :stability: experimental
        '''
        ...

    @indent_style.setter
    def indent_style(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="indentWidth")
    def indent_width(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The size of the indentation applied to JSON (and its super languages) files.

        Default to 2.

        :stability: experimental
        '''
        ...

    @indent_width.setter
    def indent_width(self, value: typing.Optional[jsii.Number]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="lineEnding")
    def line_ending(self) -> typing.Optional[builtins.str]:
        '''(experimental) The type of line ending applied to JSON (and its super languages) files.

        :stability: experimental
        '''
        ...

    @line_ending.setter
    def line_ending(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="lineWidth")
    def line_width(self) -> typing.Optional[jsii.Number]:
        '''(experimental) What's the max width of a line applied to JSON (and its super languages) files.

        Defaults to 80.

        :stability: experimental
        '''
        ...

    @line_width.setter
    def line_width(self, value: typing.Optional[jsii.Number]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="trailingCommas")
    def trailing_commas(self) -> typing.Optional[builtins.str]:
        '''(experimental) Print trailing commas wherever possible in multi-line comma-separated syntactic structures.

        Defaults to "none".

        :stability: experimental
        '''
        ...

    @trailing_commas.setter
    def trailing_commas(self, value: typing.Optional[builtins.str]) -> None:
        ...


class _IJsonFormatterProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.IJsonFormatter"

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Control the formatter for JSON (and its super languages) files.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5ad54d8b4c9b8e9424b196d3907875d99a83e20c200c3e6da90d9079e6fcbc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="indentSize")
    def indent_size(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The size of the indentation applied to JSON (and its super languages) files.

        Default to 2.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "indentSize"))

    @indent_size.setter
    def indent_size(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f21d8ceab01190d857817a1494a100c90af324295e7db002f7ee2e08347f439f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "indentSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="indentStyle")
    def indent_style(self) -> typing.Optional[builtins.str]:
        '''(experimental) The indent style applied to JSON (and its super languages) files.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "indentStyle"))

    @indent_style.setter
    def indent_style(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77fed4b6575d63d3f2b3989eda2d1edebc8aeb91507a9e1981883335306afb09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "indentStyle", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="indentWidth")
    def indent_width(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The size of the indentation applied to JSON (and its super languages) files.

        Default to 2.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "indentWidth"))

    @indent_width.setter
    def indent_width(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e2e288874d81794d2483df3786708701bada79f0291b62b172acfd90418c763)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "indentWidth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lineEnding")
    def line_ending(self) -> typing.Optional[builtins.str]:
        '''(experimental) The type of line ending applied to JSON (and its super languages) files.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lineEnding"))

    @line_ending.setter
    def line_ending(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7468d3f4b91745bd32dab02c371321f8ad230ac024dd422d8ef1859300bcc32f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lineEnding", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lineWidth")
    def line_width(self) -> typing.Optional[jsii.Number]:
        '''(experimental) What's the max width of a line applied to JSON (and its super languages) files.

        Defaults to 80.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "lineWidth"))

    @line_width.setter
    def line_width(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a4f6d032a10e6395c3f001e414b1f30bf8a52fc057f861a6764562c1173b2a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lineWidth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="trailingCommas")
    def trailing_commas(self) -> typing.Optional[builtins.str]:
        '''(experimental) Print trailing commas wherever possible in multi-line comma-separated syntactic structures.

        Defaults to "none".

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "trailingCommas"))

    @trailing_commas.setter
    def trailing_commas(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__336daf3ca9f566aad5d44d70aa6971da9250b7c513ab5b26654fc01e3e7732b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trailingCommas", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IJsonFormatter).__jsii_proxy_class__ = lambda : _IJsonFormatterProxy


@jsii.interface(jsii_type="projen.javascript.biome_config.IJsonLinter")
class IJsonLinter(typing_extensions.Protocol):
    '''(experimental) Linter options specific to the JSON linter.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Control the linter for JSON (and its super languages) files.

        :stability: experimental
        '''
        ...

    @enabled.setter
    def enabled(self, value: typing.Optional[builtins.bool]) -> None:
        ...


class _IJsonLinterProxy:
    '''(experimental) Linter options specific to the JSON linter.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.IJsonLinter"

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Control the linter for JSON (and its super languages) files.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30db05d5034aae0f99b8fc2e83d1e104e0e682948c8e6c5b03a25a4b0824c3b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IJsonLinter).__jsii_proxy_class__ = lambda : _IJsonLinterProxy


@jsii.interface(jsii_type="projen.javascript.biome_config.IJsonParser")
class IJsonParser(typing_extensions.Protocol):
    '''(experimental) Options that changes how the JSON parser behaves.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="allowComments")
    def allow_comments(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Allow parsing comments in ``.json`` files.

        :stability: experimental
        '''
        ...

    @allow_comments.setter
    def allow_comments(self, value: typing.Optional[builtins.bool]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="allowTrailingCommas")
    def allow_trailing_commas(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Allow parsing trailing commas in ``.json`` files.

        :stability: experimental
        '''
        ...

    @allow_trailing_commas.setter
    def allow_trailing_commas(self, value: typing.Optional[builtins.bool]) -> None:
        ...


class _IJsonParserProxy:
    '''(experimental) Options that changes how the JSON parser behaves.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.IJsonParser"

    @builtins.property
    @jsii.member(jsii_name="allowComments")
    def allow_comments(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Allow parsing comments in ``.json`` files.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "allowComments"))

    @allow_comments.setter
    def allow_comments(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19f222cbea6108eb6bd6591ecb757b94ce31971a3fa1a77b04e5dce1c266d34a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowComments", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowTrailingCommas")
    def allow_trailing_commas(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Allow parsing trailing commas in ``.json`` files.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "allowTrailingCommas"))

    @allow_trailing_commas.setter
    def allow_trailing_commas(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c4b253e21a41817d2640766265c87b869d6e32a444864aca3f92c122d0eb9d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowTrailingCommas", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IJsonParser).__jsii_proxy_class__ = lambda : _IJsonParserProxy


@jsii.interface(jsii_type="projen.javascript.biome_config.ILinterConfiguration")
class ILinterConfiguration(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) if ``false``, it disables the feature and the linter won't be executed.

        ``true`` by default

        :stability: experimental
        '''
        ...

    @enabled.setter
    def enabled(self, value: typing.Optional[builtins.bool]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="ignore")
    def ignore(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of Unix shell style patterns.

        The formatter will ignore files/folders that will match these patterns.

        :stability: experimental
        '''
        ...

    @ignore.setter
    def ignore(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="include")
    def include(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of Unix shell style patterns.

        The formatter will include files/folders that will match these patterns.

        :stability: experimental
        '''
        ...

    @include.setter
    def include(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="rules")
    def rules(self) -> typing.Optional["IRules"]:
        '''(experimental) List of rules.

        :stability: experimental
        '''
        ...

    @rules.setter
    def rules(self, value: typing.Optional["IRules"]) -> None:
        ...


class _ILinterConfigurationProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.ILinterConfiguration"

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) if ``false``, it disables the feature and the linter won't be executed.

        ``true`` by default

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1faea36fdc017cb47551a62063d019a0f802e96dc37838d0c992c0723d26330)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ignore")
    def ignore(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of Unix shell style patterns.

        The formatter will ignore files/folders that will match these patterns.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "ignore"))

    @ignore.setter
    def ignore(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b830bb0414fbeb0b7856fb7792c6de4923c780fbb9e5c3f760cb0d952abd936)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignore", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="include")
    def include(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of Unix shell style patterns.

        The formatter will include files/folders that will match these patterns.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "include"))

    @include.setter
    def include(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef8c98cf32e46f068a4b3aff83ff7320df0a1e39bf192a118963a167b2853a12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "include", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rules")
    def rules(self) -> typing.Optional["IRules"]:
        '''(experimental) List of rules.

        :stability: experimental
        '''
        return typing.cast(typing.Optional["IRules"], jsii.get(self, "rules"))

    @rules.setter
    def rules(self, value: typing.Optional["IRules"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2486cfe6da32919241cb2c842786ae2c068269bee69a8dde8ee06abaf979005d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rules", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ILinterConfiguration).__jsii_proxy_class__ = lambda : _ILinterConfigurationProxy


@jsii.interface(jsii_type="projen.javascript.biome_config.INamingConventionOptions")
class INamingConventionOptions(typing_extensions.Protocol):
    '''(experimental) Rule's options.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="conventions")
    def conventions(self) -> typing.Optional[typing.List[IConvention]]:
        '''(experimental) Custom conventions.

        :stability: experimental
        '''
        ...

    @conventions.setter
    def conventions(self, value: typing.Optional[typing.List[IConvention]]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="enumMemberCase")
    def enum_member_case(self) -> typing.Optional[builtins.str]:
        '''(experimental) Allowed cases for *TypeScript* ``enum`` member names.

        :stability: experimental
        '''
        ...

    @enum_member_case.setter
    def enum_member_case(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="requireAscii")
    def require_ascii(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If ``false``, then non-ASCII characters are allowed.

        :stability: experimental
        '''
        ...

    @require_ascii.setter
    def require_ascii(self, value: typing.Optional[builtins.bool]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="strictCase")
    def strict_case(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If ``false``, then consecutive uppercase are allowed in *camel* and *pascal* cases.

        This does not affect other [Case].

        :stability: experimental
        '''
        ...

    @strict_case.setter
    def strict_case(self, value: typing.Optional[builtins.bool]) -> None:
        ...


class _INamingConventionOptionsProxy:
    '''(experimental) Rule's options.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.INamingConventionOptions"

    @builtins.property
    @jsii.member(jsii_name="conventions")
    def conventions(self) -> typing.Optional[typing.List[IConvention]]:
        '''(experimental) Custom conventions.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[IConvention]], jsii.get(self, "conventions"))

    @conventions.setter
    def conventions(self, value: typing.Optional[typing.List[IConvention]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f60fa954dd713236cd784e2d5bb21741d8e2e67183ce7afaac2c32ebbd25e23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "conventions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enumMemberCase")
    def enum_member_case(self) -> typing.Optional[builtins.str]:
        '''(experimental) Allowed cases for *TypeScript* ``enum`` member names.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "enumMemberCase"))

    @enum_member_case.setter
    def enum_member_case(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e71c6834677231abf8994a8ef48d04d1e7e0f0a6e82a371354d71061ad4085f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enumMemberCase", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requireAscii")
    def require_ascii(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If ``false``, then non-ASCII characters are allowed.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "requireAscii"))

    @require_ascii.setter
    def require_ascii(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d76453d720470ddff58ae455add9ca46393ae55a797e7afdef788488ec22a676)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requireAscii", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="strictCase")
    def strict_case(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If ``false``, then consecutive uppercase are allowed in *camel* and *pascal* cases.

        This does not affect other [Case].

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "strictCase"))

    @strict_case.setter
    def strict_case(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c632890b09c7cd39ba77acedd53148096b31281bcb7f053afb9358190613c963)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "strictCase", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, INamingConventionOptions).__jsii_proxy_class__ = lambda : _INamingConventionOptionsProxy


@jsii.interface(jsii_type="projen.javascript.biome_config.INoConsoleOptions")
class INoConsoleOptions(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="allow")
    def allow(self) -> typing.List[builtins.str]:
        '''(experimental) Allowed calls on the console object.

        :stability: experimental
        '''
        ...

    @allow.setter
    def allow(self, value: typing.List[builtins.str]) -> None:
        ...


class _INoConsoleOptionsProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.INoConsoleOptions"

    @builtins.property
    @jsii.member(jsii_name="allow")
    def allow(self) -> typing.List[builtins.str]:
        '''(experimental) Allowed calls on the console object.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allow"))

    @allow.setter
    def allow(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85a2d8b594b08aeaee6b06fb087467a36ddb1c8deb4bebf06340e2d3be3e036c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allow", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, INoConsoleOptions).__jsii_proxy_class__ = lambda : _INoConsoleOptionsProxy


@jsii.interface(jsii_type="projen.javascript.biome_config.INoDoubleEqualsOptions")
class INoDoubleEqualsOptions(typing_extensions.Protocol):
    '''(experimental) Rule's options.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="ignoreNull")
    def ignore_null(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If ``true``, an exception is made when comparing with ``null``, as it's often relied on to check both for ``null`` or ``undefined``.

        If ``false``, no such exception will be made.

        :stability: experimental
        '''
        ...

    @ignore_null.setter
    def ignore_null(self, value: typing.Optional[builtins.bool]) -> None:
        ...


class _INoDoubleEqualsOptionsProxy:
    '''(experimental) Rule's options.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.INoDoubleEqualsOptions"

    @builtins.property
    @jsii.member(jsii_name="ignoreNull")
    def ignore_null(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If ``true``, an exception is made when comparing with ``null``, as it's often relied on to check both for ``null`` or ``undefined``.

        If ``false``, no such exception will be made.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "ignoreNull"))

    @ignore_null.setter
    def ignore_null(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef5df1e2df3c98c46fa3a814ff30e72ebda42c1b7173e1a7d10dc1bf16a114d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreNull", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, INoDoubleEqualsOptions).__jsii_proxy_class__ = lambda : _INoDoubleEqualsOptionsProxy


@jsii.interface(
    jsii_type="projen.javascript.biome_config.INoLabelWithoutControlOptions"
)
class INoLabelWithoutControlOptions(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="inputComponents")
    def input_components(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Array of component names that should be considered the same as an ``input`` element.

        :stability: experimental
        '''
        ...

    @input_components.setter
    def input_components(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="labelAttributes")
    def label_attributes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Array of attributes that should be treated as the ``label`` accessible text content.

        :stability: experimental
        '''
        ...

    @label_attributes.setter
    def label_attributes(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="labelComponents")
    def label_components(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Array of component names that should be considered the same as a ``label`` element.

        :stability: experimental
        '''
        ...

    @label_components.setter
    def label_components(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        ...


class _INoLabelWithoutControlOptionsProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.INoLabelWithoutControlOptions"

    @builtins.property
    @jsii.member(jsii_name="inputComponents")
    def input_components(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Array of component names that should be considered the same as an ``input`` element.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "inputComponents"))

    @input_components.setter
    def input_components(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0746030c163cf359edc57c32a0fa8b7269e818aa96a6d0d65cded6ff22932f35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inputComponents", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labelAttributes")
    def label_attributes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Array of attributes that should be treated as the ``label`` accessible text content.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "labelAttributes"))

    @label_attributes.setter
    def label_attributes(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12a7636a9576fc97dd28f5d886f38d9385927c58e72023e927c67a6d6723ac03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labelAttributes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labelComponents")
    def label_components(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Array of component names that should be considered the same as a ``label`` element.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "labelComponents"))

    @label_components.setter
    def label_components(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f73109fede6df77b42b6f5e046905e3b20e1e69e7a09b89d768522c0035a8078)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labelComponents", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, INoLabelWithoutControlOptions).__jsii_proxy_class__ = lambda : _INoLabelWithoutControlOptionsProxy


@jsii.interface(jsii_type="projen.javascript.biome_config.INoRestrictedTypesOptions")
class INoRestrictedTypesOptions(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="types")
    def types(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, ICustomRestrictedTypeOptions]]]:
        '''
        :stability: experimental
        '''
        ...

    @types.setter
    def types(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, ICustomRestrictedTypeOptions]]],
    ) -> None:
        ...


class _INoRestrictedTypesOptionsProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.INoRestrictedTypesOptions"

    @builtins.property
    @jsii.member(jsii_name="types")
    def types(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, ICustomRestrictedTypeOptions]]]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, ICustomRestrictedTypeOptions]]], jsii.get(self, "types"))

    @types.setter
    def types(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, ICustomRestrictedTypeOptions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46fda788d4729d29eb2abea2ccc319bc622ad35f3ea0b0f23f2070aede653966)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "types", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, INoRestrictedTypesOptions).__jsii_proxy_class__ = lambda : _INoRestrictedTypesOptionsProxy


@jsii.interface(jsii_type="projen.javascript.biome_config.INoSecretsOptions")
class INoSecretsOptions(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="entropyThreshold")
    def entropy_threshold(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Set entropy threshold (default is 41).

        :stability: experimental
        '''
        ...

    @entropy_threshold.setter
    def entropy_threshold(self, value: typing.Optional[jsii.Number]) -> None:
        ...


class _INoSecretsOptionsProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.INoSecretsOptions"

    @builtins.property
    @jsii.member(jsii_name="entropyThreshold")
    def entropy_threshold(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Set entropy threshold (default is 41).

        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "entropyThreshold"))

    @entropy_threshold.setter
    def entropy_threshold(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2ac78dad41389d348fc26cb25244800e8da3c3d536a8162aa177511e68a855a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "entropyThreshold", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, INoSecretsOptions).__jsii_proxy_class__ = lambda : _INoSecretsOptionsProxy


@jsii.interface(jsii_type="projen.javascript.biome_config.INursery")
class INursery(typing_extensions.Protocol):
    '''(experimental) A list of rules that belong to this group.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="all")
    def all(self) -> typing.Optional[builtins.bool]:
        '''(experimental) It enables ALL rules for this group.

        :stability: experimental
        '''
        ...

    @all.setter
    def all(self, value: typing.Optional[builtins.bool]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noCommonJs")
    def no_common_js(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow use of CommonJs module system in favor of ESM style imports.

        :stability: experimental
        '''
        ...

    @no_common_js.setter
    def no_common_js(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noDescendingSpecificity")
    def no_descending_specificity(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow a lower specificity selector from coming after a higher specificity selector.

        :stability: experimental
        '''
        ...

    @no_descending_specificity.setter
    def no_descending_specificity(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noDocumentCookie")
    def no_document_cookie(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow direct assignments to document.cookie.

        :stability: experimental
        '''
        ...

    @no_document_cookie.setter
    def no_document_cookie(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noDocumentImportInPage")
    def no_document_import_in_page(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Prevents importing next/document outside of pages/_document.jsx in Next.js projects.

        :stability: experimental
        '''
        ...

    @no_document_import_in_page.setter
    def no_document_import_in_page(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noDuplicateCustomProperties")
    def no_duplicate_custom_properties(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow duplicate custom properties within declaration blocks.

        :stability: experimental
        '''
        ...

    @no_duplicate_custom_properties.setter
    def no_duplicate_custom_properties(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noDuplicatedFields")
    def no_duplicated_fields(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) No duplicated fields in GraphQL operations.

        :stability: experimental
        '''
        ...

    @no_duplicated_fields.setter
    def no_duplicated_fields(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noDuplicateElseIf")
    def no_duplicate_else_if(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow duplicate conditions in if-else-if chains.

        :stability: experimental
        '''
        ...

    @no_duplicate_else_if.setter
    def no_duplicate_else_if(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noDuplicateProperties")
    def no_duplicate_properties(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow duplicate properties within declaration blocks.

        :stability: experimental
        '''
        ...

    @no_duplicate_properties.setter
    def no_duplicate_properties(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noDynamicNamespaceImportAccess")
    def no_dynamic_namespace_import_access(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow accessing namespace imports dynamically.

        :stability: experimental
        '''
        ...

    @no_dynamic_namespace_import_access.setter
    def no_dynamic_namespace_import_access(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noEnum")
    def no_enum(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow TypeScript enum.

        :stability: experimental
        '''
        ...

    @no_enum.setter
    def no_enum(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noExportedImports")
    def no_exported_imports(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow exporting an imported variable.

        :stability: experimental
        '''
        ...

    @no_exported_imports.setter
    def no_exported_imports(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noHeadElement")
    def no_head_element(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Prevent usage of <head> element in a Next.js project.

        :stability: experimental
        '''
        ...

    @no_head_element.setter
    def no_head_element(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noHeadImportInDocument")
    def no_head_import_in_document(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Prevent using the next/head module in pages/_document.js on Next.js projects.

        :stability: experimental
        '''
        ...

    @no_head_import_in_document.setter
    def no_head_import_in_document(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noImgElement")
    def no_img_element(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Prevent usage of <img> element in a Next.js project.

        :stability: experimental
        '''
        ...

    @no_img_element.setter
    def no_img_element(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noIrregularWhitespace")
    def no_irregular_whitespace(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallows the use of irregular whitespace characters.

        :stability: experimental
        '''
        ...

    @no_irregular_whitespace.setter
    def no_irregular_whitespace(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noMissingVarFunction")
    def no_missing_var_function(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow missing var function for css variables.

        :stability: experimental
        '''
        ...

    @no_missing_var_function.setter
    def no_missing_var_function(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noNestedTernary")
    def no_nested_ternary(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow nested ternary expressions.

        :stability: experimental
        '''
        ...

    @no_nested_ternary.setter
    def no_nested_ternary(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noOctalEscape")
    def no_octal_escape(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow octal escape sequences in string literals.

        :stability: experimental
        '''
        ...

    @no_octal_escape.setter
    def no_octal_escape(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noProcessEnv")
    def no_process_env(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow the use of process.env.

        :stability: experimental
        '''
        ...

    @no_process_env.setter
    def no_process_env(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noRestrictedImports")
    def no_restricted_imports(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithRestrictedImportsOptions"]]:
        '''(experimental) Disallow specified modules when loaded by import or require.

        :stability: experimental
        '''
        ...

    @no_restricted_imports.setter
    def no_restricted_imports(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithRestrictedImportsOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noRestrictedTypes")
    def no_restricted_types(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoRestrictedTypesOptions"]]:
        '''(experimental) Disallow user defined types.

        :stability: experimental
        '''
        ...

    @no_restricted_types.setter
    def no_restricted_types(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoRestrictedTypesOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noSecrets")
    def no_secrets(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoSecretsOptions"]]:
        '''(experimental) Disallow usage of sensitive data such as API keys and tokens.

        :stability: experimental
        '''
        ...

    @no_secrets.setter
    def no_secrets(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoSecretsOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noStaticElementInteractions")
    def no_static_element_interactions(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Enforce that static, visible elements (such as <div>) that have click handlers use the valid role attribute.

        :stability: experimental
        '''
        ...

    @no_static_element_interactions.setter
    def no_static_element_interactions(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noSubstr")
    def no_substr(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Enforce the use of String.slice() over String.substr() and String.substring().

        :stability: experimental
        '''
        ...

    @no_substr.setter
    def no_substr(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noTemplateCurlyInString")
    def no_template_curly_in_string(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow template literal placeholder syntax in regular strings.

        :stability: experimental
        '''
        ...

    @no_template_curly_in_string.setter
    def no_template_curly_in_string(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noUnknownPseudoClass")
    def no_unknown_pseudo_class(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow unknown pseudo-class selectors.

        :stability: experimental
        '''
        ...

    @no_unknown_pseudo_class.setter
    def no_unknown_pseudo_class(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noUnknownPseudoElement")
    def no_unknown_pseudo_element(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow unknown pseudo-element selectors.

        :stability: experimental
        '''
        ...

    @no_unknown_pseudo_element.setter
    def no_unknown_pseudo_element(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noUnknownTypeSelector")
    def no_unknown_type_selector(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow unknown type selectors.

        :stability: experimental
        '''
        ...

    @no_unknown_type_selector.setter
    def no_unknown_type_selector(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noUselessEscapeInRegex")
    def no_useless_escape_in_regex(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Disallow unnecessary escape sequence in regular expression literals.

        :stability: experimental
        '''
        ...

    @no_useless_escape_in_regex.setter
    def no_useless_escape_in_regex(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noUselessStringRaw")
    def no_useless_string_raw(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow unnecessary String.raw function in template string literals without any escape sequence.

        :stability: experimental
        '''
        ...

    @no_useless_string_raw.setter
    def no_useless_string_raw(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noValueAtRule")
    def no_value_at_rule(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow use of.

        :stability: experimental
        :value: rule in css modules.
        '''
        ...

    @no_value_at_rule.setter
    def no_value_at_rule(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="recommended")
    def recommended(self) -> typing.Optional[builtins.bool]:
        '''(experimental) It enables the recommended rules for this group.

        :stability: experimental
        '''
        ...

    @recommended.setter
    def recommended(self, value: typing.Optional[builtins.bool]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useAdjacentOverloadSignatures")
    def use_adjacent_overload_signatures(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow the use of overload signatures that are not next to each other.

        :stability: experimental
        '''
        ...

    @use_adjacent_overload_signatures.setter
    def use_adjacent_overload_signatures(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useAriaPropsSupportedByRole")
    def use_aria_props_supported_by_role(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Enforce that ARIA properties are valid for the roles that are supported by the element.

        :stability: experimental
        '''
        ...

    @use_aria_props_supported_by_role.setter
    def use_aria_props_supported_by_role(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useAtIndex")
    def use_at_index(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Use at() instead of integer index access.

        :stability: experimental
        '''
        ...

    @use_at_index.setter
    def use_at_index(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useCollapsedIf")
    def use_collapsed_if(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Enforce using single if instead of nested if clauses.

        :stability: experimental
        '''
        ...

    @use_collapsed_if.setter
    def use_collapsed_if(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useComponentExportOnlyModules")
    def use_component_export_only_modules(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithUseComponentExportOnlyModulesOptions"]]:
        '''(experimental) Enforce declaring components only within modules that export React Components exclusively.

        :stability: experimental
        '''
        ...

    @use_component_export_only_modules.setter
    def use_component_export_only_modules(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithUseComponentExportOnlyModulesOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useConsistentCurlyBraces")
    def use_consistent_curly_braces(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) This rule enforces consistent use of curly braces inside JSX attributes and JSX children.

        :stability: experimental
        '''
        ...

    @use_consistent_curly_braces.setter
    def use_consistent_curly_braces(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useConsistentMemberAccessibility")
    def use_consistent_member_accessibility(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithConsistentMemberAccessibilityOptions"]]:
        '''(experimental) Require consistent accessibility modifiers on class properties and methods.

        :stability: experimental
        '''
        ...

    @use_consistent_member_accessibility.setter
    def use_consistent_member_accessibility(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithConsistentMemberAccessibilityOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useDeprecatedReason")
    def use_deprecated_reason(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(deprecated) Require specifying the reason argument when using.

        :deprecated: directive

        :stability: deprecated
        '''
        ...

    @use_deprecated_reason.setter
    def use_deprecated_reason(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useExplicitType")
    def use_explicit_type(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Require explicit return types on functions and class methods.

        :stability: experimental
        '''
        ...

    @use_explicit_type.setter
    def use_explicit_type(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useGoogleFontDisplay")
    def use_google_font_display(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Enforces the use of a recommended display strategy with Google Fonts.

        :stability: experimental
        '''
        ...

    @use_google_font_display.setter
    def use_google_font_display(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useGuardForIn")
    def use_guard_for_in(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Require for-in loops to include an if statement.

        :stability: experimental
        '''
        ...

    @use_guard_for_in.setter
    def use_guard_for_in(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useImportRestrictions")
    def use_import_restrictions(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallows package private imports.

        :stability: experimental
        '''
        ...

    @use_import_restrictions.setter
    def use_import_restrictions(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useSortedClasses")
    def use_sorted_classes(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithUtilityClassSortingOptions"]]:
        '''(experimental) Enforce the sorting of CSS utility classes.

        :stability: experimental
        '''
        ...

    @use_sorted_classes.setter
    def use_sorted_classes(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithUtilityClassSortingOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useStrictMode")
    def use_strict_mode(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Enforce the use of the directive "use strict" in script files.

        :stability: experimental
        '''
        ...

    @use_strict_mode.setter
    def use_strict_mode(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useTrimStartEnd")
    def use_trim_start_end(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Enforce the use of String.trimStart() and String.trimEnd() over String.trimLeft() and String.trimRight().

        :stability: experimental
        '''
        ...

    @use_trim_start_end.setter
    def use_trim_start_end(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useValidAutocomplete")
    def use_valid_autocomplete(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithUseValidAutocompleteOptions"]]:
        '''(experimental) Use valid values for the autocomplete attribute on input elements.

        :stability: experimental
        '''
        ...

    @use_valid_autocomplete.setter
    def use_valid_autocomplete(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithUseValidAutocompleteOptions"]],
    ) -> None:
        ...


class _INurseryProxy:
    '''(experimental) A list of rules that belong to this group.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.INursery"

    @builtins.property
    @jsii.member(jsii_name="all")
    def all(self) -> typing.Optional[builtins.bool]:
        '''(experimental) It enables ALL rules for this group.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "all"))

    @all.setter
    def all(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7098fa635a567a594fec7474846a238f047a9756d12d5f4b4d6dd0b0417a1844)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "all", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noCommonJs")
    def no_common_js(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow use of CommonJs module system in favor of ESM style imports.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "noCommonJs"))

    @no_common_js.setter
    def no_common_js(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f37453f0f8183b7a8276f4b886a377235895b9c09481faed358c79af2ff385a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noCommonJs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noDescendingSpecificity")
    def no_descending_specificity(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow a lower specificity selector from coming after a higher specificity selector.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "noDescendingSpecificity"))

    @no_descending_specificity.setter
    def no_descending_specificity(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32020291c8dcea7de662caea6819e7bb9e3b6f89b893bb98e16c384e219aae9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noDescendingSpecificity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noDocumentCookie")
    def no_document_cookie(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow direct assignments to document.cookie.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "noDocumentCookie"))

    @no_document_cookie.setter
    def no_document_cookie(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b39c0b329c18cb4bf215190dc27b940ff24e81561efeb8edd0f597ec97125ee5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noDocumentCookie", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noDocumentImportInPage")
    def no_document_import_in_page(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Prevents importing next/document outside of pages/_document.jsx in Next.js projects.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "noDocumentImportInPage"))

    @no_document_import_in_page.setter
    def no_document_import_in_page(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34245abc673c4838fdfc26f89b64a75170c7ad6c3d437020716ed1be4612a5ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noDocumentImportInPage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noDuplicateCustomProperties")
    def no_duplicate_custom_properties(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow duplicate custom properties within declaration blocks.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "noDuplicateCustomProperties"))

    @no_duplicate_custom_properties.setter
    def no_duplicate_custom_properties(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d3e06bea2364a3f402fe08f631d5a47daad86bdd86747637fa23e25acb4d545)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noDuplicateCustomProperties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noDuplicatedFields")
    def no_duplicated_fields(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) No duplicated fields in GraphQL operations.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "noDuplicatedFields"))

    @no_duplicated_fields.setter
    def no_duplicated_fields(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df06d5644c925d656f70313efdf3b48931f1d55d2e016a62e938f40900b9a3fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noDuplicatedFields", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noDuplicateElseIf")
    def no_duplicate_else_if(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow duplicate conditions in if-else-if chains.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "noDuplicateElseIf"))

    @no_duplicate_else_if.setter
    def no_duplicate_else_if(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e7da289b3d8c7b5851e5c9c6971797d40286834bda8e1a91bec22abb888936e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noDuplicateElseIf", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noDuplicateProperties")
    def no_duplicate_properties(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow duplicate properties within declaration blocks.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "noDuplicateProperties"))

    @no_duplicate_properties.setter
    def no_duplicate_properties(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7456d472f91bac40ef9613085229984599264b655b2567a42cbc8d7dd7df4bde)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noDuplicateProperties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noDynamicNamespaceImportAccess")
    def no_dynamic_namespace_import_access(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow accessing namespace imports dynamically.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "noDynamicNamespaceImportAccess"))

    @no_dynamic_namespace_import_access.setter
    def no_dynamic_namespace_import_access(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3967de35c5355d023b1edc13137303b5c078656e267ce5eea3a6c0077319df16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noDynamicNamespaceImportAccess", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noEnum")
    def no_enum(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow TypeScript enum.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "noEnum"))

    @no_enum.setter
    def no_enum(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__934f4a829cdcb0c67688544d8d862ad521d25adf3950fbd883f923cef6f9044b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noEnum", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noExportedImports")
    def no_exported_imports(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow exporting an imported variable.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "noExportedImports"))

    @no_exported_imports.setter
    def no_exported_imports(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa604ecf974a08994fa44c926ff8bc67bdf2b70f040f07f6d26d0a851040632e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noExportedImports", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noHeadElement")
    def no_head_element(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Prevent usage of <head> element in a Next.js project.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "noHeadElement"))

    @no_head_element.setter
    def no_head_element(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42475cd54accdc6630da5eb4697b6fbb958aae32df9aa7e7a143ed41909a2101)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noHeadElement", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noHeadImportInDocument")
    def no_head_import_in_document(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Prevent using the next/head module in pages/_document.js on Next.js projects.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "noHeadImportInDocument"))

    @no_head_import_in_document.setter
    def no_head_import_in_document(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c52b0ab3001cfe5791e631039369da4e48155ada55bae3fe21da7c8d52af877)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noHeadImportInDocument", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noImgElement")
    def no_img_element(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Prevent usage of <img> element in a Next.js project.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "noImgElement"))

    @no_img_element.setter
    def no_img_element(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1103c1ad5c94fca1d5f70145ea8a3da7cc32eead57f32eb1e5a048b37f8e684f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noImgElement", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noIrregularWhitespace")
    def no_irregular_whitespace(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallows the use of irregular whitespace characters.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "noIrregularWhitespace"))

    @no_irregular_whitespace.setter
    def no_irregular_whitespace(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6412d7053e79e5b50434fa538c23b3c3da7c63a6a1c1d20bffe9765a82a0f78d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noIrregularWhitespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noMissingVarFunction")
    def no_missing_var_function(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow missing var function for css variables.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "noMissingVarFunction"))

    @no_missing_var_function.setter
    def no_missing_var_function(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff110a6185afa749e49ea163b27998696e5ad0dfea99befa9cb4751794377480)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noMissingVarFunction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noNestedTernary")
    def no_nested_ternary(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow nested ternary expressions.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "noNestedTernary"))

    @no_nested_ternary.setter
    def no_nested_ternary(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bded73f1f632d2d19d35322d45a6fb10f9590f2a0bd62bc9704168fb8977f8ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noNestedTernary", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noOctalEscape")
    def no_octal_escape(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow octal escape sequences in string literals.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "noOctalEscape"))

    @no_octal_escape.setter
    def no_octal_escape(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59116a4af7ad3b90f9a82a000f0bf953379ef28d2537ab5b0a2eb3bab598d2ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noOctalEscape", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noProcessEnv")
    def no_process_env(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow the use of process.env.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "noProcessEnv"))

    @no_process_env.setter
    def no_process_env(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58c575f48a75403a33e9218ffdb1ac788f825cb23d9050b6594a71fae5a2d43f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noProcessEnv", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noRestrictedImports")
    def no_restricted_imports(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithRestrictedImportsOptions"]]:
        '''(experimental) Disallow specified modules when loaded by import or require.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithRestrictedImportsOptions"]], jsii.get(self, "noRestrictedImports"))

    @no_restricted_imports.setter
    def no_restricted_imports(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithRestrictedImportsOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__481a30d3bbcc117cc2d1c844180dac93e4d82751e234e3b256af98d7fc5731a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noRestrictedImports", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noRestrictedTypes")
    def no_restricted_types(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoRestrictedTypesOptions"]]:
        '''(experimental) Disallow user defined types.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoRestrictedTypesOptions"]], jsii.get(self, "noRestrictedTypes"))

    @no_restricted_types.setter
    def no_restricted_types(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoRestrictedTypesOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ef0b0df4ddc23228797b227a57f7ac3bba11c045563c34cb8f2b78ec975243a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noRestrictedTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noSecrets")
    def no_secrets(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoSecretsOptions"]]:
        '''(experimental) Disallow usage of sensitive data such as API keys and tokens.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoSecretsOptions"]], jsii.get(self, "noSecrets"))

    @no_secrets.setter
    def no_secrets(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoSecretsOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__961ba8e58951a1cac0506b3141ea6f9834bd960a68b074b121270bd0641b6a4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noSecrets", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noStaticElementInteractions")
    def no_static_element_interactions(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Enforce that static, visible elements (such as <div>) that have click handlers use the valid role attribute.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "noStaticElementInteractions"))

    @no_static_element_interactions.setter
    def no_static_element_interactions(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0be94a539de03064e9a1208033a90066cfbaf83c24e2381f0947977a902a418)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noStaticElementInteractions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noSubstr")
    def no_substr(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Enforce the use of String.slice() over String.substr() and String.substring().

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]], jsii.get(self, "noSubstr"))

    @no_substr.setter
    def no_substr(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d39bda1f70a8e792be4de03b9cd66109c49388cb8804390c1643790da01b483)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noSubstr", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noTemplateCurlyInString")
    def no_template_curly_in_string(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow template literal placeholder syntax in regular strings.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "noTemplateCurlyInString"))

    @no_template_curly_in_string.setter
    def no_template_curly_in_string(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c92de2ceb1f14aeb6a0ca6f8da7b6d6d2348049376c53ba547b29c8dcbd94f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noTemplateCurlyInString", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noUnknownPseudoClass")
    def no_unknown_pseudo_class(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow unknown pseudo-class selectors.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "noUnknownPseudoClass"))

    @no_unknown_pseudo_class.setter
    def no_unknown_pseudo_class(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86c7b68bf5392f03bff73f27feb9bf1ce7fd0a547a25cf3db26d11dc2d5a8a98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noUnknownPseudoClass", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noUnknownPseudoElement")
    def no_unknown_pseudo_element(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow unknown pseudo-element selectors.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "noUnknownPseudoElement"))

    @no_unknown_pseudo_element.setter
    def no_unknown_pseudo_element(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5cc191a9daa6aeb85f6bf40bd979f9318d0468480fccd11220aefd184d3006c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noUnknownPseudoElement", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noUnknownTypeSelector")
    def no_unknown_type_selector(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow unknown type selectors.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "noUnknownTypeSelector"))

    @no_unknown_type_selector.setter
    def no_unknown_type_selector(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4f0601789b393c153be69bf23c6ecbca886be761d0f3f16a39736f591d5c12d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noUnknownTypeSelector", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noUselessEscapeInRegex")
    def no_useless_escape_in_regex(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Disallow unnecessary escape sequence in regular expression literals.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]], jsii.get(self, "noUselessEscapeInRegex"))

    @no_useless_escape_in_regex.setter
    def no_useless_escape_in_regex(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a15e73b8bdaf03f491d564596283e70864492068a8c13f99434c8cf59b44010c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noUselessEscapeInRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noUselessStringRaw")
    def no_useless_string_raw(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow unnecessary String.raw function in template string literals without any escape sequence.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "noUselessStringRaw"))

    @no_useless_string_raw.setter
    def no_useless_string_raw(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__156ac23d28fb867e567c059336309abcdc68286f119c1de9b40ce965b0d04e74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noUselessStringRaw", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noValueAtRule")
    def no_value_at_rule(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow use of.

        :stability: experimental
        :value: rule in css modules.
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "noValueAtRule"))

    @no_value_at_rule.setter
    def no_value_at_rule(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4eee81431afaed6621ab8c25aaa0afbd5be659cf1a1afaa79451401563b8fdd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noValueAtRule", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recommended")
    def recommended(self) -> typing.Optional[builtins.bool]:
        '''(experimental) It enables the recommended rules for this group.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "recommended"))

    @recommended.setter
    def recommended(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa2184170f5beff37d56f18d71cc1b9ffc9c5cbab8c7b877ebe6a39f2892b9c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recommended", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useAdjacentOverloadSignatures")
    def use_adjacent_overload_signatures(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow the use of overload signatures that are not next to each other.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "useAdjacentOverloadSignatures"))

    @use_adjacent_overload_signatures.setter
    def use_adjacent_overload_signatures(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ac507894ac00532a80c979788414faf5cbd89752a3ff7f7a39bdfe0a0145731)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useAdjacentOverloadSignatures", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useAriaPropsSupportedByRole")
    def use_aria_props_supported_by_role(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Enforce that ARIA properties are valid for the roles that are supported by the element.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "useAriaPropsSupportedByRole"))

    @use_aria_props_supported_by_role.setter
    def use_aria_props_supported_by_role(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aaa4e2db8ee0c12008d8e250cd624336834b466c5bfceb491ad4c09732f3cbc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useAriaPropsSupportedByRole", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useAtIndex")
    def use_at_index(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Use at() instead of integer index access.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]], jsii.get(self, "useAtIndex"))

    @use_at_index.setter
    def use_at_index(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b1bfb3a55f10cdc2fa22c956dacb70efa6b32f61c0be9aa96317e2fcc361c0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useAtIndex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useCollapsedIf")
    def use_collapsed_if(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Enforce using single if instead of nested if clauses.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]], jsii.get(self, "useCollapsedIf"))

    @use_collapsed_if.setter
    def use_collapsed_if(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6977f5a886d92cb62e7437f329f517c893fd7ff0baa10343f268e94eb8f9f1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useCollapsedIf", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useComponentExportOnlyModules")
    def use_component_export_only_modules(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithUseComponentExportOnlyModulesOptions"]]:
        '''(experimental) Enforce declaring components only within modules that export React Components exclusively.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithUseComponentExportOnlyModulesOptions"]], jsii.get(self, "useComponentExportOnlyModules"))

    @use_component_export_only_modules.setter
    def use_component_export_only_modules(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithUseComponentExportOnlyModulesOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e7ec98c7f6f4aa10baca5ed6aa5f12f280f90b7e2c39c427097310aba76fafc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useComponentExportOnlyModules", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useConsistentCurlyBraces")
    def use_consistent_curly_braces(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) This rule enforces consistent use of curly braces inside JSX attributes and JSX children.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]], jsii.get(self, "useConsistentCurlyBraces"))

    @use_consistent_curly_braces.setter
    def use_consistent_curly_braces(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c396ae3c06a9dff5afa5c33ffe992f342337835316fd61148008e05fe4519a20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useConsistentCurlyBraces", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useConsistentMemberAccessibility")
    def use_consistent_member_accessibility(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithConsistentMemberAccessibilityOptions"]]:
        '''(experimental) Require consistent accessibility modifiers on class properties and methods.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithConsistentMemberAccessibilityOptions"]], jsii.get(self, "useConsistentMemberAccessibility"))

    @use_consistent_member_accessibility.setter
    def use_consistent_member_accessibility(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithConsistentMemberAccessibilityOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7e2111995e133affc00f03631cb9b94be3fd7e6775a517907e3616369979d56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useConsistentMemberAccessibility", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useDeprecatedReason")
    def use_deprecated_reason(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(deprecated) Require specifying the reason argument when using.

        :deprecated: directive

        :stability: deprecated
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "useDeprecatedReason"))

    @use_deprecated_reason.setter
    def use_deprecated_reason(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bd88427d788e7b49099535d8d4ed602a406af87bbf9fa7aa4461ba8432cde03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useDeprecatedReason", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useExplicitType")
    def use_explicit_type(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Require explicit return types on functions and class methods.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "useExplicitType"))

    @use_explicit_type.setter
    def use_explicit_type(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c66a28c8ec197c510d5f806b02c9efe983d984f905d84bdcb4f6e13db4d23bba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useExplicitType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useGoogleFontDisplay")
    def use_google_font_display(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Enforces the use of a recommended display strategy with Google Fonts.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "useGoogleFontDisplay"))

    @use_google_font_display.setter
    def use_google_font_display(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7eaa8bb80000514571e9c088d5becf9e0a53b04d5f62aaf235df3dfa4ddbe2c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useGoogleFontDisplay", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useGuardForIn")
    def use_guard_for_in(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Require for-in loops to include an if statement.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "useGuardForIn"))

    @use_guard_for_in.setter
    def use_guard_for_in(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddb32845c7bd980b5506883f258b5014258d9bb3df42c6d865f046837547b999)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useGuardForIn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useImportRestrictions")
    def use_import_restrictions(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallows package private imports.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "useImportRestrictions"))

    @use_import_restrictions.setter
    def use_import_restrictions(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e91d12531a6749f388b69f3ee3f053cfd77d3b585f429abeae6b037e33d96fce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useImportRestrictions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useSortedClasses")
    def use_sorted_classes(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithUtilityClassSortingOptions"]]:
        '''(experimental) Enforce the sorting of CSS utility classes.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithUtilityClassSortingOptions"]], jsii.get(self, "useSortedClasses"))

    @use_sorted_classes.setter
    def use_sorted_classes(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithUtilityClassSortingOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b487ab3e4f4adc08bc83f4fe78c1d03e29589bb7b865339510a152edfbbaf6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useSortedClasses", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useStrictMode")
    def use_strict_mode(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Enforce the use of the directive "use strict" in script files.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]], jsii.get(self, "useStrictMode"))

    @use_strict_mode.setter
    def use_strict_mode(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d76e67d15a4e64a75330ae3568f5d8520bf466904a74ad792ec231307f85d4b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useStrictMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useTrimStartEnd")
    def use_trim_start_end(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Enforce the use of String.trimStart() and String.trimEnd() over String.trimLeft() and String.trimRight().

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]], jsii.get(self, "useTrimStartEnd"))

    @use_trim_start_end.setter
    def use_trim_start_end(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2114761c0476df25a0d45053dcc35b4243df9992a07a75b85e5aa16efd1ede1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useTrimStartEnd", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useValidAutocomplete")
    def use_valid_autocomplete(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithUseValidAutocompleteOptions"]]:
        '''(experimental) Use valid values for the autocomplete attribute on input elements.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithUseValidAutocompleteOptions"]], jsii.get(self, "useValidAutocomplete"))

    @use_valid_autocomplete.setter
    def use_valid_autocomplete(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithUseValidAutocompleteOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ff9dffdb4f0c6e94c273e81996aeb6701c7c2fe1a7b63932a36e8bdabdc3285)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useValidAutocomplete", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, INursery).__jsii_proxy_class__ = lambda : _INurseryProxy


@jsii.interface(jsii_type="projen.javascript.biome_config.IOrganizeImports")
class IOrganizeImports(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables the organization of imports.

        :stability: experimental
        '''
        ...

    @enabled.setter
    def enabled(self, value: typing.Optional[builtins.bool]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="ignore")
    def ignore(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of Unix shell style patterns.

        The formatter will ignore files/folders that will match these patterns.

        :stability: experimental
        '''
        ...

    @ignore.setter
    def ignore(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="include")
    def include(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of Unix shell style patterns.

        The formatter will include files/folders that will match these patterns.

        :stability: experimental
        '''
        ...

    @include.setter
    def include(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        ...


class _IOrganizeImportsProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.IOrganizeImports"

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables the organization of imports.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10b6ad2989f780cb82bb42d3ea23de966ccc938259cdb31897d9964095299c13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ignore")
    def ignore(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of Unix shell style patterns.

        The formatter will ignore files/folders that will match these patterns.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "ignore"))

    @ignore.setter
    def ignore(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91712bd4a8ec79877ef9303b50ee143787ab60bd7884bfa2cb4b9b1eed93f560)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignore", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="include")
    def include(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of Unix shell style patterns.

        The formatter will include files/folders that will match these patterns.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "include"))

    @include.setter
    def include(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__036cf4c3e56a3243bf787f283f54c7e2c59f99c84e72efa67e7f0e23d1b99c14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "include", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IOrganizeImports).__jsii_proxy_class__ = lambda : _IOrganizeImportsProxy


@jsii.interface(
    jsii_type="projen.javascript.biome_config.IOverrideFormatterConfiguration"
)
class IOverrideFormatterConfiguration(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="attributePosition")
    def attribute_position(self) -> typing.Optional[builtins.str]:
        '''(experimental) The attribute position style.

        :stability: experimental
        '''
        ...

    @attribute_position.setter
    def attribute_position(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="bracketSpacing")
    def bracket_spacing(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to insert spaces around brackets in object literals.

        Defaults to true.

        :stability: experimental
        '''
        ...

    @bracket_spacing.setter
    def bracket_spacing(self, value: typing.Optional[builtins.bool]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        ...

    @enabled.setter
    def enabled(self, value: typing.Optional[builtins.bool]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="formatWithErrors")
    def format_with_errors(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Stores whether formatting should be allowed to proceed if a given file has syntax errors.

        :stability: experimental
        '''
        ...

    @format_with_errors.setter
    def format_with_errors(self, value: typing.Optional[builtins.bool]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="indentSize")
    def indent_size(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The size of the indentation, 2 by default (deprecated, use ``indent-width``).

        :stability: experimental
        '''
        ...

    @indent_size.setter
    def indent_size(self, value: typing.Optional[jsii.Number]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="indentStyle")
    def indent_style(self) -> typing.Optional[builtins.str]:
        '''(experimental) The indent style.

        :stability: experimental
        '''
        ...

    @indent_style.setter
    def indent_style(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="indentWidth")
    def indent_width(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The size of the indentation, 2 by default.

        :stability: experimental
        '''
        ...

    @indent_width.setter
    def indent_width(self, value: typing.Optional[jsii.Number]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="lineEnding")
    def line_ending(self) -> typing.Optional[builtins.str]:
        '''(experimental) The type of line ending.

        :stability: experimental
        '''
        ...

    @line_ending.setter
    def line_ending(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="lineWidth")
    def line_width(self) -> typing.Optional[jsii.Number]:
        '''(experimental) What's the max width of a line.

        Defaults to 80.

        :stability: experimental
        '''
        ...

    @line_width.setter
    def line_width(self, value: typing.Optional[jsii.Number]) -> None:
        ...


class _IOverrideFormatterConfigurationProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.IOverrideFormatterConfiguration"

    @builtins.property
    @jsii.member(jsii_name="attributePosition")
    def attribute_position(self) -> typing.Optional[builtins.str]:
        '''(experimental) The attribute position style.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "attributePosition"))

    @attribute_position.setter
    def attribute_position(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04eeca7a12c488e41b660a8cb82fe79d813642299997d9f805dc0cf29f3c3b13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "attributePosition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bracketSpacing")
    def bracket_spacing(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to insert spaces around brackets in object literals.

        Defaults to true.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "bracketSpacing"))

    @bracket_spacing.setter
    def bracket_spacing(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__642aafd4b395d7e05a5c3e7c79bd1df448299693279402c4e193688be9b8a92b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bracketSpacing", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7340712b6b614062e542ff0ac1deed027a3ae431ca0485f7799af53cf07045d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="formatWithErrors")
    def format_with_errors(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Stores whether formatting should be allowed to proceed if a given file has syntax errors.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "formatWithErrors"))

    @format_with_errors.setter
    def format_with_errors(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4c8c85c2f34be3e3cbd56b256ebe6a1d3f03275cc36b6bd852417fccfdeaf03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "formatWithErrors", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="indentSize")
    def indent_size(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The size of the indentation, 2 by default (deprecated, use ``indent-width``).

        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "indentSize"))

    @indent_size.setter
    def indent_size(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8061a114a765b98260c5a52fa7e9d8748479263d19d2facbb2871f504f64cecf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "indentSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="indentStyle")
    def indent_style(self) -> typing.Optional[builtins.str]:
        '''(experimental) The indent style.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "indentStyle"))

    @indent_style.setter
    def indent_style(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14d67b174df07c745a13d0a81cf3840cace2af4465f00302399d7e8d00870bb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "indentStyle", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="indentWidth")
    def indent_width(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The size of the indentation, 2 by default.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "indentWidth"))

    @indent_width.setter
    def indent_width(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f3c0fe24ce6182678a6f97e3d42b7b529321cacbe408c72939c51553b422a3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "indentWidth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lineEnding")
    def line_ending(self) -> typing.Optional[builtins.str]:
        '''(experimental) The type of line ending.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lineEnding"))

    @line_ending.setter
    def line_ending(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bf3497618a755c2a70d8b005775eae4362c50870be318e1e78fd9ba9ab06b01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lineEnding", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lineWidth")
    def line_width(self) -> typing.Optional[jsii.Number]:
        '''(experimental) What's the max width of a line.

        Defaults to 80.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "lineWidth"))

    @line_width.setter
    def line_width(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cec15ebd39b3a357c306491a3e899f114d9aea1e2e13d8b4b60b2b6b59e89334)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lineWidth", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IOverrideFormatterConfiguration).__jsii_proxy_class__ = lambda : _IOverrideFormatterConfigurationProxy


@jsii.interface(
    jsii_type="projen.javascript.biome_config.IOverrideLinterConfiguration"
)
class IOverrideLinterConfiguration(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) if ``false``, it disables the feature and the linter won't be executed.

        ``true`` by default

        :stability: experimental
        '''
        ...

    @enabled.setter
    def enabled(self, value: typing.Optional[builtins.bool]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="rules")
    def rules(self) -> typing.Optional["IRules"]:
        '''(experimental) List of rules.

        :stability: experimental
        '''
        ...

    @rules.setter
    def rules(self, value: typing.Optional["IRules"]) -> None:
        ...


class _IOverrideLinterConfigurationProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.IOverrideLinterConfiguration"

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) if ``false``, it disables the feature and the linter won't be executed.

        ``true`` by default

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__daee87e9fe1ea32ee7fd208aa012af88c8830d2ec8ca667eda2799833bab11e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rules")
    def rules(self) -> typing.Optional["IRules"]:
        '''(experimental) List of rules.

        :stability: experimental
        '''
        return typing.cast(typing.Optional["IRules"], jsii.get(self, "rules"))

    @rules.setter
    def rules(self, value: typing.Optional["IRules"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9e95a948405660f04e19b5d72c598d881386b85ad8e6aeca602434cca539cb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rules", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IOverrideLinterConfiguration).__jsii_proxy_class__ = lambda : _IOverrideLinterConfigurationProxy


@jsii.interface(
    jsii_type="projen.javascript.biome_config.IOverrideOrganizeImportsConfiguration"
)
class IOverrideOrganizeImportsConfiguration(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) if ``false``, it disables the feature and the linter won't be executed.

        ``true`` by default

        :stability: experimental
        '''
        ...

    @enabled.setter
    def enabled(self, value: typing.Optional[builtins.bool]) -> None:
        ...


class _IOverrideOrganizeImportsConfigurationProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.IOverrideOrganizeImportsConfiguration"

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) if ``false``, it disables the feature and the linter won't be executed.

        ``true`` by default

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51266df200f686d906768266691bd4d85d562e041d5464edc25c04804c4833cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IOverrideOrganizeImportsConfiguration).__jsii_proxy_class__ = lambda : _IOverrideOrganizeImportsConfigurationProxy


@jsii.interface(jsii_type="projen.javascript.biome_config.IOverridePattern")
class IOverridePattern(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="css")
    def css(self) -> typing.Optional[ICssConfiguration]:
        '''(experimental) Specific configuration for the Css language.

        :stability: experimental
        '''
        ...

    @css.setter
    def css(self, value: typing.Optional[ICssConfiguration]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="formatter")
    def formatter(self) -> typing.Optional[IOverrideFormatterConfiguration]:
        '''(experimental) Specific configuration for the Json language.

        :stability: experimental
        '''
        ...

    @formatter.setter
    def formatter(
        self,
        value: typing.Optional[IOverrideFormatterConfiguration],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="graphql")
    def graphql(self) -> typing.Optional[IGraphqlConfiguration]:
        '''(experimental) Specific configuration for the Graphql language.

        :stability: experimental
        '''
        ...

    @graphql.setter
    def graphql(self, value: typing.Optional[IGraphqlConfiguration]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="ignore")
    def ignore(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of Unix shell style patterns.

        The formatter will ignore files/folders that will match these patterns.

        :stability: experimental
        '''
        ...

    @ignore.setter
    def ignore(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="include")
    def include(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of Unix shell style patterns.

        The formatter will include files/folders that will match these patterns.

        :stability: experimental
        '''
        ...

    @include.setter
    def include(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="javascript")
    def javascript(self) -> typing.Optional[IJavascriptConfiguration]:
        '''(experimental) Specific configuration for the JavaScript language.

        :stability: experimental
        '''
        ...

    @javascript.setter
    def javascript(self, value: typing.Optional[IJavascriptConfiguration]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="json")
    def json(self) -> typing.Optional[IJsonConfiguration]:
        '''(experimental) Specific configuration for the Json language.

        :stability: experimental
        '''
        ...

    @json.setter
    def json(self, value: typing.Optional[IJsonConfiguration]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="linter")
    def linter(self) -> typing.Optional[IOverrideLinterConfiguration]:
        '''(experimental) Specific configuration for the Json language.

        :stability: experimental
        '''
        ...

    @linter.setter
    def linter(self, value: typing.Optional[IOverrideLinterConfiguration]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="organizeImports")
    def organize_imports(
        self,
    ) -> typing.Optional[IOverrideOrganizeImportsConfiguration]:
        '''(experimental) Specific configuration for the Json language.

        :stability: experimental
        '''
        ...

    @organize_imports.setter
    def organize_imports(
        self,
        value: typing.Optional[IOverrideOrganizeImportsConfiguration],
    ) -> None:
        ...


class _IOverridePatternProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.IOverridePattern"

    @builtins.property
    @jsii.member(jsii_name="css")
    def css(self) -> typing.Optional[ICssConfiguration]:
        '''(experimental) Specific configuration for the Css language.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[ICssConfiguration], jsii.get(self, "css"))

    @css.setter
    def css(self, value: typing.Optional[ICssConfiguration]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36843010c44ef7218c8fcd9581fb5eb1a559b2463b8edc285b4ceabcf4d4c4e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "css", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="formatter")
    def formatter(self) -> typing.Optional[IOverrideFormatterConfiguration]:
        '''(experimental) Specific configuration for the Json language.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[IOverrideFormatterConfiguration], jsii.get(self, "formatter"))

    @formatter.setter
    def formatter(
        self,
        value: typing.Optional[IOverrideFormatterConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e89ab1d4582824af32b5df4b8bd3f4a29ac64e520e10a121bcd3dc4d64ef7cdd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "formatter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="graphql")
    def graphql(self) -> typing.Optional[IGraphqlConfiguration]:
        '''(experimental) Specific configuration for the Graphql language.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[IGraphqlConfiguration], jsii.get(self, "graphql"))

    @graphql.setter
    def graphql(self, value: typing.Optional[IGraphqlConfiguration]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfb0e146f81a96376a3ced37181741ea2e0474eccb1b17f9f0821ae019e234a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "graphql", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ignore")
    def ignore(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of Unix shell style patterns.

        The formatter will ignore files/folders that will match these patterns.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "ignore"))

    @ignore.setter
    def ignore(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab08ae587969cea7a750fa7202b5a86c94687970b90c6f42d713785c663b38f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignore", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="include")
    def include(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of Unix shell style patterns.

        The formatter will include files/folders that will match these patterns.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "include"))

    @include.setter
    def include(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbd5b4e9f0552303b20dcb0265798669c35589dfea0f8d065f6fc9e070f65f96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "include", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="javascript")
    def javascript(self) -> typing.Optional[IJavascriptConfiguration]:
        '''(experimental) Specific configuration for the JavaScript language.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[IJavascriptConfiguration], jsii.get(self, "javascript"))

    @javascript.setter
    def javascript(self, value: typing.Optional[IJavascriptConfiguration]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d34b80b0bb9c39820993e89d907d443fbcbb21fe606b2d8abab547663550c77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "javascript", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="json")
    def json(self) -> typing.Optional[IJsonConfiguration]:
        '''(experimental) Specific configuration for the Json language.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[IJsonConfiguration], jsii.get(self, "json"))

    @json.setter
    def json(self, value: typing.Optional[IJsonConfiguration]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e04c771c9a2ff9c5a1168d7944c36dd1526283bd29659ed8f5fc7fe94942eb61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "json", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="linter")
    def linter(self) -> typing.Optional[IOverrideLinterConfiguration]:
        '''(experimental) Specific configuration for the Json language.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[IOverrideLinterConfiguration], jsii.get(self, "linter"))

    @linter.setter
    def linter(self, value: typing.Optional[IOverrideLinterConfiguration]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e88e13a66b299498f5541ce455af19d24e8f29b3c304f7f4839a34a4481bdcb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "linter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="organizeImports")
    def organize_imports(
        self,
    ) -> typing.Optional[IOverrideOrganizeImportsConfiguration]:
        '''(experimental) Specific configuration for the Json language.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[IOverrideOrganizeImportsConfiguration], jsii.get(self, "organizeImports"))

    @organize_imports.setter
    def organize_imports(
        self,
        value: typing.Optional[IOverrideOrganizeImportsConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a06f7252353ecf327acd9191ae57302434d7adfa87ee8da8562aafd1a80a80ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "organizeImports", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IOverridePattern).__jsii_proxy_class__ = lambda : _IOverridePatternProxy


@jsii.interface(jsii_type="projen.javascript.biome_config.IPerformance")
class IPerformance(typing_extensions.Protocol):
    '''(experimental) A list of rules that belong to this group.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="all")
    def all(self) -> typing.Optional[builtins.bool]:
        '''(experimental) It enables ALL rules for this group.

        :stability: experimental
        '''
        ...

    @all.setter
    def all(self, value: typing.Optional[builtins.bool]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noAccumulatingSpread")
    def no_accumulating_spread(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow the use of spread (...) syntax on accumulators.

        :stability: experimental
        '''
        ...

    @no_accumulating_spread.setter
    def no_accumulating_spread(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noBarrelFile")
    def no_barrel_file(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow the use of barrel file.

        :stability: experimental
        '''
        ...

    @no_barrel_file.setter
    def no_barrel_file(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noDelete")
    def no_delete(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Disallow the use of the delete operator.

        :stability: experimental
        '''
        ...

    @no_delete.setter
    def no_delete(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noReExportAll")
    def no_re_export_all(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Avoid re-export all.

        :stability: experimental
        '''
        ...

    @no_re_export_all.setter
    def no_re_export_all(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="recommended")
    def recommended(self) -> typing.Optional[builtins.bool]:
        '''(experimental) It enables the recommended rules for this group.

        :stability: experimental
        '''
        ...

    @recommended.setter
    def recommended(self, value: typing.Optional[builtins.bool]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useTopLevelRegex")
    def use_top_level_regex(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Require regex literals to be declared at the top level.

        :stability: experimental
        '''
        ...

    @use_top_level_regex.setter
    def use_top_level_regex(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        ...


class _IPerformanceProxy:
    '''(experimental) A list of rules that belong to this group.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.IPerformance"

    @builtins.property
    @jsii.member(jsii_name="all")
    def all(self) -> typing.Optional[builtins.bool]:
        '''(experimental) It enables ALL rules for this group.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "all"))

    @all.setter
    def all(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4bd59642520c4f651d70ba7da6efe2ad3a0f68f51952810d44b71c852aac97e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "all", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noAccumulatingSpread")
    def no_accumulating_spread(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow the use of spread (...) syntax on accumulators.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "noAccumulatingSpread"))

    @no_accumulating_spread.setter
    def no_accumulating_spread(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32280177979886dfcfde429b04b911b8d2492a79095415e839eee8329a91a716)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noAccumulatingSpread", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noBarrelFile")
    def no_barrel_file(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Disallow the use of barrel file.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "noBarrelFile"))

    @no_barrel_file.setter
    def no_barrel_file(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3076267c34ffdabca9906f0a50b02633ba7405304c78176c3d834339648e500)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noBarrelFile", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noDelete")
    def no_delete(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]]:
        '''(experimental) Disallow the use of the delete operator.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]], jsii.get(self, "noDelete"))

    @no_delete.setter
    def no_delete(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithFixNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d336c9b7ae2bc694bfe1368b9813f49b810b792ac6aa693af8c43bfd968f27c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noDelete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noReExportAll")
    def no_re_export_all(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Avoid re-export all.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "noReExportAll"))

    @no_re_export_all.setter
    def no_re_export_all(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1e011ebc9322ce0b4f846d9394be364cb6e75a740361057a710c47ffd01952b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noReExportAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recommended")
    def recommended(self) -> typing.Optional[builtins.bool]:
        '''(experimental) It enables the recommended rules for this group.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "recommended"))

    @recommended.setter
    def recommended(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9690228dc0e7bf69f79cea6be9e03dd13498b3fce0a20d99f70e0f28f257fb2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recommended", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useTopLevelRegex")
    def use_top_level_regex(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]]:
        '''(experimental) Require regex literals to be declared at the top level.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]], jsii.get(self, "useTopLevelRegex"))

    @use_top_level_regex.setter
    def use_top_level_regex(
        self,
        value: typing.Optional[typing.Union[builtins.str, "IRuleWithNoOptions"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24d70c9c0ce784a0cc2b84599cb055eb6a4ed8c9b4a2a10ba829aefdaf56e46c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useTopLevelRegex", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IPerformance).__jsii_proxy_class__ = lambda : _IPerformanceProxy


@jsii.interface(jsii_type="projen.javascript.biome_config.IRestrictedGlobalsOptions")
class IRestrictedGlobalsOptions(typing_extensions.Protocol):
    '''(experimental) Options for the rule ``noRestrictedGlobals``.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="deniedGlobals")
    def denied_globals(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of names that should trigger the rule.

        :stability: experimental
        '''
        ...

    @denied_globals.setter
    def denied_globals(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        ...


class _IRestrictedGlobalsOptionsProxy:
    '''(experimental) Options for the rule ``noRestrictedGlobals``.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.IRestrictedGlobalsOptions"

    @builtins.property
    @jsii.member(jsii_name="deniedGlobals")
    def denied_globals(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of names that should trigger the rule.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "deniedGlobals"))

    @denied_globals.setter
    def denied_globals(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__030606b1c93d83c19ab639e68fd81d4067cdd9a7a9d67fddee2af1b488d37119)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deniedGlobals", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IRestrictedGlobalsOptions).__jsii_proxy_class__ = lambda : _IRestrictedGlobalsOptionsProxy


@jsii.interface(jsii_type="projen.javascript.biome_config.IRestrictedImportsOptions")
class IRestrictedImportsOptions(typing_extensions.Protocol):
    '''(experimental) Options for the rule ``noRestrictedImports``.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="paths")
    def paths(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) A list of names that should trigger the rule.

        :stability: experimental
        '''
        ...

    @paths.setter
    def paths(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
    ) -> None:
        ...


class _IRestrictedImportsOptionsProxy:
    '''(experimental) Options for the rule ``noRestrictedImports``.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.IRestrictedImportsOptions"

    @builtins.property
    @jsii.member(jsii_name="paths")
    def paths(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) A list of names that should trigger the rule.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "paths"))

    @paths.setter
    def paths(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31f5428261892778dfa820c9ed3e1a5851c08d40ef7f761d1058fc3fbc4e1861)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "paths", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IRestrictedImportsOptions).__jsii_proxy_class__ = lambda : _IRestrictedImportsOptionsProxy


@jsii.interface(jsii_type="projen.javascript.biome_config.IRuleWithAllowDomainOptions")
class IRuleWithAllowDomainOptions(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        '''(experimental) The severity of the emitted diagnostics by the rule.

        :stability: experimental
        '''
        ...

    @level.setter
    def level(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="fix")
    def fix(self) -> typing.Optional[builtins.str]:
        '''(experimental) The kind of the code actions emitted by the rule.

        :stability: experimental
        '''
        ...

    @fix.setter
    def fix(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="options")
    def options(self) -> typing.Optional[IAllowDomainOptions]:
        '''(experimental) Rule's options.

        :stability: experimental
        '''
        ...

    @options.setter
    def options(self, value: typing.Optional[IAllowDomainOptions]) -> None:
        ...


class _IRuleWithAllowDomainOptionsProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.IRuleWithAllowDomainOptions"

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        '''(experimental) The severity of the emitted diagnostics by the rule.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "level"))

    @level.setter
    def level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c712b17bc92c847121143f78e252dcc4d59b111c314bb029b38549b18b7a246d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "level", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fix")
    def fix(self) -> typing.Optional[builtins.str]:
        '''(experimental) The kind of the code actions emitted by the rule.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fix"))

    @fix.setter
    def fix(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62a5ac9161e33195175e4361fa933939e97a7afb92219dc0fff2d14cbc194fca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="options")
    def options(self) -> typing.Optional[IAllowDomainOptions]:
        '''(experimental) Rule's options.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[IAllowDomainOptions], jsii.get(self, "options"))

    @options.setter
    def options(self, value: typing.Optional[IAllowDomainOptions]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ecbb6b3744e4c3c0160e07cdb6db8fd28a86b13e8eb83f92b705e4e4ec5845d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "options", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IRuleWithAllowDomainOptions).__jsii_proxy_class__ = lambda : _IRuleWithAllowDomainOptionsProxy


@jsii.interface(jsii_type="projen.javascript.biome_config.IRuleWithComplexityOptions")
class IRuleWithComplexityOptions(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        '''(experimental) The severity of the emitted diagnostics by the rule.

        :stability: experimental
        '''
        ...

    @level.setter
    def level(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="options")
    def options(self) -> typing.Optional[IComplexityOptions]:
        '''(experimental) Rule's options.

        :stability: experimental
        '''
        ...

    @options.setter
    def options(self, value: typing.Optional[IComplexityOptions]) -> None:
        ...


class _IRuleWithComplexityOptionsProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.IRuleWithComplexityOptions"

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        '''(experimental) The severity of the emitted diagnostics by the rule.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "level"))

    @level.setter
    def level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d6cb05a8a9baf9f40c655fe27fb187c6675a260225fa5d5afe9792ead0aa8f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "level", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="options")
    def options(self) -> typing.Optional[IComplexityOptions]:
        '''(experimental) Rule's options.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[IComplexityOptions], jsii.get(self, "options"))

    @options.setter
    def options(self, value: typing.Optional[IComplexityOptions]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b79c5095bec60f7df45bf3726ec346b7b8d2ae43ed1a99f36490827b27ef358)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "options", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IRuleWithComplexityOptions).__jsii_proxy_class__ = lambda : _IRuleWithComplexityOptionsProxy


@jsii.interface(
    jsii_type="projen.javascript.biome_config.IRuleWithConsistentArrayTypeOptions"
)
class IRuleWithConsistentArrayTypeOptions(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        '''(experimental) The severity of the emitted diagnostics by the rule.

        :stability: experimental
        '''
        ...

    @level.setter
    def level(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="fix")
    def fix(self) -> typing.Optional[builtins.str]:
        '''(experimental) The kind of the code actions emitted by the rule.

        :stability: experimental
        '''
        ...

    @fix.setter
    def fix(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="options")
    def options(self) -> typing.Optional[IConsistentArrayTypeOptions]:
        '''(experimental) Rule's options.

        :stability: experimental
        '''
        ...

    @options.setter
    def options(self, value: typing.Optional[IConsistentArrayTypeOptions]) -> None:
        ...


class _IRuleWithConsistentArrayTypeOptionsProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.IRuleWithConsistentArrayTypeOptions"

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        '''(experimental) The severity of the emitted diagnostics by the rule.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "level"))

    @level.setter
    def level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__609221c2d3b885ecc28ff42572fd611905fdcc786d51c22f95854318cf48f853)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "level", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fix")
    def fix(self) -> typing.Optional[builtins.str]:
        '''(experimental) The kind of the code actions emitted by the rule.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fix"))

    @fix.setter
    def fix(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__396150b54651de2cec023b3126362e3272eb77bdf7cceb964919d2276cd00531)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="options")
    def options(self) -> typing.Optional[IConsistentArrayTypeOptions]:
        '''(experimental) Rule's options.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[IConsistentArrayTypeOptions], jsii.get(self, "options"))

    @options.setter
    def options(self, value: typing.Optional[IConsistentArrayTypeOptions]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27a8be1934146e26c8eb3883e28144d8334ef482f4d237890aad9b6a71f15d07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "options", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IRuleWithConsistentArrayTypeOptions).__jsii_proxy_class__ = lambda : _IRuleWithConsistentArrayTypeOptionsProxy


@jsii.interface(
    jsii_type="projen.javascript.biome_config.IRuleWithConsistentMemberAccessibilityOptions"
)
class IRuleWithConsistentMemberAccessibilityOptions(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        '''(experimental) The severity of the emitted diagnostics by the rule.

        :stability: experimental
        '''
        ...

    @level.setter
    def level(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="options")
    def options(self) -> typing.Optional[IConsistentMemberAccessibilityOptions]:
        '''(experimental) Rule's options.

        :stability: experimental
        '''
        ...

    @options.setter
    def options(
        self,
        value: typing.Optional[IConsistentMemberAccessibilityOptions],
    ) -> None:
        ...


class _IRuleWithConsistentMemberAccessibilityOptionsProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.IRuleWithConsistentMemberAccessibilityOptions"

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        '''(experimental) The severity of the emitted diagnostics by the rule.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "level"))

    @level.setter
    def level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e937a76d175adaa2a5ae5cfb35018919df30ff49d0f043f3248facf907e2ea2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "level", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="options")
    def options(self) -> typing.Optional[IConsistentMemberAccessibilityOptions]:
        '''(experimental) Rule's options.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[IConsistentMemberAccessibilityOptions], jsii.get(self, "options"))

    @options.setter
    def options(
        self,
        value: typing.Optional[IConsistentMemberAccessibilityOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bc3372d0bf66efb0e1f6c4a7cba2404926b88d59b7e7f2979ae7f0a4a38b4e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "options", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IRuleWithConsistentMemberAccessibilityOptions).__jsii_proxy_class__ = lambda : _IRuleWithConsistentMemberAccessibilityOptionsProxy


@jsii.interface(
    jsii_type="projen.javascript.biome_config.IRuleWithDeprecatedHooksOptions"
)
class IRuleWithDeprecatedHooksOptions(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        '''(experimental) The severity of the emitted diagnostics by the rule.

        :stability: experimental
        '''
        ...

    @level.setter
    def level(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="options")
    def options(self) -> typing.Optional[IDeprecatedHooksOptions]:
        '''(experimental) Rule's options.

        :stability: experimental
        '''
        ...

    @options.setter
    def options(self, value: typing.Optional[IDeprecatedHooksOptions]) -> None:
        ...


class _IRuleWithDeprecatedHooksOptionsProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.IRuleWithDeprecatedHooksOptions"

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        '''(experimental) The severity of the emitted diagnostics by the rule.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "level"))

    @level.setter
    def level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bf816437c9055f086c831bdd67215a76f3519d1e1c1d908316b23b789e45cfc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "level", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="options")
    def options(self) -> typing.Optional[IDeprecatedHooksOptions]:
        '''(experimental) Rule's options.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[IDeprecatedHooksOptions], jsii.get(self, "options"))

    @options.setter
    def options(self, value: typing.Optional[IDeprecatedHooksOptions]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dde99ac5e14d758decc8b4823e29767c2f925f3118cb9d8c7cb7505dd05260c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "options", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IRuleWithDeprecatedHooksOptions).__jsii_proxy_class__ = lambda : _IRuleWithDeprecatedHooksOptionsProxy


@jsii.interface(
    jsii_type="projen.javascript.biome_config.IRuleWithFilenamingConventionOptions"
)
class IRuleWithFilenamingConventionOptions(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        '''(experimental) The severity of the emitted diagnostics by the rule.

        :stability: experimental
        '''
        ...

    @level.setter
    def level(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="options")
    def options(self) -> typing.Optional[IFilenamingConventionOptions]:
        '''(experimental) Rule's options.

        :stability: experimental
        '''
        ...

    @options.setter
    def options(self, value: typing.Optional[IFilenamingConventionOptions]) -> None:
        ...


class _IRuleWithFilenamingConventionOptionsProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.IRuleWithFilenamingConventionOptions"

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        '''(experimental) The severity of the emitted diagnostics by the rule.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "level"))

    @level.setter
    def level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6c1404d544b4633c45f389a6ce47dd5c0c67f50202ba9fdc764d3062ffe43c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "level", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="options")
    def options(self) -> typing.Optional[IFilenamingConventionOptions]:
        '''(experimental) Rule's options.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[IFilenamingConventionOptions], jsii.get(self, "options"))

    @options.setter
    def options(self, value: typing.Optional[IFilenamingConventionOptions]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64e8786caf3e13e3c60a5a696f5e413d390fbcacb66297109ccf7e7e3ed0acba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "options", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IRuleWithFilenamingConventionOptions).__jsii_proxy_class__ = lambda : _IRuleWithFilenamingConventionOptionsProxy


@jsii.interface(jsii_type="projen.javascript.biome_config.IRuleWithFixNoOptions")
class IRuleWithFixNoOptions(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        '''(experimental) The severity of the emitted diagnostics by the rule.

        :stability: experimental
        '''
        ...

    @level.setter
    def level(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="fix")
    def fix(self) -> typing.Optional[builtins.str]:
        '''(experimental) The kind of the code actions emitted by the rule.

        :stability: experimental
        '''
        ...

    @fix.setter
    def fix(self, value: typing.Optional[builtins.str]) -> None:
        ...


class _IRuleWithFixNoOptionsProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.IRuleWithFixNoOptions"

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        '''(experimental) The severity of the emitted diagnostics by the rule.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "level"))

    @level.setter
    def level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7db58781e48ac7d907788085317963354ec7de5a919bce58bc30bc8c27432fd3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "level", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fix")
    def fix(self) -> typing.Optional[builtins.str]:
        '''(experimental) The kind of the code actions emitted by the rule.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fix"))

    @fix.setter
    def fix(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b75577940ad46ebbe5282e02f216acdfdfc055f099d729410f20eadf7ec878c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fix", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IRuleWithFixNoOptions).__jsii_proxy_class__ = lambda : _IRuleWithFixNoOptionsProxy


@jsii.interface(
    jsii_type="projen.javascript.biome_config.IRuleWithNamingConventionOptions"
)
class IRuleWithNamingConventionOptions(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        '''(experimental) The severity of the emitted diagnostics by the rule.

        :stability: experimental
        '''
        ...

    @level.setter
    def level(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="fix")
    def fix(self) -> typing.Optional[builtins.str]:
        '''(experimental) The kind of the code actions emitted by the rule.

        :stability: experimental
        '''
        ...

    @fix.setter
    def fix(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="options")
    def options(self) -> typing.Optional[INamingConventionOptions]:
        '''(experimental) Rule's options.

        :stability: experimental
        '''
        ...

    @options.setter
    def options(self, value: typing.Optional[INamingConventionOptions]) -> None:
        ...


class _IRuleWithNamingConventionOptionsProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.IRuleWithNamingConventionOptions"

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        '''(experimental) The severity of the emitted diagnostics by the rule.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "level"))

    @level.setter
    def level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59e6160a3378d4e94ff6a8394b7da2f7f1a34f5233a6bd6abfa36d50a8b40771)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "level", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fix")
    def fix(self) -> typing.Optional[builtins.str]:
        '''(experimental) The kind of the code actions emitted by the rule.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fix"))

    @fix.setter
    def fix(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79826f39d94c46a8cc2a2a097bd5edf5b0068e126425c33950b922237e23f7c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="options")
    def options(self) -> typing.Optional[INamingConventionOptions]:
        '''(experimental) Rule's options.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[INamingConventionOptions], jsii.get(self, "options"))

    @options.setter
    def options(self, value: typing.Optional[INamingConventionOptions]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8f51a099a2d6cf71978e4c5feba8fa641f40cfd35dade3c15842f73eec547a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "options", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IRuleWithNamingConventionOptions).__jsii_proxy_class__ = lambda : _IRuleWithNamingConventionOptionsProxy


@jsii.interface(jsii_type="projen.javascript.biome_config.IRuleWithNoConsoleOptions")
class IRuleWithNoConsoleOptions(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        '''(experimental) The severity of the emitted diagnostics by the rule.

        :stability: experimental
        '''
        ...

    @level.setter
    def level(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="fix")
    def fix(self) -> typing.Optional[builtins.str]:
        '''(experimental) The kind of the code actions emitted by the rule.

        :stability: experimental
        '''
        ...

    @fix.setter
    def fix(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="options")
    def options(self) -> typing.Optional[INoConsoleOptions]:
        '''(experimental) Rule's options.

        :stability: experimental
        '''
        ...

    @options.setter
    def options(self, value: typing.Optional[INoConsoleOptions]) -> None:
        ...


class _IRuleWithNoConsoleOptionsProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.IRuleWithNoConsoleOptions"

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        '''(experimental) The severity of the emitted diagnostics by the rule.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "level"))

    @level.setter
    def level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eeab537bd6bcae9ce3d55939eb876589828bc12348b887ba32d0a77497df48c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "level", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fix")
    def fix(self) -> typing.Optional[builtins.str]:
        '''(experimental) The kind of the code actions emitted by the rule.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fix"))

    @fix.setter
    def fix(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25adb4cbd3fe9c8868e116de37a76c5d4e8ed4cdc92f3aadd564d4c1549472b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="options")
    def options(self) -> typing.Optional[INoConsoleOptions]:
        '''(experimental) Rule's options.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[INoConsoleOptions], jsii.get(self, "options"))

    @options.setter
    def options(self, value: typing.Optional[INoConsoleOptions]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38d3d7c8fc3da224b65bf133005feaf1e1758a34d305405b309f3dbc0dc626b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "options", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IRuleWithNoConsoleOptions).__jsii_proxy_class__ = lambda : _IRuleWithNoConsoleOptionsProxy


@jsii.interface(
    jsii_type="projen.javascript.biome_config.IRuleWithNoDoubleEqualsOptions"
)
class IRuleWithNoDoubleEqualsOptions(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        '''(experimental) The severity of the emitted diagnostics by the rule.

        :stability: experimental
        '''
        ...

    @level.setter
    def level(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="fix")
    def fix(self) -> typing.Optional[builtins.str]:
        '''(experimental) The kind of the code actions emitted by the rule.

        :stability: experimental
        '''
        ...

    @fix.setter
    def fix(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="options")
    def options(self) -> typing.Optional[INoDoubleEqualsOptions]:
        '''(experimental) Rule's options.

        :stability: experimental
        '''
        ...

    @options.setter
    def options(self, value: typing.Optional[INoDoubleEqualsOptions]) -> None:
        ...


class _IRuleWithNoDoubleEqualsOptionsProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.IRuleWithNoDoubleEqualsOptions"

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        '''(experimental) The severity of the emitted diagnostics by the rule.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "level"))

    @level.setter
    def level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4addff9f8b62ae2c19c26158236bdf524520c14f55ca683754b1dd4225ed304a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "level", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fix")
    def fix(self) -> typing.Optional[builtins.str]:
        '''(experimental) The kind of the code actions emitted by the rule.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fix"))

    @fix.setter
    def fix(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2923cbaa051184632a80348a744af3f982efdfc7e66f60ac4bdc79ab96c821c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="options")
    def options(self) -> typing.Optional[INoDoubleEqualsOptions]:
        '''(experimental) Rule's options.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[INoDoubleEqualsOptions], jsii.get(self, "options"))

    @options.setter
    def options(self, value: typing.Optional[INoDoubleEqualsOptions]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78483eb28be3c363cde9bced10e08e67bf5c191eb35992af8263c6566a604b16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "options", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IRuleWithNoDoubleEqualsOptions).__jsii_proxy_class__ = lambda : _IRuleWithNoDoubleEqualsOptionsProxy


@jsii.interface(
    jsii_type="projen.javascript.biome_config.IRuleWithNoLabelWithoutControlOptions"
)
class IRuleWithNoLabelWithoutControlOptions(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        '''(experimental) The severity of the emitted diagnostics by the rule.

        :stability: experimental
        '''
        ...

    @level.setter
    def level(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="options")
    def options(self) -> typing.Optional[INoLabelWithoutControlOptions]:
        '''(experimental) Rule's options.

        :stability: experimental
        '''
        ...

    @options.setter
    def options(self, value: typing.Optional[INoLabelWithoutControlOptions]) -> None:
        ...


class _IRuleWithNoLabelWithoutControlOptionsProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.IRuleWithNoLabelWithoutControlOptions"

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        '''(experimental) The severity of the emitted diagnostics by the rule.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "level"))

    @level.setter
    def level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fe3748201c171b15702fc5e6ca90e0bdd2d5c442951503adeac4aa969225774)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "level", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="options")
    def options(self) -> typing.Optional[INoLabelWithoutControlOptions]:
        '''(experimental) Rule's options.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[INoLabelWithoutControlOptions], jsii.get(self, "options"))

    @options.setter
    def options(self, value: typing.Optional[INoLabelWithoutControlOptions]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c44591ce06042b398ba71e757b887038f51fc00aab0105dbde6dfcc02bfeb93d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "options", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IRuleWithNoLabelWithoutControlOptions).__jsii_proxy_class__ = lambda : _IRuleWithNoLabelWithoutControlOptionsProxy


@jsii.interface(jsii_type="projen.javascript.biome_config.IRuleWithNoOptions")
class IRuleWithNoOptions(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        '''(experimental) The severity of the emitted diagnostics by the rule.

        :stability: experimental
        '''
        ...

    @level.setter
    def level(self, value: builtins.str) -> None:
        ...


class _IRuleWithNoOptionsProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.IRuleWithNoOptions"

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        '''(experimental) The severity of the emitted diagnostics by the rule.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "level"))

    @level.setter
    def level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb19b10c6a87dd18f594a7f7621a186e176b41703aea42aba4df2845087afb44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "level", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IRuleWithNoOptions).__jsii_proxy_class__ = lambda : _IRuleWithNoOptionsProxy


@jsii.interface(
    jsii_type="projen.javascript.biome_config.IRuleWithNoRestrictedTypesOptions"
)
class IRuleWithNoRestrictedTypesOptions(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        '''(experimental) The severity of the emitted diagnostics by the rule.

        :stability: experimental
        '''
        ...

    @level.setter
    def level(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="fix")
    def fix(self) -> typing.Optional[builtins.str]:
        '''(experimental) The kind of the code actions emitted by the rule.

        :stability: experimental
        '''
        ...

    @fix.setter
    def fix(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="options")
    def options(self) -> typing.Optional[INoRestrictedTypesOptions]:
        '''(experimental) Rule's options.

        :stability: experimental
        '''
        ...

    @options.setter
    def options(self, value: typing.Optional[INoRestrictedTypesOptions]) -> None:
        ...


class _IRuleWithNoRestrictedTypesOptionsProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.IRuleWithNoRestrictedTypesOptions"

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        '''(experimental) The severity of the emitted diagnostics by the rule.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "level"))

    @level.setter
    def level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a81b671ffb73c6511f2b61a6906af16973f67c5d1a7e037a06e88168490980f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "level", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fix")
    def fix(self) -> typing.Optional[builtins.str]:
        '''(experimental) The kind of the code actions emitted by the rule.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fix"))

    @fix.setter
    def fix(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8585e2a15ab739d1817844a5f1fe7d4e980ed3f59a8353e46a345cd9f8c2828f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="options")
    def options(self) -> typing.Optional[INoRestrictedTypesOptions]:
        '''(experimental) Rule's options.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[INoRestrictedTypesOptions], jsii.get(self, "options"))

    @options.setter
    def options(self, value: typing.Optional[INoRestrictedTypesOptions]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfe087d2695a9a504a48e052f1b1332b1ee0e69007b829f881f8a6f89b1ba7a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "options", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IRuleWithNoRestrictedTypesOptions).__jsii_proxy_class__ = lambda : _IRuleWithNoRestrictedTypesOptionsProxy


@jsii.interface(jsii_type="projen.javascript.biome_config.IRuleWithNoSecretsOptions")
class IRuleWithNoSecretsOptions(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        '''(experimental) The severity of the emitted diagnostics by the rule.

        :stability: experimental
        '''
        ...

    @level.setter
    def level(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="options")
    def options(self) -> typing.Optional[INoSecretsOptions]:
        '''(experimental) Rule's options.

        :stability: experimental
        '''
        ...

    @options.setter
    def options(self, value: typing.Optional[INoSecretsOptions]) -> None:
        ...


class _IRuleWithNoSecretsOptionsProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.IRuleWithNoSecretsOptions"

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        '''(experimental) The severity of the emitted diagnostics by the rule.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "level"))

    @level.setter
    def level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab035c665923dabc5d870cdcc7ebb50687c667f73b15eef7ecf08d1d5c041cca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "level", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="options")
    def options(self) -> typing.Optional[INoSecretsOptions]:
        '''(experimental) Rule's options.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[INoSecretsOptions], jsii.get(self, "options"))

    @options.setter
    def options(self, value: typing.Optional[INoSecretsOptions]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b7c778e3a1b7032c50250010f973ab9870d60472670eef2e5213c9d7a444e12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "options", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IRuleWithNoSecretsOptions).__jsii_proxy_class__ = lambda : _IRuleWithNoSecretsOptionsProxy


@jsii.interface(
    jsii_type="projen.javascript.biome_config.IRuleWithRestrictedGlobalsOptions"
)
class IRuleWithRestrictedGlobalsOptions(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        '''(experimental) The severity of the emitted diagnostics by the rule.

        :stability: experimental
        '''
        ...

    @level.setter
    def level(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="options")
    def options(self) -> typing.Optional[IRestrictedGlobalsOptions]:
        '''(experimental) Rule's options.

        :stability: experimental
        '''
        ...

    @options.setter
    def options(self, value: typing.Optional[IRestrictedGlobalsOptions]) -> None:
        ...


class _IRuleWithRestrictedGlobalsOptionsProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.IRuleWithRestrictedGlobalsOptions"

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        '''(experimental) The severity of the emitted diagnostics by the rule.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "level"))

    @level.setter
    def level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__492028b0a9f7954d44a0c7a93858a557e795281dbf23ccc0f6c4bc212c56c340)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "level", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="options")
    def options(self) -> typing.Optional[IRestrictedGlobalsOptions]:
        '''(experimental) Rule's options.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[IRestrictedGlobalsOptions], jsii.get(self, "options"))

    @options.setter
    def options(self, value: typing.Optional[IRestrictedGlobalsOptions]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1a875f5dddddc886ec58e6e13954ab979ff4b03d2276516911d61d0081a1b92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "options", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IRuleWithRestrictedGlobalsOptions).__jsii_proxy_class__ = lambda : _IRuleWithRestrictedGlobalsOptionsProxy


@jsii.interface(
    jsii_type="projen.javascript.biome_config.IRuleWithRestrictedImportsOptions"
)
class IRuleWithRestrictedImportsOptions(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        '''(experimental) The severity of the emitted diagnostics by the rule.

        :stability: experimental
        '''
        ...

    @level.setter
    def level(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="options")
    def options(self) -> typing.Optional[IRestrictedImportsOptions]:
        '''(experimental) Rule's options.

        :stability: experimental
        '''
        ...

    @options.setter
    def options(self, value: typing.Optional[IRestrictedImportsOptions]) -> None:
        ...


class _IRuleWithRestrictedImportsOptionsProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.IRuleWithRestrictedImportsOptions"

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        '''(experimental) The severity of the emitted diagnostics by the rule.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "level"))

    @level.setter
    def level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db76ef0190ac0c1ab658e69e47727ace4a8007bb2bbcd8f382d2f58013c04657)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "level", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="options")
    def options(self) -> typing.Optional[IRestrictedImportsOptions]:
        '''(experimental) Rule's options.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[IRestrictedImportsOptions], jsii.get(self, "options"))

    @options.setter
    def options(self, value: typing.Optional[IRestrictedImportsOptions]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d805009f791b2436eb6f87f9e2334d37bc5b523a8d4f1123997a47cc056d511)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "options", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IRuleWithRestrictedImportsOptions).__jsii_proxy_class__ = lambda : _IRuleWithRestrictedImportsOptionsProxy


@jsii.interface(
    jsii_type="projen.javascript.biome_config.IRuleWithUseComponentExportOnlyModulesOptions"
)
class IRuleWithUseComponentExportOnlyModulesOptions(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        '''(experimental) The severity of the emitted diagnostics by the rule.

        :stability: experimental
        '''
        ...

    @level.setter
    def level(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="options")
    def options(self) -> typing.Optional["IUseComponentExportOnlyModulesOptions"]:
        '''(experimental) Rule's options.

        :stability: experimental
        '''
        ...

    @options.setter
    def options(
        self,
        value: typing.Optional["IUseComponentExportOnlyModulesOptions"],
    ) -> None:
        ...


class _IRuleWithUseComponentExportOnlyModulesOptionsProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.IRuleWithUseComponentExportOnlyModulesOptions"

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        '''(experimental) The severity of the emitted diagnostics by the rule.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "level"))

    @level.setter
    def level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77eab468ddbb14f6ddad5db8e6cbeb195ffd09fe9db9dc0f05d4b1cedb83d6f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "level", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="options")
    def options(self) -> typing.Optional["IUseComponentExportOnlyModulesOptions"]:
        '''(experimental) Rule's options.

        :stability: experimental
        '''
        return typing.cast(typing.Optional["IUseComponentExportOnlyModulesOptions"], jsii.get(self, "options"))

    @options.setter
    def options(
        self,
        value: typing.Optional["IUseComponentExportOnlyModulesOptions"],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb3b8dd9529a114c6da5fc615fccc34b6c540352f078beabf9aa731fe333d37e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "options", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IRuleWithUseComponentExportOnlyModulesOptions).__jsii_proxy_class__ = lambda : _IRuleWithUseComponentExportOnlyModulesOptionsProxy


@jsii.interface(
    jsii_type="projen.javascript.biome_config.IRuleWithUseExhaustiveDependenciesOptions"
)
class IRuleWithUseExhaustiveDependenciesOptions(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        '''(experimental) The severity of the emitted diagnostics by the rule.

        :stability: experimental
        '''
        ...

    @level.setter
    def level(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="options")
    def options(self) -> typing.Optional["IUseExhaustiveDependenciesOptions"]:
        '''(experimental) Rule's options.

        :stability: experimental
        '''
        ...

    @options.setter
    def options(
        self,
        value: typing.Optional["IUseExhaustiveDependenciesOptions"],
    ) -> None:
        ...


class _IRuleWithUseExhaustiveDependenciesOptionsProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.IRuleWithUseExhaustiveDependenciesOptions"

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        '''(experimental) The severity of the emitted diagnostics by the rule.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "level"))

    @level.setter
    def level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a155bdfac3ab7ea25a66c7a7d87e787bc513df419a50a51f9514db60b73664a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "level", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="options")
    def options(self) -> typing.Optional["IUseExhaustiveDependenciesOptions"]:
        '''(experimental) Rule's options.

        :stability: experimental
        '''
        return typing.cast(typing.Optional["IUseExhaustiveDependenciesOptions"], jsii.get(self, "options"))

    @options.setter
    def options(
        self,
        value: typing.Optional["IUseExhaustiveDependenciesOptions"],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a90e05ca35603ae645955c66ca9bb731354e06687289bba78a318e8330caaf6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "options", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IRuleWithUseExhaustiveDependenciesOptions).__jsii_proxy_class__ = lambda : _IRuleWithUseExhaustiveDependenciesOptionsProxy


@jsii.interface(
    jsii_type="projen.javascript.biome_config.IRuleWithUseImportExtensionsOptions"
)
class IRuleWithUseImportExtensionsOptions(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        '''(experimental) The severity of the emitted diagnostics by the rule.

        :stability: experimental
        '''
        ...

    @level.setter
    def level(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="fix")
    def fix(self) -> typing.Optional[builtins.str]:
        '''(experimental) The kind of the code actions emitted by the rule.

        :stability: experimental
        '''
        ...

    @fix.setter
    def fix(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="options")
    def options(self) -> typing.Optional["IUseImportExtensionsOptions"]:
        '''(experimental) Rule's options.

        :stability: experimental
        '''
        ...

    @options.setter
    def options(self, value: typing.Optional["IUseImportExtensionsOptions"]) -> None:
        ...


class _IRuleWithUseImportExtensionsOptionsProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.IRuleWithUseImportExtensionsOptions"

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        '''(experimental) The severity of the emitted diagnostics by the rule.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "level"))

    @level.setter
    def level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23432c2b5966f4bc60853a5068ea336a3fa0e98bb08b2981d5a4ad88593602f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "level", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fix")
    def fix(self) -> typing.Optional[builtins.str]:
        '''(experimental) The kind of the code actions emitted by the rule.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fix"))

    @fix.setter
    def fix(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a809ce8bc006991524094af9f718f896eb9d2dc6c3b588ea3317213e173fc148)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="options")
    def options(self) -> typing.Optional["IUseImportExtensionsOptions"]:
        '''(experimental) Rule's options.

        :stability: experimental
        '''
        return typing.cast(typing.Optional["IUseImportExtensionsOptions"], jsii.get(self, "options"))

    @options.setter
    def options(self, value: typing.Optional["IUseImportExtensionsOptions"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3576ad5e4b811f6ff0b9db3c5476e61585d6eb248107d534f5e82b74b77d12f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "options", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IRuleWithUseImportExtensionsOptions).__jsii_proxy_class__ = lambda : _IRuleWithUseImportExtensionsOptionsProxy


@jsii.interface(
    jsii_type="projen.javascript.biome_config.IRuleWithUseValidAutocompleteOptions"
)
class IRuleWithUseValidAutocompleteOptions(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        '''(experimental) The severity of the emitted diagnostics by the rule.

        :stability: experimental
        '''
        ...

    @level.setter
    def level(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="options")
    def options(self) -> typing.Optional["IUseValidAutocompleteOptions"]:
        '''(experimental) Rule's options.

        :stability: experimental
        '''
        ...

    @options.setter
    def options(self, value: typing.Optional["IUseValidAutocompleteOptions"]) -> None:
        ...


class _IRuleWithUseValidAutocompleteOptionsProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.IRuleWithUseValidAutocompleteOptions"

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        '''(experimental) The severity of the emitted diagnostics by the rule.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "level"))

    @level.setter
    def level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fba5a73ee2b82bb6089df92cc87bf8af4db240469a0acd2c5ecd40eb3ff86a64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "level", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="options")
    def options(self) -> typing.Optional["IUseValidAutocompleteOptions"]:
        '''(experimental) Rule's options.

        :stability: experimental
        '''
        return typing.cast(typing.Optional["IUseValidAutocompleteOptions"], jsii.get(self, "options"))

    @options.setter
    def options(self, value: typing.Optional["IUseValidAutocompleteOptions"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e7730b1a62dc09d7aa2cd8b4e50ab6c803b3d40c5e63706a231b83e2cc178c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "options", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IRuleWithUseValidAutocompleteOptions).__jsii_proxy_class__ = lambda : _IRuleWithUseValidAutocompleteOptionsProxy


@jsii.interface(
    jsii_type="projen.javascript.biome_config.IRuleWithUtilityClassSortingOptions"
)
class IRuleWithUtilityClassSortingOptions(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        '''(experimental) The severity of the emitted diagnostics by the rule.

        :stability: experimental
        '''
        ...

    @level.setter
    def level(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="fix")
    def fix(self) -> typing.Optional[builtins.str]:
        '''(experimental) The kind of the code actions emitted by the rule.

        :stability: experimental
        '''
        ...

    @fix.setter
    def fix(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="options")
    def options(self) -> typing.Optional["IUtilityClassSortingOptions"]:
        '''(experimental) Rule's options.

        :stability: experimental
        '''
        ...

    @options.setter
    def options(self, value: typing.Optional["IUtilityClassSortingOptions"]) -> None:
        ...


class _IRuleWithUtilityClassSortingOptionsProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.IRuleWithUtilityClassSortingOptions"

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        '''(experimental) The severity of the emitted diagnostics by the rule.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "level"))

    @level.setter
    def level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__692ccab272ce4d4a7ad37820696fed26a42114bee2f68a9874837df87982c3ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "level", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fix")
    def fix(self) -> typing.Optional[builtins.str]:
        '''(experimental) The kind of the code actions emitted by the rule.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fix"))

    @fix.setter
    def fix(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cc259341b4abca3011654bdc1c3d7792db7a951f864ee0235a2e62526bcc85b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="options")
    def options(self) -> typing.Optional["IUtilityClassSortingOptions"]:
        '''(experimental) Rule's options.

        :stability: experimental
        '''
        return typing.cast(typing.Optional["IUtilityClassSortingOptions"], jsii.get(self, "options"))

    @options.setter
    def options(self, value: typing.Optional["IUtilityClassSortingOptions"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a37e07704c6d0315a610f231aabd5bfce457f37b684d1d5b8f2bd20aa3eba55b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "options", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IRuleWithUtilityClassSortingOptions).__jsii_proxy_class__ = lambda : _IRuleWithUtilityClassSortingOptionsProxy


@jsii.interface(
    jsii_type="projen.javascript.biome_config.IRuleWithValidAriaRoleOptions"
)
class IRuleWithValidAriaRoleOptions(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        '''(experimental) The severity of the emitted diagnostics by the rule.

        :stability: experimental
        '''
        ...

    @level.setter
    def level(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="fix")
    def fix(self) -> typing.Optional[builtins.str]:
        '''(experimental) The kind of the code actions emitted by the rule.

        :stability: experimental
        '''
        ...

    @fix.setter
    def fix(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="options")
    def options(self) -> typing.Optional["IValidAriaRoleOptions"]:
        '''(experimental) Rule's options.

        :stability: experimental
        '''
        ...

    @options.setter
    def options(self, value: typing.Optional["IValidAriaRoleOptions"]) -> None:
        ...


class _IRuleWithValidAriaRoleOptionsProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.IRuleWithValidAriaRoleOptions"

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        '''(experimental) The severity of the emitted diagnostics by the rule.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "level"))

    @level.setter
    def level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e038de659dbcaf1ea5c4d091afc76401b9dc2b6fb2afaab98654308cff53fb67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "level", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fix")
    def fix(self) -> typing.Optional[builtins.str]:
        '''(experimental) The kind of the code actions emitted by the rule.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fix"))

    @fix.setter
    def fix(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6ca52ba939b4b20b89e1699f3af4d7668d1a77409e1925b0e1aa501a52a2c3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="options")
    def options(self) -> typing.Optional["IValidAriaRoleOptions"]:
        '''(experimental) Rule's options.

        :stability: experimental
        '''
        return typing.cast(typing.Optional["IValidAriaRoleOptions"], jsii.get(self, "options"))

    @options.setter
    def options(self, value: typing.Optional["IValidAriaRoleOptions"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45bc209e05b8556c1e51b80d0b9845dda47ef5a45853fc111ac0eea7692aa994)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "options", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IRuleWithValidAriaRoleOptions).__jsii_proxy_class__ = lambda : _IRuleWithValidAriaRoleOptionsProxy


@jsii.interface(jsii_type="projen.javascript.biome_config.IRules")
class IRules(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="a11y")
    def a11y(self) -> typing.Optional[IA11y]:
        '''
        :stability: experimental
        '''
        ...

    @a11y.setter
    def a11y(self, value: typing.Optional[IA11y]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="all")
    def all(self) -> typing.Optional[builtins.bool]:
        '''(experimental) It enables ALL rules.

        The rules that belong to ``nursery`` won't be enabled.

        :stability: experimental
        '''
        ...

    @all.setter
    def all(self, value: typing.Optional[builtins.bool]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="complexity")
    def complexity(self) -> typing.Optional[IComplexity]:
        '''
        :stability: experimental
        '''
        ...

    @complexity.setter
    def complexity(self, value: typing.Optional[IComplexity]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="correctness")
    def correctness(self) -> typing.Optional[ICorrectness]:
        '''
        :stability: experimental
        '''
        ...

    @correctness.setter
    def correctness(self, value: typing.Optional[ICorrectness]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="nursery")
    def nursery(self) -> typing.Optional[INursery]:
        '''
        :stability: experimental
        '''
        ...

    @nursery.setter
    def nursery(self, value: typing.Optional[INursery]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="performance")
    def performance(self) -> typing.Optional[IPerformance]:
        '''
        :stability: experimental
        '''
        ...

    @performance.setter
    def performance(self, value: typing.Optional[IPerformance]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="recommended")
    def recommended(self) -> typing.Optional[builtins.bool]:
        '''(experimental) It enables the lint rules recommended by Biome.

        ``true`` by default.

        :stability: experimental
        '''
        ...

    @recommended.setter
    def recommended(self, value: typing.Optional[builtins.bool]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="security")
    def security(self) -> typing.Optional["ISecurity"]:
        '''
        :stability: experimental
        '''
        ...

    @security.setter
    def security(self, value: typing.Optional["ISecurity"]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="style")
    def style(self) -> typing.Optional["IStyle"]:
        '''
        :stability: experimental
        '''
        ...

    @style.setter
    def style(self, value: typing.Optional["IStyle"]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="suspicious")
    def suspicious(self) -> typing.Optional["ISuspicious"]:
        '''
        :stability: experimental
        '''
        ...

    @suspicious.setter
    def suspicious(self, value: typing.Optional["ISuspicious"]) -> None:
        ...


class _IRulesProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.IRules"

    @builtins.property
    @jsii.member(jsii_name="a11y")
    def a11y(self) -> typing.Optional[IA11y]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[IA11y], jsii.get(self, "a11y"))

    @a11y.setter
    def a11y(self, value: typing.Optional[IA11y]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80353c4af30e7715f57809eb4d005b4c39dfd2e0a5e11ce5906a75b7bbd8ccf0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "a11y", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="all")
    def all(self) -> typing.Optional[builtins.bool]:
        '''(experimental) It enables ALL rules.

        The rules that belong to ``nursery`` won't be enabled.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "all"))

    @all.setter
    def all(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61e10a4821368e9a192337f2248658b408862a9bc36ad69e9504e413a87044a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "all", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="complexity")
    def complexity(self) -> typing.Optional[IComplexity]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[IComplexity], jsii.get(self, "complexity"))

    @complexity.setter
    def complexity(self, value: typing.Optional[IComplexity]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b112b84e3fe60df1001f21c688bd3fbf4222cd16a31c73a814e18350775c2fbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "complexity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="correctness")
    def correctness(self) -> typing.Optional[ICorrectness]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[ICorrectness], jsii.get(self, "correctness"))

    @correctness.setter
    def correctness(self, value: typing.Optional[ICorrectness]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30dbf678299a96e170712804c846f480595e70dcc0011cb108601c12f31dc30c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "correctness", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nursery")
    def nursery(self) -> typing.Optional[INursery]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[INursery], jsii.get(self, "nursery"))

    @nursery.setter
    def nursery(self, value: typing.Optional[INursery]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__825db897eba98ea78de06620f119ac4960f666b85af371528a5939e7bcde9b35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nursery", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="performance")
    def performance(self) -> typing.Optional[IPerformance]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[IPerformance], jsii.get(self, "performance"))

    @performance.setter
    def performance(self, value: typing.Optional[IPerformance]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cfb14783260626da54cc1797807690431426b6d6da51401beb3d6db00566468)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "performance", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recommended")
    def recommended(self) -> typing.Optional[builtins.bool]:
        '''(experimental) It enables the lint rules recommended by Biome.

        ``true`` by default.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "recommended"))

    @recommended.setter
    def recommended(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a156acee705f9a8c854e898bbaa1eeccfc5287b118e6e8fe1d3632ade181aa94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recommended", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="security")
    def security(self) -> typing.Optional["ISecurity"]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional["ISecurity"], jsii.get(self, "security"))

    @security.setter
    def security(self, value: typing.Optional["ISecurity"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4555486d71e8ce1d7de0dceb557069025e39f54eb51a1e3e42a02db8fe21d075)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "security", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="style")
    def style(self) -> typing.Optional["IStyle"]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional["IStyle"], jsii.get(self, "style"))

    @style.setter
    def style(self, value: typing.Optional["IStyle"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b33ad65ff26071dfadc76fb3baad8aa0266fd04beb3922c06411318e4c200f54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "style", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="suspicious")
    def suspicious(self) -> typing.Optional["ISuspicious"]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional["ISuspicious"], jsii.get(self, "suspicious"))

    @suspicious.setter
    def suspicious(self, value: typing.Optional["ISuspicious"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8caa2dce8e555bc1ba3b9e08a49d1df4a3ae766eb98a5893b453fcd6e10a4337)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suspicious", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IRules).__jsii_proxy_class__ = lambda : _IRulesProxy


@jsii.interface(jsii_type="projen.javascript.biome_config.ISecurity")
class ISecurity(typing_extensions.Protocol):
    '''(experimental) A list of rules that belong to this group.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="all")
    def all(self) -> typing.Optional[builtins.bool]:
        '''(experimental) It enables ALL rules for this group.

        :stability: experimental
        '''
        ...

    @all.setter
    def all(self, value: typing.Optional[builtins.bool]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noDangerouslySetInnerHtml")
    def no_dangerously_set_inner_html(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Prevent the usage of dangerous JSX props.

        :stability: experimental
        '''
        ...

    @no_dangerously_set_inner_html.setter
    def no_dangerously_set_inner_html(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noDangerouslySetInnerHtmlWithChildren")
    def no_dangerously_set_inner_html_with_children(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Report when a DOM element or a component uses both children and dangerouslySetInnerHTML prop.

        :stability: experimental
        '''
        ...

    @no_dangerously_set_inner_html_with_children.setter
    def no_dangerously_set_inner_html_with_children(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noGlobalEval")
    def no_global_eval(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow the use of global eval().

        :stability: experimental
        '''
        ...

    @no_global_eval.setter
    def no_global_eval(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="recommended")
    def recommended(self) -> typing.Optional[builtins.bool]:
        '''(experimental) It enables the recommended rules for this group.

        :stability: experimental
        '''
        ...

    @recommended.setter
    def recommended(self, value: typing.Optional[builtins.bool]) -> None:
        ...


class _ISecurityProxy:
    '''(experimental) A list of rules that belong to this group.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.ISecurity"

    @builtins.property
    @jsii.member(jsii_name="all")
    def all(self) -> typing.Optional[builtins.bool]:
        '''(experimental) It enables ALL rules for this group.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "all"))

    @all.setter
    def all(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce2727dc0da9f0a66cbe058ab48338081bdc9aa7d1fa1a1e22cc92745d33b5f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "all", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noDangerouslySetInnerHtml")
    def no_dangerously_set_inner_html(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Prevent the usage of dangerous JSX props.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]], jsii.get(self, "noDangerouslySetInnerHtml"))

    @no_dangerously_set_inner_html.setter
    def no_dangerously_set_inner_html(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c145352ddd20e79b619ec3fcc9c15f7024480c9f2d61844927a12c7bd31f912)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noDangerouslySetInnerHtml", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noDangerouslySetInnerHtmlWithChildren")
    def no_dangerously_set_inner_html_with_children(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Report when a DOM element or a component uses both children and dangerouslySetInnerHTML prop.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]], jsii.get(self, "noDangerouslySetInnerHtmlWithChildren"))

    @no_dangerously_set_inner_html_with_children.setter
    def no_dangerously_set_inner_html_with_children(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26d1cea21722764b8e550d0729b457826f18181d619c48c86845eadf67316a36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noDangerouslySetInnerHtmlWithChildren", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noGlobalEval")
    def no_global_eval(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow the use of global eval().

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]], jsii.get(self, "noGlobalEval"))

    @no_global_eval.setter
    def no_global_eval(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e22b86179adbe2e6f8b0da1e34fbc4715f588f3044769a0d0310261152d58c5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noGlobalEval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recommended")
    def recommended(self) -> typing.Optional[builtins.bool]:
        '''(experimental) It enables the recommended rules for this group.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "recommended"))

    @recommended.setter
    def recommended(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a36080a1e16d845ca69852e6cc0d33f80438f17412af945e1774f34f3e65f7c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recommended", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ISecurity).__jsii_proxy_class__ = lambda : _ISecurityProxy


@jsii.interface(jsii_type="projen.javascript.biome_config.ISelector")
class ISelector(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="kind")
    def kind(self) -> typing.Optional[builtins.str]:
        '''(experimental) Declaration kind.

        :stability: experimental
        '''
        ...

    @kind.setter
    def kind(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="modifiers")
    def modifiers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Modifiers used on the declaration.

        :stability: experimental
        '''
        ...

    @modifiers.setter
    def modifiers(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(self) -> typing.Optional[builtins.str]:
        '''(experimental) Scope of the declaration.

        :stability: experimental
        '''
        ...

    @scope.setter
    def scope(self, value: typing.Optional[builtins.str]) -> None:
        ...


class _ISelectorProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.ISelector"

    @builtins.property
    @jsii.member(jsii_name="kind")
    def kind(self) -> typing.Optional[builtins.str]:
        '''(experimental) Declaration kind.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kind"))

    @kind.setter
    def kind(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3922a2f94e81ee1336bb83b21dc411010d10354667da3cc487525b3a333dddf6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kind", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="modifiers")
    def modifiers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Modifiers used on the declaration.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "modifiers"))

    @modifiers.setter
    def modifiers(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0347ec5b843a6bccc1299fc42290b813d8919432853e3a31eed8d2a30abd0aac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "modifiers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(self) -> typing.Optional[builtins.str]:
        '''(experimental) Scope of the declaration.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scope"))

    @scope.setter
    def scope(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f83e9bc8416ea6f9634f049b01d7d1b06731b7bbe9519cb02d37cb749b1fe3e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scope", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ISelector).__jsii_proxy_class__ = lambda : _ISelectorProxy


@jsii.interface(jsii_type="projen.javascript.biome_config.ISource")
class ISource(typing_extensions.Protocol):
    '''(experimental) A list of rules that belong to this group.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="sortJsxProps")
    def sort_jsx_props(self) -> typing.Optional[builtins.str]:
        '''(experimental) Enforce props sorting in JSX elements.

        :stability: experimental
        '''
        ...

    @sort_jsx_props.setter
    def sort_jsx_props(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useSortedKeys")
    def use_sorted_keys(self) -> typing.Optional[builtins.str]:
        '''(experimental) Sorts the keys of a JSON object in natural order.

        :stability: experimental
        '''
        ...

    @use_sorted_keys.setter
    def use_sorted_keys(self, value: typing.Optional[builtins.str]) -> None:
        ...


class _ISourceProxy:
    '''(experimental) A list of rules that belong to this group.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.ISource"

    @builtins.property
    @jsii.member(jsii_name="sortJsxProps")
    def sort_jsx_props(self) -> typing.Optional[builtins.str]:
        '''(experimental) Enforce props sorting in JSX elements.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sortJsxProps"))

    @sort_jsx_props.setter
    def sort_jsx_props(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c12a933c4567044fc53e984bf814ec65558f371c32e3112c36cc922834fe5874)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sortJsxProps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useSortedKeys")
    def use_sorted_keys(self) -> typing.Optional[builtins.str]:
        '''(experimental) Sorts the keys of a JSON object in natural order.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "useSortedKeys"))

    @use_sorted_keys.setter
    def use_sorted_keys(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6b3884c9bdacd77202d9bebae17c5e72dcfd7047d13e90ec76dece72b8f0bdb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useSortedKeys", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ISource).__jsii_proxy_class__ = lambda : _ISourceProxy


@jsii.interface(jsii_type="projen.javascript.biome_config.IStyle")
class IStyle(typing_extensions.Protocol):
    '''(experimental) A list of rules that belong to this group.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="all")
    def all(self) -> typing.Optional[builtins.bool]:
        '''(experimental) It enables ALL rules for this group.

        :stability: experimental
        '''
        ...

    @all.setter
    def all(self, value: typing.Optional[builtins.bool]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noArguments")
    def no_arguments(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow the use of arguments.

        :stability: experimental
        '''
        ...

    @no_arguments.setter
    def no_arguments(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noCommaOperator")
    def no_comma_operator(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow comma operator.

        :stability: experimental
        '''
        ...

    @no_comma_operator.setter
    def no_comma_operator(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noDefaultExport")
    def no_default_export(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow default exports.

        :stability: experimental
        '''
        ...

    @no_default_export.setter
    def no_default_export(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noDoneCallback")
    def no_done_callback(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow using a callback in asynchronous tests and hooks.

        :stability: experimental
        '''
        ...

    @no_done_callback.setter
    def no_done_callback(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noImplicitBoolean")
    def no_implicit_boolean(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Disallow implicit true values on JSX boolean attributes.

        :stability: experimental
        '''
        ...

    @no_implicit_boolean.setter
    def no_implicit_boolean(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noInferrableTypes")
    def no_inferrable_types(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Disallow type annotations for variables, parameters, and class properties initialized with a literal expression.

        :stability: experimental
        '''
        ...

    @no_inferrable_types.setter
    def no_inferrable_types(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noNamespace")
    def no_namespace(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow the use of TypeScript's namespaces.

        :stability: experimental
        '''
        ...

    @no_namespace.setter
    def no_namespace(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noNamespaceImport")
    def no_namespace_import(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow the use of namespace imports.

        :stability: experimental
        '''
        ...

    @no_namespace_import.setter
    def no_namespace_import(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noNegationElse")
    def no_negation_else(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Disallow negation in the condition of an if statement if it has an else clause.

        :stability: experimental
        '''
        ...

    @no_negation_else.setter
    def no_negation_else(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noNonNullAssertion")
    def no_non_null_assertion(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Disallow non-null assertions using the !

        postfix operator.

        :stability: experimental
        '''
        ...

    @no_non_null_assertion.setter
    def no_non_null_assertion(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noParameterAssign")
    def no_parameter_assign(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow reassigning function parameters.

        :stability: experimental
        '''
        ...

    @no_parameter_assign.setter
    def no_parameter_assign(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noParameterProperties")
    def no_parameter_properties(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow the use of parameter properties in class constructors.

        :stability: experimental
        '''
        ...

    @no_parameter_properties.setter
    def no_parameter_properties(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noRestrictedGlobals")
    def no_restricted_globals(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithRestrictedGlobalsOptions]]:
        '''(experimental) This rule allows you to specify global variable names that you don’t want to use in your application.

        :stability: experimental
        '''
        ...

    @no_restricted_globals.setter
    def no_restricted_globals(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithRestrictedGlobalsOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noShoutyConstants")
    def no_shouty_constants(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Disallow the use of constants which its value is the upper-case version of its name.

        :stability: experimental
        '''
        ...

    @no_shouty_constants.setter
    def no_shouty_constants(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noUnusedTemplateLiteral")
    def no_unused_template_literal(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Disallow template literals if interpolation and special-character handling are not needed.

        :stability: experimental
        '''
        ...

    @no_unused_template_literal.setter
    def no_unused_template_literal(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noUselessElse")
    def no_useless_else(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Disallow else block when the if block breaks early.

        :stability: experimental
        '''
        ...

    @no_useless_else.setter
    def no_useless_else(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noVar")
    def no_var(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Disallow the use of var.

        :stability: experimental
        '''
        ...

    @no_var.setter
    def no_var(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noYodaExpression")
    def no_yoda_expression(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Disallow the use of yoda expressions.

        :stability: experimental
        '''
        ...

    @no_yoda_expression.setter
    def no_yoda_expression(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="recommended")
    def recommended(self) -> typing.Optional[builtins.bool]:
        '''(experimental) It enables the recommended rules for this group.

        :stability: experimental
        '''
        ...

    @recommended.setter
    def recommended(self, value: typing.Optional[builtins.bool]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useAsConstAssertion")
    def use_as_const_assertion(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Enforce the use of as const over literal type and type annotation.

        :stability: experimental
        '''
        ...

    @use_as_const_assertion.setter
    def use_as_const_assertion(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useBlockStatements")
    def use_block_statements(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Requires following curly brace conventions.

        :stability: experimental
        '''
        ...

    @use_block_statements.setter
    def use_block_statements(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useCollapsedElseIf")
    def use_collapsed_else_if(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Enforce using else if instead of nested if in else clauses.

        :stability: experimental
        '''
        ...

    @use_collapsed_else_if.setter
    def use_collapsed_else_if(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useConsistentArrayType")
    def use_consistent_array_type(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithConsistentArrayTypeOptions]]:
        '''(experimental) Require consistently using either T[] or Array<T>.

        :stability: experimental
        '''
        ...

    @use_consistent_array_type.setter
    def use_consistent_array_type(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithConsistentArrayTypeOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useConsistentBuiltinInstantiation")
    def use_consistent_builtin_instantiation(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Enforce the use of new for all builtins, except String, Number and Boolean.

        :stability: experimental
        '''
        ...

    @use_consistent_builtin_instantiation.setter
    def use_consistent_builtin_instantiation(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useConst")
    def use_const(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Require const declarations for variables that are only assigned once.

        :stability: experimental
        '''
        ...

    @use_const.setter
    def use_const(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useDefaultParameterLast")
    def use_default_parameter_last(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Enforce default function parameters and optional function parameters to be last.

        :stability: experimental
        '''
        ...

    @use_default_parameter_last.setter
    def use_default_parameter_last(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useDefaultSwitchClause")
    def use_default_switch_clause(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Require the default clause in switch statements.

        :stability: experimental
        '''
        ...

    @use_default_switch_clause.setter
    def use_default_switch_clause(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useEnumInitializers")
    def use_enum_initializers(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Require that each enum member value be explicitly initialized.

        :stability: experimental
        '''
        ...

    @use_enum_initializers.setter
    def use_enum_initializers(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useExplicitLengthCheck")
    def use_explicit_length_check(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Enforce explicitly comparing the length, size, byteLength or byteOffset property of a value.

        :stability: experimental
        '''
        ...

    @use_explicit_length_check.setter
    def use_explicit_length_check(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useExponentiationOperator")
    def use_exponentiation_operator(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Disallow the use of Math.pow in favor of the ** operator.

        :stability: experimental
        '''
        ...

    @use_exponentiation_operator.setter
    def use_exponentiation_operator(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useExportType")
    def use_export_type(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Promotes the use of export type for types.

        :stability: experimental
        '''
        ...

    @use_export_type.setter
    def use_export_type(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useFilenamingConvention")
    def use_filenaming_convention(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFilenamingConventionOptions]]:
        '''(experimental) Enforce naming conventions for JavaScript and TypeScript filenames.

        :stability: experimental
        '''
        ...

    @use_filenaming_convention.setter
    def use_filenaming_convention(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFilenamingConventionOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useForOf")
    def use_for_of(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) This rule recommends a for-of loop when in a for loop, the index used to extract an item from the iterated array.

        :stability: experimental
        '''
        ...

    @use_for_of.setter
    def use_for_of(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useFragmentSyntax")
    def use_fragment_syntax(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) This rule enforces the use of <>...</> over <Fragment>...</Fragment>.

        :stability: experimental
        '''
        ...

    @use_fragment_syntax.setter
    def use_fragment_syntax(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useImportType")
    def use_import_type(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Promotes the use of import type for types.

        :stability: experimental
        '''
        ...

    @use_import_type.setter
    def use_import_type(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useLiteralEnumMembers")
    def use_literal_enum_members(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Require all enum members to be literal values.

        :stability: experimental
        '''
        ...

    @use_literal_enum_members.setter
    def use_literal_enum_members(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useNamingConvention")
    def use_naming_convention(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNamingConventionOptions]]:
        '''(experimental) Enforce naming conventions for everything across a codebase.

        :stability: experimental
        '''
        ...

    @use_naming_convention.setter
    def use_naming_convention(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNamingConventionOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useNodeAssertStrict")
    def use_node_assert_strict(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Promotes the usage of node:assert/strict over node:assert.

        :stability: experimental
        '''
        ...

    @use_node_assert_strict.setter
    def use_node_assert_strict(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useNodejsImportProtocol")
    def use_nodejs_import_protocol(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Enforces using the node: protocol for Node.js builtin modules.

        :stability: experimental
        '''
        ...

    @use_nodejs_import_protocol.setter
    def use_nodejs_import_protocol(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useNumberNamespace")
    def use_number_namespace(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Use the Number properties instead of global ones.

        :stability: experimental
        '''
        ...

    @use_number_namespace.setter
    def use_number_namespace(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useNumericLiterals")
    def use_numeric_literals(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Disallow parseInt() and Number.parseInt() in favor of binary, octal, and hexadecimal literals.

        :stability: experimental
        '''
        ...

    @use_numeric_literals.setter
    def use_numeric_literals(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useSelfClosingElements")
    def use_self_closing_elements(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Prevent extra closing tags for components without children.

        :stability: experimental
        '''
        ...

    @use_self_closing_elements.setter
    def use_self_closing_elements(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useShorthandArrayType")
    def use_shorthand_array_type(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) When expressing array types, this rule promotes the usage of T[] shorthand instead of Array<T>.

        :stability: experimental
        '''
        ...

    @use_shorthand_array_type.setter
    def use_shorthand_array_type(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useShorthandAssign")
    def use_shorthand_assign(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Require assignment operator shorthand where possible.

        :stability: experimental
        '''
        ...

    @use_shorthand_assign.setter
    def use_shorthand_assign(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useShorthandFunctionType")
    def use_shorthand_function_type(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Enforce using function types instead of object type with call signatures.

        :stability: experimental
        '''
        ...

    @use_shorthand_function_type.setter
    def use_shorthand_function_type(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useSingleCaseStatement")
    def use_single_case_statement(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Enforces switch clauses have a single statement, emits a quick fix wrapping the statements in a block.

        :stability: experimental
        '''
        ...

    @use_single_case_statement.setter
    def use_single_case_statement(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useSingleVarDeclarator")
    def use_single_var_declarator(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Disallow multiple variable declarations in the same variable statement.

        :stability: experimental
        '''
        ...

    @use_single_var_declarator.setter
    def use_single_var_declarator(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useTemplate")
    def use_template(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Prefer template literals over string concatenation.

        :stability: experimental
        '''
        ...

    @use_template.setter
    def use_template(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useThrowNewError")
    def use_throw_new_error(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Require new when throwing an error.

        :stability: experimental
        '''
        ...

    @use_throw_new_error.setter
    def use_throw_new_error(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useThrowOnlyError")
    def use_throw_only_error(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow throwing non-Error values.

        :stability: experimental
        '''
        ...

    @use_throw_only_error.setter
    def use_throw_only_error(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useWhile")
    def use_while(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Enforce the use of while loops instead of for loops when the initializer and update expressions are not needed.

        :stability: experimental
        '''
        ...

    @use_while.setter
    def use_while(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        ...


class _IStyleProxy:
    '''(experimental) A list of rules that belong to this group.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.IStyle"

    @builtins.property
    @jsii.member(jsii_name="all")
    def all(self) -> typing.Optional[builtins.bool]:
        '''(experimental) It enables ALL rules for this group.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "all"))

    @all.setter
    def all(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e20996498263b2a0097ffb3adc174ddfc9bf9808535bd957cb196fa067e3fca9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "all", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noArguments")
    def no_arguments(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow the use of arguments.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]], jsii.get(self, "noArguments"))

    @no_arguments.setter
    def no_arguments(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfe364999f21db62f6c479e8f80ed798a9b8fe7a74d2734a37ba6b0a942be8fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noArguments", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noCommaOperator")
    def no_comma_operator(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow comma operator.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]], jsii.get(self, "noCommaOperator"))

    @no_comma_operator.setter
    def no_comma_operator(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a52761f97602124cfb84a805343ce56365a1678352070d438f10c9744065b84e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noCommaOperator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noDefaultExport")
    def no_default_export(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow default exports.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]], jsii.get(self, "noDefaultExport"))

    @no_default_export.setter
    def no_default_export(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64c248bceb321184ec65e3a260161b8d9ee6520910b57cc71371ebdccc011fc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noDefaultExport", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noDoneCallback")
    def no_done_callback(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow using a callback in asynchronous tests and hooks.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]], jsii.get(self, "noDoneCallback"))

    @no_done_callback.setter
    def no_done_callback(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff99fa66bacfc7f51da55d7bc0feec60daa24a8ff823e9c116c7b70eb9d0c6d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noDoneCallback", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noImplicitBoolean")
    def no_implicit_boolean(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Disallow implicit true values on JSX boolean attributes.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]], jsii.get(self, "noImplicitBoolean"))

    @no_implicit_boolean.setter
    def no_implicit_boolean(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__296f87723d73352e87d7b1768fb98be927ff0fad9eeb137f0a820d1bbd011b4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noImplicitBoolean", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noInferrableTypes")
    def no_inferrable_types(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Disallow type annotations for variables, parameters, and class properties initialized with a literal expression.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]], jsii.get(self, "noInferrableTypes"))

    @no_inferrable_types.setter
    def no_inferrable_types(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5f88a88e6deaf355e7ef7a14df3e7b282dbf3ce63ccb0b04c3f5acfa4fb8af2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noInferrableTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noNamespace")
    def no_namespace(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow the use of TypeScript's namespaces.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]], jsii.get(self, "noNamespace"))

    @no_namespace.setter
    def no_namespace(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecf34f6f84c16d8eda1ebbcd515129ce69e6d0c904dc2870fc5ad61715a1cf48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noNamespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noNamespaceImport")
    def no_namespace_import(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow the use of namespace imports.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]], jsii.get(self, "noNamespaceImport"))

    @no_namespace_import.setter
    def no_namespace_import(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f97a8c7a81f425f5a0c0136ddda956c3e828ea37c0dcdf76bf63058e2053468)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noNamespaceImport", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noNegationElse")
    def no_negation_else(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Disallow negation in the condition of an if statement if it has an else clause.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]], jsii.get(self, "noNegationElse"))

    @no_negation_else.setter
    def no_negation_else(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27bb9824e441dac0113255096b07d822f2b167d4db69d1bbb2fdfafbc39e0775)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noNegationElse", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noNonNullAssertion")
    def no_non_null_assertion(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Disallow non-null assertions using the !

        postfix operator.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]], jsii.get(self, "noNonNullAssertion"))

    @no_non_null_assertion.setter
    def no_non_null_assertion(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6706f0f3dee5550f85c5ac69370360b722776d1d5ef7d872214a137def4fdbd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noNonNullAssertion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noParameterAssign")
    def no_parameter_assign(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow reassigning function parameters.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]], jsii.get(self, "noParameterAssign"))

    @no_parameter_assign.setter
    def no_parameter_assign(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f81ed9e0c79dd25892593b3beaece435a5ec3bea91285b058bf0fdb759f8cf5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noParameterAssign", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noParameterProperties")
    def no_parameter_properties(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow the use of parameter properties in class constructors.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]], jsii.get(self, "noParameterProperties"))

    @no_parameter_properties.setter
    def no_parameter_properties(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__122e001baf27cbf5173137d3d2c1cfdbd0b41be7648226ab0b621374f948fd3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noParameterProperties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noRestrictedGlobals")
    def no_restricted_globals(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithRestrictedGlobalsOptions]]:
        '''(experimental) This rule allows you to specify global variable names that you don’t want to use in your application.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithRestrictedGlobalsOptions]], jsii.get(self, "noRestrictedGlobals"))

    @no_restricted_globals.setter
    def no_restricted_globals(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithRestrictedGlobalsOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e4de2a576e0d27f0bc3abff92c8699a6a7d8f598740ee47a8b407cb497a9099)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noRestrictedGlobals", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noShoutyConstants")
    def no_shouty_constants(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Disallow the use of constants which its value is the upper-case version of its name.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]], jsii.get(self, "noShoutyConstants"))

    @no_shouty_constants.setter
    def no_shouty_constants(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0243f1b0cfbac7a30163d32d8cdbabfd89ff85006d268d34529fe75c7d4e63e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noShoutyConstants", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noUnusedTemplateLiteral")
    def no_unused_template_literal(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Disallow template literals if interpolation and special-character handling are not needed.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]], jsii.get(self, "noUnusedTemplateLiteral"))

    @no_unused_template_literal.setter
    def no_unused_template_literal(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b77a1b745b5257a40c409b1fe5f72157ffa141cd69735413b888e838a6a35cd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noUnusedTemplateLiteral", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noUselessElse")
    def no_useless_else(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Disallow else block when the if block breaks early.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]], jsii.get(self, "noUselessElse"))

    @no_useless_else.setter
    def no_useless_else(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0d92ea883024cd008fcfc2654baf69a0c76cb2005543c742069448a5c2c2142)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noUselessElse", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noVar")
    def no_var(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Disallow the use of var.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]], jsii.get(self, "noVar"))

    @no_var.setter
    def no_var(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c280a82ffd4d2feccac8d9110d969296fdef9201040e6e4b647e8e5ceae1fc04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noVar", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noYodaExpression")
    def no_yoda_expression(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Disallow the use of yoda expressions.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]], jsii.get(self, "noYodaExpression"))

    @no_yoda_expression.setter
    def no_yoda_expression(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c8a2220a4a7a8a0645a27ed434980373d53349d284cf321e5b1636fa9f711c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noYodaExpression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recommended")
    def recommended(self) -> typing.Optional[builtins.bool]:
        '''(experimental) It enables the recommended rules for this group.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "recommended"))

    @recommended.setter
    def recommended(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6427982f4bc3e2e11c5c4b42b20edbebef73241d7d7aac7f2fd3a643c247da58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recommended", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useAsConstAssertion")
    def use_as_const_assertion(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Enforce the use of as const over literal type and type annotation.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]], jsii.get(self, "useAsConstAssertion"))

    @use_as_const_assertion.setter
    def use_as_const_assertion(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ed161de19ce31fffddadcee3dea4761f7209fe81a2431da1e4ddc3b70d53a71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useAsConstAssertion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useBlockStatements")
    def use_block_statements(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Requires following curly brace conventions.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]], jsii.get(self, "useBlockStatements"))

    @use_block_statements.setter
    def use_block_statements(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d533ea92f20364aee15df227dcabbf5817d0cf20a4c9b6a71163725260173830)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useBlockStatements", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useCollapsedElseIf")
    def use_collapsed_else_if(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Enforce using else if instead of nested if in else clauses.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]], jsii.get(self, "useCollapsedElseIf"))

    @use_collapsed_else_if.setter
    def use_collapsed_else_if(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34f5fd42307f836fbb1f5afaabe7fa390c1ad96ebe22969ad4ae91b052f60a11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useCollapsedElseIf", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useConsistentArrayType")
    def use_consistent_array_type(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithConsistentArrayTypeOptions]]:
        '''(experimental) Require consistently using either T[] or Array<T>.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithConsistentArrayTypeOptions]], jsii.get(self, "useConsistentArrayType"))

    @use_consistent_array_type.setter
    def use_consistent_array_type(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithConsistentArrayTypeOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9125a99e3a1ab46f41b7439df436cd861f2f1af1e27bff679db3fc714d479dbc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useConsistentArrayType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useConsistentBuiltinInstantiation")
    def use_consistent_builtin_instantiation(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Enforce the use of new for all builtins, except String, Number and Boolean.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]], jsii.get(self, "useConsistentBuiltinInstantiation"))

    @use_consistent_builtin_instantiation.setter
    def use_consistent_builtin_instantiation(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8c68d2053285485f02d1f5f6b89100d4d2275a8a3038d4d9fc89b117c606410)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useConsistentBuiltinInstantiation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useConst")
    def use_const(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Require const declarations for variables that are only assigned once.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]], jsii.get(self, "useConst"))

    @use_const.setter
    def use_const(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59e1f6038f5a4ba208f06b99c5cc243b0f2e3bc17bbe643590cbd2900bf06174)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useConst", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useDefaultParameterLast")
    def use_default_parameter_last(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Enforce default function parameters and optional function parameters to be last.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]], jsii.get(self, "useDefaultParameterLast"))

    @use_default_parameter_last.setter
    def use_default_parameter_last(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fc04da9952b3402e2fd3c9bdcb65cda9852dccd07bbe8ecaded54fa23f71280)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useDefaultParameterLast", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useDefaultSwitchClause")
    def use_default_switch_clause(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Require the default clause in switch statements.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]], jsii.get(self, "useDefaultSwitchClause"))

    @use_default_switch_clause.setter
    def use_default_switch_clause(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db72f35e401183f3c4798b03dd51d9ff4c523146b26d19c042be3129d5347382)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useDefaultSwitchClause", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useEnumInitializers")
    def use_enum_initializers(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Require that each enum member value be explicitly initialized.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]], jsii.get(self, "useEnumInitializers"))

    @use_enum_initializers.setter
    def use_enum_initializers(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c637b9c9cb973624cbe3b0bbeca1730807aaf343f4cbf934dd17f77cde83c9c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useEnumInitializers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useExplicitLengthCheck")
    def use_explicit_length_check(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Enforce explicitly comparing the length, size, byteLength or byteOffset property of a value.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]], jsii.get(self, "useExplicitLengthCheck"))

    @use_explicit_length_check.setter
    def use_explicit_length_check(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1fbf70a1bc083e7da3e6ce9dd3ae94fad5aee55d871fa9cfffd780ab4fbab74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useExplicitLengthCheck", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useExponentiationOperator")
    def use_exponentiation_operator(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Disallow the use of Math.pow in favor of the ** operator.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]], jsii.get(self, "useExponentiationOperator"))

    @use_exponentiation_operator.setter
    def use_exponentiation_operator(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d2bdd650730772d2916fae1bd2ea9def4b8418c74278d5b6b4422f689ef536f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useExponentiationOperator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useExportType")
    def use_export_type(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Promotes the use of export type for types.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]], jsii.get(self, "useExportType"))

    @use_export_type.setter
    def use_export_type(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e3960f1767120ad81299a77f3d2c6ead5d62868a49816f422394d7222054ec4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useExportType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useFilenamingConvention")
    def use_filenaming_convention(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFilenamingConventionOptions]]:
        '''(experimental) Enforce naming conventions for JavaScript and TypeScript filenames.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithFilenamingConventionOptions]], jsii.get(self, "useFilenamingConvention"))

    @use_filenaming_convention.setter
    def use_filenaming_convention(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFilenamingConventionOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e8571337f79b14acc078a783b7c42a61c69312f1276d92c99cc5fbe261a3c28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useFilenamingConvention", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useForOf")
    def use_for_of(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) This rule recommends a for-of loop when in a for loop, the index used to extract an item from the iterated array.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]], jsii.get(self, "useForOf"))

    @use_for_of.setter
    def use_for_of(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2beeb28f5c86ba18cefda32825bab5cc2575c977c568d1e4857fcc254c7b24cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useForOf", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useFragmentSyntax")
    def use_fragment_syntax(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) This rule enforces the use of <>...</> over <Fragment>...</Fragment>.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]], jsii.get(self, "useFragmentSyntax"))

    @use_fragment_syntax.setter
    def use_fragment_syntax(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e287a4f2d8716acf135aabdd3497bc44f78b1bbfd49078de8fc7a8bb568449a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useFragmentSyntax", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useImportType")
    def use_import_type(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Promotes the use of import type for types.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]], jsii.get(self, "useImportType"))

    @use_import_type.setter
    def use_import_type(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fda4a8c85c5e7dbf1b0d9a8200e807adf5073dc4ed90c8894b4480deb3d3f19d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useImportType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useLiteralEnumMembers")
    def use_literal_enum_members(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Require all enum members to be literal values.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]], jsii.get(self, "useLiteralEnumMembers"))

    @use_literal_enum_members.setter
    def use_literal_enum_members(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aed182ce219e955f2fa03258974d263c6de309810a3b1300c72f2992a1052e23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useLiteralEnumMembers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useNamingConvention")
    def use_naming_convention(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNamingConventionOptions]]:
        '''(experimental) Enforce naming conventions for everything across a codebase.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithNamingConventionOptions]], jsii.get(self, "useNamingConvention"))

    @use_naming_convention.setter
    def use_naming_convention(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNamingConventionOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5da8998a03bed0d1bbc8c145b983848934904101481dec7529725507c080d1a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useNamingConvention", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useNodeAssertStrict")
    def use_node_assert_strict(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Promotes the usage of node:assert/strict over node:assert.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]], jsii.get(self, "useNodeAssertStrict"))

    @use_node_assert_strict.setter
    def use_node_assert_strict(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9b8f6d1d8f7f74dc61d238c32668b59756232652e9f2b61412b3fc9b5214996)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useNodeAssertStrict", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useNodejsImportProtocol")
    def use_nodejs_import_protocol(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Enforces using the node: protocol for Node.js builtin modules.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]], jsii.get(self, "useNodejsImportProtocol"))

    @use_nodejs_import_protocol.setter
    def use_nodejs_import_protocol(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__257c24a1ee82546beae2d8bad419db162caa974235e3eb7bc213cadc1984f964)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useNodejsImportProtocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useNumberNamespace")
    def use_number_namespace(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Use the Number properties instead of global ones.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]], jsii.get(self, "useNumberNamespace"))

    @use_number_namespace.setter
    def use_number_namespace(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2d3b776d34295a524c2dee881d43e41b7d71696c526b3bdb99b8db6131e1910)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useNumberNamespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useNumericLiterals")
    def use_numeric_literals(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Disallow parseInt() and Number.parseInt() in favor of binary, octal, and hexadecimal literals.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]], jsii.get(self, "useNumericLiterals"))

    @use_numeric_literals.setter
    def use_numeric_literals(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb9b9f9e69e90d6b562fa84ecd7ab5cfffdf4eb87e6fa1cb55f6765b5c5d03aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useNumericLiterals", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useSelfClosingElements")
    def use_self_closing_elements(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Prevent extra closing tags for components without children.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]], jsii.get(self, "useSelfClosingElements"))

    @use_self_closing_elements.setter
    def use_self_closing_elements(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7486d1545594d2cc2e8747a6f862afb2ecd976b2147fd5cd904d078cef1808aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useSelfClosingElements", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useShorthandArrayType")
    def use_shorthand_array_type(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) When expressing array types, this rule promotes the usage of T[] shorthand instead of Array<T>.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]], jsii.get(self, "useShorthandArrayType"))

    @use_shorthand_array_type.setter
    def use_shorthand_array_type(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eccd29ed4a0c11f8b4d5f5a40f662102c90fe186949ae1918f4091022870d5a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useShorthandArrayType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useShorthandAssign")
    def use_shorthand_assign(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Require assignment operator shorthand where possible.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]], jsii.get(self, "useShorthandAssign"))

    @use_shorthand_assign.setter
    def use_shorthand_assign(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5eec4df3d57b98d05d79ebbb3572c5101b8452300a48c146d18e1f0efd6710d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useShorthandAssign", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useShorthandFunctionType")
    def use_shorthand_function_type(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Enforce using function types instead of object type with call signatures.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]], jsii.get(self, "useShorthandFunctionType"))

    @use_shorthand_function_type.setter
    def use_shorthand_function_type(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45e392f89f510457677ee64436e0206b3559eb24edde5d607d68a7ed45005cae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useShorthandFunctionType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useSingleCaseStatement")
    def use_single_case_statement(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Enforces switch clauses have a single statement, emits a quick fix wrapping the statements in a block.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]], jsii.get(self, "useSingleCaseStatement"))

    @use_single_case_statement.setter
    def use_single_case_statement(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5deb3d39cde1e14eddd78523756772ab9f9521232f38eeb1b1e405d8314ca055)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useSingleCaseStatement", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useSingleVarDeclarator")
    def use_single_var_declarator(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Disallow multiple variable declarations in the same variable statement.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]], jsii.get(self, "useSingleVarDeclarator"))

    @use_single_var_declarator.setter
    def use_single_var_declarator(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bed0aadbfbeffd6af0216845ca8106990fe7f2992fb9ca3cae1324886de03356)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useSingleVarDeclarator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useTemplate")
    def use_template(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Prefer template literals over string concatenation.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]], jsii.get(self, "useTemplate"))

    @use_template.setter
    def use_template(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__781390133f11692b0f0d0dc79e6f328f59cd69652c8c2ca13c994afeed86ef42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useTemplate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useThrowNewError")
    def use_throw_new_error(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Require new when throwing an error.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]], jsii.get(self, "useThrowNewError"))

    @use_throw_new_error.setter
    def use_throw_new_error(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebea9f9b77aa149e7ce200e8c6aa65ced9141464b27e9740231bfb49ab2c0ab1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useThrowNewError", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useThrowOnlyError")
    def use_throw_only_error(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow throwing non-Error values.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]], jsii.get(self, "useThrowOnlyError"))

    @use_throw_only_error.setter
    def use_throw_only_error(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48788877c8edf80edba018e3ada4528705a8261636a8249d8fcfed28d8c66947)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useThrowOnlyError", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useWhile")
    def use_while(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Enforce the use of while loops instead of for loops when the initializer and update expressions are not needed.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]], jsii.get(self, "useWhile"))

    @use_while.setter
    def use_while(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97f301bbdc491f9708f003d309912facde43599f0a0dd1aa2e9387364efcaf33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useWhile", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IStyle).__jsii_proxy_class__ = lambda : _IStyleProxy


@jsii.interface(jsii_type="projen.javascript.biome_config.ISuggestedExtensionMapping")
class ISuggestedExtensionMapping(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="component")
    def component(self) -> typing.Optional[builtins.str]:
        '''(experimental) Extension that should be used for component file imports.

        :stability: experimental
        '''
        ...

    @component.setter
    def component(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="module")
    def module(self) -> typing.Optional[builtins.str]:
        '''(experimental) Extension that should be used for module imports.

        :stability: experimental
        '''
        ...

    @module.setter
    def module(self, value: typing.Optional[builtins.str]) -> None:
        ...


class _ISuggestedExtensionMappingProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.ISuggestedExtensionMapping"

    @builtins.property
    @jsii.member(jsii_name="component")
    def component(self) -> typing.Optional[builtins.str]:
        '''(experimental) Extension that should be used for component file imports.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "component"))

    @component.setter
    def component(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a2081d8218d2bfe76c905733309c17fd4e5a3f9d53ca849aa0519f6f0129071)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "component", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="module")
    def module(self) -> typing.Optional[builtins.str]:
        '''(experimental) Extension that should be used for module imports.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "module"))

    @module.setter
    def module(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39c7d9df167a7294f7b887a7be492667e0884c003970d58f72433abba003aa18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "module", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ISuggestedExtensionMapping).__jsii_proxy_class__ = lambda : _ISuggestedExtensionMappingProxy


@jsii.interface(jsii_type="projen.javascript.biome_config.ISuspicious")
class ISuspicious(typing_extensions.Protocol):
    '''(experimental) A list of rules that belong to this group.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="all")
    def all(self) -> typing.Optional[builtins.bool]:
        '''(experimental) It enables ALL rules for this group.

        :stability: experimental
        '''
        ...

    @all.setter
    def all(self, value: typing.Optional[builtins.bool]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noApproximativeNumericConstant")
    def no_approximative_numeric_constant(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Use standard constants instead of approximated literals.

        :stability: experimental
        '''
        ...

    @no_approximative_numeric_constant.setter
    def no_approximative_numeric_constant(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noArrayIndexKey")
    def no_array_index_key(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Discourage the usage of Array index in keys.

        :stability: experimental
        '''
        ...

    @no_array_index_key.setter
    def no_array_index_key(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noAssignInExpressions")
    def no_assign_in_expressions(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow assignments in expressions.

        :stability: experimental
        '''
        ...

    @no_assign_in_expressions.setter
    def no_assign_in_expressions(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noAsyncPromiseExecutor")
    def no_async_promise_executor(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallows using an async function as a Promise executor.

        :stability: experimental
        '''
        ...

    @no_async_promise_executor.setter
    def no_async_promise_executor(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noCatchAssign")
    def no_catch_assign(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow reassigning exceptions in catch clauses.

        :stability: experimental
        '''
        ...

    @no_catch_assign.setter
    def no_catch_assign(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noClassAssign")
    def no_class_assign(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow reassigning class members.

        :stability: experimental
        '''
        ...

    @no_class_assign.setter
    def no_class_assign(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noCommentText")
    def no_comment_text(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Prevent comments from being inserted as text nodes.

        :stability: experimental
        '''
        ...

    @no_comment_text.setter
    def no_comment_text(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noCompareNegZero")
    def no_compare_neg_zero(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Disallow comparing against -0.

        :stability: experimental
        '''
        ...

    @no_compare_neg_zero.setter
    def no_compare_neg_zero(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noConfusingLabels")
    def no_confusing_labels(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow labeled statements that are not loops.

        :stability: experimental
        '''
        ...

    @no_confusing_labels.setter
    def no_confusing_labels(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noConfusingVoidType")
    def no_confusing_void_type(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Disallow void type outside of generic or return types.

        :stability: experimental
        '''
        ...

    @no_confusing_void_type.setter
    def no_confusing_void_type(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noConsole")
    def no_console(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoConsoleOptions]]:
        '''(experimental) Disallow the use of console.

        :stability: experimental
        '''
        ...

    @no_console.setter
    def no_console(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoConsoleOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noConsoleLog")
    def no_console_log(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Disallow the use of console.log.

        :stability: experimental
        '''
        ...

    @no_console_log.setter
    def no_console_log(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noConstEnum")
    def no_const_enum(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Disallow TypeScript const enum.

        :stability: experimental
        '''
        ...

    @no_const_enum.setter
    def no_const_enum(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noControlCharactersInRegex")
    def no_control_characters_in_regex(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Prevents from having control characters and some escape sequences that match control characters in regular expressions.

        :stability: experimental
        '''
        ...

    @no_control_characters_in_regex.setter
    def no_control_characters_in_regex(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noDebugger")
    def no_debugger(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Disallow the use of debugger.

        :stability: experimental
        '''
        ...

    @no_debugger.setter
    def no_debugger(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noDoubleEquals")
    def no_double_equals(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoDoubleEqualsOptions]]:
        '''(experimental) Require the use of === and !==.

        :stability: experimental
        '''
        ...

    @no_double_equals.setter
    def no_double_equals(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoDoubleEqualsOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noDuplicateAtImportRules")
    def no_duplicate_at_import_rules(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow duplicate.

        :stability: experimental
        :import: true
        '''
        ...

    @no_duplicate_at_import_rules.setter
    def no_duplicate_at_import_rules(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noDuplicateCase")
    def no_duplicate_case(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow duplicate case labels.

        :stability: experimental
        '''
        ...

    @no_duplicate_case.setter
    def no_duplicate_case(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noDuplicateClassMembers")
    def no_duplicate_class_members(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow duplicate class members.

        :stability: experimental
        '''
        ...

    @no_duplicate_class_members.setter
    def no_duplicate_class_members(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noDuplicateFontNames")
    def no_duplicate_font_names(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow duplicate names within font families.

        :stability: experimental
        '''
        ...

    @no_duplicate_font_names.setter
    def no_duplicate_font_names(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noDuplicateJsxProps")
    def no_duplicate_jsx_props(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Prevents JSX properties to be assigned multiple times.

        :stability: experimental
        '''
        ...

    @no_duplicate_jsx_props.setter
    def no_duplicate_jsx_props(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noDuplicateObjectKeys")
    def no_duplicate_object_keys(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow two keys with the same name inside objects.

        :stability: experimental
        '''
        ...

    @no_duplicate_object_keys.setter
    def no_duplicate_object_keys(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noDuplicateParameters")
    def no_duplicate_parameters(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow duplicate function parameter name.

        :stability: experimental
        '''
        ...

    @no_duplicate_parameters.setter
    def no_duplicate_parameters(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noDuplicateSelectorsKeyframeBlock")
    def no_duplicate_selectors_keyframe_block(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow duplicate selectors within keyframe blocks.

        :stability: experimental
        '''
        ...

    @no_duplicate_selectors_keyframe_block.setter
    def no_duplicate_selectors_keyframe_block(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noDuplicateTestHooks")
    def no_duplicate_test_hooks(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) A describe block should not contain duplicate hooks.

        :stability: experimental
        '''
        ...

    @no_duplicate_test_hooks.setter
    def no_duplicate_test_hooks(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noEmptyBlock")
    def no_empty_block(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow CSS empty blocks.

        :stability: experimental
        '''
        ...

    @no_empty_block.setter
    def no_empty_block(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noEmptyBlockStatements")
    def no_empty_block_statements(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow empty block statements and static blocks.

        :stability: experimental
        '''
        ...

    @no_empty_block_statements.setter
    def no_empty_block_statements(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noEmptyInterface")
    def no_empty_interface(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Disallow the declaration of empty interfaces.

        :stability: experimental
        '''
        ...

    @no_empty_interface.setter
    def no_empty_interface(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noEvolvingTypes")
    def no_evolving_types(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow variables from evolving into any type through reassignments.

        :stability: experimental
        '''
        ...

    @no_evolving_types.setter
    def no_evolving_types(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noExplicitAny")
    def no_explicit_any(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow the any type usage.

        :stability: experimental
        '''
        ...

    @no_explicit_any.setter
    def no_explicit_any(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noExportsInTest")
    def no_exports_in_test(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow using export or module.exports in files containing tests.

        :stability: experimental
        '''
        ...

    @no_exports_in_test.setter
    def no_exports_in_test(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noExtraNonNullAssertion")
    def no_extra_non_null_assertion(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Prevents the wrong usage of the non-null assertion operator (!) in TypeScript files.

        :stability: experimental
        '''
        ...

    @no_extra_non_null_assertion.setter
    def no_extra_non_null_assertion(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noFallthroughSwitchClause")
    def no_fallthrough_switch_clause(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow fallthrough of switch clauses.

        :stability: experimental
        '''
        ...

    @no_fallthrough_switch_clause.setter
    def no_fallthrough_switch_clause(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noFocusedTests")
    def no_focused_tests(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Disallow focused tests.

        :stability: experimental
        '''
        ...

    @no_focused_tests.setter
    def no_focused_tests(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noFunctionAssign")
    def no_function_assign(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow reassigning function declarations.

        :stability: experimental
        '''
        ...

    @no_function_assign.setter
    def no_function_assign(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noGlobalAssign")
    def no_global_assign(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow assignments to native objects and read-only global variables.

        :stability: experimental
        '''
        ...

    @no_global_assign.setter
    def no_global_assign(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noGlobalIsFinite")
    def no_global_is_finite(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Use Number.isFinite instead of global isFinite.

        :stability: experimental
        '''
        ...

    @no_global_is_finite.setter
    def no_global_is_finite(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noGlobalIsNan")
    def no_global_is_nan(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Use Number.isNaN instead of global isNaN.

        :stability: experimental
        '''
        ...

    @no_global_is_nan.setter
    def no_global_is_nan(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noImplicitAnyLet")
    def no_implicit_any_let(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow use of implicit any type on variable declarations.

        :stability: experimental
        '''
        ...

    @no_implicit_any_let.setter
    def no_implicit_any_let(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noImportantInKeyframe")
    def no_important_in_keyframe(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow invalid !important within keyframe declarations.

        :stability: experimental
        '''
        ...

    @no_important_in_keyframe.setter
    def no_important_in_keyframe(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noImportAssign")
    def no_import_assign(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow assigning to imported bindings.

        :stability: experimental
        '''
        ...

    @no_import_assign.setter
    def no_import_assign(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noLabelVar")
    def no_label_var(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow labels that share a name with a variable.

        :stability: experimental
        '''
        ...

    @no_label_var.setter
    def no_label_var(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noMisleadingCharacterClass")
    def no_misleading_character_class(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Disallow characters made with multiple code points in character class syntax.

        :stability: experimental
        '''
        ...

    @no_misleading_character_class.setter
    def no_misleading_character_class(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noMisleadingInstantiator")
    def no_misleading_instantiator(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Enforce proper usage of new and constructor.

        :stability: experimental
        '''
        ...

    @no_misleading_instantiator.setter
    def no_misleading_instantiator(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noMisplacedAssertion")
    def no_misplaced_assertion(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Checks that the assertion function, for example expect, is placed inside an it() function call.

        :stability: experimental
        '''
        ...

    @no_misplaced_assertion.setter
    def no_misplaced_assertion(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noMisrefactoredShorthandAssign")
    def no_misrefactored_shorthand_assign(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Disallow shorthand assign when variable appears on both sides.

        :stability: experimental
        '''
        ...

    @no_misrefactored_shorthand_assign.setter
    def no_misrefactored_shorthand_assign(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noPrototypeBuiltins")
    def no_prototype_builtins(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow direct use of Object.prototype builtins.

        :stability: experimental
        '''
        ...

    @no_prototype_builtins.setter
    def no_prototype_builtins(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noReactSpecificProps")
    def no_react_specific_props(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Prevents React-specific JSX properties from being used.

        :stability: experimental
        '''
        ...

    @no_react_specific_props.setter
    def no_react_specific_props(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noRedeclare")
    def no_redeclare(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow variable, function, class, and type redeclarations in the same scope.

        :stability: experimental
        '''
        ...

    @no_redeclare.setter
    def no_redeclare(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noRedundantUseStrict")
    def no_redundant_use_strict(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Prevents from having redundant "use strict".

        :stability: experimental
        '''
        ...

    @no_redundant_use_strict.setter
    def no_redundant_use_strict(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noSelfCompare")
    def no_self_compare(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow comparisons where both sides are exactly the same.

        :stability: experimental
        '''
        ...

    @no_self_compare.setter
    def no_self_compare(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noShadowRestrictedNames")
    def no_shadow_restricted_names(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow identifiers from shadowing restricted names.

        :stability: experimental
        '''
        ...

    @no_shadow_restricted_names.setter
    def no_shadow_restricted_names(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noShorthandPropertyOverrides")
    def no_shorthand_property_overrides(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow shorthand properties that override related longhand properties.

        :stability: experimental
        '''
        ...

    @no_shorthand_property_overrides.setter
    def no_shorthand_property_overrides(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noSkippedTests")
    def no_skipped_tests(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Disallow disabled tests.

        :stability: experimental
        '''
        ...

    @no_skipped_tests.setter
    def no_skipped_tests(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noSparseArray")
    def no_sparse_array(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Disallow sparse arrays.

        :stability: experimental
        '''
        ...

    @no_sparse_array.setter
    def no_sparse_array(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noSuspiciousSemicolonInJsx")
    def no_suspicious_semicolon_in_jsx(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) It detects possible "wrong" semicolons inside JSX elements.

        :stability: experimental
        '''
        ...

    @no_suspicious_semicolon_in_jsx.setter
    def no_suspicious_semicolon_in_jsx(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noThenProperty")
    def no_then_property(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow then property.

        :stability: experimental
        '''
        ...

    @no_then_property.setter
    def no_then_property(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noUnsafeDeclarationMerging")
    def no_unsafe_declaration_merging(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow unsafe declaration merging between interfaces and classes.

        :stability: experimental
        '''
        ...

    @no_unsafe_declaration_merging.setter
    def no_unsafe_declaration_merging(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="noUnsafeNegation")
    def no_unsafe_negation(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Disallow using unsafe negation.

        :stability: experimental
        '''
        ...

    @no_unsafe_negation.setter
    def no_unsafe_negation(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="recommended")
    def recommended(self) -> typing.Optional[builtins.bool]:
        '''(experimental) It enables the recommended rules for this group.

        :stability: experimental
        '''
        ...

    @recommended.setter
    def recommended(self, value: typing.Optional[builtins.bool]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useAwait")
    def use_await(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Ensure async functions utilize await.

        :stability: experimental
        '''
        ...

    @use_await.setter
    def use_await(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useDefaultSwitchClauseLast")
    def use_default_switch_clause_last(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Enforce default clauses in switch statements to be last.

        :stability: experimental
        '''
        ...

    @use_default_switch_clause_last.setter
    def use_default_switch_clause_last(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useErrorMessage")
    def use_error_message(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Enforce passing a message value when creating a built-in error.

        :stability: experimental
        '''
        ...

    @use_error_message.setter
    def use_error_message(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useGetterReturn")
    def use_getter_return(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Enforce get methods to always return a value.

        :stability: experimental
        '''
        ...

    @use_getter_return.setter
    def use_getter_return(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useIsArray")
    def use_is_array(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Use Array.isArray() instead of instanceof Array.

        :stability: experimental
        '''
        ...

    @use_is_array.setter
    def use_is_array(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useNamespaceKeyword")
    def use_namespace_keyword(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Require using the namespace keyword over the module keyword to declare TypeScript namespaces.

        :stability: experimental
        '''
        ...

    @use_namespace_keyword.setter
    def use_namespace_keyword(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useNumberToFixedDigitsArgument")
    def use_number_to_fixed_digits_argument(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Enforce using the digits argument with Number#toFixed().

        :stability: experimental
        '''
        ...

    @use_number_to_fixed_digits_argument.setter
    def use_number_to_fixed_digits_argument(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useValidTypeof")
    def use_valid_typeof(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) This rule verifies the result of typeof $expr unary expressions is being compared to valid values, either string literals containing valid type names or other typeof expressions.

        :stability: experimental
        '''
        ...

    @use_valid_typeof.setter
    def use_valid_typeof(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        ...


class _ISuspiciousProxy:
    '''(experimental) A list of rules that belong to this group.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.ISuspicious"

    @builtins.property
    @jsii.member(jsii_name="all")
    def all(self) -> typing.Optional[builtins.bool]:
        '''(experimental) It enables ALL rules for this group.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "all"))

    @all.setter
    def all(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4363f6fabd830798a8a7102ae11fb5ebc2a87bf8966fd2866c7936d775ed228)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "all", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noApproximativeNumericConstant")
    def no_approximative_numeric_constant(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Use standard constants instead of approximated literals.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]], jsii.get(self, "noApproximativeNumericConstant"))

    @no_approximative_numeric_constant.setter
    def no_approximative_numeric_constant(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__302c317574774fe735865fec7e44eb0eecb96374359b35f30cb8da71ad8f1f81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noApproximativeNumericConstant", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noArrayIndexKey")
    def no_array_index_key(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Discourage the usage of Array index in keys.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]], jsii.get(self, "noArrayIndexKey"))

    @no_array_index_key.setter
    def no_array_index_key(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5222f823bd3a8750366375527a1637b1bc7e738f4833530165dfa5cef0329f8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noArrayIndexKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noAssignInExpressions")
    def no_assign_in_expressions(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow assignments in expressions.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]], jsii.get(self, "noAssignInExpressions"))

    @no_assign_in_expressions.setter
    def no_assign_in_expressions(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fe999d70bbc00e640a57dc22770975a0f97219a80cdc2be89eab6c813fda7e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noAssignInExpressions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noAsyncPromiseExecutor")
    def no_async_promise_executor(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallows using an async function as a Promise executor.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]], jsii.get(self, "noAsyncPromiseExecutor"))

    @no_async_promise_executor.setter
    def no_async_promise_executor(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2590b964f2fa340e6743e488d774fba35d4bbb0cb26bd18dcba582f3b3c91b58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noAsyncPromiseExecutor", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noCatchAssign")
    def no_catch_assign(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow reassigning exceptions in catch clauses.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]], jsii.get(self, "noCatchAssign"))

    @no_catch_assign.setter
    def no_catch_assign(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40f8004928a33efa8cd03abc141ef34da1842ba2b02de29f29b4628226f43823)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noCatchAssign", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noClassAssign")
    def no_class_assign(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow reassigning class members.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]], jsii.get(self, "noClassAssign"))

    @no_class_assign.setter
    def no_class_assign(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e43ee7d309da511b473654a2967ac563fca541794f9a87bd35478c4fce4ca86f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noClassAssign", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noCommentText")
    def no_comment_text(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Prevent comments from being inserted as text nodes.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]], jsii.get(self, "noCommentText"))

    @no_comment_text.setter
    def no_comment_text(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b758709ce1c54621ac241ea9fa2f5f5b653e50d445f19fb5c0797fa66caabbe6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noCommentText", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noCompareNegZero")
    def no_compare_neg_zero(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Disallow comparing against -0.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]], jsii.get(self, "noCompareNegZero"))

    @no_compare_neg_zero.setter
    def no_compare_neg_zero(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a336f9ca2d487e1f9d9e06700a8e84adf005c16543893cee56f6cc74f7f1ac4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noCompareNegZero", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noConfusingLabels")
    def no_confusing_labels(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow labeled statements that are not loops.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]], jsii.get(self, "noConfusingLabels"))

    @no_confusing_labels.setter
    def no_confusing_labels(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77a8786500d19d10626d918f6ab2fa8e00f8ca538cb229259a4470de6fbeb648)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noConfusingLabels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noConfusingVoidType")
    def no_confusing_void_type(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Disallow void type outside of generic or return types.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]], jsii.get(self, "noConfusingVoidType"))

    @no_confusing_void_type.setter
    def no_confusing_void_type(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4e5c4da3b836c7ab3f1341d64a6f2e60c50001b56abde5a305da39a17ace110)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noConfusingVoidType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noConsole")
    def no_console(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoConsoleOptions]]:
        '''(experimental) Disallow the use of console.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithNoConsoleOptions]], jsii.get(self, "noConsole"))

    @no_console.setter
    def no_console(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoConsoleOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa3df4916b15171994fbc846a7f50560329ccb5650c7f26c05bdacac63f2f4f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noConsole", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noConsoleLog")
    def no_console_log(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Disallow the use of console.log.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]], jsii.get(self, "noConsoleLog"))

    @no_console_log.setter
    def no_console_log(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6ee2fbbf4f3983e032543541cd9542607ed5d5bf5dcf7bcc1eaca0a681bd86b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noConsoleLog", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noConstEnum")
    def no_const_enum(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Disallow TypeScript const enum.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]], jsii.get(self, "noConstEnum"))

    @no_const_enum.setter
    def no_const_enum(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdf4d58ef35309700873a30e7efe18706fbf2c8afacb7df2c4811c6cf9103b56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noConstEnum", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noControlCharactersInRegex")
    def no_control_characters_in_regex(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Prevents from having control characters and some escape sequences that match control characters in regular expressions.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]], jsii.get(self, "noControlCharactersInRegex"))

    @no_control_characters_in_regex.setter
    def no_control_characters_in_regex(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0357710c8c49e36387d980990fc697f16cbdf04eeba57ed83cf25b24388a8075)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noControlCharactersInRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noDebugger")
    def no_debugger(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Disallow the use of debugger.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]], jsii.get(self, "noDebugger"))

    @no_debugger.setter
    def no_debugger(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c4fcfb19ec9232f8fe267f6bf6031430c6259c26a74fe34147e4c8d159d7bca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noDebugger", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noDoubleEquals")
    def no_double_equals(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoDoubleEqualsOptions]]:
        '''(experimental) Require the use of === and !==.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithNoDoubleEqualsOptions]], jsii.get(self, "noDoubleEquals"))

    @no_double_equals.setter
    def no_double_equals(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoDoubleEqualsOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bc526bea434de3946993ee5703886e8ae463c24a4197f3e2d3d9634ed3f4858)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noDoubleEquals", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noDuplicateAtImportRules")
    def no_duplicate_at_import_rules(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow duplicate.

        :stability: experimental
        :import: true
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]], jsii.get(self, "noDuplicateAtImportRules"))

    @no_duplicate_at_import_rules.setter
    def no_duplicate_at_import_rules(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a54a714558a0c08ba8309d97719dc89161906453075e27e804b192f407a352a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noDuplicateAtImportRules", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noDuplicateCase")
    def no_duplicate_case(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow duplicate case labels.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]], jsii.get(self, "noDuplicateCase"))

    @no_duplicate_case.setter
    def no_duplicate_case(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5939445902dd586362a36d191864aa557bdb2cbe4c689e46cac1b1607b61da0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noDuplicateCase", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noDuplicateClassMembers")
    def no_duplicate_class_members(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow duplicate class members.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]], jsii.get(self, "noDuplicateClassMembers"))

    @no_duplicate_class_members.setter
    def no_duplicate_class_members(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46d048ca3a20232e323d59d78e96aab92dddad3f34c02686bce81d6824189c30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noDuplicateClassMembers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noDuplicateFontNames")
    def no_duplicate_font_names(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow duplicate names within font families.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]], jsii.get(self, "noDuplicateFontNames"))

    @no_duplicate_font_names.setter
    def no_duplicate_font_names(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffe45c3cb5d80b716ec024f5b016a792c8669d11bfe405943193f367d6ac8d41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noDuplicateFontNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noDuplicateJsxProps")
    def no_duplicate_jsx_props(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Prevents JSX properties to be assigned multiple times.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]], jsii.get(self, "noDuplicateJsxProps"))

    @no_duplicate_jsx_props.setter
    def no_duplicate_jsx_props(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__379df9001b16caef6363bb96769bc5e1d81ed2db8be126704556f1219820c6ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noDuplicateJsxProps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noDuplicateObjectKeys")
    def no_duplicate_object_keys(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow two keys with the same name inside objects.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]], jsii.get(self, "noDuplicateObjectKeys"))

    @no_duplicate_object_keys.setter
    def no_duplicate_object_keys(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__244b686e2d4df9e7f54de7277be3d3f90d582e074de3a0c6089fed2cb788014c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noDuplicateObjectKeys", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noDuplicateParameters")
    def no_duplicate_parameters(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow duplicate function parameter name.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]], jsii.get(self, "noDuplicateParameters"))

    @no_duplicate_parameters.setter
    def no_duplicate_parameters(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c69b2f2d27866a5627f83f68adc3794929cb8eeb774b35bda174c80450c8b647)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noDuplicateParameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noDuplicateSelectorsKeyframeBlock")
    def no_duplicate_selectors_keyframe_block(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow duplicate selectors within keyframe blocks.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]], jsii.get(self, "noDuplicateSelectorsKeyframeBlock"))

    @no_duplicate_selectors_keyframe_block.setter
    def no_duplicate_selectors_keyframe_block(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2287a2d2145654478f68259efdf31f8751b6845f1904568e7d6c6fa6002655fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noDuplicateSelectorsKeyframeBlock", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noDuplicateTestHooks")
    def no_duplicate_test_hooks(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) A describe block should not contain duplicate hooks.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]], jsii.get(self, "noDuplicateTestHooks"))

    @no_duplicate_test_hooks.setter
    def no_duplicate_test_hooks(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98c14e2c09d11214f6567c219bbff75e7c57de7b149db5b5b9dfa362feab5405)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noDuplicateTestHooks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noEmptyBlock")
    def no_empty_block(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow CSS empty blocks.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]], jsii.get(self, "noEmptyBlock"))

    @no_empty_block.setter
    def no_empty_block(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78aad3cf4c025915bae59a6ef04fcbc6b5a9dc6bfe98fa9f3c65ecb2ffa0d055)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noEmptyBlock", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noEmptyBlockStatements")
    def no_empty_block_statements(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow empty block statements and static blocks.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]], jsii.get(self, "noEmptyBlockStatements"))

    @no_empty_block_statements.setter
    def no_empty_block_statements(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf1825afad3893260ee135b705b1594c140b318505f3da3eb64d9546cd9ceac5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noEmptyBlockStatements", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noEmptyInterface")
    def no_empty_interface(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Disallow the declaration of empty interfaces.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]], jsii.get(self, "noEmptyInterface"))

    @no_empty_interface.setter
    def no_empty_interface(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a791fc720a75fe5816f2681b70e4c170521f9c38ca696ae209b8e29c62a973a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noEmptyInterface", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noEvolvingTypes")
    def no_evolving_types(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow variables from evolving into any type through reassignments.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]], jsii.get(self, "noEvolvingTypes"))

    @no_evolving_types.setter
    def no_evolving_types(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63d3b9d74cba432ca4e4630aaa711b534e8e7c0f42b81af52c22218527537931)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noEvolvingTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noExplicitAny")
    def no_explicit_any(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow the any type usage.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]], jsii.get(self, "noExplicitAny"))

    @no_explicit_any.setter
    def no_explicit_any(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4aad422e85fdeef99a68a972fc1ec2a445f6ae6499205a9e992afb3fb65b4e38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noExplicitAny", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noExportsInTest")
    def no_exports_in_test(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow using export or module.exports in files containing tests.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]], jsii.get(self, "noExportsInTest"))

    @no_exports_in_test.setter
    def no_exports_in_test(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2b4d68b8d328604172f086f1244fedbe10a3ef38e5c8efd08ddc5885d3d4435)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noExportsInTest", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noExtraNonNullAssertion")
    def no_extra_non_null_assertion(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Prevents the wrong usage of the non-null assertion operator (!) in TypeScript files.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]], jsii.get(self, "noExtraNonNullAssertion"))

    @no_extra_non_null_assertion.setter
    def no_extra_non_null_assertion(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10a80eda04d6fb514a953e1fac172b1708643924affa19c7b2f983f36010fb80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noExtraNonNullAssertion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noFallthroughSwitchClause")
    def no_fallthrough_switch_clause(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow fallthrough of switch clauses.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]], jsii.get(self, "noFallthroughSwitchClause"))

    @no_fallthrough_switch_clause.setter
    def no_fallthrough_switch_clause(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8373cd6dfba77030bbd542b5d37eea0f6e0f06a97b9c22c7bd449cf207b66bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noFallthroughSwitchClause", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noFocusedTests")
    def no_focused_tests(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Disallow focused tests.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]], jsii.get(self, "noFocusedTests"))

    @no_focused_tests.setter
    def no_focused_tests(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__373c82121040e97a5e12ee4a4a4486bae459e8e68955d5d553aea764688e2daf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noFocusedTests", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noFunctionAssign")
    def no_function_assign(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow reassigning function declarations.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]], jsii.get(self, "noFunctionAssign"))

    @no_function_assign.setter
    def no_function_assign(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ca2c6d835c2bef7f98b2283ea43912d40ac77808e12e174cc2830e4dddb2306)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noFunctionAssign", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noGlobalAssign")
    def no_global_assign(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow assignments to native objects and read-only global variables.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]], jsii.get(self, "noGlobalAssign"))

    @no_global_assign.setter
    def no_global_assign(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7086586801db68f59555103e08911e255d9e3bb0e81f972ee1b6ffb2f74e0069)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noGlobalAssign", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noGlobalIsFinite")
    def no_global_is_finite(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Use Number.isFinite instead of global isFinite.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]], jsii.get(self, "noGlobalIsFinite"))

    @no_global_is_finite.setter
    def no_global_is_finite(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c86387cdf8f4a9908cce84567554c5b2287f1fcc8b1db482494f61495f8757e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noGlobalIsFinite", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noGlobalIsNan")
    def no_global_is_nan(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Use Number.isNaN instead of global isNaN.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]], jsii.get(self, "noGlobalIsNan"))

    @no_global_is_nan.setter
    def no_global_is_nan(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db73c31ad2349cb23662fa5a8395fa866ac8ed268e050c9fd6a4c7f441dd98c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noGlobalIsNan", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noImplicitAnyLet")
    def no_implicit_any_let(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow use of implicit any type on variable declarations.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]], jsii.get(self, "noImplicitAnyLet"))

    @no_implicit_any_let.setter
    def no_implicit_any_let(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c80e9762de4d67d4714d3ebd391479e3c5b332cbbfbc62ae5ab4ff59bb879c00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noImplicitAnyLet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noImportantInKeyframe")
    def no_important_in_keyframe(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow invalid !important within keyframe declarations.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]], jsii.get(self, "noImportantInKeyframe"))

    @no_important_in_keyframe.setter
    def no_important_in_keyframe(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__390bdb163f029f3131e60358e81cd1fd1606ce15ab03681cf16c7067860fab6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noImportantInKeyframe", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noImportAssign")
    def no_import_assign(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow assigning to imported bindings.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]], jsii.get(self, "noImportAssign"))

    @no_import_assign.setter
    def no_import_assign(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7e7f05aa14a6761c39850a02cfb8b742cc3f4064d9d9a9a255f6deb834e55a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noImportAssign", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noLabelVar")
    def no_label_var(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow labels that share a name with a variable.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]], jsii.get(self, "noLabelVar"))

    @no_label_var.setter
    def no_label_var(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a9175f6c9cf3c37f7c7ab3a82d9ace42a945f9f4e5bb2d8f71cea894822daa0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noLabelVar", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noMisleadingCharacterClass")
    def no_misleading_character_class(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Disallow characters made with multiple code points in character class syntax.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]], jsii.get(self, "noMisleadingCharacterClass"))

    @no_misleading_character_class.setter
    def no_misleading_character_class(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f1f3f2f329c64f1158e80c791a80ef6891f96429b58a260c989f6b2b5c48b26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noMisleadingCharacterClass", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noMisleadingInstantiator")
    def no_misleading_instantiator(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Enforce proper usage of new and constructor.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]], jsii.get(self, "noMisleadingInstantiator"))

    @no_misleading_instantiator.setter
    def no_misleading_instantiator(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b21768c32c57bd9f6974f42a7d8a9457b5bc1d0a350952cea47bf20501ded11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noMisleadingInstantiator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noMisplacedAssertion")
    def no_misplaced_assertion(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Checks that the assertion function, for example expect, is placed inside an it() function call.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]], jsii.get(self, "noMisplacedAssertion"))

    @no_misplaced_assertion.setter
    def no_misplaced_assertion(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__813f789e4029f7b53446827f8666bdc990d043b01a646043ab213cfdd9a15898)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noMisplacedAssertion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noMisrefactoredShorthandAssign")
    def no_misrefactored_shorthand_assign(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Disallow shorthand assign when variable appears on both sides.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]], jsii.get(self, "noMisrefactoredShorthandAssign"))

    @no_misrefactored_shorthand_assign.setter
    def no_misrefactored_shorthand_assign(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9646382d00593630240c243f526d7b929a8db09f5ebce659002aa3e8c807673d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noMisrefactoredShorthandAssign", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noPrototypeBuiltins")
    def no_prototype_builtins(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow direct use of Object.prototype builtins.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]], jsii.get(self, "noPrototypeBuiltins"))

    @no_prototype_builtins.setter
    def no_prototype_builtins(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fc204b5cb6d8afeb88e25f4fcf7b30e74e478cbfca414dd26948aea55b21d6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noPrototypeBuiltins", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noReactSpecificProps")
    def no_react_specific_props(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Prevents React-specific JSX properties from being used.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]], jsii.get(self, "noReactSpecificProps"))

    @no_react_specific_props.setter
    def no_react_specific_props(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__257b6042ef82ec97b471642a7eef60289342ce9b49decd836a2be2ed945bfcee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noReactSpecificProps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noRedeclare")
    def no_redeclare(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow variable, function, class, and type redeclarations in the same scope.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]], jsii.get(self, "noRedeclare"))

    @no_redeclare.setter
    def no_redeclare(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__587c59c7c349d08735e029113e62d521c00df957240d900e213d6a7e50dd01af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noRedeclare", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noRedundantUseStrict")
    def no_redundant_use_strict(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Prevents from having redundant "use strict".

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]], jsii.get(self, "noRedundantUseStrict"))

    @no_redundant_use_strict.setter
    def no_redundant_use_strict(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2908c344331a8870921fd008febc013546d3be57345bda7ffdc85019bbf348e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noRedundantUseStrict", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noSelfCompare")
    def no_self_compare(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow comparisons where both sides are exactly the same.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]], jsii.get(self, "noSelfCompare"))

    @no_self_compare.setter
    def no_self_compare(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1eb5c612a0fc7d5e219714dadec76e5aad2c14c0de90f0b4eff4ff8fd1205384)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noSelfCompare", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noShadowRestrictedNames")
    def no_shadow_restricted_names(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow identifiers from shadowing restricted names.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]], jsii.get(self, "noShadowRestrictedNames"))

    @no_shadow_restricted_names.setter
    def no_shadow_restricted_names(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4679183d8153b092f2f2760e16a8f70926c72a0c1ef3ee7d66323de9bc20792f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noShadowRestrictedNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noShorthandPropertyOverrides")
    def no_shorthand_property_overrides(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow shorthand properties that override related longhand properties.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]], jsii.get(self, "noShorthandPropertyOverrides"))

    @no_shorthand_property_overrides.setter
    def no_shorthand_property_overrides(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6721fa1d37820ed643359409178a45b84917a764d57aca772cb7c407b2e1b9f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noShorthandPropertyOverrides", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noSkippedTests")
    def no_skipped_tests(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Disallow disabled tests.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]], jsii.get(self, "noSkippedTests"))

    @no_skipped_tests.setter
    def no_skipped_tests(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3069d7b1c45f2c015f7333aad654175e88d302ea99aea8719ae1677537cf73aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noSkippedTests", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noSparseArray")
    def no_sparse_array(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Disallow sparse arrays.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]], jsii.get(self, "noSparseArray"))

    @no_sparse_array.setter
    def no_sparse_array(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__790d733269d842e1552ebc8b0034dc59fb3b54339b39f753752c35cd0ca36d14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noSparseArray", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noSuspiciousSemicolonInJsx")
    def no_suspicious_semicolon_in_jsx(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) It detects possible "wrong" semicolons inside JSX elements.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]], jsii.get(self, "noSuspiciousSemicolonInJsx"))

    @no_suspicious_semicolon_in_jsx.setter
    def no_suspicious_semicolon_in_jsx(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6738bf62cd4b243dbec4c8643c57951b60affb6298b43977d6a24c82c9bb110f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noSuspiciousSemicolonInJsx", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noThenProperty")
    def no_then_property(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow then property.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]], jsii.get(self, "noThenProperty"))

    @no_then_property.setter
    def no_then_property(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec6bb0360375a0108804564228ceb834b466b358c94636057819c5c4243ef572)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noThenProperty", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noUnsafeDeclarationMerging")
    def no_unsafe_declaration_merging(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Disallow unsafe declaration merging between interfaces and classes.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]], jsii.get(self, "noUnsafeDeclarationMerging"))

    @no_unsafe_declaration_merging.setter
    def no_unsafe_declaration_merging(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ae0867cf27fae0c56f386e2a0bca91776d54d797b2197c76d6052dfb2bd89eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noUnsafeDeclarationMerging", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noUnsafeNegation")
    def no_unsafe_negation(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Disallow using unsafe negation.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]], jsii.get(self, "noUnsafeNegation"))

    @no_unsafe_negation.setter
    def no_unsafe_negation(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf2aa795cb549b660e7f09077c186f2f45b43927ad530c76628d77a64d8c4691)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noUnsafeNegation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recommended")
    def recommended(self) -> typing.Optional[builtins.bool]:
        '''(experimental) It enables the recommended rules for this group.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "recommended"))

    @recommended.setter
    def recommended(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41009e0e4afc663c2c1f9a5bc158f5dc4b002f1adb36a60f00162077768d61ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recommended", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useAwait")
    def use_await(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Ensure async functions utilize await.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]], jsii.get(self, "useAwait"))

    @use_await.setter
    def use_await(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ca8ccd0b2c2b43b4f492fb789c0b36cbc42a829a71f3df74b659e6cf5ebef21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useAwait", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useDefaultSwitchClauseLast")
    def use_default_switch_clause_last(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Enforce default clauses in switch statements to be last.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]], jsii.get(self, "useDefaultSwitchClauseLast"))

    @use_default_switch_clause_last.setter
    def use_default_switch_clause_last(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d0f67f47187b29e6996aa67f26a6c13092927a8a81c50e1fa556b91230da135)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useDefaultSwitchClauseLast", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useErrorMessage")
    def use_error_message(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Enforce passing a message value when creating a built-in error.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]], jsii.get(self, "useErrorMessage"))

    @use_error_message.setter
    def use_error_message(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae6bf2854256c678fabffb015d80270759e3ce127014591ba3fed7ac3419f599)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useErrorMessage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useGetterReturn")
    def use_getter_return(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]]:
        '''(experimental) Enforce get methods to always return a value.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]], jsii.get(self, "useGetterReturn"))

    @use_getter_return.setter
    def use_getter_return(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c88e609dd89734c7868062a5a010ecf643947c15aa5595b60ab87f9d68790bbc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useGetterReturn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useIsArray")
    def use_is_array(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Use Array.isArray() instead of instanceof Array.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]], jsii.get(self, "useIsArray"))

    @use_is_array.setter
    def use_is_array(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c1809ebf64ae422734ca6925eed05923033d0ef19b8c9d0282b23fc45c4f63b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useIsArray", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useNamespaceKeyword")
    def use_namespace_keyword(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Require using the namespace keyword over the module keyword to declare TypeScript namespaces.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]], jsii.get(self, "useNamespaceKeyword"))

    @use_namespace_keyword.setter
    def use_namespace_keyword(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__486f1711ad6978247d998381538f66c5a89a8c7c8cdaf22280cc28c611650aaf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useNamespaceKeyword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useNumberToFixedDigitsArgument")
    def use_number_to_fixed_digits_argument(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) Enforce using the digits argument with Number#toFixed().

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]], jsii.get(self, "useNumberToFixedDigitsArgument"))

    @use_number_to_fixed_digits_argument.setter
    def use_number_to_fixed_digits_argument(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2070abedd3e91787cf5abece8c959cbdc64054b76e47cf6aafb87d87719204c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useNumberToFixedDigitsArgument", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useValidTypeof")
    def use_valid_typeof(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]]:
        '''(experimental) This rule verifies the result of typeof $expr unary expressions is being compared to valid values, either string literals containing valid type names or other typeof expressions.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]], jsii.get(self, "useValidTypeof"))

    @use_valid_typeof.setter
    def use_valid_typeof(
        self,
        value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__645d7a2e1e51aea1e53b4c9c112d8d28fa306456c11e0cf7c2ce5b648b172bfa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useValidTypeof", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ISuspicious).__jsii_proxy_class__ = lambda : _ISuspiciousProxy


@jsii.interface(
    jsii_type="projen.javascript.biome_config.IUseComponentExportOnlyModulesOptions"
)
class IUseComponentExportOnlyModulesOptions(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="allowConstantExport")
    def allow_constant_export(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Allows the export of constants.

        This option is for environments that support it, such as `Vite <https://vitejs.dev/>`_

        :stability: experimental
        '''
        ...

    @allow_constant_export.setter
    def allow_constant_export(self, value: typing.Optional[builtins.bool]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="allowExportNames")
    def allow_export_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of names that can be additionally exported from the module This option is for exports that do not hinder `React Fast Refresh <https://github.com/facebook/react/tree/main/packages/react-refresh>`_, such as ```meta`` in Remix <https://remix.run/docs/en/main/route/meta>`_.

        :stability: experimental
        '''
        ...

    @allow_export_names.setter
    def allow_export_names(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        ...


class _IUseComponentExportOnlyModulesOptionsProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.IUseComponentExportOnlyModulesOptions"

    @builtins.property
    @jsii.member(jsii_name="allowConstantExport")
    def allow_constant_export(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Allows the export of constants.

        This option is for environments that support it, such as `Vite <https://vitejs.dev/>`_

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "allowConstantExport"))

    @allow_constant_export.setter
    def allow_constant_export(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5d4a0dfd450669012b70ec1d82f19518a05b0fa418f93f57b9f3a5e63e2a47c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowConstantExport", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowExportNames")
    def allow_export_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of names that can be additionally exported from the module This option is for exports that do not hinder `React Fast Refresh <https://github.com/facebook/react/tree/main/packages/react-refresh>`_, such as ```meta`` in Remix <https://remix.run/docs/en/main/route/meta>`_.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowExportNames"))

    @allow_export_names.setter
    def allow_export_names(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c74f8a70b9a4f5311bbb1b000807704dc8fc603cb45a2c55f31c565371502fd3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowExportNames", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IUseComponentExportOnlyModulesOptions).__jsii_proxy_class__ = lambda : _IUseComponentExportOnlyModulesOptionsProxy


@jsii.interface(
    jsii_type="projen.javascript.biome_config.IUseExhaustiveDependenciesOptions"
)
class IUseExhaustiveDependenciesOptions(typing_extensions.Protocol):
    '''(experimental) Options for the rule ``useExhaustiveDependencies``.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="hooks")
    def hooks(self) -> typing.Optional[typing.List[IHook]]:
        '''(experimental) List of hooks of which the dependencies should be validated.

        :stability: experimental
        '''
        ...

    @hooks.setter
    def hooks(self, value: typing.Optional[typing.List[IHook]]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="reportMissingDependenciesArray")
    def report_missing_dependencies_array(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to report an error when a hook has no dependencies array.

        :stability: experimental
        '''
        ...

    @report_missing_dependencies_array.setter
    def report_missing_dependencies_array(
        self,
        value: typing.Optional[builtins.bool],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="reportUnnecessaryDependencies")
    def report_unnecessary_dependencies(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to report an error when a dependency is listed in the dependencies array but isn't used.

        Defaults to true.

        :stability: experimental
        '''
        ...

    @report_unnecessary_dependencies.setter
    def report_unnecessary_dependencies(
        self,
        value: typing.Optional[builtins.bool],
    ) -> None:
        ...


class _IUseExhaustiveDependenciesOptionsProxy:
    '''(experimental) Options for the rule ``useExhaustiveDependencies``.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.IUseExhaustiveDependenciesOptions"

    @builtins.property
    @jsii.member(jsii_name="hooks")
    def hooks(self) -> typing.Optional[typing.List[IHook]]:
        '''(experimental) List of hooks of which the dependencies should be validated.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[IHook]], jsii.get(self, "hooks"))

    @hooks.setter
    def hooks(self, value: typing.Optional[typing.List[IHook]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f96be7f9a339bc344418d650903d48d72e4ea80b3d17bc15fa0ca81a431724a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hooks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="reportMissingDependenciesArray")
    def report_missing_dependencies_array(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to report an error when a hook has no dependencies array.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "reportMissingDependenciesArray"))

    @report_missing_dependencies_array.setter
    def report_missing_dependencies_array(
        self,
        value: typing.Optional[builtins.bool],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47048ca09711887f0ee5b4dd0a41e803d33255ef69621107a88c12be637e8967)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reportMissingDependenciesArray", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="reportUnnecessaryDependencies")
    def report_unnecessary_dependencies(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to report an error when a dependency is listed in the dependencies array but isn't used.

        Defaults to true.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "reportUnnecessaryDependencies"))

    @report_unnecessary_dependencies.setter
    def report_unnecessary_dependencies(
        self,
        value: typing.Optional[builtins.bool],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87c595fd551f9369ee0dd5696bee5701581e71195354fd10f457bd0322d1aa6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reportUnnecessaryDependencies", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IUseExhaustiveDependenciesOptions).__jsii_proxy_class__ = lambda : _IUseExhaustiveDependenciesOptionsProxy


@jsii.interface(jsii_type="projen.javascript.biome_config.IUseImportExtensionsOptions")
class IUseImportExtensionsOptions(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="suggestedExtensions")
    def suggested_extensions(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, ISuggestedExtensionMapping]]:
        '''(experimental) A map of custom import extension mappings, where the key is the inspected file extension, and the value is a pair of ``module`` extension and ``component`` import extension.

        :stability: experimental
        '''
        ...

    @suggested_extensions.setter
    def suggested_extensions(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, ISuggestedExtensionMapping]],
    ) -> None:
        ...


class _IUseImportExtensionsOptionsProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.IUseImportExtensionsOptions"

    @builtins.property
    @jsii.member(jsii_name="suggestedExtensions")
    def suggested_extensions(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, ISuggestedExtensionMapping]]:
        '''(experimental) A map of custom import extension mappings, where the key is the inspected file extension, and the value is a pair of ``module`` extension and ``component`` import extension.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, ISuggestedExtensionMapping]], jsii.get(self, "suggestedExtensions"))

    @suggested_extensions.setter
    def suggested_extensions(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, ISuggestedExtensionMapping]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41efe052f76dd649b2672bf99fe8dc3a68323e1ee08148e003111c8f18a3da65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suggestedExtensions", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IUseImportExtensionsOptions).__jsii_proxy_class__ = lambda : _IUseImportExtensionsOptionsProxy


@jsii.interface(
    jsii_type="projen.javascript.biome_config.IUseValidAutocompleteOptions"
)
class IUseValidAutocompleteOptions(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="inputComponents")
    def input_components(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) ``input`` like custom components that should be checked.

        :stability: experimental
        '''
        ...

    @input_components.setter
    def input_components(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        ...


class _IUseValidAutocompleteOptionsProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.IUseValidAutocompleteOptions"

    @builtins.property
    @jsii.member(jsii_name="inputComponents")
    def input_components(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) ``input`` like custom components that should be checked.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "inputComponents"))

    @input_components.setter
    def input_components(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c01e51864303044c695ee9f560229441313f0c5ca748e5c3ce19916d2a5b459d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inputComponents", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IUseValidAutocompleteOptions).__jsii_proxy_class__ = lambda : _IUseValidAutocompleteOptionsProxy


@jsii.interface(jsii_type="projen.javascript.biome_config.IUtilityClassSortingOptions")
class IUtilityClassSortingOptions(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="attributes")
    def attributes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Additional attributes that will be sorted.

        :stability: experimental
        '''
        ...

    @attributes.setter
    def attributes(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="functions")
    def functions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Names of the functions or tagged templates that will be sorted.

        :stability: experimental
        '''
        ...

    @functions.setter
    def functions(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        ...


class _IUtilityClassSortingOptionsProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.IUtilityClassSortingOptions"

    @builtins.property
    @jsii.member(jsii_name="attributes")
    def attributes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Additional attributes that will be sorted.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "attributes"))

    @attributes.setter
    def attributes(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f216fa513531782c728aa8cbcdfa5de0a81eb1f3add00cfebbf4f1c340264a33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "attributes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="functions")
    def functions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Names of the functions or tagged templates that will be sorted.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "functions"))

    @functions.setter
    def functions(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17d63db9be2f759513f375fffcd8ce75f9828ad6a6dc564c5c3ea2e80ca121b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "functions", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IUtilityClassSortingOptions).__jsii_proxy_class__ = lambda : _IUtilityClassSortingOptionsProxy


@jsii.interface(jsii_type="projen.javascript.biome_config.IValidAriaRoleOptions")
class IValidAriaRoleOptions(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="allowInvalidRoles")
    def allow_invalid_roles(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :stability: experimental
        '''
        ...

    @allow_invalid_roles.setter
    def allow_invalid_roles(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="ignoreNonDom")
    def ignore_non_dom(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        ...

    @ignore_non_dom.setter
    def ignore_non_dom(self, value: typing.Optional[builtins.bool]) -> None:
        ...


class _IValidAriaRoleOptionsProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.IValidAriaRoleOptions"

    @builtins.property
    @jsii.member(jsii_name="allowInvalidRoles")
    def allow_invalid_roles(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowInvalidRoles"))

    @allow_invalid_roles.setter
    def allow_invalid_roles(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1be15f3f46f1b59e586af0009e155012a2d0d5bc0069f5fbf5686977151ddc98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowInvalidRoles", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ignoreNonDom")
    def ignore_non_dom(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "ignoreNonDom"))

    @ignore_non_dom.setter
    def ignore_non_dom(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02e2dbe0696b1450df7596d1486a9a2357bb9982c559903d1eb3c69c8357b862)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreNonDom", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IValidAriaRoleOptions).__jsii_proxy_class__ = lambda : _IValidAriaRoleOptionsProxy


@jsii.interface(jsii_type="projen.javascript.biome_config.IVcsConfiguration")
class IVcsConfiguration(typing_extensions.Protocol):
    '''(experimental) Set of properties to integrate Biome with a VCS software.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="clientKind")
    def client_kind(self) -> typing.Optional[builtins.str]:
        '''(experimental) The kind of client.

        :stability: experimental
        '''
        ...

    @client_kind.setter
    def client_kind(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="defaultBranch")
    def default_branch(self) -> typing.Optional[builtins.str]:
        '''(experimental) The main branch of the project.

        :stability: experimental
        '''
        ...

    @default_branch.setter
    def default_branch(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether Biome should integrate itself with the VCS client.

        :stability: experimental
        '''
        ...

    @enabled.setter
    def enabled(self, value: typing.Optional[builtins.bool]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="root")
    def root(self) -> typing.Optional[builtins.str]:
        '''(experimental) The folder where Biome should check for VCS files.

        By default, Biome will use the same folder where ``biome.json`` was found.

        If Biome can't find the configuration, it will attempt to use the current working directory. If no current working directory can't be found, Biome won't use the VCS integration, and a diagnostic will be emitted

        :stability: experimental
        '''
        ...

    @root.setter
    def root(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="useIgnoreFile")
    def use_ignore_file(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether Biome should use the VCS ignore file.

        When [true], Biome will ignore the files specified in the ignore file.

        :stability: experimental
        '''
        ...

    @use_ignore_file.setter
    def use_ignore_file(self, value: typing.Optional[builtins.bool]) -> None:
        ...


class _IVcsConfigurationProxy:
    '''(experimental) Set of properties to integrate Biome with a VCS software.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.javascript.biome_config.IVcsConfiguration"

    @builtins.property
    @jsii.member(jsii_name="clientKind")
    def client_kind(self) -> typing.Optional[builtins.str]:
        '''(experimental) The kind of client.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientKind"))

    @client_kind.setter
    def client_kind(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5136e48dca5f067956c5199676ea806e278d22114d15002afc29f1a7589edc42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientKind", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultBranch")
    def default_branch(self) -> typing.Optional[builtins.str]:
        '''(experimental) The main branch of the project.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultBranch"))

    @default_branch.setter
    def default_branch(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__142cbae57818c8e62ebfef860d3d6ea0b9ce3277d377c495d481df8c4d4102ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultBranch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether Biome should integrate itself with the VCS client.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c5805fe3a31492d44837f692ff58b2ed36d79cdff36ee63051964462129cf55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="root")
    def root(self) -> typing.Optional[builtins.str]:
        '''(experimental) The folder where Biome should check for VCS files.

        By default, Biome will use the same folder where ``biome.json`` was found.

        If Biome can't find the configuration, it will attempt to use the current working directory. If no current working directory can't be found, Biome won't use the VCS integration, and a diagnostic will be emitted

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "root"))

    @root.setter
    def root(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b790bd02baf0f96befe5a7c0ce55df0e67091fdaffa34020eed99d1a33953d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "root", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useIgnoreFile")
    def use_ignore_file(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether Biome should use the VCS ignore file.

        When [true], Biome will ignore the files specified in the ignore file.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "useIgnoreFile"))

    @use_ignore_file.setter
    def use_ignore_file(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__feba7b5dc57c10bc7f4090454aecd8b6cdfabf9475ff7e39668de4f8cc4cd973)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useIgnoreFile", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IVcsConfiguration).__jsii_proxy_class__ = lambda : _IVcsConfigurationProxy


__all__ = [
    "IA11y",
    "IActions",
    "IAllowDomainOptions",
    "IAssistsConfiguration",
    "IComplexity",
    "IComplexityOptions",
    "IConfiguration",
    "IConsistentArrayTypeOptions",
    "IConsistentMemberAccessibilityOptions",
    "IConvention",
    "ICorrectness",
    "ICssAssists",
    "ICssConfiguration",
    "ICssFormatter",
    "ICssLinter",
    "ICssParser",
    "ICustomRestrictedTypeOptions",
    "IDeprecatedHooksOptions",
    "IFilenamingConventionOptions",
    "IFilesConfiguration",
    "IFormatterConfiguration",
    "IGraphqlConfiguration",
    "IGraphqlFormatter",
    "IGraphqlLinter",
    "IHook",
    "IJavascriptAssists",
    "IJavascriptConfiguration",
    "IJavascriptFormatter",
    "IJavascriptLinter",
    "IJavascriptOrganizeImports",
    "IJavascriptParser",
    "IJsonAssists",
    "IJsonConfiguration",
    "IJsonFormatter",
    "IJsonLinter",
    "IJsonParser",
    "ILinterConfiguration",
    "INamingConventionOptions",
    "INoConsoleOptions",
    "INoDoubleEqualsOptions",
    "INoLabelWithoutControlOptions",
    "INoRestrictedTypesOptions",
    "INoSecretsOptions",
    "INursery",
    "IOrganizeImports",
    "IOverrideFormatterConfiguration",
    "IOverrideLinterConfiguration",
    "IOverrideOrganizeImportsConfiguration",
    "IOverridePattern",
    "IPerformance",
    "IRestrictedGlobalsOptions",
    "IRestrictedImportsOptions",
    "IRuleWithAllowDomainOptions",
    "IRuleWithComplexityOptions",
    "IRuleWithConsistentArrayTypeOptions",
    "IRuleWithConsistentMemberAccessibilityOptions",
    "IRuleWithDeprecatedHooksOptions",
    "IRuleWithFilenamingConventionOptions",
    "IRuleWithFixNoOptions",
    "IRuleWithNamingConventionOptions",
    "IRuleWithNoConsoleOptions",
    "IRuleWithNoDoubleEqualsOptions",
    "IRuleWithNoLabelWithoutControlOptions",
    "IRuleWithNoOptions",
    "IRuleWithNoRestrictedTypesOptions",
    "IRuleWithNoSecretsOptions",
    "IRuleWithRestrictedGlobalsOptions",
    "IRuleWithRestrictedImportsOptions",
    "IRuleWithUseComponentExportOnlyModulesOptions",
    "IRuleWithUseExhaustiveDependenciesOptions",
    "IRuleWithUseImportExtensionsOptions",
    "IRuleWithUseValidAutocompleteOptions",
    "IRuleWithUtilityClassSortingOptions",
    "IRuleWithValidAriaRoleOptions",
    "IRules",
    "ISecurity",
    "ISelector",
    "ISource",
    "IStyle",
    "ISuggestedExtensionMapping",
    "ISuspicious",
    "IUseComponentExportOnlyModulesOptions",
    "IUseExhaustiveDependenciesOptions",
    "IUseImportExtensionsOptions",
    "IUseValidAutocompleteOptions",
    "IUtilityClassSortingOptions",
    "IValidAriaRoleOptions",
    "IVcsConfiguration",
]

publication.publish()

def _typecheckingstub__badd0e51dbf93a35ab5ac2799727503b1860ff7535908d55669e22bf7f9e8930(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14325cc0c0f6d6714b29a964e2eaaa788931706a7b649effa7be33d156f5bf23(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__061886d01ca59a946c6cf6b28fc22bcba9d82795c0cac570978cc470187182e5(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da101e3e53bd5c4c2bf4809333ad263149575cef80d5c3ce0902ebc80cc710c5(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e949f9a7943b853e59b5d827d16a11ee2d15624f19744abd42ed6cca7fe5df3d(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24d501db6193e9146a62a7650ae4dd49d3cfa3b7d9be9ad6d6f07af4b009d883(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithAllowDomainOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bedd0f823335951fa5b71166448bb1558408480fafa30ca579254f0f177f1b5(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3ee003c13279c1d9433519f1560be0f0a582af3e9744ef2988f0b31e334c5bc(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d3565a1863735e0d6d42521ab0700dcee8f51a7f232a3d53d9f82d20e58d0ef(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff0335d183fe2accf83547cb02ee7ef359f7e3ad57b6a60724d3bfd18d1f563a(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoLabelWithoutControlOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a34f454613118b49849da4a32dc57a4eb13e722cf205417b9956d947ce158a10(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__207c6c55fe512ab828ea3b4a488b4248792ace501e98d2ea8cbc95d4bde8eca4(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc9d6b18e8e360d8f2117ba10f2b50f59c72449599b4b94270235b690e666ac0(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f39142081ca04b6cf2dda83461d68fa7ec1e646044165ad8f8031451478118a(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5815be222cffe8cb14379a35232c28adba7fbb31051392c02fe352aff1cfb686(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8d0f1756afc844438cc5cce37384f983f9c60a7301d81e45a95b49a78b9dee9(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25f6269b6b2dceb5b14d206301614fcad8ffc67fbe040dcbe4326a40ddcf69d3(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5f54a04a64674c2cd5d536d1f50056f6094b9277e9edc723cf5a84eb6dddbc2(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e5b6769c1a6575d4dc68343057aaf2b1ec0ed7e658f3b5a8c41a04c756b80dd(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffe5d8a70d06b3ca42730f78efae5c1d666d322c2239c6b66969ef9791633ede(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a780931a71bdc977a8560b015ba95463cd2074e68bf35fe8824608ce4d8d0874(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c30b3e7cd99762f7a234f66dbf1031156692943acf0f78c6ecd29cd0f4a531c(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad76142a33de27df66b11df77653ea575209aa20090d9c31910df11a15fd665b(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__802791d714df1717098027e8c1b74cbc4a0ce31838a80b05a9094b37eef81697(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d08e03b5305db1d1603edf6496435905357608066008d4f93dfa9040e9d3a162(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bba312ea093a85fcd23cfb54f259d00507c55482f5b63f8d1431baf02c101467(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c73f85d0867aa8ade9a55d9c38cc9a0474f8a8c4253eb9b2e647440b6abb794c(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e14ec9fe6539ab57f54d77e106a80fbf0fcee37a71a5af2ecaa97563db1d2112(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d21718dec8ae4b3a898c8709014c7e31f138c31569f271004f3cf4c54927623a(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__987aa34178662376da76a1aef3568457e91259b6ff95f286136ffb1ccd2332e6(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__912323bf4fb8d4010cfb94def3b8043dc6d5f231d2ae79b8d2052ec2935a1ec4(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec4bbf3ebd038d4d14b1d542988b1bf72a2efc9565669c9dda404128a6720cf3(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b87e8452832653685744a282cfc67f9716a3b402c9f6218609e9d75646d509a(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6af18b773668a3a5c1a92becfe381333a2422cc2ae1061ff1482b1faa741421(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithValidAriaRoleOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfd213ffe79ee2a02b64001a7daa35f7af0d84203eabddd1a177973fd0c5bb3b(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac3b29c3dfebd21aaaf1c18856f70485f15f4cb387baf4f49fca690a9c368156(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7885b267242ab7487e26e20dc5ccbbace5542c71cc20540d689161aeb01669e8(
    value: typing.Optional[ISource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f9f37ceb9b03ed691283ac31b5562272a16c3ac67044d92300f67175e583fde(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d5d19d5827687684b03d2d0ad966c342b5c2f8d8d0211bdad14038c74d9378a(
    value: typing.Optional[IActions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c10ca9a804f308fc75cca8068b3b767225f4f025aa343064b7f9ec5e9aef0a2(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__663c56ce895f236cb37ecc605f09dc983b9c83aee27413c477dbe22cdb166cd5(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a80e8d8404a7a73c83041947870a887bc8696c97ec71a58466cb4abbbdafe27(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81dfef0a7b76c4b904e218b5571e951565908bb26a6f05e2f24aced76abb928e(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac576a2aa458a1f40a9ee1ff3ffd44005031cfa009832850596ba32e418e7bb4(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94bcb3eca282dc0819b1b89a8208e80dc2a18f8faeb7732550393f5325101100(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b070a07de17f2ecdc567dad6f4eb140ad07153bfe9bf59ad541f988a4697fc6(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithComplexityOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77c9921099705c4f0fc7d3b7e042fa4a250061c7729f5c2754ed00f530926531(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f7cb6920800155702b9b29318f733f20beb02c96450897bbcea97cf0b4d93ea(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09e155514481252a199e15d99de7ade8733b3ad223a9cb6916243dc0dfd38f05(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7832220cfe9ec2d7eacfe172b836a0c1c226bb2b818b85e84776bc957af1af07(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be6a363d6ed6f19911d8f3b85f27cbc100b07ff390030266d9e1b18d1064faed(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccc966a14f0ad1c4400be9d31266c4369dd5a66833db9e76773d270a94d51b62(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__550c13e7ca1d8edaf45954383393d367200faf3491b22d5277c20b29a724a48f(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48447d97386f6ebd9442fdbfa7cb432263cc029e98391be8da835361e0d56d1a(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__184b8369db2e0361462e0072711a85fc4d8b08be044bf9156a133e20c0fb9129(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d86d1faf9e93c0047ccca4ab8884a6226cd64a747f2a6c24b475d1e831fdf86(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc2d3c1b7d492628dac2404a059b2e2f06c22898abcabfe08525a14b247597b3(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4876b1ebfc889845a2f0115187febf0de5e7099f125673a3cb7301df9aa70538(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b41db8df47a49f96beb38540cb374ed37ce4b75bf7bbd23d58b48f42dacdd84(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34d5a683406556fab59f9b2c764491e1fd2630c8faeb168fe4fd20507f099a6a(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95aebc0bf4de8bd7e02193b09b628eb724623ee1e26d45b269866d389668ce77(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2374a8cb9ee2ad78532b33b0a8aa172d6056f524f8ee4df23c832248b8374c1e(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__583313ca5c9eecb07d5801862b82b0c8ef656ce978027d6504d33dd48e17248f(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35716f453cb77c716aacc372b1de5e56b8a1afa0152704a09fa6c79cd67cce6d(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__764c7ead6631aa3a414b418a731061e87636902195aea2e94658c5c26f8b3b07(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7b46453a7adc35e574d584728a4fe697a4be1f5b41c0ef6b1e1a07d52fe936e(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bddf3faef23a299d0e46750faf56278b1370de31683b6d3b135d0ff44284748(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__691b127b6bb9f45ec578da384ba4d528eb91a94a1197d41539283520ceb90a01(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9711b21685ba3a17c03b3884187be7fe6ec8492d4a2d1bb9e5c9bdccb41ef5e9(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0147b4a6a0a82fe3d35ce697a262d260a764ee168bb8981ceab9ef258fff034c(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fde1a14e4358262119414b0fb7497a1a1a19752bf4ca8eddefc2a45799e7e769(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__026f54e5038acbee5473fd1df983a2740554f3f2757b2d20401b67778715e93a(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__215c792f5bab05c9d5ddcec3b6164a5873049dd88eb9d8f94a4b18ca6b72b53e(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__284b064fd7d479aacc423beff999a1bcf5575783792b4dbe93ccd5c37c348dec(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9e6b292d2f18b74400ed84d4598817f3c3463a200984c2179b5c80abf7d5724(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e336b60462abd4ddb48fe9acd9bd5250a7f161179b5cac127cfa51ebc3008f9(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__730cb570896a87fa0abe2fb84c33cf5ffa7bf918511eea7126384a15e7b5cce8(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19ef59b92890c0302f27732b07d85b3baac8ac9f80a459d269e26941ef5945eb(
    value: typing.Optional[IAssistsConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f56cb36219d0a510ffd5110a47e6977e468d23152c729b5366c456e1c4b76dce(
    value: typing.Optional[ICssConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72c1543c48b401a114885804899042a3aeab12fe374664b0e0874b8331bd4be4(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbf5888714978c76d93f191fce6fc24afe161b4c2602e9796173392a4710c4d0(
    value: typing.Optional[IFilesConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__685ae26f5d8b96d6c516ce520a72902af5ba20be500f6b269e3a81d9bc2e89d7(
    value: typing.Optional[IFormatterConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__893d61135484b0fa3f122454da784dc165143f265ec6daf4dbe60e3808319479(
    value: typing.Optional[IGraphqlConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c52427e4ea4b41dcf9edaabb1a1d0c5a888f23607671086eaf3a81b4d14464a8(
    value: typing.Optional[IJavascriptConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e23e007685b010ac2f113fdaa1ef164bb116cc67eb9788b661f5ed56c4f56a70(
    value: typing.Optional[IJsonConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa0ba6323f05508c77e65eeedff69e17bd8c8012fc7cabd2326aa3297c53b498(
    value: typing.Optional[ILinterConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__903038f50d558cadf8b887a936ed082600c0fc8b9164a87e7624692825ad778f(
    value: typing.Optional[IOrganizeImports],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f83daa8ef482de67976967829aed7ec68c4dd5e9e51c4dfc2d1f99c6233736e1(
    value: typing.Optional[typing.List[IOverridePattern]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df9874da1131d438df5b8358df9a526e60e72a39fb6e24552f09845858308fda(
    value: typing.Optional[IVcsConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edd6030218644f5c1ff274094ba2ca482af80aaa06e8d0a5d864c1f1a54d9cca(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fe147a2a903f0a90ded05a021117f5c3f32f21821430cbace964257e1a4ec73(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d996705432f9a05786fe491b3b9394c2467b88acf03abf2de4573995ff7a2a57(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54a76e2eecbbbab9ae3f0683bdf2e516348f28e2536a09c7e533297864b8237c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__585fcee8be7ecaa7cfd54dd46e1295851adf353af3939640f9e8dd2d91b00fef(
    value: typing.Optional[ISelector],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__098230eee4022d245f3cf2bb2a023a35049ec26fcffbfbddad44eb9d2a4acc70(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9994d36d0cac2f96b77ebb93b95d6a18558d3f24a7b92b4b072f6dfadc66ff24(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e58b43c3e329e892bfd8b4cbac443acad011b52cb60f2d253790ed7cf4b0e296(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af5d59ac5671f7082a94972eafc6e387e9dbcf8a530dd50517afc35f0073138d(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1eb523d0089eddd593c4a1852f8b89f2413880fa5e6bb8f2de5333cedfe9ea2a(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c237c61f679ecfb3e90060b7b107183e8b8e51a66a07ebacc752ae2206c1fe6(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__248ad84f845aac5113de595fc6458e474b2f8e913e697cc3a053de9a19dd4328(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c7fcdd1e35aeb89c4e519901c4d6633704213133ab4e0eada6cae68970acf79(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32dbeb99cc31282c15f50fa58ec5ce565a254f7d8d35e0c0b8013572e7dec8ef(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6221f0b2b950d20bcdab7f59776be8f5bf23777ae1f4ed5a59f8a6a8d49ccb90(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__648ad48f3943e91b88cf1a716fa0fa5bd5b5ae6b7667713b3c17756b521e35ef(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5496e61b94f465b71b05d8886f3b9eebc5d0bab5b81ec168176d57f239cc0e8c(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd26ae2195ca9e313642103010ee2747f98b47a7c334e5df48b7298a2272a13e(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d64977731ca5df0ed98b5a6385aa2bfa6f337521c99860245971253f9945e07f(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f58b68456750cad22457b63a83988d26471a97b09092505ce46080a499c58bb8(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__966f8ff6be4ad6cab78155ad40f298016b5b2a3db450ba5c03c467056c47063a(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__735c79874ad28098cb4ef92cf896ec070dcfb87d30cb735663aab1aa1d92d808(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64bf88a7f183bc72b0fb7838d36fe2c258fa0bfe992e2f4a0445aafa9437520f(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee495084e223bf762c6cc58ec2207b353e81a2ee8752a27db98e415258d58977(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e46baedd5ff9617bb340b2b9a27cbeb795297c8687143b49c2535a31cec3d16d(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e53757c666925710b80a1acb1d8971bb9e95a335a0d8e51872fdde1da02da946(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45bbed23498cc2dfb696e950c1fd5a13c3a72b1a00f71e008eba28bbc15e674a(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__786b5cc23f2d599b2c8d8bc34490c9a5c948b2120c2cb7be3a2adc30f958a32e(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d812ec612c257034c485a76394525f4498c20db85bc2359be30c231b2722955(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5c80e320331b4eab558e1dd2f393d899910904282c8f020d1ec143e65e91215(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25416124d2d33d921fc0eb9cf6b1fd4ab98c09a0df78413f4f4d93347b0d1b6b(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7eef9dabb1ebfb0ddc9f826c425e50e097eff52dd84cdbe237b22a89bc034ee4(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5252c1d86c4de7b7a23c791263b87a8dc6187baab551594b73363786edc3c8d(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb812ab715c10d8c124dcfdc50eb757c6274946700344588520bcc0ff07424f9(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed0e1596f722a38bc32b5bc82b2a83d0154da0633cb247918a5e589946a4efe4(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aefc6d84ced5f132a0b8e5ebb3996a9ef4658630e1805367789a844bc174072d(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b65d2ca8686e50c4fa233049df307d12f0ddccd09b1b6dab03c7eea371e1ea7(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df90472b886a92dab37744073838016f7eabdfd8ad51844c65d6141f9b21090b(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5676ba70d61e378d9606f48a6a5a02a873127bbbcac52616904b1bf63b216fbd(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__975ba6d3bde38f393ccacdf0b728b8d129fb2f4ef652d5bf3fa6b803226863f2(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d08ca5501f4738b0174602833040907fca7ac2be552d82d545bd2a9893cc3eb(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12db216ac6b0da4d39ed5cb52b9d22216c58ab8ee059289b70092e0441184464(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00221b7246b8671839cfcec7a3de248fa8aa1aaefd968a886a2b5f0d3075bdc6(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1a3e411d74b6af150dbf64c3ba96867b2727be020b2f7c1787702a12ec16330(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a663e86bce2cbfb06c8586c23cc421cfae81b71ee484b37e797dbad496b93497(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa071ffe55968bf4a20383ad675be4d97a93940609e34dd98a49f2a2aa4da824(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__269ae961ee14164a9aff745ab26256ff07af998901f286daefb43b46fcabef3d(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b7c20a2e443261f6b2d5c542f84973461b23c5d9659cc5af45ad00af960c453(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__425353e112cebe1433db7a45ffeaa52d70e55b7578d0f24b5bf9cc8ea71b7680(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6a4b1404bf668f26aa98e3a50347e0c979d5b93cb69e083b8fb70fcbea98ce8(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c75a8712d097ad5853d2324cf357a357d7ffb436664b608c2a0ef97fb3db20d(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3c7bd295b86608b6a9ebba9fd5bdec1596386f11d668ab29b895b4d43bbe50b(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71e148401b1df5a9a54aa080923801561e6827ecbdcaef0663d6f3de1e04ecec(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cd51788e13cf60e6104d969bc02fd17b611d29051347c74447382c13f997f47(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithUseExhaustiveDependenciesOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30d66c3a8a7fbec8bfd33fd02410c78af2751e156a8741062a33881c01dc0639(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithDeprecatedHooksOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__913d910a10af876d6e6755aeaf4a2680e59d9d126c62bde720d3736bb14f507e(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithUseImportExtensionsOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd4a80de3c9ee0f4772368ab9d75b8544676e8a239a3e36895e0b0f6c9bba39b(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ef40a7236b7c1177932ef2f97d7e7485e347e489b37b26b117e3129a0df147c(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f997c1fcfeefe0ec3614552afc16b1f05575be08e51d6f51b6b2532321384deb(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__977c3c6c00b3ed0d7cd33a14beefbd8cd0334eba18ef3091a98f04ed5297ebf9(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9162ac26e13aedac41c42ce0e33b611d2267b8120b2fff01334415e34089327(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__487c70f5b2d664fc2514c6eede115a76cb4ad442396c5cde40ae2f89bd33cd68(
    value: typing.Optional[ICssAssists],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb25e6f8e596223545eddbde666181453deb9b3d041516cfba145e4f1901d8ba(
    value: typing.Optional[ICssFormatter],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d76b753d915d1a9b1cb7370b1b921317d51e5dc7c632f314525056f0b3c3ad9(
    value: typing.Optional[ICssLinter],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3b9568cfd2347f24e1f4780a7f81ee8659da36ee2cdd88636adaf6d0d3ffaa6(
    value: typing.Optional[ICssParser],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da44ebc43ae17626208347d92527115b6fe58d918f02f99546c6f1a60b170ca8(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6650589045d9bb4095648ddd4fab08f0213c0f063d64d361945e89d43e10b055(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6aa855ff702add215c5f6d36015ffb9140e5a7e7efe72544de60ab4f63c6e765(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce3a6673120c30bff3a22cb4c6525841ab58fb2b5776144ed71a33cef73cf451(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebeca7bf2c8f499bd285a378b385d51922eb483013ec751d5406d1e0fc1cd04c(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c267c92c158ea788c22709e05c1d726a644977b8b72d4faef17c024a23f27992(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5583a36866f3f1f076f9f203158837ccd46c343586156989718a644e5980afe8(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f69ffc8bef31249014c76894af04f2eaa4e8991ed39bf656007dcd48f6cc5b5(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e3eb219f02034287491a4901eaee4a6defdd94eda119e20c513a82862740657(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bdb089598bfbe59ce11b0286a4ac4e6e74e6dbe60eca9d4b0060e44160bc77d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3188d9cc6adecf012f900ec5cd4bdf4132b6be97b89212e78f0262a3fd7d8d95(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34f451e57c6bca38e791cc9ad0267d95804c1bc3027fd03471fff3289323506e(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb00409d724c1a7e7ed80d0cc68a35a13abd05751c36f583d1374a36153f6cae(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4406b322dbff8e88493af5dd8879d3794c4e8fb5db5ca25ec60737431b18ef75(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78032ae2b8140aff1b483509b8f36df2b2dcc90dc5ffb186a4360afc22288339(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2fad0b2aa22cc3334df1681a006e0f5a11125961cde1b9a8fa71d5a2eef8eed(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e230182b0d61868f918e621eb114d5f7c19b14ee6cb50c5e3a39ce23416df5e(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f911b12dfd866d82d08d9540818d97620d787c8910162b295a80895e06dd1a6(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b659e962598791441d86cf45aa838464b033269eb39aad84ef15bf47c945a1b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35f886619dcca81c7a317b9ac18a44e01c61eed84cd3341caa8476189efd80d8(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31daa0e8ca08bb67818df018db531931bf807f8464ee1ae2c263498c22b79a23(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce7b00e72be79d8bbe2f42799c64bc1e8ef9dd2f895325c053d7d4fe3f2f3cee(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d6b05c80808795fdb4766e749ce9c7a7f617f8432472888d14aed7770577e99(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6874bcbeec6dbf3a3da150a223ad430c9a917857d947fbd18eb808bdb599a737(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5eb6db758c67cacb60ccc18d54f4a52e75430de65d98b4baa45d4cb69e784d57(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ce4ee77a7e83ab1cb8761745da8e25852d39e64b9b13e60e0e406a5ec50820c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07b3f4f8ea47774e96dd2e80d16d8e224c90c984ad0049c17861dcf27c7417f3(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__299ff1fdcd6f0e8c367b9b997b902a3ef995a7e399f216da199d338bada65aae(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6aaa599169edfb63c965be53d5006d75f3561c5f6dad52b9841b0ceddadeab01(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcc775927c735486dcacbf59adf19bef48422bb2dc6dfc672b3a751f931ebc68(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea6ed61a12ed032e550a7325f3e520e15f49dddd7761bbdee2a7bb7e22475ff5(
    value: typing.Optional[IGraphqlFormatter],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97f5b7dde3d54d91c19d7a20ecc9ab2c9b0d3e4014e6c91ca2c84f16391b9210(
    value: typing.Optional[IGraphqlLinter],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99b3e53fce7d0a506392529be98ce0a33e011ee2377f82cc006c8a96da9f205d(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__873478ced7f5372e2483dcec81f2062819d7afddbd6cad4c2d900bbe7f0da81e(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee042c564f228d57470975db311ffe0676385f1a6cc3a010be8170f08ae2626d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d004e786d8dd735d54009dede2edb69b34b592fec0d0390cee3bc0a317381d8(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d736bf8ca577846f23a09409db240dd3ae393286196a082c622f12ec4873c1b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__843d929ef1c01009114e6ebf8c2041c926aa89d2d22cf8f5544fdba0d9cbb77a(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54aa923e26579938ecae34290cf4c0e2d9b754da8493b2e37e44d3daa0f9fad9(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bde9aa9118e52045889d9bd7b2391615f8f2bbe7b0efba43b236e98fce4727a3(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b23204701303e2bbf936eff96bc0476cd451078bca7cc49b0e9a98eb6d07b972(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2038e99f6017f032f2a39137b6391b37e426c1c3f2ee17a1014b7561978468a5(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c40013ce6f8ef554264029ad597e25158a7076f4bb026fc38c0428cc83c169b5(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ffa991e90af0407fa545c66b2c49cbbec83808e4c82b9b0e89d9c60448ede05(
    value: typing.Optional[typing.Union[builtins.bool, typing.List[jsii.Number]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9e8bd2a6062d2431a84fa40c0f5fec47c1e6dfc4b76651d376a40412f802f72(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df7775e52cecc3d9e508cfd21ad8c5f20ac8b041c2ec5173ac619773f18f0041(
    value: typing.Optional[IJavascriptAssists],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d6a6596e673ae8a28a21f90d71a18f1db2dfa6a675f0e4ec0059010f6ff1178(
    value: typing.Optional[IJavascriptFormatter],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eafbd538d9f407787a059d9a833b689afd039cde5689eaaef5471954c0c11902(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acfaa9c56a2c25659e2e9aeb5348aa58e11ea5edb8b53854a57f3e382d996422(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__830e7fa8c182d2b1cdf2f33ea8b432be2fce658716588754fa65ea4d93e82a99(
    value: typing.Optional[IJavascriptLinter],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca952e37b38f4f82ff37dfa6599ed597e58286b38c7803860170876f7c10d53b(
    value: typing.Optional[IJavascriptOrganizeImports],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15f2169a77f15045edcc320552ca364d5c1a5345761f3fed02785ec92426d589(
    value: typing.Optional[IJavascriptParser],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4c33f8f8df506e572000450c81891aefaf38f973c634134f849aeac9a946f5d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a86e37c5f0be9c78c3145f033cbd7eef9862dbc1cee5fb382e133c9c4e54ce1f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a7ca7714b3ecf7f5ca32352785cc1ae2340c49510bf30887356d06697298538(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9895d6a9398ad6f77d0d9c93fe871de803d95267102a4f5c5b8c7555a4dae912(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64200bff30eafe842e3c02f48d3dd9fc700cf115408d2c6298b137ee0d22e00a(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__970e4c04ca22cd11930ae9df06700b76d659cd3d90b4b9366cb4053555e246ba(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abcb7803a33213fed04a1025c761826134ecb6ceaff4ff490403d2fed4f171d0(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfd5ba625ca78c4d990a31597284f8a50537b36db5d4e349cb42f6bdcf9fdfd0(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__879ff32a863ced9e892e8894793cb3543bac036cf5c6aa14cfbd39e68db61c1e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3967fa3bc2612d47cb8da54af2554566d7e76704708a215418ad794c665b926b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06889dab4ea04f2d6376e2d5899aa9369e4eb73efa3bee44215d65696505c5d2(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8d9f95731cdb26d51251fe149b0354fc7b67912ac089fb52a49d7b668beee0d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b216b77c09f6555266f0bedcdc8f98b19dc174b8252eaea234367e7882527ce(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a496627366d4cc1fe8d8c4c4e7659ac71eb94aa06609b36ad8cedb7c0433e8f6(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46dffee5b48aa02a568a9d75ccb86bf239814830b3d0e49fadfed8475d6a66d3(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__681fd9027b5be8a4772dedbfab97e9699a9b9a08096af47f5dad4127e9246d1b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54c636b732eb87081fc3dd273bb28c9c652183c34c20bd1c2da7ef30257ae3ff(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a6f7e985439173c7ce7031153f14d2c2238d2918c2aec9a1bda56cc4424a40a(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__109184c22bfabae10e4a9b60c7d597c20a87973859f63e32cef299a3ac43bb3c(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9262983ef9235ff89fe84a67e2b7217da4e2128324cc1af72877f0ae3f459b0c(
    value: typing.Optional[IJsonAssists],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d9d6087f2ed0c337b4109f90f755e6eb2414005be8ceab97d94db0cc08ccfd1(
    value: typing.Optional[IJsonFormatter],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd91aa4e2dccd85b13872682abff82b5fac37c4be5825024f62f067d17ab3fd7(
    value: typing.Optional[IJsonLinter],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__822d0bffc62744cc1e6d209ee489744b4ea65d4bcb2bdcc867a60f49a937ce0c(
    value: typing.Optional[IJsonParser],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5ad54d8b4c9b8e9424b196d3907875d99a83e20c200c3e6da90d9079e6fcbc5(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f21d8ceab01190d857817a1494a100c90af324295e7db002f7ee2e08347f439f(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77fed4b6575d63d3f2b3989eda2d1edebc8aeb91507a9e1981883335306afb09(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e2e288874d81794d2483df3786708701bada79f0291b62b172acfd90418c763(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7468d3f4b91745bd32dab02c371321f8ad230ac024dd422d8ef1859300bcc32f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a4f6d032a10e6395c3f001e414b1f30bf8a52fc057f861a6764562c1173b2a6(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__336daf3ca9f566aad5d44d70aa6971da9250b7c513ab5b26654fc01e3e7732b7(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30db05d5034aae0f99b8fc2e83d1e104e0e682948c8e6c5b03a25a4b0824c3b7(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19f222cbea6108eb6bd6591ecb757b94ce31971a3fa1a77b04e5dce1c266d34a(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c4b253e21a41817d2640766265c87b869d6e32a444864aca3f92c122d0eb9d7(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1faea36fdc017cb47551a62063d019a0f802e96dc37838d0c992c0723d26330(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b830bb0414fbeb0b7856fb7792c6de4923c780fbb9e5c3f760cb0d952abd936(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef8c98cf32e46f068a4b3aff83ff7320df0a1e39bf192a118963a167b2853a12(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2486cfe6da32919241cb2c842786ae2c068269bee69a8dde8ee06abaf979005d(
    value: typing.Optional[IRules],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f60fa954dd713236cd784e2d5bb21741d8e2e67183ce7afaac2c32ebbd25e23(
    value: typing.Optional[typing.List[IConvention]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e71c6834677231abf8994a8ef48d04d1e7e0f0a6e82a371354d71061ad4085f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d76453d720470ddff58ae455add9ca46393ae55a797e7afdef788488ec22a676(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c632890b09c7cd39ba77acedd53148096b31281bcb7f053afb9358190613c963(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85a2d8b594b08aeaee6b06fb087467a36ddb1c8deb4bebf06340e2d3be3e036c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef5df1e2df3c98c46fa3a814ff30e72ebda42c1b7173e1a7d10dc1bf16a114d9(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0746030c163cf359edc57c32a0fa8b7269e818aa96a6d0d65cded6ff22932f35(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12a7636a9576fc97dd28f5d886f38d9385927c58e72023e927c67a6d6723ac03(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f73109fede6df77b42b6f5e046905e3b20e1e69e7a09b89d768522c0035a8078(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46fda788d4729d29eb2abea2ccc319bc622ad35f3ea0b0f23f2070aede653966(
    value: typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, ICustomRestrictedTypeOptions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2ac78dad41389d348fc26cb25244800e8da3c3d536a8162aa177511e68a855a(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7098fa635a567a594fec7474846a238f047a9756d12d5f4b4d6dd0b0417a1844(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f37453f0f8183b7a8276f4b886a377235895b9c09481faed358c79af2ff385a(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32020291c8dcea7de662caea6819e7bb9e3b6f89b893bb98e16c384e219aae9f(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b39c0b329c18cb4bf215190dc27b940ff24e81561efeb8edd0f597ec97125ee5(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34245abc673c4838fdfc26f89b64a75170c7ad6c3d437020716ed1be4612a5ae(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d3e06bea2364a3f402fe08f631d5a47daad86bdd86747637fa23e25acb4d545(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df06d5644c925d656f70313efdf3b48931f1d55d2e016a62e938f40900b9a3fc(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e7da289b3d8c7b5851e5c9c6971797d40286834bda8e1a91bec22abb888936e(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7456d472f91bac40ef9613085229984599264b655b2567a42cbc8d7dd7df4bde(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3967de35c5355d023b1edc13137303b5c078656e267ce5eea3a6c0077319df16(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__934f4a829cdcb0c67688544d8d862ad521d25adf3950fbd883f923cef6f9044b(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa604ecf974a08994fa44c926ff8bc67bdf2b70f040f07f6d26d0a851040632e(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42475cd54accdc6630da5eb4697b6fbb958aae32df9aa7e7a143ed41909a2101(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c52b0ab3001cfe5791e631039369da4e48155ada55bae3fe21da7c8d52af877(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1103c1ad5c94fca1d5f70145ea8a3da7cc32eead57f32eb1e5a048b37f8e684f(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6412d7053e79e5b50434fa538c23b3c3da7c63a6a1c1d20bffe9765a82a0f78d(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff110a6185afa749e49ea163b27998696e5ad0dfea99befa9cb4751794377480(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bded73f1f632d2d19d35322d45a6fb10f9590f2a0bd62bc9704168fb8977f8ea(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59116a4af7ad3b90f9a82a000f0bf953379ef28d2537ab5b0a2eb3bab598d2ee(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58c575f48a75403a33e9218ffdb1ac788f825cb23d9050b6594a71fae5a2d43f(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__481a30d3bbcc117cc2d1c844180dac93e4d82751e234e3b256af98d7fc5731a3(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithRestrictedImportsOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ef0b0df4ddc23228797b227a57f7ac3bba11c045563c34cb8f2b78ec975243a(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoRestrictedTypesOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__961ba8e58951a1cac0506b3141ea6f9834bd960a68b074b121270bd0641b6a4e(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoSecretsOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0be94a539de03064e9a1208033a90066cfbaf83c24e2381f0947977a902a418(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d39bda1f70a8e792be4de03b9cd66109c49388cb8804390c1643790da01b483(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c92de2ceb1f14aeb6a0ca6f8da7b6d6d2348049376c53ba547b29c8dcbd94f4(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86c7b68bf5392f03bff73f27feb9bf1ce7fd0a547a25cf3db26d11dc2d5a8a98(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5cc191a9daa6aeb85f6bf40bd979f9318d0468480fccd11220aefd184d3006c(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4f0601789b393c153be69bf23c6ecbca886be761d0f3f16a39736f591d5c12d(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a15e73b8bdaf03f491d564596283e70864492068a8c13f99434c8cf59b44010c(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__156ac23d28fb867e567c059336309abcdc68286f119c1de9b40ce965b0d04e74(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4eee81431afaed6621ab8c25aaa0afbd5be659cf1a1afaa79451401563b8fdd(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa2184170f5beff37d56f18d71cc1b9ffc9c5cbab8c7b877ebe6a39f2892b9c2(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ac507894ac00532a80c979788414faf5cbd89752a3ff7f7a39bdfe0a0145731(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aaa4e2db8ee0c12008d8e250cd624336834b466c5bfceb491ad4c09732f3cbc3(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b1bfb3a55f10cdc2fa22c956dacb70efa6b32f61c0be9aa96317e2fcc361c0c(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6977f5a886d92cb62e7437f329f517c893fd7ff0baa10343f268e94eb8f9f1f(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e7ec98c7f6f4aa10baca5ed6aa5f12f280f90b7e2c39c427097310aba76fafc(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithUseComponentExportOnlyModulesOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c396ae3c06a9dff5afa5c33ffe992f342337835316fd61148008e05fe4519a20(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7e2111995e133affc00f03631cb9b94be3fd7e6775a517907e3616369979d56(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithConsistentMemberAccessibilityOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bd88427d788e7b49099535d8d4ed602a406af87bbf9fa7aa4461ba8432cde03(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c66a28c8ec197c510d5f806b02c9efe983d984f905d84bdcb4f6e13db4d23bba(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7eaa8bb80000514571e9c088d5becf9e0a53b04d5f62aaf235df3dfa4ddbe2c0(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddb32845c7bd980b5506883f258b5014258d9bb3df42c6d865f046837547b999(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e91d12531a6749f388b69f3ee3f053cfd77d3b585f429abeae6b037e33d96fce(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b487ab3e4f4adc08bc83f4fe78c1d03e29589bb7b865339510a152edfbbaf6b(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithUtilityClassSortingOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d76e67d15a4e64a75330ae3568f5d8520bf466904a74ad792ec231307f85d4b6(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2114761c0476df25a0d45053dcc35b4243df9992a07a75b85e5aa16efd1ede1(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ff9dffdb4f0c6e94c273e81996aeb6701c7c2fe1a7b63932a36e8bdabdc3285(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithUseValidAutocompleteOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10b6ad2989f780cb82bb42d3ea23de966ccc938259cdb31897d9964095299c13(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91712bd4a8ec79877ef9303b50ee143787ab60bd7884bfa2cb4b9b1eed93f560(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__036cf4c3e56a3243bf787f283f54c7e2c59f99c84e72efa67e7f0e23d1b99c14(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04eeca7a12c488e41b660a8cb82fe79d813642299997d9f805dc0cf29f3c3b13(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__642aafd4b395d7e05a5c3e7c79bd1df448299693279402c4e193688be9b8a92b(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7340712b6b614062e542ff0ac1deed027a3ae431ca0485f7799af53cf07045d7(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4c8c85c2f34be3e3cbd56b256ebe6a1d3f03275cc36b6bd852417fccfdeaf03(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8061a114a765b98260c5a52fa7e9d8748479263d19d2facbb2871f504f64cecf(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14d67b174df07c745a13d0a81cf3840cace2af4465f00302399d7e8d00870bb5(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f3c0fe24ce6182678a6f97e3d42b7b529321cacbe408c72939c51553b422a3b(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bf3497618a755c2a70d8b005775eae4362c50870be318e1e78fd9ba9ab06b01(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cec15ebd39b3a357c306491a3e899f114d9aea1e2e13d8b4b60b2b6b59e89334(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__daee87e9fe1ea32ee7fd208aa012af88c8830d2ec8ca667eda2799833bab11e7(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9e95a948405660f04e19b5d72c598d881386b85ad8e6aeca602434cca539cb9(
    value: typing.Optional[IRules],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51266df200f686d906768266691bd4d85d562e041d5464edc25c04804c4833cc(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36843010c44ef7218c8fcd9581fb5eb1a559b2463b8edc285b4ceabcf4d4c4e6(
    value: typing.Optional[ICssConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e89ab1d4582824af32b5df4b8bd3f4a29ac64e520e10a121bcd3dc4d64ef7cdd(
    value: typing.Optional[IOverrideFormatterConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfb0e146f81a96376a3ced37181741ea2e0474eccb1b17f9f0821ae019e234a4(
    value: typing.Optional[IGraphqlConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab08ae587969cea7a750fa7202b5a86c94687970b90c6f42d713785c663b38f8(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbd5b4e9f0552303b20dcb0265798669c35589dfea0f8d065f6fc9e070f65f96(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d34b80b0bb9c39820993e89d907d443fbcbb21fe606b2d8abab547663550c77(
    value: typing.Optional[IJavascriptConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e04c771c9a2ff9c5a1168d7944c36dd1526283bd29659ed8f5fc7fe94942eb61(
    value: typing.Optional[IJsonConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e88e13a66b299498f5541ce455af19d24e8f29b3c304f7f4839a34a4481bdcb0(
    value: typing.Optional[IOverrideLinterConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a06f7252353ecf327acd9191ae57302434d7adfa87ee8da8562aafd1a80a80ad(
    value: typing.Optional[IOverrideOrganizeImportsConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4bd59642520c4f651d70ba7da6efe2ad3a0f68f51952810d44b71c852aac97e(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32280177979886dfcfde429b04b911b8d2492a79095415e839eee8329a91a716(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3076267c34ffdabca9906f0a50b02633ba7405304c78176c3d834339648e500(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d336c9b7ae2bc694bfe1368b9813f49b810b792ac6aa693af8c43bfd968f27c9(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1e011ebc9322ce0b4f846d9394be364cb6e75a740361057a710c47ffd01952b(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9690228dc0e7bf69f79cea6be9e03dd13498b3fce0a20d99f70e0f28f257fb2b(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24d70c9c0ce784a0cc2b84599cb055eb6a4ed8c9b4a2a10ba829aefdaf56e46c(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__030606b1c93d83c19ab639e68fd81d4067cdd9a7a9d67fddee2af1b488d37119(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31f5428261892778dfa820c9ed3e1a5851c08d40ef7f761d1058fc3fbc4e1861(
    value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c712b17bc92c847121143f78e252dcc4d59b111c314bb029b38549b18b7a246d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62a5ac9161e33195175e4361fa933939e97a7afb92219dc0fff2d14cbc194fca(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ecbb6b3744e4c3c0160e07cdb6db8fd28a86b13e8eb83f92b705e4e4ec5845d(
    value: typing.Optional[IAllowDomainOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d6cb05a8a9baf9f40c655fe27fb187c6675a260225fa5d5afe9792ead0aa8f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b79c5095bec60f7df45bf3726ec346b7b8d2ae43ed1a99f36490827b27ef358(
    value: typing.Optional[IComplexityOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__609221c2d3b885ecc28ff42572fd611905fdcc786d51c22f95854318cf48f853(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__396150b54651de2cec023b3126362e3272eb77bdf7cceb964919d2276cd00531(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27a8be1934146e26c8eb3883e28144d8334ef482f4d237890aad9b6a71f15d07(
    value: typing.Optional[IConsistentArrayTypeOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e937a76d175adaa2a5ae5cfb35018919df30ff49d0f043f3248facf907e2ea2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bc3372d0bf66efb0e1f6c4a7cba2404926b88d59b7e7f2979ae7f0a4a38b4e7(
    value: typing.Optional[IConsistentMemberAccessibilityOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bf816437c9055f086c831bdd67215a76f3519d1e1c1d908316b23b789e45cfc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dde99ac5e14d758decc8b4823e29767c2f925f3118cb9d8c7cb7505dd05260c7(
    value: typing.Optional[IDeprecatedHooksOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6c1404d544b4633c45f389a6ce47dd5c0c67f50202ba9fdc764d3062ffe43c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64e8786caf3e13e3c60a5a696f5e413d390fbcacb66297109ccf7e7e3ed0acba(
    value: typing.Optional[IFilenamingConventionOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7db58781e48ac7d907788085317963354ec7de5a919bce58bc30bc8c27432fd3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b75577940ad46ebbe5282e02f216acdfdfc055f099d729410f20eadf7ec878c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59e6160a3378d4e94ff6a8394b7da2f7f1a34f5233a6bd6abfa36d50a8b40771(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79826f39d94c46a8cc2a2a097bd5edf5b0068e126425c33950b922237e23f7c0(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8f51a099a2d6cf71978e4c5feba8fa641f40cfd35dade3c15842f73eec547a0(
    value: typing.Optional[INamingConventionOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eeab537bd6bcae9ce3d55939eb876589828bc12348b887ba32d0a77497df48c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25adb4cbd3fe9c8868e116de37a76c5d4e8ed4cdc92f3aadd564d4c1549472b5(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38d3d7c8fc3da224b65bf133005feaf1e1758a34d305405b309f3dbc0dc626b9(
    value: typing.Optional[INoConsoleOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4addff9f8b62ae2c19c26158236bdf524520c14f55ca683754b1dd4225ed304a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2923cbaa051184632a80348a744af3f982efdfc7e66f60ac4bdc79ab96c821c9(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78483eb28be3c363cde9bced10e08e67bf5c191eb35992af8263c6566a604b16(
    value: typing.Optional[INoDoubleEqualsOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fe3748201c171b15702fc5e6ca90e0bdd2d5c442951503adeac4aa969225774(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c44591ce06042b398ba71e757b887038f51fc00aab0105dbde6dfcc02bfeb93d(
    value: typing.Optional[INoLabelWithoutControlOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb19b10c6a87dd18f594a7f7621a186e176b41703aea42aba4df2845087afb44(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a81b671ffb73c6511f2b61a6906af16973f67c5d1a7e037a06e88168490980f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8585e2a15ab739d1817844a5f1fe7d4e980ed3f59a8353e46a345cd9f8c2828f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfe087d2695a9a504a48e052f1b1332b1ee0e69007b829f881f8a6f89b1ba7a9(
    value: typing.Optional[INoRestrictedTypesOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab035c665923dabc5d870cdcc7ebb50687c667f73b15eef7ecf08d1d5c041cca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b7c778e3a1b7032c50250010f973ab9870d60472670eef2e5213c9d7a444e12(
    value: typing.Optional[INoSecretsOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__492028b0a9f7954d44a0c7a93858a557e795281dbf23ccc0f6c4bc212c56c340(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1a875f5dddddc886ec58e6e13954ab979ff4b03d2276516911d61d0081a1b92(
    value: typing.Optional[IRestrictedGlobalsOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db76ef0190ac0c1ab658e69e47727ace4a8007bb2bbcd8f382d2f58013c04657(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d805009f791b2436eb6f87f9e2334d37bc5b523a8d4f1123997a47cc056d511(
    value: typing.Optional[IRestrictedImportsOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77eab468ddbb14f6ddad5db8e6cbeb195ffd09fe9db9dc0f05d4b1cedb83d6f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb3b8dd9529a114c6da5fc615fccc34b6c540352f078beabf9aa731fe333d37e(
    value: typing.Optional[IUseComponentExportOnlyModulesOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a155bdfac3ab7ea25a66c7a7d87e787bc513df419a50a51f9514db60b73664a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a90e05ca35603ae645955c66ca9bb731354e06687289bba78a318e8330caaf6d(
    value: typing.Optional[IUseExhaustiveDependenciesOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23432c2b5966f4bc60853a5068ea336a3fa0e98bb08b2981d5a4ad88593602f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a809ce8bc006991524094af9f718f896eb9d2dc6c3b588ea3317213e173fc148(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3576ad5e4b811f6ff0b9db3c5476e61585d6eb248107d534f5e82b74b77d12f(
    value: typing.Optional[IUseImportExtensionsOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fba5a73ee2b82bb6089df92cc87bf8af4db240469a0acd2c5ecd40eb3ff86a64(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e7730b1a62dc09d7aa2cd8b4e50ab6c803b3d40c5e63706a231b83e2cc178c9(
    value: typing.Optional[IUseValidAutocompleteOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__692ccab272ce4d4a7ad37820696fed26a42114bee2f68a9874837df87982c3ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cc259341b4abca3011654bdc1c3d7792db7a951f864ee0235a2e62526bcc85b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a37e07704c6d0315a610f231aabd5bfce457f37b684d1d5b8f2bd20aa3eba55b(
    value: typing.Optional[IUtilityClassSortingOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e038de659dbcaf1ea5c4d091afc76401b9dc2b6fb2afaab98654308cff53fb67(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6ca52ba939b4b20b89e1699f3af4d7668d1a77409e1925b0e1aa501a52a2c3d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45bc209e05b8556c1e51b80d0b9845dda47ef5a45853fc111ac0eea7692aa994(
    value: typing.Optional[IValidAriaRoleOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80353c4af30e7715f57809eb4d005b4c39dfd2e0a5e11ce5906a75b7bbd8ccf0(
    value: typing.Optional[IA11y],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61e10a4821368e9a192337f2248658b408862a9bc36ad69e9504e413a87044a1(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b112b84e3fe60df1001f21c688bd3fbf4222cd16a31c73a814e18350775c2fbe(
    value: typing.Optional[IComplexity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30dbf678299a96e170712804c846f480595e70dcc0011cb108601c12f31dc30c(
    value: typing.Optional[ICorrectness],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__825db897eba98ea78de06620f119ac4960f666b85af371528a5939e7bcde9b35(
    value: typing.Optional[INursery],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cfb14783260626da54cc1797807690431426b6d6da51401beb3d6db00566468(
    value: typing.Optional[IPerformance],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a156acee705f9a8c854e898bbaa1eeccfc5287b118e6e8fe1d3632ade181aa94(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4555486d71e8ce1d7de0dceb557069025e39f54eb51a1e3e42a02db8fe21d075(
    value: typing.Optional[ISecurity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b33ad65ff26071dfadc76fb3baad8aa0266fd04beb3922c06411318e4c200f54(
    value: typing.Optional[IStyle],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8caa2dce8e555bc1ba3b9e08a49d1df4a3ae766eb98a5893b453fcd6e10a4337(
    value: typing.Optional[ISuspicious],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce2727dc0da9f0a66cbe058ab48338081bdc9aa7d1fa1a1e22cc92745d33b5f1(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c145352ddd20e79b619ec3fcc9c15f7024480c9f2d61844927a12c7bd31f912(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26d1cea21722764b8e550d0729b457826f18181d619c48c86845eadf67316a36(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e22b86179adbe2e6f8b0da1e34fbc4715f588f3044769a0d0310261152d58c5b(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a36080a1e16d845ca69852e6cc0d33f80438f17412af945e1774f34f3e65f7c7(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3922a2f94e81ee1336bb83b21dc411010d10354667da3cc487525b3a333dddf6(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0347ec5b843a6bccc1299fc42290b813d8919432853e3a31eed8d2a30abd0aac(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f83e9bc8416ea6f9634f049b01d7d1b06731b7bbe9519cb02d37cb749b1fe3e1(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c12a933c4567044fc53e984bf814ec65558f371c32e3112c36cc922834fe5874(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6b3884c9bdacd77202d9bebae17c5e72dcfd7047d13e90ec76dece72b8f0bdb(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e20996498263b2a0097ffb3adc174ddfc9bf9808535bd957cb196fa067e3fca9(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfe364999f21db62f6c479e8f80ed798a9b8fe7a74d2734a37ba6b0a942be8fa(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a52761f97602124cfb84a805343ce56365a1678352070d438f10c9744065b84e(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64c248bceb321184ec65e3a260161b8d9ee6520910b57cc71371ebdccc011fc6(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff99fa66bacfc7f51da55d7bc0feec60daa24a8ff823e9c116c7b70eb9d0c6d4(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__296f87723d73352e87d7b1768fb98be927ff0fad9eeb137f0a820d1bbd011b4d(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5f88a88e6deaf355e7ef7a14df3e7b282dbf3ce63ccb0b04c3f5acfa4fb8af2(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecf34f6f84c16d8eda1ebbcd515129ce69e6d0c904dc2870fc5ad61715a1cf48(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f97a8c7a81f425f5a0c0136ddda956c3e828ea37c0dcdf76bf63058e2053468(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27bb9824e441dac0113255096b07d822f2b167d4db69d1bbb2fdfafbc39e0775(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6706f0f3dee5550f85c5ac69370360b722776d1d5ef7d872214a137def4fdbd(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f81ed9e0c79dd25892593b3beaece435a5ec3bea91285b058bf0fdb759f8cf5c(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__122e001baf27cbf5173137d3d2c1cfdbd0b41be7648226ab0b621374f948fd3f(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e4de2a576e0d27f0bc3abff92c8699a6a7d8f598740ee47a8b407cb497a9099(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithRestrictedGlobalsOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0243f1b0cfbac7a30163d32d8cdbabfd89ff85006d268d34529fe75c7d4e63e1(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b77a1b745b5257a40c409b1fe5f72157ffa141cd69735413b888e838a6a35cd2(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0d92ea883024cd008fcfc2654baf69a0c76cb2005543c742069448a5c2c2142(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c280a82ffd4d2feccac8d9110d969296fdef9201040e6e4b647e8e5ceae1fc04(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c8a2220a4a7a8a0645a27ed434980373d53349d284cf321e5b1636fa9f711c3(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6427982f4bc3e2e11c5c4b42b20edbebef73241d7d7aac7f2fd3a643c247da58(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ed161de19ce31fffddadcee3dea4761f7209fe81a2431da1e4ddc3b70d53a71(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d533ea92f20364aee15df227dcabbf5817d0cf20a4c9b6a71163725260173830(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34f5fd42307f836fbb1f5afaabe7fa390c1ad96ebe22969ad4ae91b052f60a11(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9125a99e3a1ab46f41b7439df436cd861f2f1af1e27bff679db3fc714d479dbc(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithConsistentArrayTypeOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8c68d2053285485f02d1f5f6b89100d4d2275a8a3038d4d9fc89b117c606410(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59e1f6038f5a4ba208f06b99c5cc243b0f2e3bc17bbe643590cbd2900bf06174(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fc04da9952b3402e2fd3c9bdcb65cda9852dccd07bbe8ecaded54fa23f71280(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db72f35e401183f3c4798b03dd51d9ff4c523146b26d19c042be3129d5347382(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c637b9c9cb973624cbe3b0bbeca1730807aaf343f4cbf934dd17f77cde83c9c9(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1fbf70a1bc083e7da3e6ce9dd3ae94fad5aee55d871fa9cfffd780ab4fbab74(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d2bdd650730772d2916fae1bd2ea9def4b8418c74278d5b6b4422f689ef536f(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e3960f1767120ad81299a77f3d2c6ead5d62868a49816f422394d7222054ec4(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e8571337f79b14acc078a783b7c42a61c69312f1276d92c99cc5fbe261a3c28(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFilenamingConventionOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2beeb28f5c86ba18cefda32825bab5cc2575c977c568d1e4857fcc254c7b24cf(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e287a4f2d8716acf135aabdd3497bc44f78b1bbfd49078de8fc7a8bb568449a4(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fda4a8c85c5e7dbf1b0d9a8200e807adf5073dc4ed90c8894b4480deb3d3f19d(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aed182ce219e955f2fa03258974d263c6de309810a3b1300c72f2992a1052e23(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5da8998a03bed0d1bbc8c145b983848934904101481dec7529725507c080d1a7(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNamingConventionOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9b8f6d1d8f7f74dc61d238c32668b59756232652e9f2b61412b3fc9b5214996(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__257c24a1ee82546beae2d8bad419db162caa974235e3eb7bc213cadc1984f964(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2d3b776d34295a524c2dee881d43e41b7d71696c526b3bdb99b8db6131e1910(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb9b9f9e69e90d6b562fa84ecd7ab5cfffdf4eb87e6fa1cb55f6765b5c5d03aa(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7486d1545594d2cc2e8747a6f862afb2ecd976b2147fd5cd904d078cef1808aa(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eccd29ed4a0c11f8b4d5f5a40f662102c90fe186949ae1918f4091022870d5a8(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5eec4df3d57b98d05d79ebbb3572c5101b8452300a48c146d18e1f0efd6710d7(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45e392f89f510457677ee64436e0206b3559eb24edde5d607d68a7ed45005cae(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5deb3d39cde1e14eddd78523756772ab9f9521232f38eeb1b1e405d8314ca055(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bed0aadbfbeffd6af0216845ca8106990fe7f2992fb9ca3cae1324886de03356(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__781390133f11692b0f0d0dc79e6f328f59cd69652c8c2ca13c994afeed86ef42(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebea9f9b77aa149e7ce200e8c6aa65ced9141464b27e9740231bfb49ab2c0ab1(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48788877c8edf80edba018e3ada4528705a8261636a8249d8fcfed28d8c66947(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97f301bbdc491f9708f003d309912facde43599f0a0dd1aa2e9387364efcaf33(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a2081d8218d2bfe76c905733309c17fd4e5a3f9d53ca849aa0519f6f0129071(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39c7d9df167a7294f7b887a7be492667e0884c003970d58f72433abba003aa18(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4363f6fabd830798a8a7102ae11fb5ebc2a87bf8966fd2866c7936d775ed228(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__302c317574774fe735865fec7e44eb0eecb96374359b35f30cb8da71ad8f1f81(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5222f823bd3a8750366375527a1637b1bc7e738f4833530165dfa5cef0329f8f(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fe999d70bbc00e640a57dc22770975a0f97219a80cdc2be89eab6c813fda7e3(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2590b964f2fa340e6743e488d774fba35d4bbb0cb26bd18dcba582f3b3c91b58(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40f8004928a33efa8cd03abc141ef34da1842ba2b02de29f29b4628226f43823(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e43ee7d309da511b473654a2967ac563fca541794f9a87bd35478c4fce4ca86f(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b758709ce1c54621ac241ea9fa2f5f5b653e50d445f19fb5c0797fa66caabbe6(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a336f9ca2d487e1f9d9e06700a8e84adf005c16543893cee56f6cc74f7f1ac4a(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77a8786500d19d10626d918f6ab2fa8e00f8ca538cb229259a4470de6fbeb648(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4e5c4da3b836c7ab3f1341d64a6f2e60c50001b56abde5a305da39a17ace110(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa3df4916b15171994fbc846a7f50560329ccb5650c7f26c05bdacac63f2f4f5(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoConsoleOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6ee2fbbf4f3983e032543541cd9542607ed5d5bf5dcf7bcc1eaca0a681bd86b(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdf4d58ef35309700873a30e7efe18706fbf2c8afacb7df2c4811c6cf9103b56(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0357710c8c49e36387d980990fc697f16cbdf04eeba57ed83cf25b24388a8075(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c4fcfb19ec9232f8fe267f6bf6031430c6259c26a74fe34147e4c8d159d7bca(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bc526bea434de3946993ee5703886e8ae463c24a4197f3e2d3d9634ed3f4858(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoDoubleEqualsOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a54a714558a0c08ba8309d97719dc89161906453075e27e804b192f407a352a9(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5939445902dd586362a36d191864aa557bdb2cbe4c689e46cac1b1607b61da0e(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46d048ca3a20232e323d59d78e96aab92dddad3f34c02686bce81d6824189c30(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffe45c3cb5d80b716ec024f5b016a792c8669d11bfe405943193f367d6ac8d41(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__379df9001b16caef6363bb96769bc5e1d81ed2db8be126704556f1219820c6ef(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__244b686e2d4df9e7f54de7277be3d3f90d582e074de3a0c6089fed2cb788014c(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c69b2f2d27866a5627f83f68adc3794929cb8eeb774b35bda174c80450c8b647(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2287a2d2145654478f68259efdf31f8751b6845f1904568e7d6c6fa6002655fd(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98c14e2c09d11214f6567c219bbff75e7c57de7b149db5b5b9dfa362feab5405(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78aad3cf4c025915bae59a6ef04fcbc6b5a9dc6bfe98fa9f3c65ecb2ffa0d055(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf1825afad3893260ee135b705b1594c140b318505f3da3eb64d9546cd9ceac5(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a791fc720a75fe5816f2681b70e4c170521f9c38ca696ae209b8e29c62a973a1(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63d3b9d74cba432ca4e4630aaa711b534e8e7c0f42b81af52c22218527537931(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4aad422e85fdeef99a68a972fc1ec2a445f6ae6499205a9e992afb3fb65b4e38(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2b4d68b8d328604172f086f1244fedbe10a3ef38e5c8efd08ddc5885d3d4435(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10a80eda04d6fb514a953e1fac172b1708643924affa19c7b2f983f36010fb80(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8373cd6dfba77030bbd542b5d37eea0f6e0f06a97b9c22c7bd449cf207b66bc(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__373c82121040e97a5e12ee4a4a4486bae459e8e68955d5d553aea764688e2daf(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ca2c6d835c2bef7f98b2283ea43912d40ac77808e12e174cc2830e4dddb2306(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7086586801db68f59555103e08911e255d9e3bb0e81f972ee1b6ffb2f74e0069(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c86387cdf8f4a9908cce84567554c5b2287f1fcc8b1db482494f61495f8757e8(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db73c31ad2349cb23662fa5a8395fa866ac8ed268e050c9fd6a4c7f441dd98c3(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c80e9762de4d67d4714d3ebd391479e3c5b332cbbfbc62ae5ab4ff59bb879c00(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__390bdb163f029f3131e60358e81cd1fd1606ce15ab03681cf16c7067860fab6c(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7e7f05aa14a6761c39850a02cfb8b742cc3f4064d9d9a9a255f6deb834e55a7(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a9175f6c9cf3c37f7c7ab3a82d9ace42a945f9f4e5bb2d8f71cea894822daa0(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f1f3f2f329c64f1158e80c791a80ef6891f96429b58a260c989f6b2b5c48b26(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b21768c32c57bd9f6974f42a7d8a9457b5bc1d0a350952cea47bf20501ded11(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__813f789e4029f7b53446827f8666bdc990d043b01a646043ab213cfdd9a15898(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9646382d00593630240c243f526d7b929a8db09f5ebce659002aa3e8c807673d(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fc204b5cb6d8afeb88e25f4fcf7b30e74e478cbfca414dd26948aea55b21d6f(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__257b6042ef82ec97b471642a7eef60289342ce9b49decd836a2be2ed945bfcee(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__587c59c7c349d08735e029113e62d521c00df957240d900e213d6a7e50dd01af(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2908c344331a8870921fd008febc013546d3be57345bda7ffdc85019bbf348e5(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1eb5c612a0fc7d5e219714dadec76e5aad2c14c0de90f0b4eff4ff8fd1205384(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4679183d8153b092f2f2760e16a8f70926c72a0c1ef3ee7d66323de9bc20792f(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6721fa1d37820ed643359409178a45b84917a764d57aca772cb7c407b2e1b9f3(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3069d7b1c45f2c015f7333aad654175e88d302ea99aea8719ae1677537cf73aa(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__790d733269d842e1552ebc8b0034dc59fb3b54339b39f753752c35cd0ca36d14(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6738bf62cd4b243dbec4c8643c57951b60affb6298b43977d6a24c82c9bb110f(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec6bb0360375a0108804564228ceb834b466b358c94636057819c5c4243ef572(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ae0867cf27fae0c56f386e2a0bca91776d54d797b2197c76d6052dfb2bd89eb(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf2aa795cb549b660e7f09077c186f2f45b43927ad530c76628d77a64d8c4691(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41009e0e4afc663c2c1f9a5bc158f5dc4b002f1adb36a60f00162077768d61ee(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ca8ccd0b2c2b43b4f492fb789c0b36cbc42a829a71f3df74b659e6cf5ebef21(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d0f67f47187b29e6996aa67f26a6c13092927a8a81c50e1fa556b91230da135(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae6bf2854256c678fabffb015d80270759e3ce127014591ba3fed7ac3419f599(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c88e609dd89734c7868062a5a010ecf643947c15aa5595b60ab87f9d68790bbc(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c1809ebf64ae422734ca6925eed05923033d0ef19b8c9d0282b23fc45c4f63b(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__486f1711ad6978247d998381538f66c5a89a8c7c8cdaf22280cc28c611650aaf(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2070abedd3e91787cf5abece8c959cbdc64054b76e47cf6aafb87d87719204c8(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__645d7a2e1e51aea1e53b4c9c112d8d28fa306456c11e0cf7c2ce5b648b172bfa(
    value: typing.Optional[typing.Union[builtins.str, IRuleWithFixNoOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5d4a0dfd450669012b70ec1d82f19518a05b0fa418f93f57b9f3a5e63e2a47c(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c74f8a70b9a4f5311bbb1b000807704dc8fc603cb45a2c55f31c565371502fd3(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f96be7f9a339bc344418d650903d48d72e4ea80b3d17bc15fa0ca81a431724a7(
    value: typing.Optional[typing.List[IHook]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47048ca09711887f0ee5b4dd0a41e803d33255ef69621107a88c12be637e8967(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87c595fd551f9369ee0dd5696bee5701581e71195354fd10f457bd0322d1aa6b(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41efe052f76dd649b2672bf99fe8dc3a68323e1ee08148e003111c8f18a3da65(
    value: typing.Optional[typing.Mapping[builtins.str, ISuggestedExtensionMapping]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c01e51864303044c695ee9f560229441313f0c5ca748e5c3ce19916d2a5b459d(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f216fa513531782c728aa8cbcdfa5de0a81eb1f3add00cfebbf4f1c340264a33(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17d63db9be2f759513f375fffcd8ce75f9828ad6a6dc564c5c3ea2e80ca121b2(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1be15f3f46f1b59e586af0009e155012a2d0d5bc0069f5fbf5686977151ddc98(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02e2dbe0696b1450df7596d1486a9a2357bb9982c559903d1eb3c69c8357b862(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5136e48dca5f067956c5199676ea806e278d22114d15002afc29f1a7589edc42(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__142cbae57818c8e62ebfef860d3d6ea0b9ce3277d377c495d481df8c4d4102ba(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c5805fe3a31492d44837f692ff58b2ed36d79cdff36ee63051964462129cf55(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b790bd02baf0f96befe5a7c0ce55df0e67091fdaffa34020eed99d1a33953d5(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__feba7b5dc57c10bc7f4090454aecd8b6cdfabf9475ff7e39668de4f8cc4cd973(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass
