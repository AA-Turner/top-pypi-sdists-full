"""
Direct Playwright action implementation from Orby subtask agent.
"""

import re
from typing import Any, Dict, List, Optional, Tuple, Literal
from playwright.async_api import Page


def _get_action_functions():
    return [
        click,
        hover,
        drag_and_release,
        scroll,
        type,
        key_press,
        wait,
        complete,
    ]


def get_action_hints() -> str:
    """
    Get formatted action hints from action function docstrings.

    Returns:
        String containing all available actions and their descriptions.
    """
    hints = []

    for func in _get_action_functions():
        if func and func.__doc__:
            # Extract the full docstring which includes signature
            doc_lines = func.__doc__.strip().split("\n")
            for line in doc_lines:
                line_stripped = line.strip()
                if line_stripped:
                    # First line is the signature, don't indent it
                    if doc_lines.index(line) == 0:
                        hints.append(line_stripped)
                    else:
                        hints.append("    " + line_stripped)
            hints.append("")

    return "\n".join(hints).strip()


async def execute_action(
    page: Page, action_string: str
) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    Parse and execute an action string.

    Args:
        page: The Playwright page to execute actions on.
        action_string: The action string to execute.

    Returns:
        Tuple of (is_complete, result_data)
        - is_complete: True if task is complete
        - result_data: Optional dictionary with execution results
    """

    # Create a mapping from function names to functions
    action_map = {func.__name__: func for func in _get_action_functions()}

    # Handle multi-line actions
    actions = action_string.split("\n")

    for single_action in actions:
        single_action = single_action.strip()
        if not single_action:
            continue

        # Parse the action
        action_name, params = _parse_action_string(single_action)

        # Get the action function from the map
        action_func = action_map.get(action_name)
        if action_func:
            # Execute the action function with page as first parameter
            is_complete, result = await action_func(page, **params)
            if is_complete:
                return True, result
        else:
            print(f"Unknown action: {single_action}")

    return False, None


def _parse_action_string(action: str) -> Tuple[str, Dict[str, Any]]:
    """
    Parse an action string to extract action name and parameters.

    Args:
        action: Action string in format "action_name(param1, param2, ...)"

    Returns:
        Tuple of (action_name, parameters_dict)
    """
    # Extract action name and parameters
    match = re.match(r"(\w+)\((.*)\)", action, re.DOTALL)
    if not match:
        return "unknown", {}

    action_name = match.group(1)
    params_str = match.group(2).strip()

    if not params_str:
        return action_name, {}

    # Parse parameters using regex - no eval for security
    params = {}

    if action_name == "click":
        # Parse click(x, y, button="left", double=False)
        parts = re.split(r",\s*(?![^()]*\))", params_str)
        if len(parts) >= 2:
            params["x"] = float(parts[0].strip())
            params["y"] = float(parts[1].strip())
            # Parse optional parameters
            for part in parts[2:]:
                if "button=" in part:
                    match = re.search(r'button=["\']?(left|right)["\']?', part)
                    if match:
                        params["button"] = match.group(1)
                elif "double=" in part:
                    params["double"] = "True" in part or "true" in part

    elif action_name == "hover":
        # Parse hover(x, y)
        parts = params_str.split(",")
        if len(parts) >= 2:
            params["x"] = float(parts[0].strip())
            params["y"] = float(parts[1].strip())

    elif action_name == "drag_and_release":
        # Parse drag_and_release(x1, y1, x2, y2)
        parts = params_str.split(",")
        if len(parts) >= 4:
            params["x1"] = float(parts[0].strip())
            params["y1"] = float(parts[1].strip())
            params["x2"] = float(parts[2].strip())
            params["y2"] = float(parts[3].strip())

    elif action_name == "scroll":
        # Parse scroll(x, y, delta_x=0, delta_y=100)
        parts = re.split(r",\s*(?![^()]*\))", params_str)
        if len(parts) >= 2:
            params["x"] = float(parts[0].strip())
            params["y"] = float(parts[1].strip())
            # Default values
            params["delta_x"] = 0
            params["delta_y"] = 100
            # Parse optional parameters
            for part in parts[2:]:
                if "delta_x=" in part:
                    match = re.search(r"delta_x=(-?\d+(?:\.\d+)?)", part)
                    if match:
                        params["delta_x"] = float(match.group(1))
                elif "delta_y=" in part:
                    match = re.search(r"delta_y=(-?\d+(?:\.\d+)?)", part)
                    if match:
                        params["delta_y"] = float(match.group(1))

    elif action_name == "type":
        # Parse type(x, y, text)
        # First extract x and y
        match = re.match(
            r"(\d+(?:\.\d+)?),\s*(\d+(?:\.\d+)?),\s*(.+)", params_str, re.DOTALL
        )
        if match:
            params["x"] = float(match.group(1))
            params["y"] = float(match.group(2))
            text_part = match.group(3).strip()
            # Extract text from quotes
            text_match = re.match(r'["\'](.+)["\']', text_part, re.DOTALL)
            if text_match:
                text = text_match.group(1)
                # Unescape the text
                text = text.encode().decode("unicode_escape")
                params["text"] = text

    elif action_name == "key_press":
        # Parse key_press(keys)
        # Extract list of keys
        match = re.search(r"\[(.*?)\]", params_str, re.DOTALL)
        if match:
            keys_str = match.group(1)
            # Parse individual keys
            keys = []
            for key_match in re.finditer(r'["\']([^"\']+)["\']', keys_str):
                keys.append(key_match.group(1))
            params["keys"] = keys

    elif action_name == "wait":
        # Parse wait(ms=1000) or wait()
        if params_str:
            match = re.search(r"(\d+)", params_str)
            if match:
                params["ms"] = int(match.group(1))
            else:
                params["ms"] = 1000
        else:
            params["ms"] = 1000
    elif action_name == "complete":
        # Parse complete(answer="...", infeasible_reason="...")
        # Extract answer if present
        answer_match = re.search(r'answer=["\']([^"\']*)["\']', params_str, re.DOTALL)
        if answer_match:
            params["answer"] = answer_match.group(1).encode().decode("unicode_escape")
        else:
            params["answer"] = ""

        # Extract infeasible_reason if present
        reason_match = re.search(
            r'infeasible_reason=["\']([^"\']*)["\']', params_str, re.DOTALL
        )
        if reason_match:
            params["infeasible_reason"] = (
                reason_match.group(1).encode().decode("unicode_escape")
            )
        else:
            params["infeasible_reason"] = ""
    else:
        raise RuntimeError("Unexpected action {}".format(action_name))

    return action_name, params


async def click(
    page: Page,
    x: float,
    y: float,
    button: Literal["left", "right"] = "left",
    double: bool = False,
) -> Tuple[bool, None]:
    """click(x: float, y: float, button: Literal['left', 'right'] = 'left', double: bool = False)
    Move the mouse to a location and click a mouse button.
    Can be used to click a button, select a checkbox, focus on a input field, etc.
    Args:
        x (float): The x coordinate of the location to click.
        y (float): The y coordinate of the location to click.
        button (Literal["left", "right"]): The button to click.
        double (bool): Whether to double click.
    Examples:
        click(324.5, 12)
        click(119, 34, button="right")
        click(34.1, 720, double=True)
        click(230, 100, button="left", double=False)"""
    if double:
        await page.mouse.dblclick(x, y, button=button)
    else:
        await page.mouse.click(x, y, button=button)
    return False, None


async def drag_and_release(
    page: Page, x1: float, y1: float, x2: float, y2: float
) -> Tuple[bool, None]:
    """drag_and_release(x1: float, y1: float, x2: float, y2: float)
    Press down the left mouse button at a location, drag the mouse to another location, and release the mouse button.
    Can be used for selecting a section of text, dragging a slider, etc.
    Args:
        x1 (float): The x coordinate of the location to press down the left mouse button.
        y1 (float): The y coordinate of the location to press down the left mouse button.
        x2 (float): The x coordinate of the location to release the left mouse button.
        y2 (float): The y coordinate of the location to release the left mouse button.
    Examples:
        drag_and_release(10.5, 200, 10.5, 230)"""
    await page.mouse.move(x1, y1)
    await page.mouse.down()
    await page.mouse.move(x2, y2)
    await page.mouse.up()
    return False, None


async def hover(page: Page, x: float, y: float) -> Tuple[bool, None]:
    """hover(x: float, y: float)
    Move the mouse to a location and stay there.
    Can be used to focus on a location, pop up a tooltip, navigate a dropdown menu, etc.
    Args:
        x (float): The x coordinate of the location to hover over.
        y (float): The y coordinate of the location to hover over.
    Examples:
        hover(102, 720)"""
    await page.mouse.move(x, y)
    return False, None


async def key_press(page: Page, keys: List[str]) -> Tuple[bool, None]:
    """key_press(keys: list[str])
    Press one or a combination of keys at the same time on the keyboard.
    Can be used
    - As various shortcuts of the current environment (e.g. ["Control", "a"], ["Control", "f"]).
    - To complete a search with ["Enter"].
    - And any other common actions that can be performed with a keyboard in the relevant application.
    This should NOT be used to type a string of text. Use the type action for that.
    The list of allowed keys are:
    - F1, F2, F3, F4, F5, F6, F7, F8, F9, F10, F11, F12
    - 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
    - a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z
    - Backspace, Tab, Enter, Shift, Control, Alt, Delete
    - ArrowUp, ArrowDown, ArrowLeft, ArrowRight
    - Home, End, PageUp, PageDown
    Args:
        keys (list[str]): The list of keys to press.
    Examples:
        key_press(["Control", "a"]) # Select all
        key_press(["Control", "f"]) # Open the search bar
        key_press(["Enter"]) # Submit a form
        key_press(["F12"]) # Open the developer tools in a browser"""
    # Join keys with + for Playwright
    key_combo = "+".join(keys)
    await page.keyboard.press(key_combo)
    return False, None


