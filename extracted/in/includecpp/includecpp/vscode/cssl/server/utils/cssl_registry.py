"""
CSSL Language Server - Dynamic Runtime Registry.

Introspects the actual CSSL runtime (builtins, types, GUI classes, modules)
to provide autocomplete, hover, and diagnostic data WITHOUT hardcoding.

Any new builtins, types, or methods added to the runtime are automatically
picked up by the language server.
"""

import inspect
import logging
from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional, Any, Tuple

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Data classes for structured info
# ---------------------------------------------------------------------------

@dataclass
class ParamInfo:
    """Single function/method parameter."""
    name: str
    type_hint: str = ""
    default: str = ""
    doc: str = ""


@dataclass
class FunctionInfo:
    """Built-in function metadata."""
    name: str
    params: List[ParamInfo] = field(default_factory=list)
    return_type: str = ""
    doc: str = ""
    signature: str = ""  # e.g. "print(value, sep=' ', end='')"


@dataclass
class MethodInfo:
    """Method on a type or class."""
    name: str
    params: List[ParamInfo] = field(default_factory=list)
    return_type: str = ""
    doc: str = ""
    signature: str = ""


@dataclass
class TypeInfo:
    """Built-in data type metadata."""
    name: str
    generic_syntax: str = ""  # e.g. "<T>", "<K, V>", "<T, size>"
    doc: str = ""
    methods: List[MethodInfo] = field(default_factory=list)
    base_class: str = ""


@dataclass
class ClassInfo:
    """GUI widget class metadata."""
    name: str
    cssl_name: str = ""  # e.g. "CsslButton"
    constructor_params: List[ParamInfo] = field(default_factory=list)
    methods: List[MethodInfo] = field(default_factory=list)
    doc: str = ""


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

