import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import threading
import subprocess

class SuperFastCutter:
    def __init__(self, root):
        self.root = root
        self.root.title("Talha's Original Fast Cutter")
        self.root.geometry("600x600")
        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.root, text="Video Automation Studio", font=("Arial", 16, "bold"), fg="#2c3e50").pack(pady=15)

        # Folder Selection
        tk.Button(self.root, text="Select Folder", command=self.select_folder, width=25, bg="#3498db", fg="white").pack(pady=5)
        self.folder_label = tk.Label(self.root, text="No folder selected", fg="gray", wraplength=500)
        self.folder_label.pack(pady=5)

        # FAST MODE CHECKBOX
        self.fast_mode_var = tk.BooleanVar(value=True)
        tk.Checkbutton(self.root, text="USE SUPER FAST MODE (FFmpeg)", variable=self.fast_mode_var, font=("Arial", 10, "bold"), fg="red").pack(pady=15)

        # Log Display
        self.log_box = tk.Text(self.root, height=12, width=70, state=tk.DISABLED, font=("Consolas", 9))
        self.log_box.pack(pady=10)

        # Start Button
        self.btn_start = tk.Button(self.root, text="START PROCESSING", bg="#27ae60", fg="white", font=("Arial", 12, "bold"), command=self.start_thread, height=2, width=25)
        self.btn_start.pack(pady=10)

    def write_log(self, msg):
        self.log_box.config(state=tk.NORMAL)
        self.log_box.insert(tk.END, f"{msg}\n")
        self.log_box.see(tk.END)
        self.log_box.config(state=tk.DISABLED)

    def select_folder(self):
        path = filedialog.askdirectory()
        if path: self.folder_label.config(text=path)

    def process_logic(self):
        folder_path = self.folder_label.cget("text")
        if not folder_path or "No folder" in folder_path:
            messagebox.showerror("Error", "Pehle folder select karen!")
            return

        # Sab formats (MKV included)
        video_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.mp4', '.mov', '.avi', '.mkv'))]
        
        for video_name in video_files:
            base_name, ext = os.path.splitext(video_name)
            txt_path = os.path.join(folder_path, base_name + ".txt")
            if not os.path.exists(txt_path): continue

            output_subfolder = os.path.join(folder_path, "Edited_" + base_name)
            if not os.path.exists(output_subfolder): os.makedirs(output_subfolder)

            with open(txt_path, 'r') as f:
                lines = f.readlines()

            for i, line in enumerate(lines):
                # 1. Aakhir wala comma hatana
                clean_line = line.strip().rstrip(',')
                if '-' in clean_line:
                    # 2. Millisecond comma (,) ko dot (.) mein badalna FFmpeg ke liye
                    parts = clean_line.replace(',', '.').split('-')
                    start, end = parts[0].strip(), parts[1].strip()
                    
                    output_file = os.path.join(output_subfolder, f"Clip_{i+1:03d}{ext}")
                    self.write_log(f"Cutting: {video_name} -> Clip {i+1}")
                    
                    # FFmpeg command optimized
                    cmd = f'ffmpeg -ss {start} -to {end} -i "{os.path.join(folder_path, video_name)}" -c copy -map 0 "{output_file}" -y'
                    subprocess.call(cmd, shell=True)

        messagebox.showinfo("Done", "Processing Complete!")

    def start_thread(self):
        threading.Thread(target=self.process_logic, daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = SuperFastCutter(root)
    root.mainloop()
