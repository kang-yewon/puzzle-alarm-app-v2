"""
Color distinction puzzle: find the one slightly-different tile in a grid.
Uses a Kivy canvas with rectangles for reliable color rendering on all platforms.
"""

import random
import colorsys

from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.metrics import dp

from .base_puzzle import BasePuzzle, COLORS

_BASE_HUES = [
    (0.92, "핑크"),
    (0.60, "파랑"),
    (0.33, "초록"),
    (0.08, "주황"),
    (0.70, "보라"),
    (0.50, "하늘"),
    (0.00, "빨강"),
    (0.14, "노랑"),
]

_GRID_COLS = 4
_GRID_ROWS = 4
_TILE = 58
_GAP = 5


def _hsv_to_hex(h, s, v):
    r, g, b = colorsys.hsv_to_rgb(h % 1.0, max(0.0, min(1.0, s)), max(0.0, min(1.0, v)))
    return (r, g, b)


def _generate_puzzle():
    hue, name = random.choice(_BASE_HUES)
    sat = random.uniform(0.50, 0.70)
    val = random.uniform(0.78, 0.90)

    mode = random.choice(["hue", "val", "sat"])
    if mode == "hue":
        delta = random.choice([-1, 1]) * random.uniform(0.007, 0.014)
        odd = _hsv_to_hex(hue + delta, sat, val)
    elif mode == "val":
        delta = random.choice([-1, 1]) * random.uniform(0.025, 0.045)
        odd = _hsv_to_hex(hue, sat, val + delta)
    else:
        delta = random.choice([-1, 1]) * random.uniform(0.04, 0.08)
        odd = _hsv_to_hex(hue, sat + delta, val)

    base = _hsv_to_hex(hue, sat, val)
    odd_row = random.randint(0, _GRID_ROWS - 1)
    odd_col = random.randint(0, _GRID_COLS - 1)
    return base, odd, odd_row, odd_col, name


class ColorGrid(Widget):
    def __init__(self, base, odd, odd_row, odd_col, on_correct, on_wrong, **kwargs):
        super().__init__(**kwargs)
        self._base = base
        self._odd = odd
        self._odd_row = odd_row
        self._odd_col = odd_col
        self._on_correct = on_correct
        self._on_wrong = on_wrong
        self._answered = False
        self.bind(pos=self._draw, size=self._draw)

    def _draw(self, *_args):
        self.canvas.clear()
        total_w = _GRID_COLS * _TILE + (_GRID_COLS + 1) * _GAP
        total_h = _GRID_ROWS * _TILE + (_GRID_ROWS + 1) * _GAP
        ox = self.x + (self.width - total_w) / 2
        oy = self.y + (self.height - total_h) / 2
        with self.canvas:
            for r in range(_GRID_ROWS):
                for col in range(_GRID_COLS):
                    color = self._odd if (r == self._odd_row and col == self._odd_col) \
                            else self._base
                    Color(*color)
                    x = ox + _GAP + col * (_TILE + _GAP)
                    y = oy + _GAP + (_GRID_ROWS - 1 - r) * (_TILE + _GAP)
                    Rectangle(pos=(x, y), size=(_TILE, _TILE))

    def on_touch_down(self, touch):
        if self._answered:
            return False
        total_w = _GRID_COLS * _TILE + (_GRID_COLS + 1) * _GAP
        total_h = _GRID_ROWS * _TILE + (_GRID_ROWS + 1) * _GAP
        ox = self.x + (self.width - total_w) / 2
        oy = self.y + (self.height - total_h) / 2
        col = int((touch.x - ox - _GAP) // (_TILE + _GAP))
        row_from_bottom = int((touch.y - oy - _GAP) // (_TILE + _GAP))
        row = _GRID_ROWS - 1 - row_from_bottom
        if not (0 <= row < _GRID_ROWS and 0 <= col < _GRID_COLS):
            return False
        x = ox + _GAP + col * (_TILE + _GAP)
        y = oy + _GAP + row_from_bottom * (_TILE + _GAP)
        if not (x <= touch.x <= x + _TILE and y <= touch.y <= y + _TILE):
            return False
        if row == self._odd_row and col == self._odd_col:
            self._answered = True
            self._on_correct()
        else:
            self._on_wrong()
        return True


class ColorPuzzle(BasePuzzle):
    def _build_ui(self) -> None:
        self._base, self._odd, self._odd_row, self._odd_col, name = _generate_puzzle()
        self.padding = [0, dp(16), 0, 0]
        self.spacing = dp(6)

        self.add_widget(Label(
            text="다른 색 하나를 찾아 터치하세요.",
            font_size=dp(14), bold=True,
            color=COLORS["text"], size_hint_y=None, height=dp(30),
        ))

        self._grid = ColorGrid(
            self._base, self._odd, self._odd_row, self._odd_col,
            on_correct=self._on_correct,
            on_wrong=self._on_wrong,
        )
        self.add_widget(self._grid)

        self._feedback = Label(
            text="", font_size=dp(11), color=COLORS["error"],
            size_hint_y=None, height=dp(24),
        )
        self.add_widget(self._feedback)

    def _on_correct(self) -> None:
        self.notify_activity()
        self._feedback.text = "정답!"
        self._feedback.color = COLORS["success"]
        Clock.schedule_once(lambda _dt: self.on_success(), 0.5)

    def _on_wrong(self) -> None:
        self.notify_activity()
        self._feedback.text = "틀렸어요. 다시 찾아보세요."
        self._feedback.color = COLORS["error"]
