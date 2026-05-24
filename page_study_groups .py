# page_study_groups.py  

# STUDY GROUPS / CULTURE EXPLORER PAGE
# Branch: page/study-groups

import tkinter as tk

from constants import BG, CARD, WHITE, BORDER


class StudyGroupsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)

        # Header
        header = tk.Frame(self, bg=BG)
        header.pack(fill="x", pady=(0, 20), padx=20)
        tk.Label(header, text="PeerSphere Study Groups",
                 font=("Georgia", 18, "bold"), fg=WHITE, bg=BG).pack(side="left")

        # Scrollable grid
        canvas = tk.Canvas(self, bg=BG, highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True, padx=(20, 0))
        sb = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        sb.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=sb.set)

        sc  = tk.Frame(canvas, bg=BG)
        win = canvas.create_window((0, 0), window=sc, anchor="nw")
        sc.bind("<Configure>",     lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(win, width=e.width - 40))

        groups = [
            ("CS", "Intro to Computer Science",     "Engineering",           "2,450 members"),
            ("BC", "Principles of Biochemistry",    "Life Sciences",          "1,120 members"),
            ("ME", "Macroeconomic Theory",           "Economics",              "890 members"),
            ("LA", "Linear Algebra & Matrices",      "Mathematics",            "1,540 members"),
            ("SU", "Sustainable Urbanism",           "Architecture",           "760 members"),
            ("MH", "Modern European History",        "Humanities",             "430 members"),
            ("DS", "Data Structures & Algos",        "Computer Science",       "3,200 members"),
            ("GH", "Global Health Policy",           "Public Health",          "510 members"),
            ("UX", "Digital Art & UX Theory",        "Design",                 "940 members"),
            ("QC", "Quantum Computing Basics",       "Physics",                "620 members"),
            ("CY", "Cybersecurity Essentials",       "Engineering",            "1,850 members"),
            ("BE", "Behavioral Economics",           "Social Science",         "480 members"),
            ("DM", "Digital Marketing Strategy",     "Business",               "710 members"),
            ("MT", "Music Theory & Composition",     "Arts",                   "350 members"),
            ("RE", "Renewable Energy Systems",       "Environmental Science",  "590 members"),
        ]

        gf = tk.Frame(sc, bg=BG)
        gf.pack(fill="both", expand=True, padx=10, pady=10)
        for i, d in enumerate(groups):
            self._group_card(gf, d).grid(row=i // 3, column=i % 3,
                                         padx=10, pady=10, sticky="nsew")
            gf.grid_columnconfigure(i % 3, weight=1)

    def _group_card(self, parent, data):
        initials, title, subtitle, members = data
        card  = tk.Frame(parent, bg=CARD, highlightthickness=1, highlightbackground=BORDER)
        inner = tk.Frame(card, bg=CARD)
        inner.pack(fill="both", expand=True, padx=16, pady=16)

        top = tk.Frame(inner, bg=CARD)
        top.pack(fill="x", anchor="w")
        tk.Label(top, text=initials, font=("Arial", 9, "bold"),
                 fg=CARD, bg=WHITE, width=3, height=1).pack(side="left", padx=(0, 10))
        tk.Label(top, text=title, font=("Arial", 10, "bold"),
                 fg=WHITE, bg=CARD, wraplength=150, justify="left").pack(side="left", anchor="w")

        tk.Label(inner, text=subtitle, font=("Arial", 9), fg=WHITE, bg=CARD).pack(anchor="w", pady=(12, 0))

        foot = tk.Frame(inner, bg=CARD)
        foot.pack(fill="x", side="bottom", pady=(12, 0))
        tk.Label(foot, text=members,        font=("Arial", 8), fg=WHITE, bg=CARD).pack(side="left")
        tk.Label(foot, text="Join Group →", font=("Arial", 8), fg=WHITE, bg=CARD,
                 cursor="hand2").pack(side="right")
        return card
