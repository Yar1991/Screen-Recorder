import customtkinter as tk
from tkinter import filedialog
import pyautogui
import cv2
import numpy
import keyboard
from PIL import Image
import shutil

from os import path


class App(tk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.resolution = (2560, 1440)
        self.codec = cv2.VideoWriter_fourcc(*"mp4v")
        self.filename = "recording.mp4"
        self.fps = 10.0
        self.video_writer = cv2.VideoWriter(self.filename, self.codec, self.fps, self.resolution)
        self.video_timer = 0
        self.frame_count = 0
        
        self.geometry("400x500")
        self.title("Screen Recorder")
        self.resizable(False, False)
        self.output_folder_path = ""

        self.grid_rowconfigure((0, 1, 2, 5, 6, 7), weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.rec_image = tk.CTkImage(light_image=Image.open("rec-button.png" if path.curdir == "." else "../../rec-button.png"),
                                     dark_image=Image.open("rec-button.png" if path.curdir == "." else "../../rec-button.png"),
                                     size=(50, 50))
        self.rec_image_label = tk.CTkLabel(self, image=self.rec_image, text="")
        
        self.rec_image_label.grid(row=0, column=0, pady=(0, 20))

        self.choose_folder_label = tk.CTkLabel(
            self, text="Choose the folder where to save the result:", font=("Poppins", 18, "bold"))
        self.choose_folder_label.grid(row=1, column=0, pady=20)
        self.choose_folder_btn = tk.CTkButton(self, text="OPEN", width=140, height=40, fg_color="#fff", border_width=0,
                                              font=("Poppins", 16, "bold"), corner_radius=10, hover_color="#EBEBEB", text_color="#333", command=self.choose_folder)
        self.choose_folder_btn.grid(row=1, column=0, pady=(150, 20))
        
        self.record_btn = tk.CTkButton(self, text="START", width=140, height=40, fg_color="#D04444", border_width=0,
                                              font=("Poppins", 16, "bold"), corner_radius=10, hover_color="#B23C3C", text_color="#fff", command=self.start_recording)
        self.record_btn.grid(row=2, column=0, pady=(20, 0))
        
        self.timer_label = tk.CTkLabel(self, text="", font=("Poppins", 17))
        self.timer_label.grid(row=3, column=0)
        
        self.info_label = tk.CTkLabel(self, text="", font=("Poppins", 17), text_color="#E16262")
        self.info_label.grid(row=4, column=0, pady=(20, 0))


    def update_counter(self):
        if self.recording:
            self.video_timer += 1
            self.timer_label.configure(text=f"{round(self.video_timer / 60):02}:{self.video_timer % 60:02}")
            self.timer_label.update()

    def choose_folder(self):
        folder = filedialog.askdirectory(initialdir="/", title="Select Folder")
        self.output_folder_path = folder
        self.choose_folder_label.configure(text=folder)
        
        
    def start_recording(self):

        self.record_btn.configure(state=tk.DISABLED)
        self.choose_folder_btn.configure(state=tk.DISABLED)
        self.info_label.configure(text="to stop recording press and hold 'ctrl+q'")
        self.info_label.update()
        
        while True:
            snapshot = pyautogui.screenshot()
            frame = numpy.array(snapshot)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.video_writer.write(frame)
            self.frame_count += 1
            
            if self.frame_count % 10 == 0:
                # it increments the counter value on each second by catching the right frame
                self.video_timer += 1
                self.timer_label.configure(text=f"{round(self.video_timer / 60):02}:{self.video_timer % 60:02}")
                self.timer_label.update()
            
            cv2.waitKey(1)
            if keyboard.is_pressed("ctrl+q") or self.video_timer >= 600:  # current time limit is set to 10 minutes
                break
        self.video_writer.release()
        self.record_btn.configure(state=tk.ACTIVE)
        self.choose_folder_btn.configure(state=tk.ACTIVE)
        self.choose_folder_label.configure(text="Choose the folder where to save the result:")
        self.info_label.configure(text="")
        self.info_label.update()
        self.timer_label.configure(text="")
        self.video_timer = 0
        self.frame_count = 0
        if self.output_folder_path:
            shutil.move("recording.mp4", self.output_folder_path)
        
        

if __name__ == "__main__":
    print(path.curdir == ".")
    # app = App()
    # app.iconbitmap("icon.ico")
    # tk.set_appearance_mode("dark")
    # app.mainloop()
