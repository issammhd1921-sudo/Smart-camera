
[app]
title = Smart Camera
package.name = smartcamera
package.domain = org.smartcamera

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 0.1
requirements = python3==3.10.11,kivy==2.3.0

orientation = portrait
fullscreen = 0

android.permissions = CAMERA
android.api = 33
android.minapi = 21
android.ndk = 25b
android.build_tools_version = 33.0.2
android.archs = arm64-v8a
android.accept_sdk_license = True
android.allow_backup = True

p4a.branch = v2024.01.21


[buildozer]
log_level = 2
warn_on_root = 1
