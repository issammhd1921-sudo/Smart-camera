[app]

# (str) Title of your application
title = Real Camera App

# (str) Package name
package.name = realcamera

# (str) Package domain (needed for android packaging)
package.domain = org.real

# (str) Source directory
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,kv,atlas

# (str) Application version
version = 0.1

# (list) Application requirements
requirements = python3==3.10.11,kivy==2.3.0,camera4kivy,gestures4kivy

# (str) CameraX / gradle hook
p4a.hook = camerax_provider/gradle_options.py

# (list) Android permissions
android.permissions = CAMERA,RECORD_AUDIO,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (int) Target Android API
android.api = 33

# (int) Minimum Android API
android.minapi = 29

# (str) Android NDK version
android.ndk = 25b

# (str) Build tools version
android.build_tools_version = 33.0.2

# (bool) Accept SDK licenses automatically
android.accept_sdk_license = True

# (list) Target architectures
android.archs = arm64-v8a,armeabi-v7a

# (str) Screen orientation
orientation = portrait

# (bool) Fullscreen
fullscreen = 1

# (str) python-for-android branch
p4a.branch = v2024.01.21


[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

