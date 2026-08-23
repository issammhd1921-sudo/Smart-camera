import os
import time
import numpy as np
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.camera import Camera

OUTPUT_DIR = "outputs"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

class SmartCameraRoot(BoxLayout):
    def __init__(self, **kwargs):
        super(SmartCameraRoot, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 15
        self.spacing = 10

        # عنوان التطبيق
        self.add_widget(Label(
            text="Smart Camera Pro",
            font_size='20sp',
            size_hint=(1, 0.08)
        ))

        # عنصر الكاميرا الحقيقية
        try:
            self.cam = Camera(play=True, resolution=(-1, -1), size_hint=(1, 0.55))
            self.add_widget(self.cam)
        except Exception as e:
            self.add_widget(Label(text=f"Camera Error: {str(e)}", size_hint=(1, 0.55)))
            self.cam = None

        # شاشة عرض الحالة والمعلومات
        self.status_label = Label(
            text="System Ready. Tap capture to process.",
            font_size='13sp',
            halign='center',
            valign='middle',
            size_hint=(1, 0.12)
        )
        self.status_label.bind(size=self.status_label.setter('text_size'))
        self.add_widget(self.status_label)

        # لوحة أزرار تحكم متقدمة
        controls_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, 0.15))
        
        # زر التقاط ومعالجة
        self.btn_capture = Button(text="Capture & Process", font_size='14sp')
        self.btn_capture.bind(on_press=self.capture_and_process)
        controls_layout.add_widget(self.btn_capture)

        # زر تبديل الكاميرا (أمامية / خلفية)
        self.btn_switch = Button(text="Switch Camera", font_size='14sp')
        self.btn_switch.bind(on_press=self.switch_camera_index)
        controls_layout.add_widget(self.btn_switch)

        self.add_widget(controls_layout)

    def switch_camera_index(self, instance):
        if self.cam:
            # تبديل مؤشر الكاميرا بين 0 (خلفية) و 1 (أمامية)
            current_index = getattr(self.cam, 'index', 0)
            new_index = 1 if current_index == 0 else 0
            self.cam.index = new_index
            self.status_label.text = f"Switched to camera index: {new_index}"

    def capture_and_process(self, instance):
        if not self.cam:
            self.status_label.text = "Camera not available!"
            return

        try:
            temp_path = os.path.join(OUTPUT_DIR, "live_snapshot.png")
            self.cam.export_to_png(temp_path)
            
            start_time = time.time()
            
            # محاكاة تحويل الصورة الملتقطة الحقيقية إلى مصفوفة NumPy مع تصحيح الاتجاه
            # (هنا يمكنك لاحقاً قراءة ملف PNG وتحويله لمصفوفة عبر PIL أو OpenCV)
            dummy_frame = np.random.randint(0, 256, (480, 640, 3), dtype=np.uint8)
            
            # تصحيح الاتجاه والدوران لتجنب مشكلة الصورة المقلوبة
            processed_frame = np.rot90(dummy_frame, k=1)
            processed_frame = np.clip(processed_frame.astype(np.float32) * 1.15, 0, 255).astype(np.uint8)
            
            elapsed = (time.time() - start_time) * 1000.0
            
            final_path = os.path.join(OUTPUT_DIR, "final_processed.npy")
            np.save(final_path, processed_frame)
            
            self.status_label.text = f"[+] Processed in {elapsed:.1f}ms & Saved successfully!"
            
        except Exception as e:
            self.status_label.text = f"[!] Error: {str(e)}"

class SmartCameraApp(App):
    def build(self):
        return SmartCameraRoot()

if __name__ == "__main__":
    SmartCameraApp().run()
