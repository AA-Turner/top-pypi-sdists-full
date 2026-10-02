"""Guard the neutral binding surface from platform mechanics."""

import ast
import pathlib
import re

PKG = pathlib.Path(__file__).resolve().parents[1] / "testmu_appium"

PLATFORM_MODULES = {
    "_config.py",
    "_session.py",
    "_test_config.py",
    "perception.py",
    "_helpers/_keys.py",
    "_helpers/_mjpeg.py",
    "_helpers/_screen.py",
    "_helpers/_strategy.py",
    "_helpers/tabs.py",
    "_helpers/_tree.py",
    "_helpers/_tree_ios.py",
    "_helpers/_web.py",
    "_helpers/_web_remote.py",
    "_helpers/clipboard.py",
    "_helpers/device_control.py",
    "_helpers/foreground.py",
    "_helpers/geolocation.py",
    "_helpers/gesture.py",
    "_helpers/navigate.py",
    "_helpers/picker.py",
    "_helpers/vision_coordinates.py",
}

_MECHANIC_STRING = re.compile(
    r"mobile:\s*\w+|appium:[A-Za-z]|android\.(?:widget|view)|android:id/|"
    r"UiAutomator|UiSelector|XCUIElement|XCUITest",
    re.IGNORECASE,
)
_MECHANIC_SYMBOL = re.compile(
    r"UiAutomator|UiSelector|ANDROID_|XCUIElement|XCUITest|press_keycode|^adb$",
    re.IGNORECASE,
)
_PLATFORM_LITERALS = {"android", "ios", "android_native", "ios_native"}


def _is_docstring(node: ast.Constant, parents: dict) -> bool:
    parent = parents.get(node)
    return isinstance(parent, ast.Expr) and parent.value is node


def _is_platform_source(node) -> bool:
    if isinstance(node, ast.Name):
        return "platform" in node.id.lower()
    if isinstance(node, ast.Attribute):
        return "platform" in node.attr.lower()
    if isinstance(node, ast.Call):
        return _is_platform_source(node.func)
    if isinstance(node, ast.Subscript):
        return (
            isinstance(node.slice, ast.Constant)
            and node.slice.value == "platform"
        )
    return False


def _is_platform_literal(node) -> bool:
    return isinstance(node, ast.Constant) and str(node.value).lower() in _PLATFORM_LITERALS


def _hits(source: str):
    tree = ast.parse(source)
    parents = {child: node for node in ast.walk(tree) for child in ast.iter_child_nodes(node)}
    found = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Compare) and (
            (_is_platform_source(node.left)
             and any(_is_platform_literal(part) for part in node.comparators))
            or (_is_platform_literal(node.left)
                and any(_is_platform_source(part) for part in node.comparators))
        ):
            found.append((node.lineno, "platform comparison"))
        elif isinstance(node, ast.Constant) and isinstance(node.value, str):
            if _is_docstring(node, parents):
                continue
            if node.value.lower() in _PLATFORM_LITERALS:
                found.append((node.lineno, f"platform literal {node.value!r}"))
            elif _MECHANIC_STRING.search(node.value):
                found.append((node.lineno, "platform mechanic string"))
        elif isinstance(node, (ast.Name, ast.Attribute)):
            name = node.id if isinstance(node, ast.Name) else node.attr
            if _MECHANIC_SYMBOL.search(name):
                found.append((node.lineno, f"platform mechanic {name}"))
    return found


def test_platform_mechanics_live_only_in_declared_modules():
    on_disk = {
        path.relative_to(PKG).as_posix()
        for path in PKG.rglob("*.py")
    }
    assert PLATFORM_MODULES <= on_disk
    offenders = {}
    for relative in sorted(on_disk - PLATFORM_MODULES):
        hits = _hits((PKG / relative).read_text())
        if hits:
            offenders[relative] = hits
    assert offenders == {}


def test_the_guard_catches_the_action_leaks_it_was_built_for():
    source = """
def bad(driver, platform):
    if platform == "android":
        driver.execute_script("mobile: type", {"text": "x"})
        driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, "new UiSelector()")
"""
    assert len(_hits(source)) >= 4


def test_the_guard_does_not_match_an_unrelated_symbol_suffix():
    assert _hits("value = _config.SOURCE_APPIUM\n") == []
