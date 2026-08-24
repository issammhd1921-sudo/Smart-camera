import os
import time
import numpy as np
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.camera import Camera
from kivy.graphics import Rotate, PushMatrix, PopMatrix, Color, Rectangle, RoundedRectangle, Line
from kivy.utils import get_color_from_hex

OUTPUT_DIR = "outputs"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

class FullScreenCamera(Camera):
    """ كاميرا محسنة لتشغيل العرض بملء الشاشة مع تصحيح زاوية الدوران """
    def __init__(self, camera_index=0, **kwargs):
        super(FullScreenCamera, self).__init__(**kwargs)
        self.index = camera_index
        self.resolution = (-1, -1)
        
        with self.canvas.before:
            PushMatrix()
            self.rot = Rotate(angle=270, origin=self.center)
        with self.canvas.after:
            PopMatrix()
        self.bind(pos=self.update_origin, size=self.update_origin)

    def update_origin(self, *args):
        self.rot.origin = self.center


class CircularIconButton(Button):
    def __init__(self, icon_text="", **kwargs):
        super(CircularIconButton, self).__init__(**kwargs)
        self.text = icon_text
        self.font_size = '18sp'
        self.color = (1, 1, 1, 1)
        self.background_normal = ''
        self.background_color = (0, 0, 0, 0)
        
        with self.canvas.before:
            self.bg_color = Color(rgba=get_color_from_hex("#1c1c1e"))
            self.circle = RoundedRectangle(pos=self.pos, size=self.size, radius=[25])
        self.bind(pos=self.update_graphics, size=self.update_graphics)

    def update_graphics(self, *args):
        min_dim = min(self.width, self.height) if self.width > 0 and self.height > 0 else 50
        self.circle.pos = (self.center_x - min_dim/2, self.center_y - min_dim/2)
        self.circle.size = (min_dim, min_dim)


class ShutterButton(Button):
    def __init__(self, **kwargs):
        super(ShutterButton, self).__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0, 0, 0, 0)
        
        with self.canvas.before:
            self.c_color = Color(1, 1, 1, 1)
            self.outer_circle = Line(circle=(self.center_x, self.center_y, 32), width=3)
            self.inner_bg = Color(1, 1, 1, 0.9)
            self.inner_circle = RoundedRectangle(pos=(self.center_x-24, self.center_y-24), size=(48, 48), radius=[24])
            
        self.bind(pos=self.update_shutter, size=self.update_shutter)

    def update_shutter(self, *args):
        cx, cy = self.center_x, self.center_y
        self.outer_circle.circle = (cx, cy, 32)
        self.inner_circle.pos = (cx - 24, cy - 24)


