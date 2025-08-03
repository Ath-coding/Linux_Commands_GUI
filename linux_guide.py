import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import os

# --- Dependency Checks ---
def check_and_import(package_name):
    try:
        return __import__(package_name)
    except ImportError:
        return None

def check_pip_dependencies():
    required = ["arabic_reshaper", "bidi"]
    missing = [pkg for pkg in required if check_and_import(pkg) is None]
    if missing:
        msg = (f"Missing Python packages: {', '.join(missing)}\n"
               "Run 'sudo bash install_dependencies.sh' to install them.")
        print(msg)
        messagebox.showwarning("Missing Dependencies", msg)


def check_apt_dependencies():
    if not os.path.exists("/etc/debian_version"):
        print("Non-Debian system. Please install dependencies manually.")
        return

    required = ["python3-tk", "fonts-noto-core", "fonts-noto-ui-core"]
    missing = []

    for pkg in required:
        try:
            subprocess.check_output(["dpkg", "-s", pkg], stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            missing.append(pkg)

    if missing:
        msg = (f"Missing system packages: {', '.join(missing)}\n"
               "Run 'sudo bash install_dependencies.sh' to install them.")
        print(msg)
        messagebox.showwarning("Missing APT Packages", msg)


# --- Arabic Support ---
arabic_reshaper = check_and_import("arabic_reshaper")
bidi = check_and_import("bidi.algorithm")
get_display = getattr(bidi, "get_display", lambda x: x)

def fix_arabic(text):
    if arabic_reshaper:
        reshaped = arabic_reshaper.reshape(text)
        return get_display(reshaped)
    return text

# --- Load Commands ---
def load_commands(file_path):
    if not os.path.exists(file_path):
        messagebox.showerror("File Not Found", f"'{file_path}' not found.")
        sys.exit(1)

    commands = []
    with open(file_path, encoding="utf-8") as f:
        for line in f:
            if ":" in line:
                cmd, desc = map(str.strip, line.strip().split(":", 1))
                commands.append((cmd, desc))
    return commands

# --- GUI Functions ---
def search_commands(*_):
    query = search_var.get().lower()
    filtered = [(cmd, desc) for cmd, desc in all_commands if query in cmd.lower() or query in desc.lower()]
    update_tree(filtered)

def update_tree(commands):
    tree.delete(*tree.get_children())
    for cmd, desc in commands:
        tree.insert("", "end", values=(cmd, fix_arabic(desc)))

def copy_command(event=None):
    selected = tree.focus()
    if not selected:
        status_label.config(text="✖ No command selected.", fg="red")
        return
    command = tree.item(selected)['values'][0]
    root.clipboard_clear()
    root.clipboard_append(command)
    status_label.config(text=f"✔ Copied: {command}", fg="green")

# --- Main UI Setup ---
def create_gui():
    global root, search_var, tree, status_label

    root = tk.Tk()
    root.title("Linux Command Reference")
    root.geometry("850x600")

    tk.Label(root, text="Search Linux Commands:", font=("Arial", 12)).pack(pady=5)
    search_var = tk.StringVar()
    search_var.trace_add("write", search_commands)
    tk.Entry(root, textvariable=search_var, width=50).pack(pady=5)

    tree_frame = ttk.Frame(root)
    tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

    columns = ("command", "description")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=20)
    tree.heading("command", text="Command")
    tree.heading("description", text="Description (Arabic)")
    tree.column("command", width=200)
    tree.column("description", width=600)
    tree.pack(fill="both", expand=True)
    tree.bind("<ButtonRelease-1>", lambda e: root.after(100, copy_command))

    status_label = tk.Label(root, text="", font=("Arial", 10), anchor="w")
    status_label.pack(fill="x", padx=10, pady=(0, 10))

    return root

# --- Main Execution ---
if __name__ == "__main__":
    check_pip_dependencies()
    check_apt_dependencies()
    all_commands = load_commands("commands_clean.txt")
    root = create_gui()
    update_tree(all_commands)
    root.mainloop()
