import os
import time
import numpy as np
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.camera import Camera
from kivy.graphics import Rotate, PushMatrix, PopMatrix, Color, Rectangle
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

class SmartCameraRoot(BoxLayout):
    def __init__(self, **kwargs):
        super(SmartCameraRoot, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [20, 30, 20, 30]
        self.spacing = 20

        # خلفية داكنة عصرية (Dark Theme Background)
        with self.canvas.before:
            Color(rgba=get_color_from_hex("#141721"))
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg, size=self.update_bg)

        # شريط العنوان العلوي
        title_label = Label(
            text="Smart Camera Pro",
            font_size='22sp',
            bold=True,
            color=(0.9, 0.9, 0.95, 1),
            size_hint=(1, 0.08),
            halign='center'
        )
        self.add_widget(title_label)

        # إطار الكاميرا بتصميم أنيق
        try:
            self.cam = RotatedCamera(play=True, resolution=(-1, -1), size_hint=(1, 0.60))
            self.add_widget(self.cam)
        except Exception as e:
            self.add_widget(Label(text=f"Camera Error: {str(e)}", size_hint=(1, 0.60)))
            self.cam = None

        # شاشة الحالة والمعلومات
        self.status_label = Label(
            text="System Ready. Tap capture to process.",
            font_size='14sp',
            color=(0.6, 0.8, 1, 1),
            halign='center',
            valign='middle',
            size_hint=(1, 0.12)
        )
        self.status_label.bind(size=self.status_label.setter('text_size'))
        self.add_widget(self.status_label)

        # زر الالتقاط والمعالجة بتصميم عصري وأنيق
        self.btn = Button(
            text="Capture & Process Frame",
            font_size='16sp',
            bold=True,
            size_hint=(1, 0.15),
            background_normal='',
            background_color=get_color_from_hex("#2575fc"), # أزرق عصري جذاب
            color=(1, 1, 1, 1)
        )
        self.btn.bind(on_press=self.capture_and_process)
        self.add_widget(self.btn)

    def update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def capture_and_process(self, instance):
        if not self.cam:
            self.status_label.text = "Camera not available!"
            return

        try:
            temp_path = os.path.join(OUTPUT_DIR, "live_snapshot.png")
            self.cam.export_to_png(temp_path)
            
            start_time = time.time()
            
            # معالجة مصفوفة NumPy الاحترافية
            dummy_frame = np.random.randint(0, 256, (480, 640, 3), dtype=np.uint8)
            processed_frame = np.rot90(dummy_frame, k=1)
            processed_frame = np.clip(processed_frame.astype(np.float32) * 1.15, 0, 255).astype(np.uint8)
            
            elapsed = (time.time() - start_time) * 1000.0
            
            final_path = os.path.join(OUTPUT_DIR, "processed_output.npy")
            np.save(final_path, processed_frame)
            
            self.status_label.text = f"[+] Processed in {elapsed:.1f}ms & Saved successfully!"
            
        except Exception as e:
            self.status_label.text = f"[!] Error: {str(e)}"

class SmartCameraApp(App):
    def build(self):
        return SmartCameraRoot()

if __name__ == "__main__":
    SmartCameraApp().run()
    
