import os
import sys
import time
import numpy as np

# التأكد من إنشاء مجلد المخرجات إذا لمש يكن موجوداً
OUTPUT_DIR = "outputs"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

print("==================================================")
print("       SMART CAMERA APPLICATION - MAIN CORE       ")
print("==================================================")
print("[*] Initializing Application Environment...")
time.sleep(0.5)

class SmartCameraApp:
    def __init__(self, width=854, height=480):
        self.width = width
        self.height = height
        self.is_running = False
        print(f"[+] Camera resolution configured to: {self.width}x{self.height}")

    def start_stream(self, frame_count=10):
        print("\n[*] Starting Live Camera Simulation & Processing Stream...")
        self.is_running = True
        
        for i in range(1, frame_count + 1):
            start_time = time.time()
            
            # محاكاة التقاط إطار خام من الكاميرا
            raw_frame = np.random.randint(0, 256, (self.height, self.width, 3), dtype=np.uint8)
            
            # معالجة الإطار عبر محرك المعالجة (CPU Pipeline)
            processed_frame = np.clip(raw_frame.astype(np.float32) * 1.05, 0, 255).astype(np.uint8)
            
            elapsed = (time.time() - start_time) * 1000.0
            fps_calc = 1000.0 / elapsed if elapsed > 0 else 0
            
            print(f"    - Frame [{i}/{frame_count}] Processed in {elapsed:.2f} ms (~{fps_calc:.1f} FPS)")
            
            # محاكاة حفظ إطار مختار كصورة
            if i == frame_count:
                sample_path = os.path.join(OUTPUT_DIR, "captured_snapshot.npy")
                np.save(sample_path, processed_frame)
                print(f"[+] Snapshot successfully saved to: {sample_path}")
                
        print("[*] Stream session completed successfully.")

    def stop(self):
        self.is_running = False
        print("[*] Application stopped safely.")

if __name__ == "__main__":
    # تشغيل التطبيق واختبار تدفق 60 إطاراً افتراضياً
    app = SmartCameraApp()
    app.start_stream(frame_count=10)
    app.stop()
    print("==================================================")
    print(" Application Core Architecture Fully Operational! ")
    print("==================================================")
