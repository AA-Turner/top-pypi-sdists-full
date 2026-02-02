"""
CSSL GUI Builder - Code parser.
Parses .cssl source code into a SceneModel using regex (no CSSL runtime dependency).
Preserves non-GUI code (event handlers, custom methods, non-widget constructor lines).
"""

import re
from typing import List, Optional, Tuple, Dict, Any

from .models import SceneModel, WidgetModel
from .constants import CsslWidgetType, WIDGET_REGISTRY, cssl_type_from_string


class CsslCodeParser:
    """Parse .cssl source code into a SceneModel."""

    # Regex patterns
    _RE_INCLUDE = re.compile(r'include\("([^"]+)"\);')
    _RE_CLASS = re.compile(
        r'class\s+(\w+)\s*:\s*extends\s+(\w+)\s*\{'
    )
    _RE_CONSTR = re.compile(r'constr\s+init\s*\(\)\s*\{')
    _RE_DESTR = re.compile(r'~init\s*\(\)\s*\{')
    _RE_METHOD = re.compile(r'define\s+(\w+)\s*\([^)]*\)\s*\{')

    # Widget instantiation: this->Name = new CsslType(args);
    _RE_WIDGET_NEW = re.compile(
        r'this->(\w+)\s*=\s*new\s+(Cssl\w+)\(([^)]*)\);'
    )
    # setPosition(x, y)
    _RE_SET_POSITION = re.compile(
        r'this->(\w+)\.setPosition\(\s*(\d+)\s*,\s*(\d+)\s*\);'
    )
    # setSize(w, h)
    _RE_SET_SIZE = re.compile(
        r'this->(\w+)\.setSize\(\s*(\d+)\s*,\s*(\d+)\s*\);'
    )
    # Generic setter: this->Name.setFoo(value);
    _RE_SETTER = re.compile(
        r'this->(\w+)\.(\w+)\(([^)]*)\);'
    )
    # show() / mainloop() - these are not widget properties
    _RE_LIFECYCLE = re.compile(
        r'this->(\w+)\.(show|mainloop|close)\(\);'
    )
    # Toolbar: this->Name.addSlot(tooltip="...", on_click=..., id="...");
    _RE_ADD_SLOT = re.compile(
        r'this->(\w+)\.addSlot\(([^)]*)\);'
    )
    # Menu bar: this->Var = this->MenuBar.addMenu("label");
    _RE_ADD_MENU = re.compile(
        r'this->(\w+)\s*=\s*this->(\w+)\.addMenu\("([^"]*)"\);'
    )
    # Menu item: this->Var.addItem("label");  or  this->Var.addItem("label", ...);
    _RE_ADD_ITEM = re.compile(
        r'this->(\w+)\.addItem\("([^"]*)"(?:,\s*[^)]*)?\);'
    )
    # Menu separator: this->Var.addSeparator();
    _RE_ADD_SEPARATOR = re.compile(
        r'this->(\w+)\.addSeparator\(\);'
    )

    # Multi-param setters: maps setter name -> list of property names
    _MULTI_PARAM_SETTERS = {
        "setColor": ["fg_color", "bg_color"],
        "setFont": ["font_family", "font_size", "bold"],
    }

    def parse(self, code: str, model: SceneModel) -> None:
        """Parse CSSL code and populate the SceneModel."""
        lines = code.splitlines()

        # Extract includes
        for line in lines:
            m = self._RE_INCLUDE.search(line)
            if m:
                inc = m.group(1)
                if inc not in model.includes:
                    model.includes.append(inc)

        # Extract class name
        for line in lines:
            m = self._RE_CLASS.search(line)
            if m:
                model.class_name = m.group(1)
                break

        # Find constructor, destructor, and method boundaries
        constr_start, constr_end = self._find_block(lines, self._RE_CONSTR)
        destr_start, destr_end = self._find_block(lines, self._RE_DESTR)
        methods = self._find_methods(lines)

        # Parse constructor body
        if constr_start >= 0 and constr_end >= 0:
            constr_lines = lines[constr_start + 1: constr_end]
            self._parse_constructor(constr_lines, model)

        # Parse destructor body
        if destr_start >= 0 and destr_end >= 0:
            destr_lines = lines[destr_start + 1: destr_end]
            body = "\n".join(l.strip() for l in destr_lines if l.strip())
            model.preserved_destructor_body = body

        # Preserve custom methods
        for method_name, start, end in methods:
            method_lines = lines[start: end + 1]
            model.preserved_methods.append("\n".join(method_lines))

    def _parse_constructor(self, constr_lines: List[str],
                            model: SceneModel) -> None:
        """Parse constructor lines to extract widgets and their properties."""
        # Track widgets by name for property assignment
        widget_names: Dict[str, WidgetModel] = {}
        # Track menu variable names -> (menubar_widget_name, menu_label)
        menu_vars: Dict[str, Tuple[str, str]] = {}
        preserved_lines: List[str] = []

        # First pass: find all widget instantiations
        for line in constr_lines:
            stripped = line.strip()
            if not stripped or stripped.startswith("//"):
                continue

            m = self._RE_WIDGET_NEW.search(stripped)
            if m:
                name, type_str, args_str = m.group(1), m.group(2), m.group(3)
                widget_type = cssl_type_from_string(type_str)
                if widget_type is None:
                    preserved_lines.append(stripped)
                    continue

                widget = WidgetModel(
                    name=name,
                    widget_type=widget_type,
                    z_order=model.get_next_z_order(),
                )

                # Parse constructor args
                self._parse_constructor_args(widget, args_str, widget_names, model)

                widget_names[name] = widget
                model.add_widget(widget)
                continue

            # setPosition
            m = self._RE_SET_POSITION.search(stripped)
            if m:
                wname, x, y = m.group(1), int(m.group(2)), int(m.group(3))
                if wname in widget_names:
                    widget_names[wname].x = x
                    widget_names[wname].y = y
                continue

            # setSize
            m = self._RE_SET_SIZE.search(stripped)
            if m:
                wname, w, h = m.group(1), int(m.group(2)), int(m.group(3))
                if wname in widget_names:
                    widget_names[wname].width = w
                    widget_names[wname].height = h
                continue

            # Lifecycle calls (show, mainloop, close) - skip
            m = self._RE_LIFECYCLE.search(stripped)
            if m:
                continue

            # Toolbar addSlot() calls
            m = self._RE_ADD_SLOT.search(stripped)
            if m:
                wname, slot_args = m.group(1), m.group(2)
                if wname in widget_names:
                    slot = self._parse_slot_args(slot_args)
                    slots = widget_names[wname].get_property("slots", [])
                    if not isinstance(slots, list):
                        slots = []
                    slots.append(slot)
                    widget_names[wname].properties["slots"] = slots
                    continue

            # Menu bar addMenu() calls: this->Var = this->MenuBar.addMenu("label");
            m = self._RE_ADD_MENU.search(stripped)
            if m:
                var_name, menubar_name, label = m.group(1), m.group(2), m.group(3)
                if menubar_name in widget_names:
                    # Track this menu variable for subsequent addItem/addSeparator
                    menu_vars[var_name] = (menubar_name, label)
                    # Ensure menus list exists on the menubar widget
                    menus = widget_names[menubar_name].get_property("menus", [])
                    if not isinstance(menus, list):
                        menus = []
                    menus.append({"label": label, "items": []})
                    widget_names[menubar_name].properties["menus"] = menus
                    continue

            # Menu addItem() calls
            m = self._RE_ADD_ITEM.search(stripped)
            if m:
                var_name, item_label = m.group(1), m.group(2)
                if var_name in menu_vars:
                    menubar_name, menu_label = menu_vars[var_name]
                    if menubar_name in widget_names:
                        menus = widget_names[menubar_name].get_property("menus", [])
                        for menu in menus:
                            if menu.get("label") == menu_label:
                                menu["items"].append({"type": "item", "label": item_label})
                                break
                        widget_names[menubar_name].properties["menus"] = menus
                    continue

            # Menu addSeparator() calls
            m = self._RE_ADD_SEPARATOR.search(stripped)
            if m:
                var_name = m.group(1)
                if var_name in menu_vars:
                    menubar_name, menu_label = menu_vars[var_name]
                    if menubar_name in widget_names:
                        menus = widget_names[menubar_name].get_property("menus", [])
                        for menu in menus:
                            if menu.get("label") == menu_label:
                                menu["items"].append({"type": "separator"})
                                break
                        widget_names[menubar_name].properties["menus"] = menus
                    continue

            # onSelect() and similar event binders - skip
            m = self._RE_SETTER.search(stripped)
            if m:
                wname, method, args = m.group(1), m.group(2), m.group(3)
                if wname in widget_names:
                    self._apply_setter(widget_names[wname], method, args)
                    continue

            # Non-GUI code - preserve it
            if stripped and not stripped.startswith("//"):
                preserved_lines.append(stripped)

        model.preserved_constructor_lines = preserved_lines

    def _parse_constructor_args(self, widget: WidgetModel, args_str: str,
                                 known_widgets: Dict[str, WidgetModel],
                                 model: SceneModel) -> None:
        """Parse constructor arguments and set widget properties."""
        args = self._split_args(args_str)
        if not args:
            return

        type_def = WIDGET_REGISTRY.get(widget.widget_type)
        if not type_def:
            return

        # Handle CsslWidget (window) separately
        if widget.widget_type == CsslWidgetType.WIDGET:
            # CsslWidget("title", width, height[, bg_color])
            if len(args) >= 1:
                widget.properties["title"] = self._unquote(args[0])
            if len(args) >= 2:
                widget.width = self._to_int(args[1], 800)
            if len(args) >= 3:
                widget.height = self._to_int(args[2], 600)
            if len(args) >= 4:
                widget.properties["bg_color"] = self._unquote(args[3])
            return

        # For other widgets: first arg is usually parent reference
        arg_idx = 0
        if type_def.parent_is_first_arg and args:
            parent_ref = args[0].strip()
            # Match "this->ParentName"
            pm = re.match(r'this->(\w+)', parent_ref)
            if pm:
                parent_name = pm.group(1)
                if parent_name in known_widgets:
                    widget.parent_id = known_widgets[parent_name].id
                elif model.window and model.window.name == parent_name:
                    widget.parent_id = model.window.id
            arg_idx = 1

        # Map remaining args to constructor params
        constr_props = [p for p in type_def.properties if p.constructor_index >= 0]
        constr_props.sort(key=lambda p: p.constructor_index)

        for prop_def in constr_props:
            if arg_idx >= len(args):
                break
            raw_value = args[arg_idx].strip()
            value = self._parse_value(raw_value, prop_def.prop_type)
            widget.properties[prop_def.name] = value
            arg_idx += 1

    def _apply_setter(self, widget: WidgetModel, method: str, args_str: str) -> None:
        """Apply a setter method call to a widget's properties."""
        type_def = WIDGET_REGISTRY.get(widget.widget_type)
        if not type_def:
            return

        # Check for multi-param setters first (e.g. setColor(fg, bg), setFont(family, size, bold))
        if method in self._MULTI_PARAM_SETTERS:
            param_names = self._MULTI_PARAM_SETTERS[method]
            args = self._split_args(args_str)
            for i, pname in enumerate(param_names):
                if i >= len(args):
                    break
                pdef = next((p for p in type_def.properties if p.name == pname), None)
                if pdef:
                    value = self._parse_value(args[i].strip(), pdef.prop_type)
                    widget.properties[pname] = value
            return

        # Single-param setters
        for prop_def in type_def.properties:
            if prop_def.cssl_setter == method:
                value = self._parse_value(args_str.strip(), prop_def.prop_type)
                widget.properties[prop_def.name] = value
                return

    def _parse_slot_args(self, args_str: str) -> Dict[str, str]:
        """Parse addSlot() keyword arguments like tooltip="...", id="..."."""
        slot: Dict[str, str] = {}
        # Split on commas, then parse key=value pairs
        parts = self._split_args(args_str)
        for part in parts:
            part = part.strip()
            eq_idx = part.find("=")
            if eq_idx < 0:
                continue
            key = part[:eq_idx].strip()
            val = part[eq_idx + 1:].strip()
            if key == "tooltip":
                slot["tooltip"] = self._unquote(val)
            elif key == "id":
                slot["id"] = self._unquote(val)
            # on_click is skipped (not editable in GUI builder)
        return slot

    def _find_block(self, lines: List[str],
                     pattern: re.Pattern) -> Tuple[int, int]:
        """Find a brace-delimited block starting with the given pattern."""
        for i, line in enumerate(lines):
            if pattern.search(line):
                depth = 0
                for j in range(i, len(lines)):
                    depth += lines[j].count("{") - lines[j].count("}")
                    if depth <= 0 and j > i:
                        return i, j
                return i, len(lines) - 1
        return -1, -1

    def _find_methods(self, lines: List[str]) -> List[Tuple[str, int, int]]:
        """Find all 'define methodName() { ... }' blocks."""
        methods = []
        i = 0
        while i < len(lines):
            m = self._RE_METHOD.search(lines[i])
            if m:
                name = m.group(1)
                depth = 0
                start = i
                for j in range(i, len(lines)):
                    depth += lines[j].count("{") - lines[j].count("}")
                    if depth <= 0 and j > i:
                        methods.append((name, start, j))
                        i = j + 1
                        break
                else:
                    methods.append((name, start, len(lines) - 1))
                    break
            else:
                i += 1
        return methods

    @staticmethod
    def _split_args(args_str: str) -> List[str]:
        """Split comma-separated arguments, respecting quotes and brackets."""
        args = []
        current = ""
        depth = 0
        in_string = False
        escape_next = False

        for ch in args_str:
            if escape_next:
                current += ch
                escape_next = False
                continue
            if ch == "\\":
                current += ch
                escape_next = True
                continue
            if ch == '"' and not escape_next:
                in_string = not in_string
                current += ch
                continue
            if in_string:
                current += ch
                continue
            if ch in ("(", "[", "{"):
                depth += 1
                current += ch
            elif ch in (")", "]", "}"):
                depth -= 1
                current += ch
            elif ch == "," and depth == 0:
                args.append(current.strip())
                current = ""
            else:
                current += ch

        if current.strip():
            args.append(current.strip())
        return args

    @staticmethod
    def _unquote(s: str) -> str:
        """Remove surrounding quotes from a string."""
        s = s.strip()
        if (s.startswith('"') and s.endswith('"')) or \
           (s.startswith("'") and s.endswith("'")):
            return s[1:-1]
        return s

    @staticmethod
    def _to_int(s: str, default: int = 0) -> int:
        try:
            return int(s.strip())
        except (ValueError, TypeError):
            return default

    def _parse_value(self, raw: str, prop_type: str) -> Any:
        """Parse a raw string value to the appropriate Python type."""
        raw = raw.strip()
        if prop_type == "string" or prop_type == "color" or prop_type == "choice":
            return self._unquote(raw)
        elif prop_type == "int":
            return self._to_int(raw, 0)
        elif prop_type == "float":
            try:
                return float(raw)
            except (ValueError, TypeError):
                return 0.0
        elif prop_type == "bool":
            return raw.lower() in ("true", "1", "yes")
        elif prop_type in ("items", "list"):
            return self._parse_list(raw)
        return raw

    def _parse_list(self, raw: str) -> List[str]:
        """Parse a CSSL list literal like ["a", "b", "c"]."""
        raw = raw.strip()
        if raw.startswith("[") and raw.endswith("]"):
            raw = raw[1:-1]
        if not raw:
            return []
        items = self._split_args(raw)
        return [self._unquote(item) for item in items]
