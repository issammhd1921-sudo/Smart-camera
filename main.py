from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.clock import Clock
from camera4kivy import Preview

class RealCameraRoot(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        
        # 1. إنشاء عارض الكاميرا الحقيقي (يملأ الشاشة بنسبة أبعاد حقيقية)
        self.preview = Preview(aspect_ratio='16:9')
        self.add_widget(self.preview)
        
        # 2. شريط الأزرار الحقيقية للتحكم بالعتاد
        controls_layout = BoxLayout(size_hint_y=0.15, spacing=10, padding=10)
        
        self.btn_capture = Button(text='Capture Photo', background_color=(0.1, 0.6, 0.1, 1))
        self.btn_capture.bind(on_press=self.take_real_photo)
        controls_layout.add_widget(self.btn_capture)
        
        self.btn_switch = Button(text='Switch Camera', background_color=(0.2, 0.2, 0.8, 1))
        self.btn_switch.bind(on_press=self.switch_real_camera)
        controls_layout.add_widget(self.btn_switch)
        
        self.add_widget(controls_layout)
        
        # متغير لتتبع الكاميرا النشطة (0: الخلفية، 1: الأمامية)
        self.camera_id = "0"

    def on_enter(self):
        # الاتصال الفعلي بالعتاد بعد بدء التطبيق بجزء من الثانية
        Clock.schedule_once(lambda dt: self.preview.connect_camera(camera_id=self.camera_id), 0.5)

    def on_leave(self):
        # قطع الاتصال بسلام عند الخروج للحفاظ على موارد الهاتف
        self.preview.disconnect_camera()

    def take_real_photo(self, instance):
        # أمر حقيقي لالتقاط الصورة وحفظها في مسار DCIM على الهاتف
        self.preview.capture_photo(subdir="RealCameraApp", name="photo.jpg")

    def switch_real_camera(self, instance):
        # التبديل الحقيقي بين الكاميرا الخلفية والأمامية
        self.preview.disconnect_camera()
        self.camera_id = "1" if self.camera_id == "0" else "0"
        self.preview.connect_camera(camera_id=self.camera_id)

class RealCameraApp(App):
    def build(self):
        root = RealCameraRoot()
        return root

    def on_start(self):
        self.root.on_enter()

    def on_stop(self):
        self.root.on_leave()

if __name__ == '__main__':
    RealCameraApp().run()
    
