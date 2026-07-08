"""
Home screen: displays alarm time, on/off toggle, and settings button.
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, RoundedRectangle
from kivy.utils import get_color_from_hex
from kivy.metrics import dp

from .base_screen import BaseScreen, BG

PRIMARY = get_color_from_hex("#B96EFF")
PRIMARY_DARK = get_color_from_hex("#9B4FE8")
TEXT = get_color_from_hex("#2D2D2D")
TEXT_SEC = get_color_from_hex("#888888")
SURFACE = get_color_from_hex("#FFFFFF")
TOGGLE_ON = get_color_from_hex("#B96EFF")
TOGGLE_OFF = get_color_from_hex("#CCCCCC")


class ToggleSwitch(Widget):
    def __init__(self, on_toggle, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (dp(56), dp(28))
        self._on = True
        self._on_toggle = on_toggle
        self.bind(pos=self._redraw, size=self._redraw)

    def set_state(self, on: bool):
        self._on = on
        self._redraw()

    def _redraw(self, *_):
        self.canvas.clear()
        color = TOGGLE_ON if self._on else TOGGLE_OFF
        knob_x = self.right - dp(14) - dp(11) if self._on else self.x + dp(3) + dp(11)
        with self.canvas:
            Color(*color)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(14)])
            Color(1, 1, 1, 1)
            Ellipse(pos=(knob_x - dp(11), self.y + dp(3)),
                    size=(dp(22), dp(22)))

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self._on = not self._on
            self._redraw()
            self._on_toggle(self._on)
            return True
        return False


class HomeScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._build_ui()

    def _build_ui(self) -> None:
        layout = BoxLayout(orientation="vertical", padding=[0, dp(40), 0, 0],
                           spacing=dp(4))
        layout.bind(size=self._on_resize)

        self._icon_lbl = Label(
            text="⏰", font_size=dp(48),
            color=TEXT, size_hint_y=None, height=dp(60),
        )
        layout.add_widget(self._icon_lbl)

        layout.add_widget(Label(
            text="다음 알람", font_size=dp(13),
            color=TEXT_SEC, size_hint_y=None, height=dp(24),
        ))

        self._time_lbl = Label(
            text="07:00 AM", font_size=dp(42), bold=True,
            color=TEXT, size_hint_y=None, height=dp(60),
        )
        layout.add_widget(self._time_lbl)

        toggle_row = BoxLayout(orientation="horizontal", size_hint_y=None,
                               height=dp(32), spacing=dp(8),
                               padding=[0, dp(8), 0, 0])
        self._toggle = ToggleSwitch(on_toggle=self._on_toggle_changed)
        toggle_row.add_widget(Widget(size_hint_x=None, width=dp(80)))
        toggle_row.add_widget(self._toggle)
        self._toggle_label = Label(
            text="ON", font_size=dp(13), bold=True,
            color=PRIMARY, size_hint_x=None, width=dp(40),
        )
        toggle_row.add_widget(self._toggle_label)
        toggle_row.add_widget(Widget(size_hint_x=None, width=dp(80)))
        layout.add_widget(toggle_row)

        layout.add_widget(Widget(size_hint_y=None, height=dp(32)))

        settings_btn = Button(
            text="⚙  알람 설정",
            font_size=dp(14), bold=True,
            background_color=PRIMARY,
            color=(1, 1, 1, 1),
            size_hint_y=None, height=dp(52),
        )
        settings_btn.bind(on_release=lambda _b: self.controller.show_screen("settings"))
        layout.add_widget(settings_btn)

        layout.add_widget(Widget())

        self.add_widget(layout)

    def _on_resize(self, *_args):
        pass

    def _on_toggle_changed(self, on: bool) -> None:
        settings = self.controller.settings
        settings.enabled = on
        self.controller.save_settings()
        self._refresh()

    def on_show(self) -> None:
        self._refresh()

    def _refresh(self) -> None:
        s = self.controller.settings
        self._time_lbl.text = s.display_time()
        self._toggle.set_state(s.enabled)
        if s.enabled:
            self._toggle_label.text = "ON"
            self._toggle_label.color = PRIMARY
        else:
            self._toggle_label.text = "OFF"
            self._toggle_label.color = TEXT_SEC
