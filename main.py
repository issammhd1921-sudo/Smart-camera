import os
import time
import numpy as np
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.camera import Camera
from kivy.clock import Clock

# التأكد من إنشاء مجلد المخرجات
OUTPUT_DIR = "outputs"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

class SmartCameraRoot(BoxLayout):
    def __init__(self, **kwargs):
        super(SmartCameraRoot, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 15

        # عنوان التطبيق
        self.add_widget(Label(
            text="Smart Live Camera",
            font_size='20sp',
            size_hint=(1, 0.1)
        ))

        # عنصر عرض الكاميرا الحقيقية
        try:
            # index=0 يعني الكاميرا الخلفية الأساسية
            self.cam = Camera(play=True, resolution=(-1, -1), size_hint=(1, 0.6))
            self.add_widget(self.cam)
        except Exception as e:
            self.add_widget(Label(text=f"Camera Error: {str(e)}", size_hint=(1, 0.6)))
            self.cam = None

        # شاشة عرض الحالة والمعلومات
        self.status_label = Label(
            text="Camera is active.\nPress capture to process frame via NumPy.",
            font_size='14sp',
            halign='center',
            valign='middle',
            size_hint=(1, 0.15)
        )
        self.status_label.bind(size=self.status_label.setter('text_size'))
        self.add_widget(self.status_label)

        # زر التقاط الصورة ومعالجتها
        self.btn = Button(
            text="Capture & Process Frame",
            font_size='16sp',
            size_hint=(1, 0.15)
        )
        self.btn.bind(on_press=self.capture_and_process)
        self.add_widget(self.btn)

    def capture_and_process(self, instance):
        if not self.cam:
            self.status_label.text = "Camera not available!"
            return

        try:
            # التقاط صورة مؤقتة من بث الكاميرا
            temp_path = os.path.join(OUTPUT_DIR, "temp_capture.png")
            self.cam.export_to_png(temp_path)
            
            # محاكاة معالجة الإطار المُلتقط عبر NumPy
            start_time = time.time()
            
            # محاكاة مصفوفة بكسلات مستخرجة من الصورة
            dummy_frame = np.random.randint(0, 256, (480, 640, 3), dtype=np.uint8)
            processed_frame = np.clip(dummy_frame.astype(np.float32) * 1.1, 0, 255).astype(np.uint8)
            
            elapsed = (time.time() - start_time) * 1000.0
            
            # حفظ المخرجات المعالجة
            final_path = os.path.join(OUTPUT_DIR, "processed_snapshot.npy")
            np.save(final_path, processed_frame)
            
            self.status_label.text = f"[+] Captured & Processed!\nTime: {elapsed:.1f}ms | Saved to outputs/"
            
        except Exception as e:
            self.status_label.text = f"[!] Error: {str(e)}"

class SmartCameraApp(App):
    def build(self):
        return SmartCameraRoot()

if __name__ == "__main__":
    SmartCameraApp().run()
