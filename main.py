import os
import time
import numpy as np
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

# التأكد من إنشاء مجلد المخرجات
OUTPUT_DIR = "outputs"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

class SmartCameraRoot(BoxLayout):
    def __init__(self, **kwargs):
        super(SmartCameraRoot, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 30
        self.spacing = 20

        # عنوان في الواجهة
        self.label = Label(
            text="Smart Camera Ready",
            font_size='24sp',
            size_hint=(1, 0.5)
        )
        self.add_widget(self.label)

        # زر لبدء المحاكاة والمعالجة
        self.btn = Button(
            text="Start Stream & Process",
            font_size='20sp',
            size_hint=(1, 0.5)
        )
        self.btn.bind(on_press=self.run_simulation)
        self.add_widget(self.btn)

    def run_simulation(self, instance):
        self.label.text = "Processing frames..."
        # محاكاة المعالجة
        width, height = 854, 480
        raw_frame = np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)
        processed_frame = np.clip(raw_frame.astype(np.float32) * 1.05, 0, 255).astype(np.uint8)
        
        sample_path = os.path.join(OUTPUT_DIR, "captured_snapshot.npy")
        np.save(sample_path, processed_frame)
        
        self.label.text = "Done! Snapshot Saved."

class SmartCameraApp(App):
    def build(self):
        return SmartCameraRoot()

if __name__ == "__main__":
    SmartCameraApp().run()
