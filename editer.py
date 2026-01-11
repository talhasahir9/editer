import tkinter as tk
from tkinter import filedialog, messagebox
import os
import subprocess
import threading

class FinalCutterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Talha's Ultimate Cutter v1.8")
        self.root.geometry("600x550")
        self.root.configure(bg="#1e1e2e")
        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.root, text="VIDEO CUTTER - FINAL FIX", font=("Arial", 14, "bold"), bg="#1e1e2e", fg="#1abc9c").pack(pady=20)
        tk.Button(self.root, text="Select Folder", command=self.select_folder, bg="#1abc9c", fg="white", width=20).pack(pady=10)
        self.folder_label = tk.Label(self.root, text="No folder selected", bg="#1e1e2e", fg="gray")
        self.folder_label.pack()
        self.log_box = tk.Text(self.root, height=12, bg="#12121e", fg="#00ff00", font=("Consolas", 9))
        self.log_box.pack(padx=20, pady=20, fill="x")
        self.btn_start = tk.Button(self.root, text="START PROCESSING", command=self.start_thread, bg="#e74c3c", fg="white", font=("Arial", 12, "bold"), height=2)
        self.btn_start.pack(fill="x", side="bottom")

    def select_folder(self):
        self.folder_path = filedialog.askdirectory()
        if self.folder_path: self.folder_label.config(text=self.folder_path)

    def write_log(self, msg):
        self.log_box.insert(tk.END, f"{msg}\n")
        self.log_box.see(tk.END)

    def process_logic(self):
        if not hasattr(self, 'folder_path'): return
        video_files = [f for f in os.listdir(self.folder_path) if f.lower().endswith(('.mp4', '.mov', '.avi', '.mkv'))]
        
        for video_name in video_files:
            base_name, ext = os.path.splitext(video_name)
            txt_path = os.path.join(self.folder_path, base_name + ".txt")
            if not os.path.exists(txt_path): continue

            output_dir = os.path.join(self.folder_path, "Edited_" + base_name)
            if not os.path.exists(output_dir): os.makedirs(output_dir)

            with open(txt_path, 'r') as f:
                lines = f.readlines()

            for i, line in enumerate(lines):
                clean_line = line.strip().rstrip(',')
                if '-' in clean_line:
                    # IMPORTANT: Comma ko Dot mein badalna (Fixes Screenshot 7 error)
                    start, end = clean_line.replace(',', '.').split('-')
                    output_file = os.path.join(output_dir, f"Clip_{i+1:03d}{ext}")
                    
                    self.write_log(f"Processing {video_name} -> Clip {i+1}")
                    
                    # FFmpeg command optimized for milliseconds
                    cmd = f'ffmpeg -ss {start.strip()} -to {end.strip()} -i "{os.path.join(self.folder_path, video_name)}" -c copy -map 0 "{output_file}" -y'
                    
                    # Log real FFmpeg output if error occurs
                    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                    if result.returncode != 0:
                        self.write_log(f"FFmpeg Error on Clip {i+1}: {result.stderr[:100]}")

        messagebox.showinfo("Success", "Process Complete!")

    def start_thread(self):
        threading.Thread(target=self.process_logic, daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = FinalCutterApp(root)
    root.mainloop()
