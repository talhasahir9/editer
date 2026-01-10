import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import threading
import subprocess
from moviepy.editor import VideoFileClip, concatenate_videoclips

class VideoCutterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Talha's Super Fast Automator v1.3")
        self.root.geometry("600x650")
        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.root, text="Video Automation Studio (Fast Mode)", font=("Arial", 16, "bold")).pack(pady=10)

        # Folder Selection
        tk.Button(self.root, text="Select Input Folder", command=self.select_folder, bg="#3498db", fg="white").pack(pady=5)
        self.folder_label = tk.Label(self.root, text="No folder selected", fg="gray")
        self.folder_label.pack()

        # Mode Selection
        tk.Label(self.root, text="Step 2: Export Mode", font=("Arial", 10, "bold")).pack(pady=(15, 5))
        self.mode_var = tk.StringVar(value="Individual")
        tk.Radiobutton(self.root, text="Merge into Single Video", variable=self.mode_var, value="Single").pack()
        tk.Radiobutton(self.root, text="Export Individual Clips (Best for CapCut)", variable=self.mode_var, value="Individual").pack()

        # FAST MODE CHECKBOX
        self.fast_mode_var = tk.BooleanVar(value=True)
        self.chk_fast = tk.Checkbutton(self.root, text="USE SUPER FAST MODE (No Rendering)", variable=self.fast_mode_var, font=("Arial", 10, "bold"), fg="red")
        self.chk_fast.pack(pady=10)

        # Progress
        self.progress_bar = ttk.Progressbar(self.root, length=450, mode='determinate')
        self.progress_bar.pack(pady=20)
        self.status_label = tk.Label(self.root, text="Ready", fg="blue")
        self.status_label.pack()

        self.log_box = tk.Text(self.root, height=10, width=70, state=tk.DISABLED, font=("Consolas", 9))
        self.log_box.pack(pady=10)

        tk.Button(self.root, text="START PROCESSING", bg="#27ae60", fg="white", font=("Arial", 12, "bold"), command=self.start_thread).pack(pady=10)

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
        if not folder_path or "No folder" in folder_path: return
        
        video_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.mp4', '.mov', '.avi'))]
        self.progress_bar['maximum'] = len(video_files)

        for idx, video_name in enumerate(video_files):
            base_name = os.path.splitext(video_name)[0]
            txt_path = os.path.join(folder_path, base_name + ".txt")
            if not os.path.exists(txt_path): continue

            output_subfolder = os.path.join(folder_path, "Edited_" + base_name)
            if not os.path.exists(output_subfolder): os.makedirs(output_subfolder)

            video_full_path = os.path.join(folder_path, video_name)
            
            with open(txt_path, 'r') as f:
                content = f.read().strip().replace('\n', ',')
                segments = [s.strip().split('-') for s in content.split(',') if '-' in s]

            if self.fast_mode_var.get():
                # --- SUPER FAST MODE (FFMPEG) ---
                for i, s in enumerate(segments):
                    start, end = s[0].strip(), s[1].strip()
                    output_file = os.path.join(output_subfolder, f"Clip_{i+1:03d}.mp4")
                    self.write_log(f"Fast Cutting {video_name} -> Clip {i+1}...")
                    
                    # FFmpeg command logic
                    cmd = f'ffmpeg -ss {start} -to {end} -i "{video_full_path}" -c copy "{output_file}" -y'
                    subprocess.call(cmd, shell=True)
            else:
                # --- NORMAL MODE (MOVIEPY) ---
                video = VideoFileClip(video_full_path)
                if self.mode_var.get() == "Single":
                    clips = [video.subclip(s[0], s[1]) for s in segments]
                    final = concatenate_videoclips(clips)
                    final.write_videofile(os.path.join(output_subfolder, "Full_Video.mp4"), codec="libx264")
                else:
                    for i, s in enumerate(segments):
                        clip = video.subclip(s[0], s[1])
                        clip.write_videofile(os.path.join(output_subfolder, f"Clip_{i+1:03d}.mp4"), codec="libx264")
                video.close()

            self.progress_bar['value'] = idx + 1
        
        messagebox.showinfo("Done", "Super Fast Processing Completed!")

    def start_thread(self):
        threading.Thread(target=self.process_logic, daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoCutterApp(root)
    root.mainloop()