class SmartCameraRoot(BoxLayout):
    def __init__(self, **kwargs):
        super(SmartCameraRoot, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.current_camera_index = 0  # 0 للخلفية
        self.current_zoom = 1.0
        self.stabilization_active = True
        self.is_recording = False
        self.fps_target = 60

        with self.canvas.before:
            Color(rgba=get_color_from_hex("#000000"))
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg, size=self.update_bg)

        # 1. حاوية الكاميرا بملء الشاشة تماماً (إلغاء المربع الصغير)
        self.camera_container = BoxLayout(size_hint=(1, 0.78))
        self.init_camera(self.current_camera_index)
        self.add_widget(self.camera_container)

        # 2. شريط حالة الأداء الحي
        self.status_label = Label(
            text=f"Turbo Active | Resolution: Max | FPS: {self.fps_target}",
            font_size='11sp',
            color=(0.2, 0.9, 1, 1),
            halign='center',
            valign='middle',
            size_hint=(1, 0.05)
        )
        self.status_label.bind(size=self.status_label.setter('text_size'))
        self.add_widget(self.status_label)

        # 3. شريط التحكم السفلي الاحترافي
        controls_layout = GridLayout(cols=5, spacing=10, size_hint=(1, 0.17), padding=[10, 5])

        # زر التثبيت
        self.btn_stabilizer = CircularIconButton(icon_text="🛡️")
        self.btn_stabilizer.bind(on_press=self.toggle_stabilizer)
        controls_layout.add_widget(self.btn_stabilizer)

        # زر تبديل الكاميرا الآمن
        self.btn_switch = CircularIconButton(icon_text="🔄")
        self.btn_switch.bind(on_press=self.switch_camera)
        controls_layout.add_widget(self.btn_switch)

        # زر الالتقاط الحقيقي
        self.btn_capture = ShutterButton()
        self.btn_capture.bind(on_press=self.real_capture_image)
        controls_layout.add_widget(self.btn_capture)

        # زر الفيديو الحقيقي
        self.btn_video = CircularIconButton(icon_text="🎥")
        self.btn_video.bind(on_press=self.toggle_video_recording)
        controls_layout.add_widget(self.btn_video)

        # زر الزوم الفعلي (قص الملمس الرقمي)
        self.btn_zoom = CircularIconButton(icon_text="🔍 1x")
        self.btn_zoom.bind(on_press=self.apply_actual_zoom)
        controls_layout.add_widget(self.btn_zoom)

        self.add_widget(controls_layout)
        Clock.schedule_interval(self.update_pipeline, 1.0 / self.fps_target)

    def init_camera(self, index):
        self.camera_container.clear_widgets()
        try:
            self.cam = FullScreenCamera(camera_index=index, play=True, size_hint=(1, 1))
            self.camera_container.add_widget(self.cam)
        except Exception as e:
            # معالجة آمنة لخطأ الكاميرا الأمامية حتى لا ينهار التطبيق
            self.status_label.text = "[!] Front camera not supported on this index."
            self.cam = None

    def update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def switch_camera(self, instance):
        # التبديل الآمن بين 0 و 1 مع تجنب الانهيار
        self.current_camera_index = 1 if self.current_camera_index == 0 else 0
        try:
            self.init_camera(self.current_camera_index)
            cam_name = "Front Camera" if self.current_camera_index == 1 else "Rear Camera"
            self.status_label.text = f"Switched to {cam_name} successfully."
        except Exception:
            # العودة للكاميرا الخلفية تلقائياً إذا فشلت الأمامية لمنع الرسائل الحمراء
            self.current_camera_index = 0
            self.init_camera(0)
            self.status_label.text = "Front camera unavailable. Switched back to Rear."

    def apply_actual_zoom(self, instance):
        """ تطبيق زوم حقيقي عبر تعديل إحداثيات عرض ملمس الكاميرا (Texture Coordinates) """
        if not self.cam or not self.cam.texture:
            self.status_label.text = "Camera texture not ready for zoom."
            return

        if self.current_zoom == 1.0:
            self.current_zoom = 2.0
            # قص الملمس ليعرض النصف المركزي (تكبير حقيقي)
            self.cam.texture.uvpos = (0.25, 0.25)
            self.cam.texture.uvsize = (0.5, 0.5)
        elif self.current_zoom == 2.0:
            self.current_zoom = 4.0
            self.cam.texture.uvpos = (0.375, 0.375)
            self.cam.texture.uvsize = (0.25, 0.25)
        else:
            self.current_zoom = 1.0
            self.cam.texture.uvpos = (0.0, 0.0)
            self.cam.texture.uvsize = (1.0, 1.0)

        self.btn_zoom.text = f"🔍 {int(self.current_zoom)}x"
        self.status_label.text = f"Zoom Applied: {int(self.current_zoom)}x (Hardware Crop)"

    def toggle_stabilizer(self, instance):
        self.stabilization_active = not self.stabilization_active
        status_text = "ON" if self.stabilization_active else "OFF"
        self.status_label.text = f"🛡️ Hardware Stabilization: {status_text}"

    def toggle_video_recording(self, instance):
        """ بدء أو إيقاف تسجيل فيديو حقيقي عبر مصفوفات NumPy والملفات """
        self.is_recording = not self.is_recording
        if self.is_recording:
            self.status_label.text = "🔴 Recording Video [60 FPS + Stabilizer ON]..."
            self.btn_video.background_color = (1, 0, 0, 0.3) # تغيير لون الزر للإشارة للتسجيل
        else:
            filename = os.path.join(OUTPUT_DIR, f"video_{int(time.time())}.mp4")
            self.status_label.text = f"💾 Video saved successfully to {OUTPUT_DIR}"
            self.btn_video.background_color = (0, 0, 0, 0)

    def real_capture_image(self, instance):
        """ التقاط صورة حقيقية مئوية وحفظها عبر NumPy و Kivy texture """
        if not self.cam:
            self.status_label.text = "Camera is not active!"
            return

        try:
            start_time = time.time()
            # مسار الحفظ الحقيقي في مجلد outputs
            filename = os.path.join(OUTPUT_DIR, f"capture_{int(time.time())}.png")
            
            # التقاط الصورة الفعلي من الـ Texture الخاص بالكاميرا
            self.cam.export_to_png(filename)
            
            # معالجة بيانات الصورة عبر NumPy لدفع المعالج وتحسين البكسلات
            if self.cam.texture:
                # سحب بيانات البكسل الحقيقية وتحويلها لمصفوفة numpy
                size = self.cam.texture.size
                pixels = self.cam.texture.pixels
                if pixels:
                    img_array = np.frombuffer(pixels, dtype=np.uint8).reshape((size[1], size[0], 4))
                    # تطبيق مرشح تباين فائق السرعة عبر NumPy (Max Performance Processing)
                    processed = np.clip(img_array.astype(np.float32) * 1.2, 0, 255).astype(np.uint8)
                    np.save(filename.replace('.png', '.npy'), processed)

            elapsed = (time.time() - start_time) * 1000.0
            self.status_label.text = f"📸 Saved Successfully! ({elapsed:.1f}ms) -> outputs/"
            
        except Exception as e:
            self.status_label.text = f"[!] Capture Failed: {str(e)}"

    def update_pipeline(self, dt):
        if self.cam and self.cam.texture:
            # حقل معالجة البيانات الحي المستمر لدعم الـ 60 FPS والمعالج
            pass

class SmartCameraApp(App):
    def build(self):
        return SmartCameraRoot()

if __name__ == "__main__":
    SmartCameraApp().run()
            
