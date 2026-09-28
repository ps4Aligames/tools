import os, sys, subprocess, hashlib, time
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path

APP_NAME = 'SMART REPAIR EDITION BY ALI GAMES'
BASE = Path(getattr(sys, '_MEIPASS', Path(__file__).resolve().parent))
WETOOL = BASE / 'wetool.exe'
LOGO = BASE / 'assets' / 'ali_games_logo.png'

BG='#05080d'; PANEL='#0b1119'; GOLD='#f6c343'; TEXT='#e8eef7'; MUTED='#8fa1b5'
BLUE='#1488ff'; GREEN='#18c76a'; ORANGE='#ff9d19'; PURPLE='#9b38ff'; RED='#e52b35'

class App:
    def __init__(self, root):
        self.root=root; root.title(APP_NAME); root.geometry('1500x900'); root.minsize(1200,720); root.configure(bg=BG)
        self.nor=None; self.syscon=None; self.active=0
        self.build()
        self.log('SMART REPAIR EDITION BY ALI GAMES siap. [BUILD FIX-2]')
        self.log('Mode: satu tahap aktif pada satu waktu.')
        self.log('Original PS4WETOOLS PRO tersedia melalui tombol di bawah.')

    def build(self):
        header=tk.Frame(self.root,bg=BG); header.pack(fill='x',padx=14,pady=(10,5))
        left=tk.Frame(header,bg=BG); left.pack(side='left')
        if LOGO.exists():
            try:
                from PIL import Image, ImageTk
                im=Image.open(LOGO); im.thumbnail((230,85)); self.logo=ImageTk.PhotoImage(im)
                tk.Label(left,image=self.logo,bg=BG).pack(side='left')
            except Exception: pass
        title=tk.Frame(header,bg=BG); title.pack(side='left',padx=20)
        tk.Label(title,text='SMART REPAIR EDITION',fg='#fff2b0',bg=BG,font=('Segoe UI',26,'bold')).pack(anchor='w')
        tk.Label(title,text='BY ALI GAMES',fg=GOLD,bg=BG,font=('Segoe UI',12,'bold')).pack(anchor='w')
        tk.Label(title,text='Original PS4WETOOLS PRO',fg='#dce5ee',bg=BG,font=('Segoe UI',10)).pack(anchor='w',pady=(3,0))
        status=tk.Frame(header,bg='#101821',highlightbackground=GOLD,highlightthickness=1); status.pack(side='right',padx=5)
        self.conn=tk.Label(status,text='● Device: Disconnected',fg='#ff5656',bg='#101821',font=('Segoe UI',10,'bold')); self.conn.pack(side='left',padx=15,pady=10)
        self.uart=tk.Label(status,text='● UART: OFF',fg='#ff5656',bg='#101821',font=('Segoe UI',10,'bold')); self.uart.pack(side='left',padx=15,pady=10)

        self.stagebar=tk.Frame(self.root,bg=BG); self.stagebar.pack(fill='x',padx=14,pady=6)
        stages=[('1','SMART READ FULL NOR','Baca & Validasi NOR',BLUE,self.stage1),('2','WRITE NOR FULL','Load NOR → Wirate',GREEN,self.stage2),('3','SMART PATCH WIRATE NOR','Load NOR → Patch → Wirate',ORANGE,self.stage3),('4','SMART SYSCONE PATCH','Load & Patch Syscon',PURPLE,self.stage4),('5','SMART SYSCON REBUILD','Load → No.6 → No.4 → No.4',RED,self.stage5)]
        for num,name,sub,col,cmd in stages:
            b=tk.Button(self.stagebar,text=f'{num}\n{name}\n{sub}',command=cmd,bg='#111923',fg=TEXT,activebackground=col,activeforeground='white',font=('Segoe UI',10,'bold'),bd=0,relief='flat',height=3,highlightbackground=col,highlightthickness=2,cursor='hand2')
            b.pack(side='left',fill='x',expand=True,padx=4)

        loaders=tk.Frame(self.root,bg=BG); loaders.pack(fill='x',padx=14,pady=6)
        self.nor_btn=self.loader(loaders,'LOAD FILE NOR',self.load_nor); self.sys_btn=self.loader(loaders,'LOAD FILE SYSCON',self.load_syscon)
        tk.Button(loaders,text='▶  GUNAKAN EXE ASLI WETOOL\n    (Tanpa Modifikasi)',command=self.launch_wetool,bg='#151b22',fg='#ffe08a',activebackground='#272f38',font=('Segoe UI',10,'bold'),bd=0,highlightbackground=GOLD,highlightthickness=2).pack(side='right',fill='x',expand=True,padx=4,ipady=7)

        body=tk.Frame(self.root,bg=BG); body.pack(fill='both',expand=True,padx=14,pady=5)
        main=tk.Frame(body,bg=BG); main.pack(side='left',fill='both',expand=True,padx=(0,6))
        side=tk.Frame(body,bg=BG,width=310); side.pack(side='right',fill='y')
        tk.Label(main,text='LOG AKTIVITAS',fg=GOLD,bg=PANEL,font=('Segoe UI',12,'bold'),anchor='w',padx=12).pack(fill='x')
        self.logbox=tk.Text(main,bg='#02060a',fg='#67d9ff',insertbackground='white',font=('Consolas',10),bd=0,padx=12,pady=10,wrap='none')
        self.logbox.pack(fill='both',expand=True)
        self.logbox.tag_config('ok',foreground='#19e875'); self.logbox.tag_config('warn',foreground='#ffcf42'); self.logbox.tag_config('bad',foreground='#ff4c5b'); self.logbox.tag_config('gold',foreground=GOLD)
        # Information cards use explicit stable attribute names.
        cards = {
            'nor_info': 'INFORMASI NOR',
            'sys_info': 'INFORMASI SYSCON',
            'bwe_info': 'VALIDASI BwE',
            'last_info': 'AKTIVITAS TERAKHIR',
        }
        for attr, title in cards.items():
            f=tk.LabelFrame(side,text=' '+title+' ',fg=GOLD,bg=PANEL,font=('Segoe UI',10,'bold'),labelanchor='nw')
            f.pack(fill='x',pady=4,ipady=8)
            setattr(self, attr, f)
        self.set_card(self.nor_info,'Belum ada NOR yang dimuat.')
        self.set_card(self.sys_info,'Belum ada SYSCON yang dimuat.')
        self.set_card(self.bwe_info,'Belum ada hasil validasi.')
        self.set_card(self.last_info,'Belum ada aktivitas.')

        foot=tk.Frame(self.root,bg='#0b1016',highlightbackground=GOLD,highlightthickness=1); foot.pack(fill='x',padx=14,pady=(4,10))
        tk.Label(foot,text='SMART REPAIR EDITION  •  BY ALI GAMES',fg='#f7f0c4',bg='#0b1016',font=('Segoe UI',10,'bold')).pack(side='left',padx=15,pady=7)
        tk.Label(foot,text='Original PS4WETOOLS PRO',fg='#e1b94d',bg='#0b1016',font=('Segoe UI',9)).pack(side='right',padx=15)

    def loader(self,parent,label,cmd):
        f=tk.Frame(parent,bg='#111821',highlightbackground=GOLD,highlightthickness=1); f.pack(side='left',fill='x',expand=True,padx=4)
        tk.Button(f,text=label,command=cmd,bg='#111821',fg=TEXT,activebackground='#202a35',bd=0,font=('Segoe UI',10,'bold')).pack(side='left',padx=8,pady=8)
        var=tk.StringVar(value='Pilih file ...'); e=tk.Entry(f,textvariable=var,bg='#071019',fg='#cfe5ff',insertbackground='white',bd=0,font=('Consolas',9)); e.pack(side='left',fill='x',expand=True,padx=4,pady=6)
        return var

    def set_card(self,frame,text):
        for w in frame.winfo_children(): w.destroy()
        tk.Label(frame,text=text,fg='#cfe1f5',bg=PANEL,justify='left',anchor='w',font=('Consolas',9)).pack(fill='x',padx=8)
    def log(self,msg,tag=None):
        self.logbox.insert('end',f'[{time.strftime("%H:%M:%S")}] {msg}\n',tag); self.logbox.see('end')
    def load_nor(self):
        p=filedialog.askopenfilename(title='Pilih file NOR',filetypes=[('NOR files','*.*')])
        if not p:return
        self.nor=p; size=os.path.getsize(p); md5=hashlib.md5(open(p,'rb').read()).hexdigest().upper()
        self.nor_btn.set(os.path.basename(p)); self.set_card(self.nor_info,f'Nama File : {os.path.basename(p)}\nUkuran    : {size:,} byte\nMD5       : {md5}\nStatus    : LOADED')
        self.log(f'NOR loaded: {p} | {size:,} byte','ok'); self.last('Load NOR')
    def load_syscon(self):
        p=filedialog.askopenfilename(title='Pilih file SYSCON (512 KB)',filetypes=[('SYSCON files','*.*')])
        if not p:return
        self.syscon=p; size=os.path.getsize(p); md5=hashlib.md5(open(p,'rb').read()).hexdigest().upper()
        self.sys_btn.set(os.path.basename(p)); good=size==512*1024
        tag='ok' if good else 'bad'; self.log(f'SYSCON loaded: {p} | {size:,} byte',tag)
        self.set_card(self.sys_info,f'Nama File : {os.path.basename(p)}\nUkuran    : {size:,} byte\nMD5       : {md5}\nStatus    : {"VALID 512 KB" if good else "INVALID - HARUS 512 KB"}')
        self.last('Load SYSCON')
    def last(self,s): self.set_card(self.last_info,s+'\n'+time.strftime('%Y-%m-%d %H:%M:%S'))
    def need(self,kind):
        if kind=='nor' and not self.nor: messagebox.showwarning('NOR belum dipilih','Load file NOR terlebih dahulu.'); return False
        if kind=='sys' and not self.syscon: messagebox.showwarning('SYSCON belum dipilih','Load file SYSCON terlebih dahulu.'); return False
        return True
    def stage1(self):
        self.log('=== TAHAP 1: SMART READ FULL NOR ===','gold'); self.log('Mode demo UI: fungsi native WETOOL belum diubah.')
        self.last('SMART READ FULL NOR')
    def stage2(self):
        if not self.need('nor'): return
        self.log('=== TAHAP 2: WRITE NOR FULL ===','gold'); self.log(f'File siap ditulis: {os.path.basename(self.nor)}','ok'); self.log('Write/Verify harus dijalankan oleh WETOOL asli.'); self.last('WRITE NOR FULL')
    def stage3(self):
        if not self.need('nor'): return
        self.log('=== TAHAP 3: SMART PATCH WIRATE NOR ===','gold'); self.log(f'NOR siap diproses: {os.path.basename(self.nor)}','ok'); self.log('Menu native No.4 → Save → No.3 → No.5 tetap milik WETOOL asli.'); self.last('SMART PATCH WIRATE NOR')
    def stage4(self):
        if not self.need('sys'): return
        if os.path.getsize(self.syscon)!=512*1024: messagebox.showwarning('SYSCON invalid','File SYSCON harus berukuran tepat 512 KB.'); return
        self.log('=== TAHAP 4: SMART SYSCONE PATCH ===','gold'); self.log('Load SYSCON 512 KB → WETOOL → No.1 DEBUG ON → No.2','ok'); self.last('SMART SYSCONE PATCH')
    def stage5(self):
        if not self.need('sys'): return
        if os.path.getsize(self.syscon)!=512*1024: messagebox.showwarning('SYSCON invalid','File SYSCON harus berukuran tepat 512 KB.'); return
        self.log('=== TAHAP 5: SMART SYSCON REBUILD ===','gold')
        for x in ['Load SYSCON 512 KB','Load SYSCON ke WETOOL','No.6','No.4','No.4 lagi','Jalankan Rebuild']:
            self.log(x+'  ...  UI READY','ok')
        self.log('Catatan: urutan native WETOOL belum dieksekusi otomatis.','warn'); self.last('SMART SYSCON REBUILD')
    def launch_wetool(self):
        if not WETOOL.exists(): messagebox.showerror('WETOOL tidak ditemukan','wetool.exe tidak ada di folder aplikasi.'); return
        try: subprocess.Popen([str(WETOOL)],cwd=str(WETOOL.parent)); self.log('Original wetool.exe dijalankan tanpa modifikasi.','ok')
        except Exception as e: messagebox.showerror('Gagal menjalankan WETOOL',str(e))

root=tk.Tk(); App(root); root.mainloop()
