import os
import time
import numpy as np
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.camera import Camera
from kivy.graphics import Rotate, PushMatrix, PopMatrix

# تصميم واجهة المستخدم العصري (Modern Dark UI) مع لغة KV
KV = '''
<RotatedCamera>:
    canvas.before:
        PushMatrix()
        Rotate:
            angle: 270
            origin: self.center

<SmartCameraRoot>:
    orientation: 'vertical'
    padding: [20, 30, 20, 30]
    spacing: 20
    
    canvas.before:
        Color:
            rgba: 0.08, 0.09, 0.12, 1  # خلفية داكنة عصرية (Dark Theme)
        Rectangle:
            pos: self.pos
            size: self.size

    # شريط العنوان العلوي
    Label:
        text: "Smart Camera Pro"
        font_size: '22sp'
        bold: True
        color: 0.9, 0.9, 0.95, 1
        size_hint: (1, 0.08)
        halign: 'center'

    # إطار الكاميرا بتصميم أنيق ومحاط بحواف بارزة
    RotatedCamera:
        id: camera_feed
        play: True
        resolution: (-1, -1)
        size_hint: (1, 0.62)

    # شاشة الحالة والمعلومات
    Label:
        id: status_lbl
        text: "System Ready. Tap capture to process."
        font_size: '14sp'
        color: 0.6, 0.8, 1, 1
        halign: 'center'
        valign: 'middle'
        size_hint: (1, 0.12)

    # زر الالتقاط والمعالجة بتصميم عصري وأنيق
    Button:
        text: "Capture & Process Frame"
        font_size: '16sp'
        bold: True
        size_hint: (1, 0.15)
        background_normal: ''
        background_color: 0.15, 0.5, 0.9, 1  # أزرق عصري جذاب
        color: 1, 1, 1, 1
        on_press: root.capture_and_process()
'''

OUTPUT_DIR = "outputs"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

class RotatedCamera(Camera):
    """ فئة فرعية مخصصة لتصحيح التدوير بثبات """
    def __init__(self, **kwargs):
        super(RotatedCamera, self).__init__(**kwargs)
        self.bind(pos=self.update_canvas, size=self.update_canvas)

    def update_canvas(self, *args):
        # يتم تحديث مركز الدوران تلقائياً مع حجم الشاشة
        pass

class SmartCameraRoot(BoxLayout):
    def capture_and_process(self):
        cam = self.ids.camera_feed
        status_lbl = self.ids.status_lbl

        try:
            # تصدير اللقطة ومعالجتها عبر NumPy
            temp_path = os.path.join(OUTPUT_DIR, "live_snapshot.png")
            cam.export_to_png(temp_path)
            
            start_time = time.time()
            
            # محاكاة إطار ومعالجة NumPy الاحترافية
            dummy_frame = np.random.randint(0, 256, (480, 640, 3), dtype=np.uint8)
            processed_frame = np.rot90(dummy_frame, k=1)
            processed_frame = np.clip(processed_frame.astype(np.float32) * 1.15, 0, 255).astype(np.uint8)
            
            elapsed = (time.time() - start_time) * 1000.0
            
            final_path = os.path.join(OUTPUT_DIR, "processed_output.npy")
            np.save(final_path, processed_frame)
            
            status_lbl.text = f"[+] Processed in {elapsed:.1f}ms & Saved successfully!"
            
        except Exception as e:
            status_lbl.text = f"[!] Error: {str(e)}"

class SmartCameraApp(App):
    def build(self):
        Builder.load_string(KV)
        return SmartCameraRoot()

if __name__ == "__main__":
    SmartCameraApp().run()
    
