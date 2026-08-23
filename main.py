import os
import time
import numpy as np
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock

# التأكد من إنشاء مجلد المخرجات داخل مسار التطبيق
OUTPUT_DIR = "outputs"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

class SmartCameraRoot(BoxLayout):
    def __init__(self, **kwargs):
        super(SmartCameraRoot, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 40
        self.spacing = 20

        # عنوان رئيسي
        self.title_label = Label(
            text="Smart Camera AI Core",
            font_size='22sp',
            size_hint=(1, 0.2)
        )
        self.add_widget(self.title_label)

        # شاشة عرض الحالة والنتيجة
        self.status_label = Label(
            text="System Ready.\nPress Start to run NumPy pipeline.",
            font_size='16sp',
            halign='center',
            valign='middle',
            size_hint=(1, 0.5)
        )
        self.status_label.bind(size=self.status_label.setter('text_size'))
        self.add_widget(self.status_label)

        # زر تشغيل المعالجة
        self.btn = Button(
            text="Start Processing Stream",
            font_size='18sp',
            size_hint=(1, 0.3)
        )
        self.btn.bind(on_press=self.start_pipeline_async)
        self.add_widget(self.btn)

    def start_pipeline_async(self, instance):
        self.btn.disabled = True
        self.status_label.text = "Processing frames..."
        # جدولة التنفيذ لكي لا تتجمد الواجهة
        Clock.schedule_once(self.run_numpy_pipeline, 0.1)

    def run_numpy_pipeline(self, dt):
        try:
            width, height = 854, 480
            frame_count = 10
            log_text = "[*] Starting NumPy Pipeline...\n"
            
            for i in range(1, frame_count + 1):
                start_time = time.time()
                
                # محاكاة التقاط إطار وعمليات الرياضيات عبر NumPy
                raw_frame = np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)
                processed_frame = np.clip(raw_frame.astype(np.float32) * 1.05, 0, 255).astype(np.uint8)
                
                elapsed = (time.time() - start_time) * 1000.0
                fps_calc = 1000.0 / elapsed if elapsed > 0 else 0
                
                if i == frame_count or i == 1:
                    log_text += f"Frame {i}: {elapsed:.1f}ms (~{fps_calc:.1f} FPS)\n"

            # حفظ عينة مخرجات
            sample_path = os.path.join(OUTPUT_DIR, "captured_snapshot.npy")
            np.save(sample_path, processed_frame)
            
            log_text += f"\n[+] Snapshot saved successfully!\nPath: {OUTPUT_DIR}"
            self.status_label.text = log_text
            
        except Exception as e:
            self.status_label.text = f"[!] Error: str({e})"
            
        finally:
            self.btn.disabled = False

class SmartCameraApp(App):
    def build(self):
        return SmartCameraRoot()

if __name__ == "__main__":
    SmartCameraApp().run()
