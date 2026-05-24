#   main.py               ← entry point
#   constants.py          ← shared colours
#   page_login.py         ← OSASO
#   page_dashboard.py     ← KEVIN
#   page_chat.py          ← DAYANN
#   page_events.py        ← PHILIP
#   page_study_groups.py  ← DIVINE
#   page_profile.py       ← HARMONIE
#   login.csv             ← user database


import time
import tkinter as tk
from tkinter import ttk, messagebox

from constants        import BG, CARD, TEAL, WHITE, MUTED, FIELD_BG, BORDER, SIDEBAR
from page_login       import setup_db, LoginWindow
from page_dashboard   import DashboardPage
from page_chat        import GlobalChatPage
from page_events      import EventsPage
from page_study_groups import StudyGroupsPage
from page_profile     import UserProfilePage


#  SPLASH SCREEN


class SplashScreen:
    def __init__(self, root, on_done):
        self.root    = root
        self.on_done = on_done

        root.title("PeerSphere")
        root.geometry("700x400")
        root.resizable(False, False)
        root.configure(bg=BG)

        sw = root.winfo_screenwidth()
        sh = root.winfo_screenheight()
        root.geometry(f"700x400+{(sw - 700) // 2}+{(sh - 400) // 2}")

        tk.Label(root, text="PeerSphere", bg=BG, fg=WHITE,
                 font=("Georgia", 28, "bold")).pack(pady=(110, 8))
        tk.Label(root, text="Connecting students everywhere", bg=BG, fg=MUTED,
                 font=("Arial", 12)).pack(pady=(0, 36))

        self.bar = ttk.Progressbar(root, orient="horizontal", length=340)
        self.bar.pack()
        root.after(500, self._tick)

    def _tick(self, val=0):
        if val <= 100:
            self.bar["value"] = val
            self.root.after(10, self._tick, val + 1)
        else:
            self.on_done()



#  MAIN APP  (launched after successful login)

