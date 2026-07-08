"""
Typing puzzle: type the displayed sentence exactly.
"""

import random

from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.metrics import dp

from .base_puzzle import BasePuzzle, COLORS

_SENTENCES = [
    "오늘도 좋은 하루입니다.",
    "일어나서 하루를 시작하세요.",
    "좋은 아침이에요, 힘내세요!",
    "오늘 하루도 파이팅입니다.",
    "일어나야 할 시간이에요.",
    "새로운 하루가 시작되었습니다.",
    "건강한 하루 보내세요.",
    "일찍 일어나는 새가 먹이를 잡는다.",
    "지금 일어나면 하루가 달라집니다.",
    "알람을 끄고 기지개를 켜세요.",
]


def pick_sentence() -> str:
    return random.choice(_SENTENCES)


class TypingPuzzle(BasePuzzle):
    def _build_ui(self) -> None:
        self._target = pick_sentence()
        self.padding = [0, dp(20), 0, 0]
        self.spacing = dp(8)

        self.add_widget(Label(
            text="아래 문장을 똑같이 입력하세요.",
            font_size=dp(13), color=COLORS["text_secondary"],
            size_hint_y=None, height=dp(24),
        ))

        target_lbl = Label(
            text=self._target,
            font_size=dp(16), bold=True,
            color=COLORS["primary"],
            size_hint_y=None, height=dp(60),
            text_size=(dp(280), None), halign="center",
        )
        self.add_widget(target_lbl)

        self._entry = TextInput(
            multiline=False, font_size=dp(14),
            halign="center", padding_y=(dp(10), dp(10)),
            size_hint_y=None, height=dp(48),
            background_color=COLORS["input_bg"],
            foreground_color=COLORS["text"],
        )
        self._entry.bind(text=self._on_text_changed)
        self._entry.bind(on_text_validate=lambda _w: self._check())
        self.add_widget(self._entry)

        self.add_widget(Label(
            text="여기에 입력하세요.", font_size=dp(11),
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
        typed = self._entry.text
        if typed == self._target:
            self._feedback.text = "정답!"
            self._feedback.color = COLORS["success"]
            Clock.schedule_once(lambda _dt: self.on_success(), 0.4)
        else:
            self._feedback.text = "똑같이 입력해 주세요."
            self._feedback.color = COLORS["error"]
            self._entry.text = ""
