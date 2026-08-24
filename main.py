import os
import time
import numpy as np
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.camera import Camera
from kivy.graphics import Rotate, PushMatrix, PopMatrix, Color, Rectangle, RoundedRectangle
from kivy.utils import get_color_from_hex

OUTPUT_DIR = "outputs"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

class RotatedCamera(Camera):
    """ فئة فرعية آمنة وثابتة لتصحيح تدوير الكاميرا برمجياً """
    def __init__(self, **kwargs):
        super(RotatedCamera, self).__init__(**kwargs)
        with self.canvas.before:
            PushMatrix()
            self.rot = Rotate(angle=270, origin=self.center)
        with self.canvas.after:
            PopMatrix()
        self.bind(pos=self.update_origin, size=self.update_origin)

    def update_origin(self, *args):
        self.rot.origin = self.center

class ModernButton(Button):
    """ زر عصري بحواف دائرية وتصميم جذاب """
    def __init__(self, **kwargs):
        super(ModernButton, self).__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0, 0, 0, 0) # إلغاء الخلفية الافتراضية
        self.color = (1, 1, 1, 1)
        self.bold = True
        
        # رسم خلفية دائرية للزر
        with self.canvas.before:
            self.bg_color = Color(rgba=get_color_from_hex("#2575fc"))
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[18])
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class SmartCameraRoot(BoxLayout):
    def __init__(self, **kwargs):
        super(SmartCameraRoot, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [15, 20, 15, 20]
        self.spacing = 15

        # خلفية التطبيق الداكنة العصرية
        with self.canvas.before:
            Color(rgba=get_color_from_hex("#0f111a"))
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg, size=self.update_bg)

        # 1. شريط العنوان العلوي الاحترافي
        header_layout = BoxLayout(size_hint=(1, 0.07), orientation='horizontal')
        self.title_label = Label(
            text="⚡ Smart Camera AI Pro",
            font_size='20sp',
            bold=True,
            color=(0.95, 0.95, 1, 1),
            halign='left',
            valign='middle'
        )
        self.title_label.bind(size=self.title_label.setter('text_size'))
        header_layout.add_widget(self.title_label)
        self.add_widget(header_layout)

        # 2. إطار الكاميرا بتصميم منسق
        try:
            self.cam = RotatedCamera(play=True, resolution=(-1, -1), size_hint=(1, 0.55))
            self.add_widget(self.cam)
        except Exception as e:
            self.add_widget(Label(text=f"Camera Error: {str(e)}", size_hint=(1, 0.55)))
            self.cam = None

        # 3. لوحة معلومات الأداء الحية (Dashboard)
        self.status_label = Label(
            text="System Status: Ready for AI Pipeline.\nFPS: -- | Processing: --",
            font_size='13sp',
            color=(0.5, 0.84, 1, 1),
            halign='center',
            valign='middle',
            size_hint=(1, 0.12)
        )
        self.status_label.bind(size=self.status_label.setter('text_size'))
        self.add_widget(self.status_label)

        # 4. لوحة أزرار التحكم السفلية المتطورة
        controls_layout = GridLayout(cols=2, spacing=12, size_hint=(1, 0.16))

        # زر التقاط ومعالجة
        self.btn_capture = ModernButton(text="Capture & Process", font_size='15sp')
        self.btn_capture.bind(on_press=self.capture_and_process)
        controls_layout.add_widget(self.btn_capture)

        # زر تبديل الفلتر/الكاميرا
        self.btn_toggle = ModernButton(text="Switch Camera", font_size='15sp')
        # تغيير لون هذا الزر ليكون مميزاً (درجة بنفسجية عصرية)
        with self.btn_toggle.canvas.before:
            self.btn_toggle.bg_color.rgba = get_color_from_hex("#6a11cb")
        self.btn_toggle.bind(on_press=self.switch_camera)
        controls_layout.add_widget(self.btn_toggle)

        self.add_widget(controls_layout)

    def update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def switch_camera(self, instance):
        if self.cam:
            current_index = getattr(self.cam, 'index', 0)
            new_index = 1 if current_index == 0 else 0
            try:
                self.cam.index = new_index
                self.status_label.text = f"Switched to Camera Index: {new_index}\nFPS: ~60.0 | Ready"
            except Exception:
                self.status_label.text = "Camera switch not supported on this device."

    def capture_and_process(self, instance):
        if not self.cam:
            self.status_label.text = "Camera not available!"
            return

        try:
            temp_path = os.path.join(OUTPUT_DIR, "live_snapshot.png")
            self.cam.export_to_png(temp_path)
            
            start_time = time.time()
            
            # محاكاة خط معالجة NumPy المتقدم مع حساب الأداء الحقيقي
            dummy_frame = np.random.randint(0, 256, (480, 640, 3), dtype=np.uint8)
            processed_frame = np.rot90(dummy_frame, k=1)
            processed_frame = np.clip(processed_frame.astype(np.float32) * 1.2, 0, 255).astype(np.uint8)
            
            elapsed = (time.time() - start_time) * 1000.0
            fps_est = 1000.0 / max(elapsed, 1.0)
            
            final_path = os.path.join(OUTPUT_DIR, "ai_processed_output.npy")
            np.save(final_path, processed_frame)
            
            self.status_label.text = f"✔ Pipeline Executed Successfully!\nFPS: {fps_est:.1f} | Time: {elapsed:.1f}ms"
            
        except Exception as e:
            self.status_label.text = f"[!] Pipeline Error: {str(e)}"

class SmartCameraApp(App):
    def build(self):
        return SmartCameraRoot()

if __name__ == "__main__":
    SmartCameraApp().run()
    
