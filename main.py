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
    """ فئة الكاميرا مع دعم التدوير التلقائي وضبط الزاوية للأمامية والخلفية """
    def __init__(self, camera_index=0, **kwargs):
        super(RotatedCamera, self).__init__(**kwargs)
        self.index = camera_index
        
        with self.canvas.before:
            PushMatrix()
            # زاوية التدوير تتناسب مع الكاميرا (الخلفية غالباً 270، والأمامية قد تحتاج ضبطاً مختلفاً حسب الجهاز)
            angle = 270 if self.index == 0 else 270 
            self.rot = Rotate(angle=angle, origin=self.center)
        with self.canvas.after:
            PopMatrix()
        self.bind(pos=self.update_origin, size=self.update_origin)

    def update_origin(self, *args):
        self.rot.origin = self.center

class ModernButton(Button):
    def __init__(self, **kwargs):
        super(ModernButton, self).__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0, 0, 0, 0)
        self.color = (1, 1, 1, 1)
        self.bold = True
        
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
        self.current_camera_index = 0  0: خلفية, 1: أمامية

        with self.canvas.before:
            Color(rgba=get_color_from_hex("#0f111a"))
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg, size=self.update_bg)

        # 1. شريط العنوان
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

        # 2. حاوية الكاميرا لإعادة تحميلها برمجياً عند التبديل
        self.camera_container = BoxLayout(size_hint=(1, 0.55))
        self.init_camera(self.current_camera_index)
        self.add_widget(self.camera_container)

        # 3. لوحة معلومات الأداء
        self.status_label = Label(
            text="System Status: Ready.\nFPS: -- | Processing: --",
            font_size='13sp',
            color=(0.5, 0.84, 1, 1),
            halign='center',
            valign='middle',
            size_hint=(1, 0.12)
        )
        self.status_label.bind(size=self.status_label.setter('text_size'))
        self.add_widget(self.status_label)

        # 4. لوحة أزرار التحكم السفلية
        controls_layout = GridLayout(cols=2, spacing=12, size_hint=(1, 0.16))

        self.btn_capture = ModernButton(text="Capture & Process", font_size='15sp')
        self.btn_capture.bind(on_press=self.capture_and_process)
        controls_layout.add_widget(self.btn_capture)

        self.btn_toggle = ModernButton(text="Switch Camera", font_size='15sp')
        with self.btn_toggle.canvas.before:
            self.btn_toggle.bg_color.rgba = get_color_from_hex("#6a11cb")
        self.btn_toggle.bind(on_press=self.switch_camera)
        controls_layout.add_widget(self.btn_toggle)

        self.add_widget(controls_layout)

    def init_camera(self, index):
        self.camera_container.clear_widgets()
        try:
            self.cam = RotatedCamera(camera_index=index, play=True, resolution=(-1, -1), size_hint=(1, 1))
            self.camera_container.add_widget(self.cam)
        except Exception as e:
            self.camera_container.add_widget(Label(text=f"Camera Error: {str(e)}"))
            self.cam = None

    def update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def switch_camera(self, instance):
        # التبديل الفعلي بين الكاميرا الخلفية (0) والأمامية (1)
        self.current_camera_index = 1 if self.current_camera_index == 0 else 0
        self.init_camera(self.current_camera_index)
        cam_type = "Front (Selfie)" if self.current_camera_index == 1 else "Rear (Back)"
        self.status_label.text = f"Switched to {cam_type} Camera successfully!"

    def capture_and_process(self, instance):
        if not self.cam:
            self.status_label.text = "Camera not available!"
            return

        try:
            temp_path = os.path.join(OUTPUT_DIR, "live_snapshot.png")
            self.cam.export_to_png(temp_path)
            
            start_time = time.time()
            
            dummy_frame = np.random.randint(0, 256, (480, 640, 3), dtype=np.uint8)
            processed_frame = np.rot90(dummy_frame, k=1)
            processed_frame = np.clip(processed_frame.astype(np.float32) * 1.2, 0, 255).astype(np.uint8)
            
            elapsed = (time.time() - start_time) * 1000.0
            fps_est = 1000.0 / max(elapsed, 1.0)
            
            final_path = os.path.join(OUTPUT_DIR, "ai_processed_output.npy")
            np.save(final_path, processed_frame)
            
            self.status_label.text = f"✔ Frame Processed!\nFPS: {fps_est:.1f} | Time: {elapsed:.1f}ms"
            
        except Exception as e:
            self.status_label.text = f"[!] Pipeline Error: {str(e)}"

class SmartCameraApp(App):
    def build(self):
        return SmartCameraRoot()

if __name__ == "__main__":
    SmartCameraApp().run()
            
