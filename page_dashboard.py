# page_dashboard.py  
# DASHBOARD PAGE
# Branch: page/dashboard

import tkinter as tk

from constants import BG, CARD, TEAL, WHITE, MUTED, BORDER, ACCENT_BLUE


class DashboardPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller

    def refresh(self):
        """Called once after login so display_name is available."""
        for w in self.winfo_children():
            w.destroy()
        self._build()

    def _build(self):
        dn = getattr(self.controller, "display_name", "User")

        content = tk.Frame(self, bg=BG, padx=30, pady=20)
        content.pack(fill="both", expand=True)

        welcome = tk.Frame(content, bg=CARD, pady=22, padx=28)
        welcome.pack(fill="x")
        tk.Label(welcome, text="WORKSPACE ACTIVE",
                 font=("Arial", 10, "bold"), fg=TEAL, bg=CARD).pack(anchor="w")

        row = tk.Frame(welcome, bg=CARD)
        row.pack(fill="x", pady=(10, 0))
        tk.Label(row, text=f"Welcome back, {dn}",
                 font=("Georgia", 24, "bold"), fg=WHITE, bg=CARD).pack(side="left")
        tk.Button(row, text="▶ Quick Study Sprint", bg=ACCENT_BLUE, fg=WHITE,
                  font=("Arial", 11, "bold"), relief="flat",
                  padx=18, pady=7).pack(side="right", padx=8)
        tk.Button(row, text="🌍 Explore Culture Map", bg=CARD, fg=WHITE,
                  font=("Arial", 11, "bold"), relief="flat",
                  highlightthickness=1, highlightbackground=BORDER).pack(side="right")

        # Stats row 
        stats = tk.Frame(content, bg=BG)
        stats.pack(fill="x", pady=25)
        for title, val in [("GLOBAL COLLABORATIONS", "8 Regions"),
                            ("STUDY SPRINT TIME",      "14.5 Hrs"),
                            ("COLLABORATIVE STREAKS",  "9 Days")]:
            f = tk.Frame(stats, bg=CARD, width=260, height=120)
            f.pack(side="left", padx=10, fill="both", expand=True)
            f.pack_propagate(False)
            tk.Label(f, text=title, font=("Arial", 9),          fg=MUTED, bg=CARD).pack(anchor="w", padx=22, pady=(22, 5))
            tk.Label(f, text=val,   font=("Arial", 26, "bold"), fg=TEAL,  bg=CARD).pack(anchor="w", padx=22)

        #  Peers + Clusters 
        bottom = tk.Frame(content, bg=BG)
        bottom.pack(fill="both", expand=True)

        left = tk.Frame(bottom, bg=CARD, padx=22, pady=18)
        left.pack(side="left", fill="both", expand=True, padx=(0, 15))
        tk.Label(left, text="RECOMMENDED GLOBAL PEERS",
                 font=("Arial", 13, "bold"), fg=WHITE, bg=CARD).pack(anchor="w", pady=(0, 15))
        self._peer_card(left, "Kenji Sato",   "University of Tokyo",  "#14B8A6")
        self._peer_card(left, "Clara Dubois", "Sorbonne Université",  "#F87171")

        right = tk.Frame(bottom, bg=CARD, padx=22, pady=18)
        right.pack(side="left", fill="both", expand=True)
        tk.Label(right, text="POPULAR STUDY CLUSTERS",
                 font=("Arial", 13, "bold"), fg=WHITE, bg=CARD).pack(anchor="w", pady=(0, 15))
        self._cluster_card(right, "Quantum Cryptography Hub", "142 members", "#4338CA")
        self._cluster_card(right, "Global Hackathon Circle",  "89 members",  "#2563EB")

    def _peer_card(self, parent, name, school, color):
        f = tk.Frame(parent, bg=CARD, pady=14, padx=16)
        f.pack(fill="x", pady=6)
        tk.Label(f, text="●", font=("Arial", 28), fg=color, bg=CARD).pack(side="left")
        info = tk.Frame(f, bg=CARD)
        info.pack(side="left", padx=14)
        tk.Label(info, text=name,   font=("Arial", 12, "bold"), fg=WHITE, bg=CARD).pack(anchor="w")
        tk.Label(info, text=school, font=("Arial", 10),         fg=MUTED, bg=CARD).pack(anchor="w")
        tk.Button(f, text="Chat Peer", bg=ACCENT_BLUE, fg=WHITE,
                  font=("Arial", 10, "bold"), relief="flat",
                  padx=16, pady=5).pack(side="right")

    def _cluster_card(self, parent, name, count, color):
        f = tk.Frame(parent, bg=color, pady=22, padx=22)
        f.pack(fill="x", pady=7)
        tk.Label(f, text=name,  font=("Arial", 14, "bold"), fg=WHITE,     bg=color).pack(anchor="w")
        tk.Label(f, text=count, font=("Arial", 11),         fg="#E0F2FE", bg=color).pack(anchor="w", pady=4)
        tk.Button(f, text="Join Cluster →", bg=WHITE, fg="#1E3A8A",
                  font=("Arial", 10, "bold"), relief="flat").pack(anchor="w", pady=(8, 0))