async def scroll(
    page: Page, x: float, y: float, delta_x: float = 0, delta_y: float = 100
) -> Tuple[bool, None]:
    """scroll(x: float, y: float, delta_x: float = 0, delta_y: float = 100)
    Move the mouse to a location and scroll the mouse wheel in the x and y directions.
    Can be used to scroll a webpage, scroll a dropdown menu, etc.
    Args:
        x (float): The x coordinate of the location to scroll over.
        y (float): The y coordinate of the location to scroll over.
        delta_x (float): The amount to scroll horizontally.
        delta_y (float): The amount to scroll vertically.
    Examples:
        scroll(102, 320)
        scroll(102, 320, 0, 200)
        scroll(90, 32.7, 0, -300)
        scroll(620, 105, 68, 49.6)"""
    # Move mouse to position first
    await page.mouse.move(x, y)
    # Then scroll
    await page.mouse.wheel(delta_x, delta_y)
    return False, None


async def type(page: Page, x: float, y: float, text: str) -> Tuple[bool, None]:
    """type(x: float, y: float, text: str)
    Focus on a location and type a string of text in it.
    Can be used to type in a text field, search bar, edit a document, etc.
    Args:
        x (float): The x coordinate of the location to type text in.
        y (float): The y coordinate of the location to type text in.
        text (str): The text to type.
    Examples:
        type(102, 70.6, "\\nThank you for the coffee!\\n")
        type(44, 120, "Best sellers")"""
    # Click to focus first
    await page.mouse.click(x, y)
    # Then type the text
    await page.keyboard.type(text)
    return False, None


