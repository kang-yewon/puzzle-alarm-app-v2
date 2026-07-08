"""
AppController: owns the ScreenManager, alarm manager, and navigation.
Single source of truth for app state.
"""

from typing import Literal

from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager

from .models import AlarmSettings
from . import storage, audio_manager
from .alarm_manager import AlarmManager

ScreenName = Literal["home", "settings", "ringing", "puzzle", "complete", "sound"]


class AppController:
    def __init__(self) -> None:
        self.settings: AlarmSettings = storage.load_settings()
        self.root = ScreenManager()
        self._build_screens()
        self._alarm_manager = AlarmManager(on_alarm_trigger=self._on_alarm_trigger)
        self._alarm_manager.start(self.settings)
        self.show_screen("home")

    def _build_screens(self) -> None:
        from .screens.home_screen import HomeScreen
        from .screens.settings_screen import SettingsScreen
        from .screens.alarm_ringing_screen import AlarmRingingScreen
        from .screens.puzzle_screen import PuzzleScreen
        from .screens.complete_screen import CompleteScreen
        from .screens.sound_settings_screen import SoundSettingsScreen

        self._screens = {
            "home": HomeScreen(name="home", controller=self),
            "settings": SettingsScreen(name="settings", controller=self),
            "ringing": AlarmRingingScreen(name="ringing", controller=self),
            "puzzle": PuzzleScreen(name="puzzle", controller=self),
            "complete": CompleteScreen(name="complete", controller=self),
            "sound": SoundSettingsScreen(name="sound", controller=self),
        }
        for screen in self._screens.values():
            self.root.add_widget(screen)

    def show_screen(self, name: ScreenName) -> None:
        screen = self._screens[name]
        self.root.current = name
        screen.on_show()

    def _on_alarm_trigger(self) -> None:
        Clock.schedule_once(lambda _dt: self._alarm_fire())

    def _alarm_fire(self) -> None:
        audio_manager.play_alarm(self.settings.sound_path)
        self.show_screen("ringing")

    def on_puzzles_complete(self) -> None:
        audio_manager.stop_alarm()
        self.show_screen("home")

    def save_settings(self) -> None:
        storage.save_settings(self.settings)
        self._alarm_manager.update_settings(self.settings)

    def cleanup(self) -> None:
        self._alarm_manager.stop()
        audio_manager.stop_alarm()

    def debug_trigger_alarm(self) -> None:
        self._alarm_fire()
