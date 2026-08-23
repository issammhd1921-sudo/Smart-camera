[app]
title = Smart Camera
package.name = smartcamera
package.domain = org.smartcamera

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 0.1
requirements = python3,kivy

orientation = portrait
fullscreen = 0

android.permissions = CAMERA,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.build_tools_version = 33.0.2
android.accept_sdk_license = True
android.archs = arm64-v8a,armeabi-v7a
p4a.branch = v2024.01.21

[buildozer]
log_level = 2
warn_on_root = 1
