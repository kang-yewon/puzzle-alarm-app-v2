"""
Math puzzle: simple but tricky arithmetic questions.
"""

import random

from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.metrics import dp

from .base_puzzle import BasePuzzle, COLORS


def _make(a, op1, b, op2, c):
    if op1 == "×" and op2 == "+":
        answer = a * b + c
    elif op1 == "×" and op2 == "-":
        answer = a * b - c
    elif op1 == "+" and op2 == "×":
        answer = a + b * c
    elif op1 == "-" and op2 == "+":
        answer = a - b + c
    else:
        answer = a + b - c
    question = f"{a} {op1} {b} {op2} {c} = ?"
    return question, answer


def _make_div():
    b = random.randint(2, 9)
    a = b * random.randint(3, 12)
    c = random.randint(1, 10)
    answer = a // b + c
    question = f"{a} ÷ {b} + {c} = ?"
    return question, answer


_TEMPLATES = [
    lambda: _make(random.randint(11, 19), "×", random.randint(2, 9),
                  "-", random.randint(1, 20)),
    lambda: _make(random.randint(2, 9), "×", random.randint(11, 19),
                  "+", random.randint(1, 20)),
    lambda: _make(random.randint(10, 30), "+", random.randint(10, 30),
                  "×", random.randint(2, 5)),
    lambda: _make_div(),
    lambda: _make(random.randint(50, 99), "-", random.randint(11, 49),
                  "+", random.randint(1, 15)),
]


def generate_question() -> tuple[str, int]:
    template = random.choice(_TEMPLATES)
    return template()


class MathPuzzle(BasePuzzle):
    def _build_ui(self) -> None:
        self._question, self._answer = generate_question()
        self.padding = [0, dp(30), 0, 0]
        self.spacing = dp(8)

        self.add_widget(Label(
            text=self._question,
            font_size=dp(28), bold=True,
            color=COLORS["text"], size_hint_y=None, height=dp(50),
        ))

        self._entry = TextInput(
            multiline=False, font_size=dp(16),
            halign="center", padding_y=(dp(10), dp(10)),
            size_hint_y=None, height=dp(48),
            background_color=COLORS["input_bg"],
            foreground_color=COLORS["text"],
        )
        self._entry.bind(text=self._on_text_changed)
        self._entry.bind(on_text_validate=lambda _w: self._check())
        self.add_widget(self._entry)

        self.add_widget(Label(
            text="정답 입력", font_size=dp(11),
            color=COLORS["text_secondary"], size_hint_y=None, height=dp(20),
        ))

        confirm_btn = Button(
            text="확인", font_size=dp(14), bold=True,
            background_color=COLORS["primary"], color=(1, 1, 1, 1),
            size_hint_y=None, height=dp(48),
        )
        confirm_btn.bind(on_release=lambda _b: self._check())
        self.add_widget(confirm_btn)

        self._feedback = Label(
            text="", font_size=dp(11), color=COLORS["error"],
            size_hint_y=None, height=dp(24),
        )
        self.add_widget(self._feedback)

        self.add_widget(Widget())

    def _on_text_changed(self, _inst, _value) -> None:
        self.notify_activity()

    def _check(self) -> None:
        self.notify_activity()
        raw = self._entry.text.strip()
        try:
            value = int(raw)
        except ValueError:
            self._feedback.text = "숫자를 입력해 주세요."
            self._feedback.color = COLORS["error"]
            return
        if value == self._answer:
            self._feedback.text = "정답!"
            self._feedback.color = COLORS["success"]
            Clock.schedule_once(lambda _dt: self.on_success(), 0.4)
        else:
            self._feedback.text = "틀렸어요. 다시 시도하세요."
            self._feedback.color = COLORS["error"]
            self._entry.text = ""
