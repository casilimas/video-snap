import cv2
import tkinter as tk
from tkinter import Label, Button
from PIL import Image, ImageTk
import os
import datetime
import uuid

class VideoCaptureApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Captura de Video")

        self.video_source = 0
        self.vid = cv2.VideoCapture(self.video_source)

        self.canvas = tk.Canvas(root, width=self.vid.get(cv2.CAP_PROP_FRAME_WIDTH), height=self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.pack()

        self.btn_snapshot = tk.Button(root, text="Tomar Snapshot", width=25, command=self.snapshot)
        self.btn_snapshot.pack(anchor=tk.CENTER, side=tk.LEFT, padx=5, pady=5)

        self.btn_start_record = tk.Button(root, text="Iniciar Grabación", width=25, command=self.start_recording)
        self.btn_start_record.pack(anchor=tk.CENTER, side=tk.LEFT, padx=5, pady=5)

        self.btn_stop_record = tk.Button(root, text="Detener Grabación", width=25, command=self.stop_recording)
        self.btn_stop_record.pack(anchor=tk.CENTER, side=tk.LEFT, padx=5, pady=5)

        self.btn_play_video = tk.Button(root, text="Reproducir Video", width=25, command=self.play_video)
        self.btn_play_video.pack(anchor=tk.CENTER, side=tk.LEFT, padx=5, pady=5)

        self.recording = False
        self.out = None
        self.video_dir = "C:\\Users\\fredd_\\Videos\\Captures"
        self.video_path = ""
        self.delay = 15
        self.update()

        self.root.mainloop()

    def snapshot(self):
        ret, frame = self.vid.read()
        if ret:
            snapshot_filename = os.path.join(self.video_dir, f"snapshot_{uuid.uuid4()}.jpg")
            cv2.imwrite(snapshot_filename, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    def start_recording(self):
        self.recording = True
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        
        # Crear carpeta para la galería si no existe
        if not os.path.exists(self.video_dir):
            os.makedirs(self.video_dir)
        
        # Generar nombre de archivo único
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.video_path = os.path.join(self.video_dir, f'output_{timestamp}.avi')
        self.out = cv2.VideoWriter(self.video_path, fourcc, 20.0, (int(self.vid.get(3)), int(self.vid.get(4))))

    def stop_recording(self):
        self.recording = False
        if self.out:
            self.out.release()
            self.out = None

    def play_video(self):
        cap = cv2.VideoCapture(self.video_path)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            cv2.imshow('Video', frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()

    def update(self):
        ret, frame = self.vid.read()
        if ret:
            if self.recording:
                self.out.write(frame)
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.root.after(self.delay, self.update)

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
        if self.out:
            self.out.release()

root = tk.Tk()
app = VideoCaptureApp(root)
