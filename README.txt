SMART REPAIR EDITION BY ALI GAMES — SMALL EXE BUILD

Perubahan:
- WETOOL ASLI tidak dimasukkan ke dalam Smart_Repair_Edition_Ali_Games.exe.
- WETOOL tetap berada di external\wetool.exe.
- UI tidak menggunakan Pillow; logo dibaca langsung oleh Tkinter untuk mengurangi dependency.
- Build memakai PyInstaller --onefile --windowed.

Build:
GitHub Actions -> Build Smart Repair EXE -> Run workflow.
Artifact Smart-Repair-EXE berisi EXE utama saja.
Artifact Smart-Repair-Portable berisi EXE + logo + external\wetool.exe.
