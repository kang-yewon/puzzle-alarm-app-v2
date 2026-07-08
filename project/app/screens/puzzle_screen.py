"""
Puzzle screen: sequences N puzzles, manages the 15-second idle timer,
pauses alarm while on screen, resumes alarm if idle timer expires.
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.utils import get_color_from_hex
from kivy.metrics import dp

from .base_screen import BaseScreen, BG
from ..models import PuzzleType
from ..puzzles.math_puzzle import MathPuzzle
from ..puzzles.color_puzzle import ColorPuzzle
from ..puzzles.typing_puzzle import TypingPuzzle

PRIMARY = get_color_from_hex("#B96EFF")
TEXT = get_color_from_hex("#2D2D2D")
TEXT_SEC = get_color_from_hex("#888888")
SURFACE = get_color_from_hex("#FFFFFF")
PROGRESS_BG = get_color_from_hex("#E8D5FF")
WARNING = get_color_from_hex("#FF9800")

IDLE_SECONDS = 15


class PuzzleScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._current_puzzle_widget = None
        self._idle_event = None
        self._alarm_resume_event = None
        self._puzzle_index = 0
        self._total = 1
        self._remaining = IDLE_SECONDS
        self._build_ui()

    def _build_ui(self) -> None:
        layout = BoxLayout(orientation="vertical")
        self._layout = layout

        # Header
        self._progress_lbl = Label(
            text="문제 1 / 1", font_size=dp(14), bold=True,
            color=TEXT, size_hint_y=None, height=dp(44),
        )
        layout.add_widget(self._progress_lbl)

        # Progress bar
        self._progress_bar = Widget(size_hint_y=None, height=dp(6))
        self._progress_bar.bind(pos=self._redraw_progress,
                                size=self._redraw_progress)
        layout.add_widget(self._progress_bar)

        # Puzzle container
        self._puzzle_container = BoxLayout(orientation="vertical")
        layout.add_widget(self._puzzle_container)

        # Idle timer warning
        self._timer_lbl = Label(
            text=f"⏱ {IDLE_SECONDS}초 동안 아무 행동이 없으면 알람이 다시 울려요.",
            font_size=dp(10), color=TEXT_SEC,
            size_hint_y=None, height=dp(40),
            text_size=(dp(300), None), halign="center",
        )
        layout.add_widget(self._timer_lbl)

        self.add_widget(layout)

    def on_show(self) -> None:
        from .. import audio_manager
        audio_manager.pause_alarm()
        self._puzzle_index = 0
        self._total = self.controller.settings.puzzle_count
        self._load_puzzle()
        self._reset_idle_timer()

    def _load_puzzle(self) -> None:
        if self._current_puzzle_widget is not None:
            self._puzzle_container.remove_widget(self._current_puzzle_widget)
            self._current_puzzle_widget = None

        self._progress_lbl.text = f"문제 {self._puzzle_index + 1} / {self._total}"
        self._redraw_progress()

        puzzle_type = self.controller.settings.puzzle_type
        klass = {
            PuzzleType.MATH: MathPuzzle,
            PuzzleType.COLOR: ColorPuzzle,
            PuzzleType.TYPING: TypingPuzzle,
        }[puzzle_type]

        widget = klass(on_success=self._on_puzzle_solved,
                       on_activity=self._on_activity)
        self._puzzle_container.add_widget(widget)
        self._current_puzzle_widget = widget

    def _on_puzzle_solved(self) -> None:
        self._reset_idle_timer()
        self._puzzle_index += 1
        if self._puzzle_index >= self._total:
            self._finish()
        else:
            self._load_puzzle()

    def _finish(self) -> None:
        self._cancel_idle_timer()
        from .. import audio_manager
        audio_manager.stop_alarm()
        self.controller.show_screen("complete")

    def _on_activity(self) -> None:
        self._reset_idle_timer()

    def _reset_idle_timer(self) -> None:
        self._cancel_idle_timer()
        self._remaining = IDLE_SECONDS
        self._tick_idle()

    def _cancel_idle_timer(self) -> None:
        if self._idle_event is not None:
            self._idle_event.cancel()
            self._idle_event = None
        if self._alarm_resume_event is not None:
            self._alarm_resume_event.cancel()
            self._alarm_resume_event = None

    def _tick_idle(self) -> None:
        if self._remaining <= 5:
            self._timer_lbl.text = f"⏱ {self._remaining}초 후 알람이 다시 울려요!"
            self._timer_lbl.color = WARNING
        else:
            self._timer_lbl.text = f"⏱ {self._remaining}초 동안 아무 행동이 없으면 알람이 다시 울려요."
            self._timer_lbl.color = TEXT_SEC
        if self._remaining <= 0:
            self._on_idle_timeout()
            return
        self._remaining -= 1
        self._idle_event = Clock.schedule_once(lambda _dt: self._tick_idle(), 1)

    def _on_idle_timeout(self) -> None:
        from .. import audio_manager
        audio_manager.resume_alarm()
        self._alarm_resume_event = Clock.schedule_once(
            lambda _dt: self._re_pause_alarm(), 5)

    def _re_pause_alarm(self, _dt=None) -> None:
        from .. import audio_manager
        audio_manager.pause_alarm()
        self._reset_idle_timer()

    def _redraw_progress(self, *_args) -> None:
        bar = self._progress_bar
        bar.canvas.clear()
        w, h = bar.size
        if w <= 1:
            return
        with bar.canvas:
            Color(*PROGRESS_BG)
            Rectangle(pos=bar.pos, size=(w, h))
            if self._total > 0:
                filled = w * self._puzzle_index / self._total
                if filled > 0:
                    Color(*PRIMARY)
                    Rectangle(pos=bar.pos, size=(filled, h))

    def on_pre_leave(self):
        self._cancel_idle_timer()