async def wait(page: Page, ms: int = 1000) -> Tuple[bool, None]:
    """wait(ms: int = 1000)
    Wait for a specified amount of time.
    Can be used to wait for a webpage to load, a long form to display, etc.
    Args:
        ms (int): The amount of time to wait in milliseconds.
    Examples:
        wait()
        wait(1000)
        wait(500)"""
    await page.wait_for_timeout(ms)
    return False, None


async def complete(
    page: Page, answer: str = "", infeasible_reason: str = ""
) -> Tuple[bool, Dict[str, str]]:
    """complete(answer: str = '', infeasible_reason: str = '')
    Complete the task and optionally provide the user some feedback.
    Fill in the answer if the completion of the task requires providing a response to the user.
    Fill in the infeasible_reason if the task is infeasible.
    DO NOT fill in both answer and infeasible_reason at the same time.
    Args:
        answer (str): The answer to the task, if any.
        infeasible_reason (str): The reason the task is infeasible, if any.
    Examples:
        complete(answer="To request a refund, you need to call the customer service at 123-456-7890.")
        complete(infeasible_reason="The task is infeasible because the user has not provided a valid email address.")
        complete()
        complete(answer="{\\n  \\"name\\": \\"John\\",\\n  \\"age\\": 30,\\n  \\"city\\": \\"New York\\"\\n}")"""
    result = {}
    if answer:
        print(f"Task completed with answer: {answer}")
        result["answer"] = answer
    elif infeasible_reason:
        print(f"Task marked as infeasible: {infeasible_reason}")
        result["infeasible_reason"] = infeasible_reason
    else:
        print("Task completed")
    return True, result
