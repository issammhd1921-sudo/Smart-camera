[app]
title = Real Camera App
package.name = realcamera
package.domain = org.real
source.include_exts = py,png,jpg,kv,atlas
source.include_dir = .
version = 0.1
requirements = python3,kivy,camera4kivy,gestures4kivy
p4a.hook = camerax_provider/gradle_options.py
android.permissions = CAMERA,RECORD_AUDIO,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 29
orientation = portrait
fullscreen = 1
android.archs = arm64-v8a, armeabi-v7a

[buildozer]
log_level = 2
warn_on_root = 1