class PeerSphereApp(tk.Toplevel):
    def __init__(self, root, display_name, username):
        super().__init__(root)
        self.root         = root
        self.display_name = display_name
        self.username     = username

        self.title("PeerSphere — Workspace")
        self.geometry("1100x700")
        self.minsize(900, 600)
        self.configure(bg=BG)
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        self._clock_running = True
        self.active_nav_btn = None
        self.nav_buttons    = {}

        self._build_topbar()

        self.body = tk.Frame(self, bg=BG)
        self.body.pack(fill="both", expand=True)

        self._build_sidebar()

        self.main_container = tk.Frame(self.body, bg=BG)
        self.main_container.pack(side="left", fill="both", expand=True, padx=20, pady=16)
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)

        # Instantiate every page
        self.pages = {}
        for PageClass in (DashboardPage, GlobalChatPage, EventsPage,
                          StudyGroupsPage, UserProfilePage):
            name  = PageClass.__name__
            frame = PageClass(parent=self.main_container, controller=self)
            self.pages[name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Pages that need post-login data
        self.pages["DashboardPage"].refresh()
        self.pages["UserProfilePage"].refresh()

        # Default page
        self.show_page("DashboardPage", "Dashboard")

    #  Top bar 

    def _build_topbar(self):
        topbar = tk.Frame(self, bg=SIDEBAR, height=54)
        topbar.pack(side="top", fill="x")
        topbar.pack_propagate(False)

        badge = tk.Frame(topbar, bg=TEAL, width=36, height=36)
        badge.pack(side="left", padx=(14, 6), pady=9)
        badge.pack_propagate(False)
        tk.Label(badge, text="PS", font=("Georgia", 11, "bold"),
                 fg=WHITE, bg=TEAL).place(relx=.5, rely=.5, anchor="center")

        bw = tk.Frame(topbar, bg=SIDEBAR)
        bw.pack(side="left", pady=6)
        tk.Label(bw, text="PEERSPHERE",     font=("Georgia", 12, "bold"), fg=WHITE, bg=SIDEBAR).pack(anchor="w")
        tk.Label(bw, text="UPLINK: ONLINE", font=("Arial", 7),            fg=TEAL,  bg=SIDEBAR).pack(anchor="w")

        tk.Label(topbar, text=" v1.4.0-beta ", font=("Arial", 8), fg=MUTED, bg=CARD,
                 relief="flat", bd=0, highlightthickness=1,
                 highlightbackground=BORDER).pack(side="left", padx=10)

        sf = tk.Frame(topbar, bg=FIELD_BG, highlightthickness=1, highlightbackground=BORDER)
        sf.pack(side="left", padx=20, fill="y", pady=10, expand=True)
        tk.Label(sf, text="🔍", fg=MUTED, bg=FIELD_BG, font=("Arial", 10)).pack(side="left", padx=(8, 2))
        tk.Entry(sf, font=("Arial", 10), bg=FIELD_BG, fg=MUTED,
                 insertbackground=WHITE, relief="flat", bd=0, width=38).pack(side="left", pady=6, ipady=2)

        self.clock_lbl = tk.Label(topbar, text="", font=("Arial", 10, "bold"), fg=WHITE, bg=SIDEBAR)
        self.clock_lbl.pack(side="right", padx=(4, 14))
        tk.Label(topbar, text="● 24ms ping", font=("Arial", 9), fg=TEAL, bg=SIDEBAR).pack(side="right", padx=(4, 0))
        self._tick_clock()

    #Sidebar

    def _build_sidebar(self):
        sidebar = tk.Frame(self.body, bg=SIDEBAR, width=190)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        nav_pad = tk.Frame(sidebar, bg=SIDEBAR)
        nav_pad.pack(fill="x", pady=(16, 0))

        nav_items = [
            ("Dashboard",        "DashboardPage"),
            ("Global Chat",      "GlobalChatPage"),
            ("Culture Explorer", "StudyGroupsPage"),
            ("User Profile",     "UserProfilePage"),
            ("Events",           "EventsPage"),
        ]

        for label, page_ref in nav_items:
            btn = tk.Button(nav_pad, text=f"  {label}", font=("Arial", 10, "normal"),
                            bg=SIDEBAR, fg=WHITE, activebackground=CARD,
                            activeforeground=TEAL, relief="flat", bd=0,
                            anchor="w", cursor="hand2", pady=10,
                            command=lambda p=page_ref, l=label: self.show_page(p, l))
            btn.pack(fill="x")
            self.nav_buttons[label] = btn
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=CARD)    if b is not self.active_nav_btn else None)
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=SIDEBAR) if b is not self.active_nav_btn else None)

        tk.Frame(sidebar, bg=BORDER, height=1).pack(fill="x", padx=14, pady=16)

        tk.Button(sidebar, text="  Logout", font=("Arial", 10, "normal"),
                  bg=SIDEBAR, fg="#EF4444", activebackground="#1f1f1f",
                  relief="flat", bd=0, anchor="w", cursor="hand2", pady=10,
                  command=self._logout).pack(fill="x")

    #  Page switching 

    def show_page(self, page_name, label_name):
        if self.active_nav_btn:
            self.active_nav_btn.config(bg=SIDEBAR, fg=WHITE, font=("Arial", 10, "normal"))
        btn = self.nav_buttons.get(label_name)
        if btn:
            btn.config(bg=CARD, fg=TEAL, font=("Arial", 10, "bold"))
            self.active_nav_btn = btn
        frame = self.pages.get(page_name)
        if frame:
            frame.tkraise()

    #  Clock 

    def _tick_clock(self):
        if not self._clock_running:
            return
        self.clock_lbl.config(text=time.strftime("%I:%M %p"))
        self.after(1000, self._tick_clock)

    #  Logout / close ────────────────────────────────────────────────────────

    def _logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self._clock_running = False
            self.destroy()
            LoginWindow(self.root, _launch_app)

    def _on_close(self):
        self._clock_running = False
        self.root.destroy()



#  WIRING: splash → login → app


def _launch_app(display_name, username):
    PeerSphereApp(root, display_name, username)


def _show_login():
    for w in root.winfo_children():
        w.destroy()
    root.withdraw()
    LoginWindow(root, _launch_app)

setup_db()

root = tk.Tk()
root.title("PeerSphere")
root.configure(bg=BG)
root.withdraw()
root.deiconify()

SplashScreen(root, on_done=_show_login)
root.mainloop()
