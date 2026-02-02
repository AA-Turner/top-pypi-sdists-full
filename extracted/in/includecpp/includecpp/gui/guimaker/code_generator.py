"""
CSSL GUI Builder - Code generator.
Converts SceneModel into valid .cssl source code.
"""

from typing import List, Optional

from .models import SceneModel, WidgetModel
from .constants import CsslWidgetType, WIDGET_REGISTRY, PropertyDef


class CsslCodeGenerator:
    """Generate .cssl code from a SceneModel."""

    # Setters that combine multiple properties into one call
    _MULTI_PARAM_SETTERS = {
        "setColor": ["fg_color", "bg_color"],
        "setFont": ["font_family", "font_size", "bold"],
    }

    def generate(self, model: SceneModel) -> str:
        """Generate complete .cssl file content."""
        lines: List[str] = []

        # Includes
        for inc in model.includes:
            lines.append(f'include("{inc}");')
        lines.append("")

        # Class definition
        lines.append(f"class {model.class_name} : extends CsslParent {{")
        lines.append("")

        # Constructor
        lines.append("    constr init() {")
        self._generate_constructor_body(model, lines)
        lines.append("    }")
        lines.append("")

        # Destructor
        lines.append("    ~init() {")
        if model.preserved_destructor_body:
            for dl in model.preserved_destructor_body.splitlines():
                lines.append(f"        {dl.strip()}" if dl.strip() else "")
        else:
            if model.window:
                lines.append(f"        this->{model.window.name}.close();")
        lines.append("    }")

        # Preserved custom methods
        if model.preserved_methods:
            lines.append("")
            for method_block in model.preserved_methods:
                for ml in method_block.splitlines():
                    lines.append(f"    {ml}" if ml.strip() else "")

        lines.append("}")
        lines.append("")

        return "\n".join(lines)

    def _generate_constructor_body(self, model: SceneModel,
                                    lines: List[str]) -> None:
        """Generate all widget instantiations and property setters."""
        if not model.window:
            return

        window = model.window
        indent = "        "

        # Window instantiation
        title = window.get_property("title", "CSSL Application")
        bg = window.get_property("bg_color", "")
        window_args = f'"{title}", {window.width}, {window.height}'
        if bg:
            window_args += f', "{bg}"'
        lines.append(f"{indent}this->{window.name} = new CsslWidget({window_args});")
        lines.append("")

        # Get all non-window widgets ordered by z_order
        widgets = [w for w in model.get_all_widgets_ordered()
                   if w.widget_type != CsslWidgetType.WIDGET]

        for widget in widgets:
            self._generate_widget(model, widget, lines, indent)
            lines.append("")

        # Preserved constructor lines (non-GUI code)
        if model.preserved_constructor_lines:
            lines.append(f"{indent}// --- Preserved Code ---")
            for cl in model.preserved_constructor_lines:
                stripped = cl.strip()
                if stripped:
                    lines.append(f"{indent}{stripped}")
                else:
                    lines.append("")
            lines.append("")

        # Show + mainloop
        lines.append(f"{indent}this->{window.name}.show();")
        lines.append(f"{indent}this->{window.name}.mainloop();")

    def _generate_widget(self, model: SceneModel, widget: WidgetModel,
                          lines: List[str], indent: str) -> None:
        """Generate code for a single widget."""
        type_def = WIDGET_REGISTRY.get(widget.widget_type)
        if not type_def:
            return

        # Build constructor args
        args = self._build_constructor_args(model, widget, type_def)
        type_name = widget.widget_type.value
        lines.append(f"{indent}this->{widget.name} = new {type_name}({args});")

        # Position
        lines.append(f"{indent}this->{widget.name}.setPosition({widget.x}, {widget.y});")

        # Size (only if non-default or non-zero)
        if widget.width > 0 and widget.height > 0:
            lines.append(f"{indent}this->{widget.name}.setSize({widget.width}, {widget.height});")

        # Settable properties (via setters, not constructor args)
        # Handle special complex types first
        for prop_def in type_def.properties:
            if prop_def.prop_type == "toolbar_slots":
                slots = widget.get_property(prop_def.name, [])
                if slots:
                    self._generate_toolbar_slots(widget.name, slots, indent, lines)
                continue
            if prop_def.prop_type == "menu_structure":
                menus = widget.get_property(prop_def.name, [])
                if menus:
                    self._generate_menu_structure(widget.name, menus, indent, lines)
                continue

        # Regular properties with multi-param setter consolidation
        emitted_setters: set[str] = set()
        for prop_def in type_def.properties:
            if prop_def.constructor_index >= 0 or not prop_def.cssl_setter:
                continue
            if prop_def.prop_type in ("toolbar_slots", "menu_structure"):
                continue
            if prop_def.cssl_setter in emitted_setters:
                continue

            if prop_def.cssl_setter in self._MULTI_PARAM_SETTERS:
                param_names = self._MULTI_PARAM_SETTERS[prop_def.cssl_setter]
                values = []
                has_non_default = False
                for pname in param_names:
                    pdef = next((p for p in type_def.properties if p.name == pname), None)
                    val = widget.get_property(pname, pdef.default if pdef else None)
                    if val and val != (pdef.default if pdef else None):
                        has_non_default = True
                    values.append((val, pdef))
                if has_non_default:
                    args = ", ".join(
                        self._format_value(v, pd.prop_type) if v else '""'
                        for v, pd in values
                    )
                    lines.append(
                        f'{indent}this->{widget.name}.{prop_def.cssl_setter}({args});'
                    )
                emitted_setters.add(prop_def.cssl_setter)
            else:
                value = widget.get_property(prop_def.name)
                if value is None or value == prop_def.default:
                    continue
                setter_code = self._format_setter(widget.name, prop_def, value)
                if setter_code:
                    lines.append(f"{indent}{setter_code}")
                emitted_setters.add(prop_def.cssl_setter)

    def _build_constructor_args(self, model: SceneModel, widget: WidgetModel,
                                 type_def) -> str:
        """Build the constructor argument string."""
        args_parts: List[str] = []

        # Parent reference (most widgets take parent as first arg)
        if type_def.parent_is_first_arg and widget.parent_id:
            parent = model.get_widget(widget.parent_id)
            if parent:
                args_parts.append(f"this->{parent.name}")

        # Gather constructor params ordered by index
        constr_props = [p for p in type_def.properties if p.constructor_index >= 0]
        constr_props.sort(key=lambda p: p.constructor_index)

        for prop_def in constr_props:
            value = widget.get_property(prop_def.name, prop_def.default)
            args_parts.append(self._format_value(value, prop_def.prop_type))

        return ", ".join(args_parts)

    def _format_setter(self, widget_name: str, prop_def: PropertyDef,
                        value) -> str:
        """Format a property setter call."""
        formatted = self._format_value(value, prop_def.prop_type)
        return f"this->{widget_name}.{prop_def.cssl_setter}({formatted});"

    @staticmethod
    def _format_value(value, prop_type: str) -> str:
        """Format a value for CSSL code output."""
        if value is None:
            return '""'
        if prop_type == "string":
            return f'"{value}"'
        elif prop_type == "bool":
            return "true" if value else "false"
        elif prop_type in ("int", "float"):
            return str(value)
        elif prop_type == "color":
            return f'"{value}"' if value else '""'
        elif prop_type == "choice":
            return f'"{value}"'
        elif prop_type in ("items", "list"):
            if isinstance(value, list):
                items_str = ", ".join(f'"{v}"' for v in value)
                return f"[{items_str}]"
            return "[]"
        return str(value)

    def _generate_toolbar_slots(self, widget_name: str, slots: list,
                                 indent: str, lines: List[str]) -> None:
        """Generate addSlot() calls for a toolbar widget."""
        for slot in slots:
            if not isinstance(slot, dict):
                continue
            tooltip = slot.get("tooltip", "")
            slot_id = slot.get("id", "")
            parts = []
            if tooltip:
                parts.append(f'tooltip="{tooltip}"')
            parts.append("on_click=null")
            if slot_id:
                parts.append(f'id="{slot_id}"')
            args = ", ".join(parts)
            lines.append(f'{indent}this->{widget_name}.addSlot({args});')

    def _generate_menu_structure(self, widget_name: str, menus: list,
                                  indent: str, lines: List[str]) -> None:
        """Generate addMenu()/addItem()/addSeparator() calls for a menu bar."""
        for menu in menus:
            if not isinstance(menu, dict):
                continue
            label = menu.get("label", "Menu")
            # Use auto to store the menu reference
            var = f"{widget_name}_{label.replace(' ', '')}"
            lines.append(
                f'{indent}this->{var} = this->{widget_name}.addMenu("{label}");'
            )
            for item in menu.get("items", []):
                if not isinstance(item, dict):
                    continue
                if item.get("type") == "separator":
                    lines.append(f'{indent}this->{var}.addSeparator();')
                else:
                    item_label = item.get("label", "")
                    if item_label:
                        lines.append(
                            f'{indent}this->{var}.addItem("{item_label}");'
                        )
