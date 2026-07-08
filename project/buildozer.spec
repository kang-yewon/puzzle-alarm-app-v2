[app]

# (str) Title of your application
title = PuzzleAlarm

# (str) Package name
package.name = puzzlealarm

# (str) Package domain (needed for Android package)
package.domain = org.puzzlealarm

# (str) Source code directory
source.dir = .

# (str) Source files to include (let buildozer find main.py + app/)
source.include_exts = py,png,jpg,kv,atlas,ttf,otf,mp3,wav,ogg,m4a

# (list) Source files to exclude
source.exclude_exts = spec,txt,md,lock

# (list) Directory to exclude
source.exclude_dirs = .git,__pycache__,.bolt

# (str) Application versioning
version = 1.0.0

# (str) Application versioning (method 2)
# version.regex = __version__ = ['"](.*)['"]
# version.filename = main.py

# (list) Application requirements
# Kivy + pygame for audio + numpy for beep fallback
requirements = python3,kivy,pygame,numpy,pyjnius

# (str) Custom source folders for requirements (let buildozer handle recipes)
# requirements.source.kivy = ../../kivy

# (str) Presplash image
# presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon
# icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientations
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = WAKE_LOCK,VIBRATE

# (int) Android API to use
android.api = 34

# (int) Minimum API required
android.minapi = 21

# (int) Android SDK version to use
android.sdk = 34

# (str) Android NDK version to use
android.ndk = 23b

# (bool) Use --private data storage (True) or --dir location (False)
android.private_storage = True

# (str) Android NDK compilers to target
# android.ndk_api = 21

# (bool) Skip byte compile for .py files
no-byte-compile-python = False

# (str) The Android arch to build for
android.arch = arm64-v8a

# (bool) Enable AndroidX
android.enable_androidx = True

# (bool) Enable gradle
android.gradle = True

# (bool) Copy library instead of making a .pyd
# android.copy_libs = 1

# (str) The log level for the build
log_level = 2

# (str) Logger name
# log_name = puzzlealarm

# (bool) Show the build progress
# show_progress = True

# (bool) Can be overridden by the --debug flag
# debug = False

# (bool) Use python-crouts for logging
# log_enable = 1

# (bool) Allow the app to be installed on the internal storage
# android.allow_backup = 1

# (bool) Allow the app to be installed on the external storage
# android.install_on_external = 0

# (bool) Skip the build of the python recipe
# python.skip_build = 0

# (bool) Use the python-for-android build system
# p4a.branch = master

# (bool) Use the python-for-android bootstrap
# p4a.bootstrap = sdl2

# (str) URL to a custom p4a source
# p4a.source_dir =

# (str) URL to a custom p4a fork
# p4a.fork =

# (str) URL to a custom p4a branch
# p4a.branch =

# (str) URL to a custom p4a commit
# p4a.commit =

# (bool) Use the buildozer build system
# buildozer = True

# (bool) Skip the build of the kivy recipe
# kivy.skip_build = 0

# (str) URL to a custom kivy source
# kivy.source_dir =

# (str) URL to a custom kivy fork
# kivy.fork =

# (str) URL to a custom kivy branch
# kivy.branch =

# (str) URL to a custom kivy commit
# kivy.commit =

# (bool) Use the kivy launcher
# kivy.launcher = 0

# (bool) Use the kivy garden
# garden = True

# (bool) Use the kivy garden for the build
# garden.skip_build = 0

# (bool) Use the kivy garden for the build
# garden.requirements =

# (bool) Use the kivy garden for the build
# garden.url =

# (bool) Use the kivy garden for the build
# garden.branch =

# (bool) Use the kivy garden for the build
# garden.commit =

# (bool) Use the kivy garden for the build
# garden.fork =

# (bool) Use the kivy garden for the build
# garden.source_dir =

# (bool) Use the kivy garden for the build
# garden.recipe =

# (bool) Use the kivy garden for the build
# garden.recipe_url =

# (bool) Use the kivy garden for the build
# garden.recipe_branch =

# (bool) Use the kivy garden for the build
# garden.recipe_commit =

# (bool) Use the kivy garden for the build
# garden.recipe_fork =

# (bool) Use the kivy garden for the build
# garden.recipe_source_dir =

# (bool) Use the kivy garden for the build
# garden.recipe_requirements =

# (bool) Use the kivy garden for the build
# garden.recipe_url =

# (bool) Use the kivy garden for the build
# garden.recipe_branch =

# (bool) Use the kivy garden for the build
# garden.recipe_commit =

# (bool) Use the kivy garden for the build
# garden.recipe_fork =

# (bool) Use the kivy garden for the build
# garden.recipe_source_dir =

# (bool) Use the kivy garden for the build
# garden.recipe_requirements =

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) If 1, warnings are shown when a deprecated feature is used
warn_on_deprecated = 1

# (str) Path to the buildozer config file
# config = buildozer.spec

# (str) Path to the buildozer cache directory
# cache = .buildozer

# (str) Path to the buildozer bin directory
# bin = bin

# (str) Path to the buildozer build directory
# build = .buildozer

# (str) Path to the buildozer app directory
# app = .

# (str) Path to the buildozer global config directory
# global_config = ~/.config/buildozer

# (str) Path to the buildozer global cache directory
# global_cache = ~/.cache/buildozer
