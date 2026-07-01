"""
JavaScript code templates for the Python Selenium code generator.

These templates are used to generate JavaScript code that gets executed
via driver.execute_script() for scroll operations and other DOM interactions.
"""


class ScrollJS:
    """JavaScript templates for scroll operations."""

    @staticmethod
    def wheel_event(delta_axis: str, delta_value: str) -> str:
        """Generate JavaScript for wheel event dispatch."""
        return (
            f"let event = new WheelEvent('wheel', "
            f"{{bubbles: true, cancelable: true, {delta_axis}: {delta_value}}}); "
            f"arguments[0].dispatchEvent(event);"
        )

    @staticmethod
    def wheel_event_with_args(
        delta_x: str = "arguments[1]", delta_y: str = "arguments[2]"
    ) -> str:
        """Generate wheel event with argument placeholders."""
        return (
            f"let event = new WheelEvent('wheel', "
            f"{{bubbles: true, cancelable: true, deltaX: {delta_x}, deltaY: {delta_y}}}); "
            f"arguments[0].dispatchEvent(event);"
        )

    @staticmethod
    def scroll_by(x_value: str, y_value: str) -> str:
        """Generate JavaScript for scrollBy on element."""
        return f"arguments[0].scrollBy({x_value}, {y_value});"

    @staticmethod
    def scroll_by_with_args() -> str:
        """Generate scrollBy with argument placeholders."""
        return "arguments[0].scrollBy(arguments[1], arguments[2]);"

    @staticmethod
    def window_scroll_to(direction_prefix: str, target: str) -> str:
        """Generate window scrollTo for full page scroll."""
        return f"window.scrollTo(0, {direction_prefix}document.documentElement.scrollHeight)"

    @staticmethod
    def window_scroll_by(x: str, y: str) -> str:
        """Generate window.scrollBy call."""
        return f"window.scrollBy({x}, {y})"

    @staticmethod
    def window_scroll_by_with_args() -> str:
        """Generate window.scrollBy with argument placeholders."""
        return "window.scrollBy(0, arguments[0] * arguments[1])"

    @staticmethod
    def get_scroll_height() -> str:
        """Get scrollHeight of element."""
        return "return arguments[0].scrollHeight"

    @staticmethod
    def get_scroll_width() -> str:
        """Get scrollWidth of element."""
        return "return arguments[0].scrollWidth"

    @staticmethod
    def get_body_scroll_height() -> str:
        """Get document body scrollHeight."""
        return "return document.body.scrollHeight"

    @staticmethod
    def get_window_inner_height() -> str:
        """Get window inner height."""
        return "return window.innerHeight"

    @staticmethod
    def get_event_listener_list() -> str:
        """Get event listener list from element."""
        return "return arguments[0].eventListenerList || []"

    @staticmethod
    def times_scroll_wheel(
        axis: str, abs_value: int, client_dim: str, multiplier: str
    ) -> str:
        """Generate wheel event for times-based scroll."""
        return (
            f"let amount = {abs_value} * arguments[0].{client_dim} * {multiplier};"
            f" let event = new WheelEvent('wheel', "
            f"{{bubbles: true, cancelable: true, delta{axis}: amount}}); "
            f"arguments[0].dispatchEvent(event);"
        )

    @staticmethod
    def times_scroll_by(
        scroll_value: int, client_dim: str, scroll_x: str, scroll_y: str
    ) -> str:
        """Generate scrollBy for times-based scroll."""
        return (
            f"let amount = {scroll_value} * arguments[0].{client_dim};"
            f" arguments[0].scrollBy({scroll_x}, {scroll_y});"
        )

    @staticmethod
    def times_body_scroll(scroll_value: int, client_dim: str, axis: str) -> str:
        """Generate window scroll for body element."""
        other_axis = "Y" if axis == "X" else "X"
        return (
            f"let amount = {scroll_value} * document.documentElement.{client_dim};"
            f" window.scrollBy("
            f"{{'{axis}': [amount, 0], '{other_axis}': [0, amount]}}['{axis}'][0], "
            f"{{'{axis}': [amount, 0], '{other_axis}': [0, amount]}}['{axis}'][1]);"
        )


class ShadowDomJS:
    """JavaScript templates for Shadow DOM operations."""

    @staticmethod
    def get_shadow_root_child() -> str:
        """Get first child of shadow root."""
        return "return arguments[0].shadowRoot.children[0]"
