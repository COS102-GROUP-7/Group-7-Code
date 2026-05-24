# page_events.py  

# EVENTS PAGE
# Branch: page/events

import tkinter as tk

from constants import BG, TEAL, WHITE, MUTED, BORDER, ACCENT2


class EventsPage(tk.Frame):
    # Category background colours
    CAT_TECH     = "#2e1065"
    CAT_GLOBAL   = "#451a03"
    CAT_ACADEMIC = "#1e293b"
    CAT_SPRINT   = "#115e59"

    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)

        #Header 
        header = tk.Frame(self, bg=BG)
        header.pack(fill="x", pady=(0, 20), padx=20)
        tk.Label(header, text="PeerSphere Events",
                 font=("Georgia", 18, "bold"), fg=WHITE, bg=BG).pack(side="left")
        tk.Button(header, text="+ Global AI Events", font=("Arial", 9, "bold"),
                  bg=TEAL, fg=WHITE, activebackground=ACCENT2,
                  relief="flat", bd=0, cursor="hand2", padx=14, pady=6).pack(side="right")

        #  Scrollable grid 
        canvas = tk.Canvas(self, bg=BG, highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True, padx=(20, 0))
        sb = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        sb.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=sb.set)

        sc  = tk.Frame(canvas, bg=BG)
        win = canvas.create_window((0, 0), window=sc, anchor="nw")
        sc.bind("<Configure>",     lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(win, width=e.width))
        canvas.bind_all("<MouseWheel>",
                        lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

        categorized_events = {
            "💻 TECH & AI DEVELOPMENTS": [
                ("💻", "Global AI & Ethics Summit",  self.CAT_TECH,     "1,240 members", "Starts in 5m",    "Discuss ethical implications of AI in modern education."),
                ("⚛",  "Quantum Computing Class",     self.CAT_TECH,     "430 members",   "Join Session",    "Introductory masterclass on quantum algorithms."),
                ("🚀", "Global Hackathon 2026",        self.CAT_TECH,     "2,100 members", "Starts Tomorrow", "Build software solutions addressing global climate change."),
                ("🧬", "Bioinformatics Workshop",      self.CAT_TECH,     "275 members",   "Starts in 2h",    "Data science revolutionizing genetics and healthcare."),
            ],
            "🌍 GLOBAL & COMMUNITY FORUMS": [
                ("🌍", "Pan-African Tech Forum",       self.CAT_GLOBAL,   "850 members",   "Join Session",    "African students showcase innovative software solutions."),
                ("🗣️", "Language Exchange Mixer",      self.CAT_GLOBAL,   "1,850 members", "In Progress",     "Practice your target language with native speakers."),
            ],
            "📚 ACADEMIC & FINANCE SYMPOSIUMS": [
                ("⚖",  "International Law Symposium", self.CAT_ACADEMIC, "315 members",   "Join Session",    "Debate international treaties with law students worldwide."),
                ("📈", "Global Economics Forum",       self.CAT_ACADEMIC, "620 members",   "Join Session",    "Analyze emerging market trends with finance majors."),
            ],
            "⏱️ FOCUS SPRINTS & PRACTICAL WORKSHOPS": [
                ("⏱",  "24-Hour Study Sprint",         self.CAT_SPRINT,   "5,000+ members", "In Progress",   "Focused continuous study session with Pomodoro breaks."),
                ("🎨", "Digital Art & UX Masterclass", self.CAT_SPRINT,   "940 members",    "Join Session",  "Modern UI/UX principles with industry pros."),
                ("🌿", "Sustainability Hackathon",      self.CAT_SPRINT,   "1,150 members",  "Starts Monday", "Eco-friendly tech solutions for university campuses."),
                ("📝", "Thesis Writing Retreat",        self.CAT_SPRINT,   "890 members",    "In Progress",   "Quiet, accountable co-working space for deep writing."),
            ],
        }

        for heading, events in categorized_events.items():
            sf = tk.Frame(sc, bg=BG)
            sf.pack(fill="x", pady=(20, 10), padx=10)
            tk.Label(sf, text=heading, font=("Arial", 11, "bold"), fg=WHITE, bg=BG).pack(anchor="w")
            tk.Frame(sc, bg="#1e293b", height=1).pack(fill="x", padx=10, pady=(0, 10))

            gf = tk.Frame(sc, bg=BG)
            gf.pack(fill="x", padx=10, pady=(0, 20))
            for i, data in enumerate(events):
                self._event_card(gf, data).grid(row=i // 3, column=i % 3,
                                                padx=10, pady=10, sticky="nsew")
                gf.grid_columnconfigure(i % 3, weight=1)

    def _event_card(self, parent, data):
        icon, title, color, members, status, desc = data
        card  = tk.Frame(parent, bg=color, highlightthickness=1, highlightbackground=BORDER)
        inner = tk.Frame(card, bg=color)
        inner.pack(fill="both", expand=True, padx=16, pady=16)

        top = tk.Frame(inner, bg=color)
        top.pack(fill="x")
        tk.Label(top, text=icon,  font=("Arial", 22), bg=color, fg=WHITE).pack(side="left", padx=(0, 10))
        tk.Label(top, text=title, font=("Arial", 10, "bold"), fg=WHITE, bg=color,
                 wraplength=160, justify="left").pack(side="left", anchor="w")
        tk.Label(inner, text=desc, font=("Arial", 9), fg=MUTED, bg=color,
                 wraplength=200, justify="left").pack(anchor="w", pady=(10, 0))

        foot = tk.Frame(inner, bg=color)
        foot.pack(fill="x", side="bottom", pady=(12, 0))
        tk.Label(foot, text=f"⊙ {members}", font=("Arial", 8), fg=MUTED, bg=color).pack(side="left")
        tk.Label(foot, text=status,          font=("Arial", 8), fg=TEAL,  bg=color).pack(side="right")
        return card
