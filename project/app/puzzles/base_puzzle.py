"""
Abstract base for all puzzle types.
Each puzzle is a self-contained Kivy BoxLayout.
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.utils import get_color_from_hex
from abc import ABC, abstractmethod
from typing import Callable

COLORS = {
    "bg": get_color_from_hex("#FFF0F5"),
    "primary": get_color_from_hex("#B96EFF"),
    "primary_dark": get_color_from_hex("#9B4FE8"),
    "surface": get_color_from_hex("#FFFFFF"),
    "text": get_color_from_hex("#2D2D2D"),
    "text_secondary": get_color_from_hex("#888888"),
    "input_bg": get_color_from_hex("#F8F0FF"),
    "border": get_color_from_hex("#E8D5FF"),
    "success": get_color_from_hex("#4CAF50"),
    "error": get_color_from_hex("#FF5252"),
    "timer_warning": get_color_from_hex("#FF9800"),
}


class BasePuzzle(BoxLayout, ABC):
    """
    One puzzle instance. on_success is called when the user solves it.
    on_activity is called on any user interaction to reset the idle timer.
    """

    def __init__(self, on_success: Callable[[], None],
                 on_activity: Callable[[], None] | None = None,
                 **kwargs) -> None:
        super().__init__(orientation="vertical", **kwargs)
        self.on_success = on_success
        self._on_activity_cb = on_activity or (lambda: None)
        self._build_ui()

    @abstractmethod
    def _build_ui(self) -> None:
        """Render puzzle-specific widgets."""

    def notify_activity(self) -> None:
        self._on_activity_cb()
