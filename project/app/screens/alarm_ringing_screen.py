"""
Alarm ringing screen: shown when alarm fires.
Animated clock drawn on a Kivy canvas.
"""

import math

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line, Arc
from kivy.clock import Clock
from kivy.utils import get_color_from_hex
from kivy.metrics import dp

from .base_screen import BaseScreen, BG

PRIMARY = get_color_from_hex("#B96EFF")
TEXT = get_color_from_hex("#2D2D2D")
TEXT_SEC = get_color_from_hex("#888888")
BTN_PUZZLE = get_color_from_hex("#FF6B9D")
CLOCK_BODY = get_color_from_hex("#FFB8DC")
CLOCK_OUTLINE = get_color_from_hex("#FF6BAD")
CLOCK_BUMP = get_color_from_hex("#FF9CC8")


class ClockWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (dp(140), dp(140))
        self._step = 0
        self._event = None

    def start(self):
        if self._event is None:
            self._event = Clock.schedule_interval(self._tick, 0.08)

    def stop(self):
        if self._event is not None:
            self._event.cancel()
            self._event = None

    def _tick(self, _dt):
        self._step += 1
        self.canvas.clear()
        self._draw()

    def _draw(self):
        step = self._step
        shake = 4 * math.sin(step * 0.5)
        cx = self.x + self.width / 2 + shake
        cy = self.y + self.height / 2
        r = dp(48)
        with self.canvas:
            Color(*CLOCK_BODY)
            Ellipse(pos=(cx - r, cy - r), size=(2 * r, 2 * r))
            Color(*CLOCK_OUTLINE)
            Line(circle=(cx, cy, r), width=dp(3))
            # Bell bumps
            Color(*CLOCK_BUMP)
            Ellipse(pos=(cx - dp(34), cy + dp(4)), size=(dp(12), dp(12)))
            Ellipse(pos=(cx + dp(22), cy + dp(4)), size=(dp(12), dp(12)))
            Color(*CLOCK_OUTLINE)
            Line(circle=(cx - dp(28), cy + dp(10), dp(6)), width=dp(2))
            Line(circle=(cx + dp(28), cy + dp(10), dp(6)), width=dp(2))
            # Legs
            Color(*CLOCK_BUMP)
            Ellipse(pos=(cx - dp(30), cy - dp(42)), size=(dp(12), dp(12)))
            Ellipse(pos=(cx + dp(18), cy - dp(42)), size=(dp(12), dp(12)))
            # Hour hand
            angle_h = math.radians(-60 + shake * 2)
            Color(*TEXT)
            Line(points=[cx, cy,
                         cx + 22 * math.sin(angle_h),
                         cy - 22 * math.cos(angle_h)],
                 width=dp(3))
            # Minute hand
            angle_m = math.radians(90 + step * 6)
            Color(*PRIMARY)
            Line(points=[cx, cy,
                         cx + 30 * math.sin(angle_m),
                         cy - 30 * math.cos(angle_m)],
                 width=dp(2))
            # Center dot
            Color(*TEXT)
            Ellipse(pos=(cx - dp(4), cy - dp(4)), size=(dp(8), dp(8)))


class AlarmRingingScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._build_ui()

    def _build_ui(self) -> None:
        layout = BoxLayout(orientation="vertical", padding=[0, dp(50), 0, 0],
                           spacing=dp(8))
        self._clock = ClockWidget()
        layout.add_widget(self._clock)

        layout.add_widget(Label(
            text="알람입니다!", font_size=dp(24), bold=True,
            color=TEXT, size_hint_y=None, height=dp(40),
        ))

        layout.add_widget(Label(
            text="일어나서 퍼즐을 풀어 알람을 해제하세요.",
            font_size=dp(13), color=TEXT_SEC,
            size_hint_y=None, height=dp(40),
            text_size=(dp(280), None), halign="center",
        ))

        layout.add_widget(Widget())

        puzzle_btn = Button(
            text="퍼즐 풀기",
            font_size=dp(18), bold=True,
            background_color=BTN_PUZZLE,
            color=(1, 1, 1, 1),
            size_hint_y=None, height=dp(56),
        )
        puzzle_btn.bind(on_release=lambda _b: self._go_to_puzzle())
        layout.add_widget(puzzle_btn)
        layout.add_widget(Widget(size_hint_y=None, height=dp(48)))

        self.add_widget(layout)

    def on_show(self) -> None:
        self._clock.start()

    def _go_to_puzzle(self) -> None:
        self._clock.stop()
        self.controller.show_screen("puzzle")

    def on_pre_leave(self):
        self._clock.stop()
