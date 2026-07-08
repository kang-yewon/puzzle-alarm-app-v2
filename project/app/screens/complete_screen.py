"""
Completion screen: shown for 3 seconds after all puzzles are solved.
"""

import random

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Ellipse
from kivy.clock import Clock
from kivy.utils import get_color_from_hex
from kivy.metrics import dp

from .base_screen import BaseScreen

TEXT = get_color_from_hex("#2D2D2D")
TEXT_SEC = get_color_from_hex("#888888")
SUCCESS = get_color_from_hex("#4CAF50")
CONFETTI_COLORS = [
    get_color_from_hex("#B96EFF"),
    get_color_from_hex("#FF6B9D"),
    get_color_from_hex("#4CAF50"),
    get_color_from_hex("#FFB800"),
    get_color_from_hex("#42A5F5"),
]


class ConfettiWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(size_hint_y=None, height=dp(80), **kwargs)
        self._pieces = []
        self.bind(pos=self._draw, size=self._draw)

    def scatter(self):
        w = self.width if self.width > 1 else dp(300)
        self._pieces = [
            (random.randint(0, int(w)), random.randint(0, int(dp(70))),
             random.randint(4, 10), random.choice(CONFETTI_COLORS))
            for _ in range(30)
        ]
        self._draw()

    def _draw(self, *_args):
        self.canvas.clear()
        with self.canvas:
            for (rx, ry, size, col) in self._pieces:
                Color(*col)
                Rectangle(pos=(self.x + rx, self.y + ry), size=(size, size // 2 + 2))


class CompleteScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._after_event = None
        self._build_ui()

    def _build_ui(self) -> None:
        layout = BoxLayout(orientation="vertical", padding=[0, dp(30), 0, 0],
                           spacing=dp(8))

        self._confetti = ConfettiWidget()
        layout.add_widget(self._confetti)

        # Green check circle drawn via canvas on a Widget
        check = Widget(size_hint_y=None, height=dp(100))
        with check.canvas:
            Color(*SUCCESS)
            Ellipse(pos=(0, 0), size=(dp(100), dp(100)))
        check_lbl = Label(
            text="✓", font_size=dp(44), bold=True, color=(1, 1, 1, 1),
            size_hint_y=None, height=dp(100),
        )
        layout.add_widget(check_lbl)

        layout.add_widget(Label(
            text="완료!", font_size=dp(32), bold=True,
            color=TEXT, size_hint_y=None, height=dp(50),
        ))

        layout.add_widget(Label(
            text="모든 퍼즐을 성공했어요.",
            font_size=dp(14), color=TEXT_SEC,
            size_hint_y=None, height=dp(30),
        ))

        layout.add_widget(Widget())

        self._counter_lbl = Label(
            text="3초 후 홈 화면으로 돌아갑니다.",
            font_size=dp(11), color=TEXT_SEC,
            size_hint_y=None, height=dp(40),
        )
        layout.add_widget(self._counter_lbl)

        self._countdown = 3
        self.add_widget(layout)

    def on_show(self) -> None:
        self._countdown = 3
        self._confetti.scatter()
        self._tick()

    def _tick(self) -> None:
        if self._countdown > 0:
            self._counter_lbl.text = f"{self._countdown}초 후 홈 화면으로 돌아갑니다."
            self._countdown -= 1
            self._after_event = Clock.schedule_once(lambda _dt: self._tick(), 1)
        else:
            self.controller.on_puzzles_complete()
