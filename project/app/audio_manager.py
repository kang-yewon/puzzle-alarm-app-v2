"""
Audio playback abstraction layer.

Desktop: pygame.mixer for file playback, numpy-generated beep fallback.
Android: uses android.media.MediaPlayer via pyjnius when available.
"""

import os
import threading

_playing = False
_paused = False
_channel = None
_sound = None
_stop_event = threading.Event()
_loop_thread = None
_current_sound_path = ""
_using_android = False
_android_player = None

try:
    import pygame
    _pygame_available = True
except ImportError:
    _pygame_available = False

_mixer_initialized = False


def _init_mixer() -> bool:
    global _mixer_initialized
    if _mixer_initialized:
        return True
    if not _pygame_available:
        return False
    try:
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        _mixer_initialized = True
        return True
    except Exception:
        return False


def _make_beep_sound():
    try:
        import numpy as np
        sample_rate = 22050
        duration = 0.6
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        wave = (np.sin(2 * np.pi * 880 * t) * 28000).astype(np.int16)
        stereo = np.column_stack([wave, wave])
        return pygame.sndarray.make_sound(stereo)
    except Exception:
        return None


def _init_android() -> bool:
    global _using_android, _android_player
    try:
        from jnius import autoclass
        MediaPlayer = autoclass("android.media.MediaPlayer")
        _android_player = MediaPlayer()
        _using_android = True
        return True
    except Exception:
        return False


def play_alarm(sound_path: str = "") -> None:
    global _playing, _channel, _sound, _loop_thread, _current_sound_path
    if _playing:
        return
    _playing = True
    _paused = False
    _stop_event.clear()
    _current_sound_path = sound_path

    if _init_android() and _android_player is not None:
        try:
            if sound_path and os.path.isfile(sound_path):
                fis = None
                try:
                    from jnius import autoclass
                    File = autoclass("java.io.File")
                    _android_player.setDataSource(File(sound_path).getAbsolutePath())
                except Exception:
                    _android_player.setDataSource(sound_path)
                _android_player.setLooping(True)
                _android_player.prepare()
                _android_player.start()
            return
        except Exception:
            pass

    if _init_mixer():
        if sound_path and os.path.isfile(sound_path):
            try:
                _sound = pygame.mixer.Sound(sound_path)
                _channel = _sound.play(-1)
                return
            except Exception:
                pass
        beep = _make_beep_sound()
        if beep is not None:
            _sound = beep
            _channel = _sound.play(-1)
            return

    _loop_thread = threading.Thread(target=_beep_loop, args=(_stop_event,), daemon=True)
    _loop_thread.start()


def _beep_loop(stop_event: threading.Event) -> None:
    import sys
    while not stop_event.is_set():
        try:
            if sys.platform == "win32":
                import winsound
                winsound.Beep(880, 400)
            else:
                print("\a", end="", flush=True)
        except Exception:
            pass
        stop_event.wait(0.8)


def pause_alarm() -> None:
    global _paused
    if not _playing:
        return
    _paused = True
    if _using_android and _android_player is not None:
        try:
            if _android_player.isPlaying():
                _android_player.pause()
            return
        except Exception:
            pass
    if _channel is not None:
        try:
            _channel.pause()
        except Exception:
            pass
    else:
        _stop_event.set()


def resume_alarm() -> None:
    global _paused, _loop_thread
    if not _playing:
        play_alarm(_current_sound_path)
        return
    _paused = False
    if _using_android and _android_player is not None:
        try:
            if not _android_player.isPlaying():
                _android_player.start()
            return
        except Exception:
            pass
    if _channel is not None:
        try:
            _channel.unpause()
            return
        except Exception:
            pass
    _stop_event.clear()
    _loop_thread = threading.Thread(target=_beep_loop, args=(_stop_event,), daemon=True)
    _loop_thread.start()


def stop_alarm() -> None:
    global _playing, _channel, _sound, _loop_thread, _android_player
    _playing = False
    _stop_event.set()
    if _using_android and _android_player is not None:
        try:
            _android_player.stop()
            _android_player.release()
        except Exception:
            pass
        _android_player = None
    if _channel is not None:
        try:
            _channel.stop()
        except Exception:
            pass
    if _sound is not None:
        try:
            _sound.stop()
        except Exception:
            pass
    _channel = None
    _sound = None
    _loop_thread = None
