"""
Puzzle Alarm App — Kivy entry point.

Run on desktop:
    python main.py

Build APK (on Linux/macOS with Buildozer):
    pip install buildozer cython
    buildozer -v android debug
    # APK appears at bin/ PuzzleAlarm-*.apk

Debug flag triggers the alarm 1s after launch.
"""

import sys

from kivy.app import App
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

from app.app_controller import AppController


class PuzzleAlarmApp(App):
    def build(self):
        Window.size = (360, 720)
        Window.clearcolor = get_color_from_hex("#FFF0F5")
        self.controller = AppController()
        if "--debug" in sys.argv:
            from kivy.clock import Clock
            Clock.schedule_once(lambda _dt: self.controller.debug_trigger_alarm(), 1)
        return self.controller.root

    def on_stop(self):
        self.controller.cleanup()


def main() -> None:
    PuzzleAlarmApp().run()


if __name__ == "__main__":
    main()
