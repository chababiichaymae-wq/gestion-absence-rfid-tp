import customtkinter as ctk
import mysql.connector

from admin_exit import admin_exit
from apogee import check_apogee  


db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="pfe"
)
cursor = db.cursor()

def verifier(event=None):
    num = entry.get().strip()
    
    
    if not check_apogee(num):
        label_result.configure(text="Format invalide — 7 chiffres requis", text_color="orange")
        return

    
    cursor.execute("SELECT * FROM etudiants WHERE apogee=%s", (num,))
    result = cursor.fetchone()

    if result:
        label_result.configure(text="✅ Accès Autorisé", text_color="green")
        app.after(200, app.destroy)
    else:
        label_result.configure(text="❌ Étudiant Non Trouvable", text_color="red")

def supprimer():
    entry.delete(0, ctk.END)
    label_result.configure(text="")


app = ctk.CTk()
app.title("Apogée Login")
app.geometry("500x350")
app.attributes("-topmost", False)
app.overrideredirect(False)
app.protocol("WM_DELETE_WINDOW", lambda: None)

ctk.set_appearance_mode("dark")

ctk.CTkLabel(app, text="🎓 Vérification Apogée", font=("Arial", 24, "bold")).pack(pady=(30,5))
ctk.CTkLabel(app, text="Entrez votre numéro Apogée à 7 chiffres", font=("Arial", 12)).pack(pady=(0, 15))

entry = ctk.CTkEntry(app, width=280, height=45, font=("Courier", 20), justify="center", placeholder_text="0000000")
entry.pack(pady=(0,20))

btn_frame = ctk.CTkFrame(app, fg_color="transparent")
btn_frame.pack()
ctk.CTkButton(btn_frame, text="Reset", command=supprimer, width=130, height=40, corner_radius=12, fg_color="#555").pack(padx=5, side="left")
ctk.CTkButton(btn_frame, text="Vérifier", command=verifier, width=130, height=40, corner_radius=12).pack(padx=5, side="right")

label_result = ctk.CTkLabel(app, text="", font=("Arial", 18, "bold"))
label_result.pack(pady=(20,0))

app.bind('<Return>', verifier)

app.bind("<Control-Shift-Q>", lambda event: admin_exit(app))

app.resizable(False, False)
app.focus_force()
app.grab_set()

app.mainloop()
