import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os

VBOXMANAGE_PATH = r"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe"

def select_img():
    file = filedialog.askopenfilename(
        title="IMG-Datei auswählen",
        filetypes=[("IMG Files", "*.img"), ("All Files", "*.*")]
    )
    if file:
        input_entry.delete(0, tk.END)
        input_entry.insert(0, file)

        output = os.path.splitext(file)[0] + ".vdi"
        output_entry.delete(0, tk.END)
        output_entry.insert(0, output)

def convert():
    input_file = input_entry.get()
    output_file = output_entry.get()

    if not os.path.isfile(input_file):
        messagebox.showerror("Fehler", "IMG-Datei nicht gefunden")
        return

    if not os.path.isfile(VBOXMANAGE_PATH):
        messagebox.showerror("Fehler", "VBoxManage.exe nicht gefunden")
        return

    cmd = [
        VBOXMANAGE_PATH,
        "convertfromraw",
        input_file,
        output_file,
        "--format",
        "VDI"
    ]

    try:
        status_label.config(text="Konvertierung läuft...")
        root.update()

        subprocess.run(cmd, check=True)

        status_label.config(text="Fertig!")
        messagebox.showinfo("Erfolg", "IMG wurde erfolgreich in VDI konvertiert")

    except subprocess.CalledProcessError as e:
        status_label.config(text="Fehler!")
        messagebox.showerror("Fehler", f"Konvertierung fehlgeschlagen:\n{e}")

# ---------- GUI ----------
root = tk.Tk()
root.title("IMG → VDI Converter (VBoxManage)")
root.geometry("520x220")
root.resizable(False, False)

tk.Label(root, text="IMG-Datei:").pack(anchor="w", padx=10, pady=5)
input_entry = tk.Entry(root, width=70)
input_entry.pack(padx=10)

tk.Button(root, text="Durchsuchen", command=select_img).pack(pady=5)

tk.Label(root, text="Output VDI:").pack(anchor="w", padx=10, pady=5)
output_entry = tk.Entry(root, width=70)
output_entry.pack(padx=10)

tk.Button(root, text="Konvertieren", command=convert, bg="#4CAF50", fg="white").pack(pady=15)

status_label = tk.Label(root, text="Bereit")
status_label.pack()

root.mainloop()
