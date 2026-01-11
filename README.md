Talha's Video Automator Pro aik powerful Python-based tool hai jo video editing ke ghanton ka kaam minton mein badal deta hai. Ye khaas tor par YouTube Automation aur Horror Story channels ke liye design kiya gaya hai.

✨ Key Features
Batch Processing: Aik saath saari videos ko process karen.

Super Fast Mode: FFmpeg "Stream Copy" engine jo 400+ cuts ko minton mein nikal deta hai (No Rendering).

Individual Clip Export: Har cut ko alag MP4 file mein save karta hai taake CapCut mein drag-and-drop asani se ho sake.

Quality Selector: Choose between High (CRF 18), Medium, or Low settings.

Logging System: Har session ka log file (session_log.txt) khud hi ban jata hai.

User-Friendly UI: Simple desktop interface (Tkinter) jisay koi bhi chala sakta hai.

🛠️ Requirements & Installation
1. Python
Python 3.10+ install hona zaroori hai. Install karte waqt "Add Python to PATH" par laazmi tik karen.

2. FFmpeg (For Super Fast Mode)
Fast mode chalane ke liye FFmpeg install karna zaroori hai:

FFmpeg download karke C:\ffmpeg mein rakhen.

C:\ffmpeg\bin ko Windows ke Environment Variables (PATH) mein add karen.

3. Python Libraries
CMD kholen aur ye command chalaein:

Bash

pip install moviepy pyinstaller
📂 Folder Structure (Important)
Software ko sahi se chalane ke liye aapka input folder kuch is tarah dikhna chahiye:

Plaintext

/My_Project_Folder
│-- video1.mp4
│-- video1.txt     <-- Isme timestamps honge (e.g. 10-20)
│-- movie_vlog.mov
│-- movie_vlog.txt <-- Video aur Text file ka naam bilkul aik hona chahiye
🚀 How to Use
Launch: Script run karen ya .exe file par double click karen.

Select Folder: Apne project wala folder choose karen.

Set Mode: Agar CapCut ke liye clips chahiye to "Individual Clips" select karen.

Check Fast Mode: Speed ke liye "Super Fast Mode" ko ON rakhen.

Run: "START PROCESSING" dabayen aur magic dekhen!

🔧 Troubleshooting
FFmpeg Error: Agar fast mode error de, to check karen ke CMD mein ffmpeg -version chal raha hai ya nahi.

Naming Error: Ensure karen ke .txt file aur video file ka naam (Case-sensitive) same ho.

Memory Issues: RDP par kaam karte waqt hamesha Fast Mode use karen taake RAM crash na ho.

👨‍💻 Developer
Talha Khalid Former Chemist | Content Strategist | Python Developer# editer


pyinstaller --noconsole --onefile --collect-all imageio --collect-all moviepy --name "Talha_Auto_Cutter" editer.py