class CSSLRegistry:
    """Dynamic registry that introspects the CSSL runtime.

    Singleton - built once on first access via get_registry().
    All data is extracted dynamically from the runtime modules.
    """

    _instance: Optional['CSSLRegistry'] = None

    def __init__(self):
        self.builtin_functions: Dict[str, FunctionInfo] = {}
        self.builtin_types: Dict[str, TypeInfo] = {}
        self.type_methods: Dict[str, List[MethodInfo]] = {}
        self.keywords: Set[str] = set()
        self.modifiers: Set[str] = set()
        self.gui_classes: Dict[str, ClassInfo] = {}
        self.namespaces: Dict[str, List[MethodInfo]] = {}
        self.module_methods: Dict[str, List[MethodInfo]] = {}
        # Flat lookup sets for quick membership tests
        self.all_builtin_names: Set[str] = set()
        self.all_type_names: Set[str] = set()
        self.all_gui_class_names: Set[str] = set()
        self._load_all()

    def _load_all(self) -> None:
        """Load everything from the runtime."""
        self._load_builtins()
        self._load_types()
        self._load_gui_classes()
        self._load_keywords_and_modifiers()
        self._load_modules()
        logger.info(
            f"CSSLRegistry loaded: {len(self.builtin_functions)} builtins, "
            f"{len(self.builtin_types)} types, {len(self.gui_classes)} gui classes, "
            f"{len(self.module_methods)} modules"
        )

    # ------------------------------------------------------------------
    # Builtins
    # ------------------------------------------------------------------

    def _load_builtins(self) -> None:
        """Import CSSLBuiltins and extract all registered functions."""
        try:
            from includecpp.core.cssl.cssl_builtins import CSSLBuiltins
            builtins = CSSLBuiltins(runtime=None)

            for name in builtins.list_functions():
                # Skip GUI class constructors registered as builtins
                if name.startswith('Cssl') or name.startswith('CSSL'):
                    continue

                method = getattr(builtins, f'builtin_{name}', None)
                if method is None:
                    # Some functions may be registered under a different attr name
                    method = builtins._functions.get(name)

                info = FunctionInfo(name=name)
                if method and callable(method):
                    info.params = self._extract_params(method)
                    info.doc = self._extract_doc(method)
                    info.return_type = self._extract_return_type(method)
                    info.signature = self._build_signature(name, info.params)

                self.builtin_functions[name] = info
                self.all_builtin_names.add(name)
        except Exception as e:
            logger.warning(f"Failed to load builtins: {e}")

    # ------------------------------------------------------------------
    # Types
    # ------------------------------------------------------------------

    # Generic syntax for each container type
    _GENERIC_MAP = {
        'stack': '<T>',
        'vector': '<T>',
        'queue': '<T, size>',
        'array': '<T>',
        'list': '<T>',
        'dictionary': '<K, V>',
        'dict': '<K, V>',
        'map': '<K, V>',
        'datastruct': '<T>',
        'dataspace': '<T>',
        'shuffled': '<T>',
        'iterator': '<T>',
        'combo': '<T>',
        'set': '<T>',
        'tuple': '<T>',
        'instance': '<"name">',
    }

    # Map CSSL type name -> Python class name in cssl_types module
    _TYPE_CLASS_MAP = {
        'stack': 'Stack',
        'vector': 'Vector',
        'queue': 'Queue',
        'array': 'Array',
        'dictionary': 'Dictionary',
        'dict': 'Dictionary',
        'map': 'Map',
        'datastruct': 'DataStruct',
        'dataspace': 'DataSpace',
        'shuffled': 'Shuffled',
        'combo': 'Combo',
        'bit': 'Bit',
        'byte': 'Byte',
    }

    # Primitive types that have no class in cssl_types but should still be registered
    _PRIMITIVE_TYPES = {
        'int', 'float', 'string', 'bool', 'void', 'json', 'dynamic', 'auto',
        'long', 'double', 'ptr', 'pointer', 'address', 'openquote',
        'iterator', 'set', 'tuple', 'instance',
    }

    def _load_types(self) -> None:
        """Import type classes from cssl_types and introspect their methods."""
        try:
            import includecpp.core.cssl.cssl_types as types_mod
        except Exception as e:
            logger.warning(f"Failed to import cssl_types: {e}")
            types_mod = None

        # Load class-based types
        for cssl_name, class_name in self._TYPE_CLASS_MAP.items():
            cls = getattr(types_mod, class_name, None) if types_mod else None
            info = TypeInfo(
                name=cssl_name,
                generic_syntax=self._GENERIC_MAP.get(cssl_name, ''),
            )
            if cls:
                info.doc = self._extract_doc(cls)
                info.base_class = cls.__bases__[0].__name__ if cls.__bases__ else ''
                methods = self._extract_class_methods(cls, cssl_name)
                info.methods = methods
                self.type_methods[cssl_name] = methods

            self.builtin_types[cssl_name] = info
            self.all_type_names.add(cssl_name)

        # Register primitive types (no introspectable class)
        for ptype in self._PRIMITIVE_TYPES:
            if ptype not in self.builtin_types:
                self.builtin_types[ptype] = TypeInfo(
                    name=ptype,
                    generic_syntax=self._GENERIC_MAP.get(ptype, ''),
                )
                self.all_type_names.add(ptype)

    def _extract_class_methods(self, cls, type_name: str) -> List[MethodInfo]:
        """Extract public methods from a type class instance."""
        methods: List[MethodInfo] = []
        # Some classes need args to instantiate
        try:
            if type_name == 'queue':
                instance = cls('dynamic', 'dynamic')
            elif type_name in ('bit', 'byte'):
                instance = cls(0)
            else:
                instance = cls('dynamic')
        except Exception:
            try:
                instance = cls()
            except Exception:
                return methods

        seen = set()
        for name in sorted(dir(instance)):
            if name.startswith('_'):
                continue
            attr = getattr(instance, name, None)
            if attr is None or not callable(attr):
                continue
            if name in seen:
                continue
            seen.add(name)

            minfo = MethodInfo(name=name)
            minfo.params = self._extract_params(attr)
            minfo.doc = self._extract_doc(attr)
            minfo.return_type = self._extract_return_type(attr)
            minfo.signature = self._build_signature(name, minfo.params)
            methods.append(minfo)

        return methods

    # ------------------------------------------------------------------
    # GUI Classes
    # ------------------------------------------------------------------

    def _load_gui_classes(self) -> None:
        """Import cssl_gui module and introspect all widget classes."""
        try:
            from includecpp.core.cssl.cssl_gui import CsslGuiModule
            gui = CsslGuiModule()

            # The __getattr__ class_map lists all class mappings
            # We use class attributes directly from the CsslGuiModule class
            for attr_name in dir(gui):
                if attr_name.startswith('_'):
                    continue
                try:
                    attr = getattr(CsslGuiModule, attr_name, None)
                except Exception:
                    continue
                if attr is None or not inspect.isclass(attr):
                    continue

                # Build both short name (Button) and Cssl name (CsslButton)
                cssl_name = attr.__name__  # e.g. "CsslButton"
                short_name = attr_name     # e.g. "Button"

                info = ClassInfo(
                    name=short_name,
                    cssl_name=cssl_name,
                    doc=self._extract_doc(attr),
                )

                # Extract constructor params
                try:
                    init = attr.__init__
                    info.constructor_params = self._extract_params(init)
                except Exception:
                    pass

                # Extract public methods
                seen = set()
                for method_name in sorted(dir(attr)):
                    if method_name.startswith('_'):
                        continue
                    method = getattr(attr, method_name, None)
                    if method is None:
                        continue
                    if not (callable(method) or isinstance(method, property)):
                        continue
                    if method_name in seen:
                        continue
                    seen.add(method_name)

                    minfo = MethodInfo(name=method_name)
                    if callable(method) and not isinstance(method, property):
                        minfo.params = self._extract_params(method)
                        minfo.doc = self._extract_doc(method)
                        minfo.return_type = self._extract_return_type(method)
                    elif isinstance(method, property) and method.fget:
                        minfo.doc = self._extract_doc(method.fget)
                    minfo.signature = self._build_signature(method_name, minfo.params)
                    info.methods.append(minfo)

                # Register under both names
                self.gui_classes[cssl_name] = info
                if short_name != cssl_name:
                    self.gui_classes[short_name] = info
                self.all_gui_class_names.add(cssl_name)
                self.all_gui_class_names.add(short_name)

                # Also register methods for type_methods lookup (for . completion)
                self.type_methods[cssl_name] = info.methods
                if short_name != cssl_name:
                    self.type_methods[short_name] = info.methods

        except Exception as e:
            logger.warning(f"Failed to load GUI classes: {e}")

    # ------------------------------------------------------------------
    # Keywords & Modifiers
    # ------------------------------------------------------------------

    def _load_keywords_and_modifiers(self) -> None:
        """Extract keywords and modifiers from semantic_analyzer constants."""
        try:
            from includecpp.vscode.cssl.server.analysis.semantic_analyzer import (
                CSSL_KEYWORDS, CSSL_MODIFIERS
            )
            self.keywords = set(CSSL_KEYWORDS)
            self.modifiers = set(CSSL_MODIFIERS)
        except Exception as e:
            logger.warning(f"Failed to load keywords/modifiers: {e}")
            # Fallback minimal set
            self.keywords = {
                'if', 'else', 'elif', 'while', 'for', 'foreach', 'in', 'range',
                'switch', 'case', 'default', 'break', 'continue', 'return',
                'try', 'catch', 'finally', 'throw', 'class', 'struct', 'enum',
                'interface', 'namespace', 'define', 'void', 'constr', 'new',
                'this', 'super', 'extends', 'include', 'true', 'false', 'null',
            }
            self.modifiers = {
                'private', 'public', 'protected', 'static', 'const', 'final',
                'abstract', 'readonly', 'virtual', 'global',
            }

    # ------------------------------------------------------------------
    # @Modules (Time, Math, etc.)
    # ------------------------------------------------------------------

    def _load_modules(self) -> None:
        """Import CSSLModuleRegistry and extract all module methods."""
        try:
            from includecpp.core.cssl.cssl_modules import CSSLModuleRegistry
            registry = CSSLModuleRegistry()

            for mod_name in registry.list_modules():
                module = registry.get_module(mod_name)
                if module is None:
                    continue

                methods: List[MethodInfo] = []
                for method_name in module.list_methods():
                    method = module.get_method(method_name)
                    minfo = MethodInfo(name=method_name)
                    if method and callable(method):
                        minfo.params = self._extract_params(method)
                        minfo.doc = self._extract_doc(method)
                        minfo.return_type = self._extract_return_type(method)
                        minfo.signature = self._build_signature(method_name, minfo.params)
                    methods.append(minfo)

                self.module_methods[mod_name] = methods
                # Also populate namespaces for :: completion
                self.namespaces[mod_name.lower()] = methods

        except Exception as e:
            logger.warning(f"Failed to load modules: {e}")

    # ------------------------------------------------------------------
    # Introspection helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _extract_params(func) -> List[ParamInfo]:
        """Extract parameter info from a callable using inspect."""
        params: List[ParamInfo] = []
        try:
            sig = inspect.signature(func)
            for pname, param in sig.parameters.items():
                if pname == 'self':
                    continue
                p = ParamInfo(name=pname)
                if param.annotation != inspect.Parameter.empty:
                    p.type_hint = getattr(param.annotation, '__name__',
                                          str(param.annotation))
                if param.default != inspect.Parameter.empty:
                    p.default = repr(param.default)
                params.append(p)
        except (ValueError, TypeError):
            pass
        return params

    @staticmethod
    def _extract_doc(obj) -> str:
        """Extract first paragraph of docstring."""
        doc = getattr(obj, '__doc__', None)
        if not doc:
            return ''
        # Take first meaningful paragraph
        lines = doc.strip().split('\n')
        result = []
        for line in lines:
            stripped = line.strip()
            if not stripped and result:
                break
            if stripped:
                result.append(stripped)
        return ' '.join(result)

    @staticmethod
    def _extract_return_type(func) -> str:
        """Extract return type annotation if available."""
        try:
            sig = inspect.signature(func)
            if sig.return_annotation != inspect.Signature.empty:
                ann = sig.return_annotation
                return getattr(ann, '__name__', str(ann))
        except (ValueError, TypeError):
            pass
        return ''

    @staticmethod
    def _build_signature(name: str, params: List[ParamInfo]) -> str:
        """Build a human-readable signature string."""
        parts = []
        for p in params:
            s = p.name
            if p.type_hint:
                s = f"{p.type_hint} {s}"
            if p.default:
                s += f"={p.default}"
            parts.append(s)
        return f"{name}({', '.join(parts)})"

    # ------------------------------------------------------------------
    # Public lookup API
    # ------------------------------------------------------------------

    def get_function_info(self, name: str) -> Optional[FunctionInfo]:
        """Get info for a builtin function by name."""
        return self.builtin_functions.get(name)

    def get_type_info(self, name: str) -> Optional[TypeInfo]:
        """Get info for a builtin type by name."""
        return self.builtin_types.get(name.lower())

    def get_type_methods_list(self, type_name: str) -> List[MethodInfo]:
        """Get methods available on a type (builtin container or GUI class)."""
        # Try exact match first, then lowercase
        methods = self.type_methods.get(type_name)
        if methods is None:
            methods = self.type_methods.get(type_name.lower())
        return methods or []

    def get_gui_class_info(self, class_name: str) -> Optional[ClassInfo]:
        """Get info for a GUI widget class."""
        return self.gui_classes.get(class_name)

    def get_namespace_methods(self, namespace: str) -> List[MethodInfo]:
        """Get methods for a namespace (:: access)."""
        methods = self.namespaces.get(namespace)
        if methods is None:
            methods = self.namespaces.get(namespace.lower())
        return methods or []

    def get_module_methods(self, module_name: str) -> List[MethodInfo]:
        """Get methods for an @Module."""
        return self.module_methods.get(module_name, [])

    def is_known_name(self, name: str) -> bool:
        """Check if a name is any known builtin, type, keyword, modifier, or GUI class."""
        return (name in self.all_builtin_names
                or name in self.all_type_names
                or name in self.keywords
                or name in self.modifiers
                or name in self.all_gui_class_names)

    def get_all_known_names(self) -> Set[str]:
        """Get the union of all known names for diagnostic checks."""
        return (self.all_builtin_names | self.all_type_names
                | self.keywords | self.modifiers | self.all_gui_class_names)


# ---------------------------------------------------------------------------
# Singleton accessor
# ---------------------------------------------------------------------------

def get_registry() -> CSSLRegistry:
    """Get the singleton CSSLRegistry instance."""
    if CSSLRegistry._instance is None:
        try:
            CSSLRegistry._instance = CSSLRegistry()
        except Exception as e:
            logger.error(f"Failed to create CSSLRegistry: {e}")
            # Return an empty registry so the server doesn't crash
            CSSLRegistry._instance = CSSLRegistry.__new__(CSSLRegistry)
            CSSLRegistry._instance.builtin_functions = {}
            CSSLRegistry._instance.builtin_types = {}
            CSSLRegistry._instance.type_methods = {}
            CSSLRegistry._instance.keywords = set()
            CSSLRegistry._instance.modifiers = set()
            CSSLRegistry._instance.gui_classes = {}
            CSSLRegistry._instance.namespaces = {}
            CSSLRegistry._instance.module_methods = {}
            CSSLRegistry._instance.all_builtin_names = set()
            CSSLRegistry._instance.all_type_names = set()
            CSSLRegistry._instance.all_gui_class_names = set()
    return CSSLRegistry._instance
