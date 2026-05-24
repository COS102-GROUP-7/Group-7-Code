# page_profile.py
# USER PROFILE PAGE
# Branch: page/profile

import tkinter as tk
from tkinter import messagebox

from constants import (BG, CARD, TEAL, WHITE, MUTED,
                       FIELD_BG, BORDER, ACCENT2)


class UserProfilePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller
        self._built     = False

    def refresh(self):
        if self._built:
            return
        self._built = True
        self._build()

    def _build(self):
        username = getattr(self.controller, "display_name", "User")

        # Page header
        header = tk.Frame(self, bg=BG)
        header.pack(fill="x", pady=(0, 18), padx=20)
        tk.Label(header, text="User Profile",
                 font=("Georgia", 18, "bold"), fg=WHITE, bg=BG).pack(side="left")
        tk.Label(header, text="Manage your personal details",
                 font=("Arial", 9), fg=MUTED, bg=BG).pack(side="left", padx=(12, 0), pady=(6, 0))

        #  Avatar card
        top_card  = tk.Frame(self, bg=CARD, highlightthickness=1, highlightbackground=BORDER)
        top_card.pack(fill="x", padx=20, pady=(0, 14))
        inner_top = tk.Frame(top_card, bg=CARD)
        inner_top.pack(fill="x", padx=24, pady=20)

        av = tk.Frame(inner_top, bg=TEAL, width=64, height=64)
        av.pack(side="left")
        av.pack_propagate(False)
        initials = "".join(p[0].upper() for p in username.split()[:2])
        tk.Label(av, text=initials, font=("Georgia", 20, "bold"),
                 fg=WHITE, bg=TEAL).place(relx=.5, rely=.5, anchor="center")

        nb = tk.Frame(inner_top, bg=CARD)
        nb.pack(side="left", padx=18)
        tk.Label(nb, text=username,               font=("Georgia", 16, "bold"), fg=WHITE, bg=CARD).pack(anchor="w")
        tk.Label(nb, text="● Online  •  Student", font=("Arial", 9),            fg=TEAL,  bg=CARD).pack(anchor="w", pady=(2, 0))
        tk.Label(nb, text="Joined PeerSphere  •  Active in 3 clusters",
                 font=("Arial", 8), fg=MUTED, bg=CARD).pack(anchor="w")

        self._edit_mode = [False]
        self._edit_btn  = tk.Button(inner_top, text="✏  Edit Profile",
                                    font=("Arial", 9, "bold"), bg=FIELD_BG, fg=WHITE,
                                    activebackground=CARD, activeforeground=TEAL,
                                    relief="flat", bd=0, cursor="hand2",
                                    highlightthickness=1, highlightbackground=BORDER,
                                    padx=12, pady=6, command=self._toggle_edit)
        self._edit_btn.pack(side="right")

        #  Two-column layout 
        cols = tk.Frame(self, bg=BG)
        cols.pack(fill="both", expand=True, padx=20)

        left_col  = tk.Frame(cols, bg=BG)
        right_col = tk.Frame(cols, bg=BG)
        left_col.pack(side="left",  fill="both", expand=True, padx=(0, 12))
        right_col.pack(side="right", fill="both", expand=True)

        # Personal Info card
        self._fields   = {}
        info_card  = tk.Frame(left_col, bg=CARD, highlightthickness=1, highlightbackground=BORDER)
        info_card.pack(fill="x", pady=(0, 14))
        info_inner = tk.Frame(info_card, bg=CARD)
        info_inner.pack(fill="x", padx=20, pady=16)
        tk.Label(info_inner, text="PERSONAL INFO",
                 font=("Arial", 8, "bold"), fg=MUTED, bg=CARD).pack(anchor="w", pady=(0, 10))

        for lbl, default in [
            ("Display Name", username),
            ("Username",     username.lower().replace(" ", "_")),
            ("Email",        "user@peersphere.io"),
            ("University",   "University of Lagos"),
            ("Country",      "Nigeria"),
        ]:
            self._add_field(info_inner, lbl, default)

        self._save_btn = tk.Button(info_inner, text="Save Changes",
                                   font=("Arial", 10, "bold"),
                                   bg=TEAL, fg=WHITE, activebackground=ACCENT2,
                                   relief="flat", bd=0, cursor="hand2",
                                   pady=8, command=self._save_changes)

        # Activity Stats card
        stats_card  = tk.Frame(right_col, bg=CARD, highlightthickness=1, highlightbackground=BORDER)
        stats_card.pack(fill="x", pady=(0, 14))
        stats_inner = tk.Frame(stats_card, bg=CARD)
        stats_inner.pack(fill="x", padx=20, pady=16)
        tk.Label(stats_inner, text="ACTIVITY STATS",
                 font=("Arial", 8, "bold"), fg=MUTED, bg=CARD).pack(anchor="w", pady=(0, 10))
        for stat_lbl, val in [("Study Sprint Hours",   "14.5 hrs"),
                               ("Collaborative Streak", "9 days"),
                               ("Clusters Joined",      "3"),
                               ("Peers Connected",      "12"),
                               ("Regions Reached",      "8")]:
            r = tk.Frame(stats_inner, bg=CARD)
            r.pack(fill="x", pady=4)
            tk.Label(r, text=stat_lbl, font=("Arial", 9),         fg=MUTED, bg=CARD).pack(side="left")
            tk.Label(r, text=val,      font=("Arial", 9, "bold"), fg=TEAL,  bg=CARD).pack(side="right")

        # Badges card
        badges_card  = tk.Frame(right_col, bg=CARD, highlightthickness=1, highlightbackground=BORDER)
        badges_card.pack(fill="x")
        badges_inner = tk.Frame(badges_card, bg=CARD)
        badges_inner.pack(fill="x", padx=20, pady=16)
        tk.Label(badges_inner, text="BADGES",
                 font=("Arial", 8, "bold"), fg=MUTED, bg=CARD).pack(anchor="w", pady=(0, 10))
        badge_row = tk.Frame(badges_inner, bg=CARD)
        badge_row.pack(anchor="w")
        for icon, tip in [("🌍", "Global Collab"), ("🔥", "9-Day Streak"),
                          ("💡", "Idea Starter"),  ("🏆", "Top Contributor")]:
            b = tk.Frame(badge_row, bg=FIELD_BG, highlightthickness=1,
                         highlightbackground=BORDER, width=52, height=52)
            b.pack(side="left", padx=(0, 8))
            b.pack_propagate(False)
            tk.Label(b, text=icon, font=("Arial", 18), bg=FIELD_BG).place(relx=.5, rely=.38, anchor="center")
            tk.Label(b, text=tip,  font=("Arial", 6),  fg=MUTED, bg=FIELD_BG).place(relx=.5, rely=.82, anchor="center")

    def _add_field(self, parent, field_label, default):
        wrapper = tk.Frame(parent, bg=CARD)
        wrapper.pack(fill="x", pady=(0, 8))
        tk.Label(wrapper, text=field_label, font=("Arial", 8), fg=MUTED, bg=CARD).pack(anchor="w")
        var = tk.StringVar(value=default)
        lbl = tk.Label(wrapper, textvariable=var, font=("Arial", 10),
                       fg=WHITE, bg=CARD, anchor="w")
        lbl.pack(fill="x")
        ent = tk.Entry(wrapper, textvariable=var, font=("Arial", 10),
                       bg=FIELD_BG, fg=WHITE, insertbackground=WHITE,
                       relief="flat", bd=0, highlightthickness=1,
                       highlightbackground=BORDER, highlightcolor=TEAL)
        ent.config(state="disabled")
        self._fields[field_label] = (lbl, ent, var)

    def _toggle_edit(self):
        editing = not self._edit_mode[0]
        self._edit_mode[0] = editing
        for lbl, ent, var in self._fields.values():
            if editing:
                lbl.pack_forget()
                ent.config(state="normal")
                ent.pack(fill="x", ipady=6)
            else:
                ent.pack_forget()
                ent.config(state="disabled")
                lbl.pack(fill="x")
        if editing:
            self._edit_btn.config(text="✕  Cancel")
            self._save_btn.pack(fill="x", pady=(12, 0), ipady=2)
        else:
            self._edit_btn.config(text="✏  Edit Profile")
            self._save_btn.pack_forget()

    def _save_changes(self):
        self._toggle_edit()
        messagebox.showinfo("Saved", "Your profile has been updated!")
