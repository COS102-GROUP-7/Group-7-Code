# page_chat.py  —  Person 2
# GLOBAL CHAT PAGE
# Branch: page/chat


import tkinter as tk

from constants import WHITE

CHAT_BG     = "#0b1120"
BUBBLE_BG   = "#1e293b"
CHAT_BORDER = "#334155"
CHAT_TEAL   = "#06b6d4"
CHAT_MUTED  = "#94a3b8"


class GlobalChatPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=CHAT_BG)

        # Header
        header = tk.Frame(self, bg=CHAT_BG)
        header.pack(fill="x", pady=(0, 20), padx=20)
        tk.Label(header, text="Global Chat",
                 font=("Georgia", 18, "bold"), fg=WHITE, bg=CHAT_BG).pack(side="left")
        tk.Button(header, text="+ Global Chat", font=("Arial", 9, "bold"),
                  bg=CHAT_TEAL, fg=WHITE, relief="flat", bd=0,
                  cursor="hand2", padx=14, pady=6).pack(side="right")

        #  Scrollable message area
        chat_box = tk.Frame(self, bg=CHAT_BG,
                            highlightthickness=1, highlightbackground=CHAT_BORDER)
        chat_box.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        canvas = tk.Canvas(chat_box, bg=CHAT_BG, highlightthickness=0)
        sb = tk.Scrollbar(chat_box, orient="vertical", command=canvas.yview)
        self._msg_frame = tk.Frame(canvas, bg=CHAT_BG)
        sw = canvas.create_window((0, 0), window=self._msg_frame, anchor="nw")

        canvas.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        canvas.bind("<Configure>", lambda e: canvas.itemconfig(sw, width=e.width))
        self._msg_frame.bind("<Configure>",
                             lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Seed messages 
        avatar_colors = {
            "Alexa Smith":    "#0ea5e9",
            "Ragnar Crimson": "#d97706",
            "Sasaki Kojiro":  "#8b5cf6",
            "Eren Jaeger":    "#14b8a6",
        }
        messages = [
            {"name": "Alexa Smith",    "initials": "AS", "is_me": False,
             "text": "Is everyone here joining the AI & Ethics Summit later?"},
            {"name": "Ragnar Crimson", "initials": "RC", "is_me": False,
             "text": "I'm definitely going. The panel on algorithmic bias sounds fascinating."},
            {"name": "Sasaki Kojiro",  "initials": "SK", "is_me": False,
             "text": "Same! I'm hoping they discuss open-source constraints."},
            {"name": "Alexa Smith",    "initials": "AS", "is_me": False,
             "text": "If anyone wants to sync up afterwards for a debrief, let me know."},
            {"name": "Sasaki Kojiro",  "initials": "SK", "is_me": False,
             "text": "That's a great idea, count me in. I'll be in the lobby at 5."},
            {"name": "Eren Jaeger",    "initials": "EJ", "is_me": True,
             "text": "Perfect. I'll see you all there!"},
        ]
        for msg in messages:
            self._add_message(msg, avatar_colors)

        # Input bar
        inp = tk.Frame(self, bg=CHAT_BG)
        inp.pack(fill="x", padx=20, pady=(0, 20))
        eb = tk.Frame(inp, bg=CHAT_BG,
                      highlightthickness=1, highlightbackground=CHAT_BORDER)
        eb.pack(side="left", fill="both", expand=True)

        self._ph    = "What do you want to say"
        self._entry = tk.Entry(eb, font=("Arial", 11), bg=CHAT_BG,
                               fg=CHAT_MUTED, bd=0, insertbackground=WHITE)
        self._entry.pack(fill="both", expand=True, padx=10, pady=12)
        self._entry.insert(0, self._ph)
        self._entry.bind("<FocusIn>",  self._clear_ph)
        self._entry.bind("<FocusOut>", self._restore_ph)

        tk.Button(inp, text="Send >", font=("Arial", 10, "bold"),
                  bg=CHAT_BORDER, fg=WHITE, relief="flat", bd=0,
                  cursor="hand2").pack(side="right", fill="y", padx=(10, 0))

    # Message builder

    def _add_message(self, msg, avatar_colors):
        row  = tk.Frame(self._msg_frame, bg=CHAT_BG)
        row.pack(fill="x", pady=10)
        wrap = tk.Frame(row, bg=CHAT_BG)
        wrap.pack(side="right" if msg["is_me"] else "left")

        av_color = avatar_colors.get(msg["name"], "#64748b")
        av = tk.Frame(wrap, bg=av_color, width=36, height=36)
        av.pack_propagate(False)
        tk.Label(av, text=msg["initials"], font=("Arial", 10, "bold"),
                 fg=WHITE, bg=av_color).place(relx=.5, rely=.5, anchor="center")

        bub = tk.Frame(wrap, bg=BUBBLE_BG)
        if msg["is_me"]:
            tk.Label(bub, text=msg["name"], font=("Arial", 9, "bold"),
                     fg=CHAT_TEAL, bg=BUBBLE_BG).pack(anchor="e", padx=12, pady=(8, 2))
            tk.Label(bub, text=msg["text"], font=("Arial", 10),
                     fg=WHITE, bg=BUBBLE_BG, justify="right").pack(anchor="e", padx=12, pady=(0, 8))
            bub.pack(side="left", padx=(0, 10))
            av.pack(side="right")
        else:
            tk.Label(bub, text=msg["name"], font=("Arial", 9, "bold"),
                     fg=CHAT_TEAL, bg=BUBBLE_BG).pack(anchor="w", padx=12, pady=(8, 2))
            tk.Label(bub, text=msg["text"], font=("Arial", 10),
                     fg=WHITE, bg=BUBBLE_BG, justify="left").pack(anchor="w", padx=12, pady=(0, 8))
            av.pack(side="left")
            bub.pack(side="left", padx=(10, 0))

    def _clear_ph(self, e):
        if self._entry.get() == self._ph:
            self._entry.delete(0, tk.END)
            self._entry.config(fg=WHITE)

    def _restore_ph(self, e):
        if not self._entry.get():
            self._entry.insert(0, self._ph)
            self._entry.config(fg=CHAT_MUTED)
