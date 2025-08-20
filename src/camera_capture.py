import cv2
import tkinter as tk
from PIL import Image, ImageTk

class CameraCapture:
    def __init__(self, device_idx=1, processors=None, pause=30):
        self._processors = processors or []
        self._cap = cv2.VideoCapture(device_idx)
        self._pause = pause

    def __call__(self):
        self._root = tk.Tk()
        self._root.title("Thermal camera with masks")

        self._canvases = []
        for i in range(1 + len(self._processors)):
            canvas = tk.Label(self._root)
            canvas.grid(row=0, column=i)
            self._canvases.append(canvas)

        self._root.protocol("WM_DELETE_WINDOW", self._on_close)
        self._update_frame(True)
        self._root.mainloop()

    def _update_frame(self, first=False):
        if first == False:
            ret, frame = self._cap.read()
            if ret:
                self._process_frame(frame)

        self._root.after(self._pause, self._update_frame)

    def _process_frame(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        masks = [p.get_mask(gray) for p in self._processors]
        
        imgs = [frame] + [cv2.cvtColor(m, cv2.COLOR_GRAY2BGR) for m in masks]

        for canvas, img in zip(self._canvases, imgs):
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img_pil = Image.fromarray(img_rgb)
            img_tk = ImageTk.PhotoImage(image=img_pil)
            canvas.img_tk = img_tk
            canvas.configure(image=img_tk)

    def _on_close(self):
        self._cap.release()
        self._root.destroy()
