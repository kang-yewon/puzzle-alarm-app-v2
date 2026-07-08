"""
Base screen class — thin wrapper around Kivy Screen.
"""

from kivy.uix.screenmanager import Screen
from kivy.utils import get_color_from_hex

BG = get_color_from_hex("#FFF0F5")


class BaseScreen(Screen):
    def __init__(self, **kwargs):
        controller = kwargs.pop("controller")
        super().__init__(**kwargs)
        self.controller = controller

    def on_show(self) -> None:
        """Called every time this screen is navigated to. Override as needed."""
