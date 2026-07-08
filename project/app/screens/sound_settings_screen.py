"""
Sound settings screen: select an alarm sound file.
On Android, uses Android file chooser via pyjnius when available.
"""

import os

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex
from kivy.metrics import dp

from .base_screen import BaseScreen, BG

PRIMARY = get_color_from_hex("#B96EFF")
PRIMARY_DARK = get_color_from_hex("#9B4FE8")
TEXT = get_color_from_hex("#2D2D2D")
TEXT_SEC = get_color_from_hex("#888888")
SURFACE = get_color_from_hex("#FFFFFF")
BORDER = get_color_from_hex("#E8D5FF")
INPUT_BG = get_color_from_hex("#F8F0FF")


class SoundSettingsScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._build_ui()

    def _build_ui(self) -> None:
        layout = BoxLayout(orientation="vertical")

        # Header
        header = BoxLayout(orientation="horizontal", size_hint_y=None,
                          height=dp(52), padding=[dp(16), dp(12)])
        back_btn = Button(
            text="←", font_size=dp(18),
            background_color=SURFACE, color=TEXT,
            size_hint_x=None, width=dp(44),
        )
        back_btn.bind(on_release=lambda _b: self.controller.show_screen("settings"))
        header.add_widget(back_btn)

        header.add_widget(Label(
            text="알람 소리", font_size=dp(16), bold=True,
            color=TEXT,
        ))
        header.add_widget(Widget(size_hint_x=None, width=dp(44)))
        layout.add_widget(header)

        body = BoxLayout(orientation="vertical", padding=[dp(24), dp(20)],
                         spacing=dp(16))

        body.add_widget(Label(
            text="현재 선택", font_size=dp(11), bold=True,
            color=TEXT_SEC, size_hint_y=None, height=dp(20),
            halign="left", valign="middle",
        ))

        current_frame = BoxLayout(orientation="horizontal", size_hint_y=None,
                                  height=dp(60), spacing=dp(12))
        current_frame.add_widget(Label(
            text="♪", font_size=dp(20), color=PRIMARY,
            size_hint_x=None, width=dp(30),
        ))
        info_box = BoxLayout(orientation="vertical")
        self._current_name = Label(
            text="기본 알람음", font_size=dp(13), bold=True,
            color=TEXT, halign="left", valign="middle",
        )
        info_box.add_widget(self._current_name)
        self._current_info = Label(
            text="내장 비프음", font_size=dp(10),
            color=TEXT_SEC, halign="left", valign="middle",
        )
        info_box.add_widget(self._current_info)
        current_frame.add_widget(info_box)
        body.add_widget(current_frame)

        body.add_widget(Label(
            text="파일 선택", font_size=dp(11), bold=True,
            color=TEXT_SEC, size_hint_y=None, height=dp(20),
            halign="left", valign="middle",
        ))

        pick_btn = Button(
            text="📂  파일 선택하기",
            font_size=dp(13), bold=True,
            background_color=INPUT_BG, color=PRIMARY,
            size_hint_y=None, height=dp(52),
        )
        pick_btn.bind(on_release=lambda _b: self._pick_file())
        body.add_widget(pick_btn)

        body.add_widget(Label(
            text="mp3 파일을 선택하면 알람 소리로 사용합니다.",
            font_size=dp(10), color=TEXT_SEC,
            size_hint_y=None, height=dp(30),
            text_size=(dp(250), None), halign="center",
        ))

        body.add_widget(Widget())

        reset_btn = Button(
            text="기본 알람음으로 초기화",
            font_size=dp(12),
            background_color=BG, color=TEXT_SEC,
            size_hint_y=None, height=dp(44),
        )
        reset_btn.bind(on_release=lambda _b: self._reset_sound())
        body.add_widget(reset_btn)

        layout.add_widget(body)
        self.add_widget(layout)

    def on_show(self) -> None:
        self._refresh()

    def _refresh(self) -> None:
        path = self.controller.settings.sound_path
        if path and os.path.isfile(path):
            self._current_name.text = os.path.basename(path)
            self._current_info.text = path
        else:
            self._current_name.text = "기본 알람음"
            self._current_info.text = "내장 비프음"

    def _pick_file(self) -> None:
        # Try Android file chooser first
        try:
            from jnius import autoclass
            PythonActivity = autoclass("org.kivy.android.PythonActivity")
            Intent = autoclass("android.content.Intent")
            current_activity = PythonActivity.mActivity
            intent = Intent(Intent.ACTION_GET_CONTENT)
            intent.setType("audio/*")
            intent.addCategory(Intent.CATEGORY_OPENABLE)
            chooser = Intent.createChooser(intent, "알람 소리 선택")
            current_activity.startActivityForResult(chooser, 42)
            # Note: result handling requires a broadcast receiver; for simplicity
            # we fall back to Kivy's file chooser on desktop.
            return
        except Exception:
            pass

        # Desktop fallback: Kivy's built-in FileChooser
        self._show_file_chooser()

    def _show_file_chooser(self) -> None:
        from kivy.uix.popup import Popup
        from kivy.uix.filechooser import FileChooserListView

        fc = FileChooserListView(filters=["*.mp3", "*.wav", "*.ogg", "*.m4a"])
        popup = Popup(title="알람 소리 선택", content=fc,
                      size_hint=(0.9, 0.9))
        fc.bind(on_submit=lambda _inst, selection, _touch: self._on_file_chosen(selection, popup))
        popup.open()

    def _on_file_chosen(self, selection, popup) -> None:
        if selection:
            path = selection[0]
            self.controller.settings.sound_path = path
            self.controller.save_settings()
            self._refresh()
        popup.dismiss()

    def _reset_sound(self) -> None:
        self.controller.settings.sound_path = ""
        self.controller.save_settings()
        self._refresh()
