import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os

VBOXMANAGE_PATH = r"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe"

# ---------- Sprachpakete ----------
LANG = {
    "de": {
        "title": "IMG → VDI Konverter",
        "img": "IMG-Datei:",
        "out": "Output VDI:",
        "browse": "Durchsuchen",
        "convert": "Konvertieren",
        "ready": "Bereit",
        "running": "Konvertierung läuft...",
        "done": "Fertig!",
        "err_img": "IMG-Datei nicht gefunden",
        "err_vbox": "VBoxManage.exe nicht gefunden",
        "err_conv": "Konvertierung fehlgeschlagen",
        "success": "Konvertierung erfolgreich",
        "select_img": "IMG-Datei auswählen"
    },
    "en": {
        "title": "IMG → VDI Converter",
        "img": "IMG file:",
        "out": "Output VDI:",
        "browse": "Browse",
        "convert": "Convert",
        "ready": "Ready",
        "running": "Conversion running...",
        "done": "Done!",
        "err_img": "IMG file not found",
        "err_vbox": "VBoxManage.exe not found",
        "err_conv": "Conversion failed",
        "success": "Conversion successful",
        "select_img": "Select IMG file"
    },
    "it": {
        "title": "Convertitore IMG → VDI",
        "img": "File IMG:",
        "out": "VDI di output:",
        "browse": "Sfoglia",
        "convert": "Converti",
        "ready": "Pronto",
        "running": "Conversione in corso...",
        "done": "Completato!",
        "err_img": "File IMG non trovato",
        "err_vbox": "VBoxManage.exe non trovato",
        "err_conv": "Conversione fallita",
        "success": "Conversione riuscita",
        "select_img": "Seleziona file IMG"
    },
    "fr": {
        "title": "Convertisseur IMG → VDI",
        "img": "Fichier IMG :",
        "out": "VDI de sortie :",
        "browse": "Parcourir",
        "convert": "Convertir",
        "ready": "Prêt",
        "running": "Conversion en cours...",
        "done": "Terminé !",
        "err_img": "Fichier IMG introuvable",
        "err_vbox": "VBoxManage.exe introuvable",
        "err_conv": "Échec de la conversion",
        "success": "Conversion réussie",
        "select_img": "Sélectionner un fichier IMG"
    }
}

selected_lang = None

# ---------- Sprach-Auswahl ----------
def choose_language(lang):
    global selected_lang
    selected_lang = lang
    lang_root.destroy()

lang_root = tk.Tk()
lang_root.title("Select language / Sprache wählen")
lang_root.geometry("300x220")
lang_root.resizable(False, False)

tk.Label(
    lang_root,
    text="Select your language\nSprache auswählen",
    font=("Arial", 12, "bold")
).pack(pady=15)

tk.Button(lang_root, text="Deutsch", width=20,
          command=lambda: choose_language("de")).pack(pady=5)
tk.Button(lang_root, text="English", width=20,
          command=lambda: choose_language("en")).pack(pady=5)
tk.Button(lang_root, text="Italiano", width=20,
          command=lambda: choose_language("it")).pack(pady=5)
tk.Button(lang_root, text="Français", width=20,
          command=lambda: choose_language("fr")).pack(pady=5)

lang_root.mainloop()

# Falls Fenster geschlossen wurde
if not selected_lang:
    exit()

T = LANG[selected_lang]

# ---------- Haupt-GUI ----------
def select_img():
    file = filedialog.askopenfilename(
        title=T["select_img"],
        filetypes=[("IMG Files", "*.img"), ("All Files", "*.*")]
    )
    if file:
        input_entry.delete(0, tk.END)
        input_entry.insert(0, file)
        output_entry.delete(0, tk.END)
        output_entry.insert(0, os.path.splitext(file)[0] + ".vdi")

def convert():
    if not os.path.isfile(input_entry.get()):
        messagebox.showerror("Error", T["err_img"])
        return

    if not os.path.isfile(VBOXMANAGE_PATH):
        messagebox.showerror("Error", T["err_vbox"])
        return

    status_label.config(text=T["running"])
    root.update()

    try:
        subprocess.run([
            VBOXMANAGE_PATH,
            "convertfromraw",
            input_entry.get(),
            output_entry.get(),
            "--format",
            "VDI"
        ], check=True)

        status_label.config(text=T["done"])
        messagebox.showinfo("
