"""
Macros Screen

Macro management screen.
"""

from ..items import MenuItem
from .base_menu import MenuScreen
from .toast import ToastScreen


class MacrosScreen(MenuScreen):
    """
    Macro management screen.

    Lists available macros for playback or management.
    """

    def __init__(self, manager):
        """
        Initialize macros screen.

        Args:
            manager: ScreenManager instance
        """
        items = self._build_items(manager)
        super().__init__(manager, "MACROS", items)

    def _get_macro_manager(self):
        """Get macro manager from daemon if available."""
        if self.manager and self.manager.daemon:
            return self.manager.daemon.macro_manager
        return None

    def _build_items(self, manager=None) -> list[MenuItem]:
        """Build menu items from available macros."""
        items = []

        # Use provided manager or self.manager
        mgr = manager if manager else getattr(self, "manager", None)
        macro_manager = None
        if mgr and mgr.daemon:
            macro_manager = mgr.daemon.macro_manager

        if macro_manager:
            summaries = macro_manager.list_macro_summaries()
            if summaries:
                for summary in summaries:
                    macro_id = summary["id"]
                    macro_name = summary["name"]
                    step_count = summary.get("step_count", 0)
                    # Truncate name if too long for display
                    display_name = macro_name[:16] if len(macro_name) > 16 else macro_name
                    items.append(
                        MenuItem(
                            id=f"macro_{macro_id}",
                            label=f"{display_name} ({step_count})",
                            action=lambda mid=macro_id: self._show_macro_info(mid),
                        )
                    )

        if not items:
            items.append(
                MenuItem(
                    id="no_macros",
                    label="No macros",
                    enabled=False,
                )
            )

        items.append(
            MenuItem(
                id="record",
                label="Record New",
                action=self._record_macro,
            )
        )

        return items

    def _show_macro_info(self, macro_id: str):
        """Show info toast for a macro."""
        mm = self._get_macro_manager()
        if mm:
            try:
                macro = mm.load_macro(macro_id)
                duration_s = macro.duration_ms / 1000.0
                toast = ToastScreen(
                    self.manager,
                    f"{macro.name}\n{macro.step_count} steps, {duration_s:.1f}s",
                )
                self.manager.show_overlay(toast, duration=2.5)
            except FileNotFoundError:
                toast = ToastScreen(self.manager, "Macro not found")
                self.manager.show_overlay(toast, duration=2.0)

    def _record_macro(self):
        """Start macro recording."""
        toast = ToastScreen(self.manager, "Use GUI to record")
        self.manager.show_overlay(toast, duration=2.0)

    def on_enter(self):
        """Refresh macro list when entering."""
        self.items = self._build_items()
        self.selected_index = 0
        self.scroll_offset = 0
        self.mark_dirty()
