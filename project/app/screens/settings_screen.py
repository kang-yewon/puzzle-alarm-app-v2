"""
Alarm settings screen: time picker, puzzle type, puzzle count, sound shortcut.
Scrollable via ScrollView.
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.rst import RstDocument  # noqa: F401  (kept for reference)
from kivy.utils import get_color_from_hex
from kivy.metrics import dp

from .base_screen import BaseScreen, BG
from ..models import PuzzleType

PRIMARY = get_color_from_hex("#B96EFF")
PRIMARY_DARK = get_color_from_hex("#9B4FE8")
TEXT = get_color_from_hex("#2D2D2D")
TEXT_SEC = get_color_from_hex("#888888")
SURFACE = get_color_from_hex("#FFFFFF")
BORDER = get_color_from_hex("#E8D5FF")
INPUT_BG = get_color_from_hex("#F8F0FF")


class Spinner(BoxLayout):
    """Up/down spinner for integer values."""

    def __init__(self, var, min_val, max_val, fmt="{:d}", **kwargs):
        super().__init__(orientation="vertical", size_hint_x=None, width=dp(70),
                         spacing=dp(2), **kwargs)
        self._var = var
        self._min = min_val
        self._max = max_val
        self._fmt = fmt

        up = Button(text="∧", font_size=dp(14),
                    background_color=SURFACE, color=PRIMARY,
                    size_hint_y=None, height=dp(32))
        up.bind(on_release=lambda _b: self._spin(1))
        self.add_widget(up)

        self._lbl = Label(
            text=self._fmt.format(var.get()),
            font_size=dp(28), bold=True, color=TEXT,
            size_hint_y=None, height=dp(44),
        )
        self.add_widget(self._lbl)

        down = Button(text="∨", font_size=dp(14),
                      background_color=SURFACE, color=PRIMARY,
                      size_hint_y=None, height=dp(32))
        down.bind(on_release=lambda _b: self._spin(-1))
        self.add_widget(down)

    def _spin(self, delta: int) -> None:
        new = self._var.get() + delta
        if new < self._min:
            new = self._max
        elif new > self._max:
            new = self._min
        self._var.set(new)

    def refresh(self) -> None:
        self._lbl.text = self._fmt.format(self._var.get())


class IntVar:
    """Tiny observable int container (mimics tk.IntVar)."""

    def __init__(self, value=0):
        self._value = value
        self._traces = []

    def get(self):
        return self._value

    def set(self, v):
        self._value = int(v)
        for cb in self._traces:
            cb()

    def trace_add(self, cb):
        self._traces.append(cb)


class StrVar:
    def __init__(self, value=""):
        self._value = value
        self._traces = []

    def get(self):
        return self._value

    def set(self, v):
        self._value = v
        for cb in self._traces:
            cb()

    def trace_add(self, cb):
        self._traces.append(cb)


class SettingsScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._build_ui()

    def _build_ui(self) -> None:
        root = BoxLayout(orientation="vertical")

        # Header
        header = BoxLayout(orientation="horizontal", size_hint_y=None,
                          height=dp(52), padding=[dp(16), dp(12)])
        with header.canvas:
            from kivy.graphics import Color as GColor, RoundedRectangle as GRRect
            GColor(*SURFACE)
            self._header_rect = GRRect(pos=header.pos, size=header.size, radius=[0])

        back_btn = Button(
            text="←", font_size=dp(18),
            background_color=SURFACE, color=TEXT,
            size_hint_x=None, width=dp(44),
        )
        back_btn.bind(on_release=lambda _b: self._cancel())
        header.add_widget(back_btn)

        header.add_widget(Label(
            text="알람 설정", font_size=dp(16), bold=True,
            color=TEXT,
        ))

        save_btn = Button(
            text="저장", font_size=dp(13), bold=True,
            background_color=SURFACE, color=PRIMARY,
            size_hint_x=None, width=dp(60),
        )
        save_btn.bind(on_release=lambda _b: self._save())
        header.add_widget(save_btn)
        root.add_widget(header)

        # Scrollable body
        scroll = ScrollView()
        body = BoxLayout(orientation="vertical", size_hint_y=None, spacing=dp(12),
                         padding=[dp(16), dp(8)])
        body.bind(minimum_height=body.setter("height"))

        # --- Time picker ---
        body.add_widget(self._section_label("알람 시간"))

        self._hour_var = IntVar(value=7)
        self._minute_var = IntVar(value=0)
        self._period_var = StrVar(value="AM")

        time_frame = BoxLayout(orientation="horizontal", size_hint_y=None,
                               height=dp(120), spacing=dp(8))
        self._hour_spinner = Spinner(self._hour_var, 1, 12)
        time_frame.add_widget(self._hour_spinner)
        time_frame.add_widget(Label(text=":", font_size=dp(28), bold=True,
                                    color=TEXT, size_hint_x=None, width=dp(20)))
        self._minute_spinner = Spinner(self._minute_var, 0, 59, fmt="{:02d}")
        time_frame.add_widget(self._minute_spinner)

        period_box = BoxLayout(orientation="vertical", size_hint_x=None,
                               width=dp(70), spacing=dp(4))
        self._am_btn = ToggleButton(
            text="AM", font_size=dp(13), bold=True,
            size_hint_y=None, height=dp(44),
            group="period",
        )
        self._am_btn.bind(on_release=lambda _b: self._set_period("AM"))
        period_box.add_widget(self._am_btn)
        self._pm_btn = ToggleButton(
            text="PM", font_size=dp(13), bold=True,
            size_hint_y=None, height=dp(44),
            group="period",
        )
        self._pm_btn.bind(on_release=lambda _b: self._set_period("PM"))
        period_box.add_widget(self._pm_btn)
        time_frame.add_widget(period_box)
        body.add_widget(time_frame)

        # --- Puzzle type ---
        body.add_widget(self._section_label("퍼즐 종류"))

        puzzle_frame = BoxLayout(orientation="vertical", size_hint_y=None,
                                 height=dp(180), spacing=dp(6))
        self._puzzle_var = StrVar(value=PuzzleType.MATH.value)
        puzzle_options = [
            (PuzzleType.MATH.value, "수학 문제", "간단한 계산 문제를 풀어요"),
            (PuzzleType.COLOR.value, "색 구분하기", "비슷한 색 중 다른 색을 찾아요"),
            (PuzzleType.TYPING.value, "문장 타이핑", "문장을 똑같이 입력해요"),
        ]
        for val, label, sub in puzzle_options:
            row = BoxLayout(orientation="horizontal", size_hint_y=None,
                            height=dp(54), spacing=dp(8))
            btn = ToggleButton(
                text=label, font_size=dp(13), bold=True,
                group="puzzle_type",
                size_hint_x=None, width=dp(120),
            )
            btn.state = "down" if val == self._puzzle_var.get() else "normal"
            btn.bind(on_release=lambda _b, v=val: self._set_puzzle_type(v))
            row.add_widget(btn)
            row.add_widget(Label(
                text=sub, font_size=dp(10), color=TEXT_SEC,
                halign="left", valign="middle",
            ))
            row.add_widget(Widget(size_hint_x=None, width=dp(8)))
            puzzle_frame.add_widget(row)
        body.add_widget(puzzle_frame)

        # --- Puzzle count ---
        body.add_widget(self._section_label("퍼즐 개수"))

        count_frame = BoxLayout(orientation="horizontal", size_hint_y=None,
                                height=dp(60), spacing=dp(12))
        self._count_var = IntVar(value=3)
        minus_btn = Button(
            text="−", font_size=dp(20), bold=True,
            background_color=SURFACE, color=PRIMARY,
            size_hint_x=None, width=dp(50),
        )
        minus_btn.bind(on_release=lambda _b: self._change_count(-1))
        count_frame.add_widget(minus_btn)

        self._count_lbl = Label(
            text="3", font_size=dp(22), bold=True, color=TEXT,
        )
        count_frame.add_widget(self._count_lbl)

        count_frame.add_widget(Label(
            text="개", font_size=dp(13), color=TEXT_SEC,
            size_hint_x=None, width=dp(30),
        ))

        plus_btn = Button(
            text="+", font_size=dp(20), bold=True,
            background_color=SURFACE, color=PRIMARY,
            size_hint_x=None, width=dp(50),
        )
        plus_btn.bind(on_release=lambda _b: self._change_count(1))
        count_frame.add_widget(plus_btn)
        body.add_widget(count_frame)

        body.add_widget(Label(
            text="(최소 1개 ~ 최대 5개)", font_size=dp(10),
            color=TEXT_SEC, size_hint_y=None, height=dp(20),
        ))

        # --- Alarm sound ---
        body.add_widget(self._section_label("알람 소리"))

        sound_btn = Button(
            text="🔔  morning.mp3",
            font_size=dp(13),
            background_color=SURFACE, color=TEXT,
            size_hint_y=None, height=dp(52),
            halign="left", valign="middle",
        )
        sound_btn.bind(on_release=lambda _b: self.controller.show_screen("sound"))
        self._sound_btn = sound_btn
        body.add_widget(sound_btn)

        body.add_widget(Widget(size_hint_y=None, height=dp(24)))

        scroll.add_widget(body)
        root.add_widget(scroll)
        self.add_widget(root)

    def _section_label(self, text):
        return Label(
            text=text, font_size=dp(12), bold=True,
            color=TEXT_SEC, size_hint_y=None, height=dp(28),
            halign="left", valign="middle",
        )

    def _set_period(self, period: str) -> None:
        self._period_var.set(period)
        if period == "AM":
            self._am_btn.state = "down"
            self._pm_btn.state = "normal"
        else:
            self._am_btn.state = "normal"
            self._pm_btn.state = "down"

    def _set_puzzle_type(self, val: str) -> None:
        self._puzzle_var.set(val)

    def _change_count(self, delta: int) -> None:
        new = max(1, min(5, self._count_var.get() + delta))
        self._count_var.set(new)
        self._count_lbl.text = str(new)

    def on_show(self) -> None:
        s = self.controller.settings
        self._hour_var.set(s.hour)
        self._minute_var.set(s.minute)
        self._period_var.set("AM" if s.is_am else "PM")
        self._set_period("AM" if s.is_am else "PM")
        self._puzzle_var.set(s.puzzle_type.value)
        self._count_var.set(s.puzzle_count)
        self._count_lbl.text = str(s.puzzle_count)
        self._hour_spinner.refresh()
        self._minute_spinner.refresh()
        name = s.sound_path.split("/")[-1].split("\\")[-1] if s.sound_path else "기본 알람음"
        self._sound_btn.text = f"🔔  {name}"

    def _save(self) -> None:
        s = self.controller.settings
        s.hour = self._hour_var.get()
        s.minute = self._minute_var.get()
        s.is_am = self._period_var.get() == "AM"
        s.puzzle_type = PuzzleType(self._puzzle_var.get())
        s.puzzle_count = self._count_var.get()
        self.controller.save_settings()
        self.controller.show_screen("home")

    def _cancel(self) -> None:
        self.controller.show_screen("home")
