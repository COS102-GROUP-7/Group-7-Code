import csv
import os
import tkinter as tk
from tkinter import messagebox

from constants import BG, CARD, TEAL, WHITE, MUTED, FIELD_BG, BORDER

DB = "login.csv"

def setup_db():
    """Create login.csv with a default user if it does not exist."""
    if os.path.exists(DB):
        return
    with open(DB, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["username", "password", "display_name"])
        writer.writeheader()
        writer.writerow({"username": "kevin", "password": "The best", "display_name": "Kevin"})


def check_logins(user, pw):
    """Return display_name on success, None on failure."""
    try:
        with open(DB, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if row["username"].strip() == user and row["password"].strip() == pw:
                    return row.get("display_name", user)
    except FileNotFoundError:
        messagebox.showerror("Oops", "Login database is missing.")
    return None


def user_exists(user):
    """Check if a username already exists in login.csv (case-insensitive)."""
    try:
        with open(DB, newline="", encoding="utf-8") as f:
            return any(row["username"].strip().lower() == user.strip().lower() 
                       for row in csv.DictReader(f))
    except FileNotFoundError:
        return False


def save_new_user(name, user, pw, parent_win):
    """Append a new user to login.csv after processing UI safety requirements."""
    if len(pw) < 6:
        messagebox.showwarning("Weak password", "Password must be at least 6 characters long.", parent=parent_win)
        return False
        
    if user_exists(user):
        messagebox.showerror("Username taken", "Please choose a different username.", parent=parent_win)
        return False

    with open(DB, "a", newline="", encoding="utf-8") as f:
        csv.DictWriter(f, fieldnames=["username", "password", "display_name"]).writerow(
            {"username": user, "password": pw, "display_name": name}
        )
    return True


def _entry_field(parent, label, hidden=False):
    tk.Label(parent, text=label, font=("Arial", 9), fg=MUTED, bg=CARD).pack(anchor="w", pady=(12, 2))
    e = tk.Entry(parent, font=("Arial", 11), bg=FIELD_BG, fg=WHITE,
                 insertbackground=WHITE, relief="flat", bd=0,
                 highlightthickness=1, highlightbackground=BORDER, highlightcolor=TEAL)
    if hidden:
        e.config(show="*")
    e.pack(fill="x", ipady=7)
    return e


def _card(win, height):
    f = tk.Frame(win, bg=CARD, bd=0, highlightthickness=1, highlightbackground=BORDER)
    f.place(relx=0.5, rely=0.5, anchor="center", width=370, height=height)
    return f



class LoginWindow:
    def __init__(self, root, on_success):
        self.root = root
        self.on_success = on_success

        self.win = tk.Toplevel(root)
        self.win.title("PeerSphere")
        self.win.geometry("900x600")
        self.win.configure(bg=BG)
        self.win.protocol("WM_DELETE_WINDOW", self.root.destroy)
        self._build()

    def _build(self):
        card = _card(self.win, 415)
        body = tk.Frame(card, bg=CARD)
        body.pack(fill="both", expand=True, padx=34, pady=28)

        top = tk.Frame(body, bg=CARD)
        top.pack()
        tk.Label(top, text="❖ ", font=("Georgia", 20), fg=TEAL, bg=CARD).pack(side="left")
        info = tk.Frame(top, bg=CARD)
        info.pack(side="left")
        tk.Label(info, text="PeerSphere", font=("Georgia", 17, "bold"), fg=WHITE, bg=CARD).pack(anchor="w")
        tk.Label(info, text="Connecting students worldwide", font=("Arial", 8), fg=MUTED, bg=CARD).pack(anchor="w")

        self.u_entry = _entry_field(body, "Username")
        self.p_entry = _entry_field(body, "Password", hidden=True)

        tk.Button(body, text="Log in  →", font=("Arial", 11, "bold"),
                  bg=TEAL, fg=WHITE, activebackground="#0096B7",
                  relief="flat", cursor="hand2", bd=0,
                  command=self._try_login).pack(fill="x", pady=(20, 0), ipady=9)

        row = tk.Frame(body, bg=CARD)
        row.pack(pady=(11, 0))
        tk.Label(row, text="New here?  ", font=("Arial", 9), fg=MUTED, bg=CARD).pack(side="left")
        link = tk.Label(row, text="Create an account",
                        font=("Arial", 9, "underline"), fg=TEAL, bg=CARD, cursor="hand2")
        link.pack(side="left")
        link.bind("<Button-1>", lambda e: (self.win.withdraw(),
                                           RegisterWindow(self, self.on_success)))

    def _try_login(self):
        u = self.u_entry.get().strip()
        p = self.p_entry.get().strip()
        if not u or not p:
            messagebox.showwarning("Hold on", "Both fields are required.", parent=self.win)
            return
        display_name = check_logins(u, p)
        if display_name:
            self.win.destroy()
            self.on_success(display_name, u)
        else:
            messagebox.showerror("Login failed", "Invalid username or password.", parent=self.win)


class RegisterWindow:
    def __init__(self, login_win_instance, on_success):
        self.login_win_instance = login_win_instance
        self.on_success = on_success

        self.win = tk.Toplevel()
        self.win.title("PeerSphere — Sign Up")
        self.win.geometry("900x600")
        self.win.configure(bg=BG)
        self.win.protocol("WM_DELETE_WINDOW", self._go_back)
        self._build()

    def _build(self):
        card = _card(self.win, 515) 
        body = tk.Frame(card, bg=CARD)
        body.pack(fill="both", expand=True, padx=34, pady=24)

        tk.Label(body, text="✦  Create Account",
                 font=("Georgia", 16, "bold"), fg=TEAL, bg=CARD).pack(anchor="w")
        tk.Label(body, text="Join thousands of students worldwide",
                 font=("Arial", 9), fg=MUTED, bg=CARD).pack(anchor="w", pady=(2, 0))

        self.name_f = _entry_field(body, "Display Name")
        self.user_f = _entry_field(body, "Username")
        self.pass_f = _entry_field(body, "Password", hidden=True)
        self.conf_f = _entry_field(body, "Confirm Password", hidden=True)

        tk.Button(body, text="Create Account  →", font=("Arial", 11, "bold"),
                  bg=TEAL, fg=WHITE, activebackground="#0096B7",
                  relief="flat", cursor="hand2", bd=0,
                  command=self._try_register).pack(fill="x", pady=(20, 0), ipady=9)

        row = tk.Frame(body, bg=CARD)
        row.pack(pady=(12, 0))
        tk.Label(row, text="Already a member?  ", font=("Arial", 9), fg=MUTED, bg=CARD).pack(side="left")
        back = tk.Label(row, text="Sign in",
                        font=("Arial", 9, "underline"), fg=TEAL, bg=CARD, cursor="hand2")
        back.pack(side="left")
        back.bind("<Button-1>", lambda e: self._go_back())

    def _try_register(self):
        dn = self.name_f.get().strip()
        u = self.user_f.get().strip()
        p = self.pass_f.get()
        cp = self.conf_f.get()
        
        if not all([dn, u, p, cp]):
            messagebox.showwarning("Incomplete", "Please fill all fields.", parent=self.win)
            return
        if p != cp:
            messagebox.showerror("Mismatch", "Passwords don't match.", parent=self.win)
            return

        if save_new_user(dn, u, p, self.win):
            messagebox.showinfo("Success", f"Account created! Welcome, {dn}!", parent=self.win)
            self._go_back()

    def _go_back(self):
        self.win.destroy()
        self.login_win_instance.win.deiconify()