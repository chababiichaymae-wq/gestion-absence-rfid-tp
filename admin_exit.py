import customtkinter as ctk


admin_code = "admin"

def admin_exit(app):
    root = ctk.CTkToplevel(app)
    root.geometry("400x250")
    root.title("Admin Exit")

    root.attributes("-topmost", True)

    ctk.CTkLabel(root,text="Entrer le code ADMIN", font=("Arial", 24, "bold")).pack(pady=(30,5))

    entry = ctk.CTkEntry(root,width=280,height=45,font=("Courier", 20), justify="center",placeholder_text="admin_code")
    entry.pack(pady=(0,20))

    def check():
        if entry.get() == admin_code:
            app.destroy()
        else:
            root.destroy()

    ctk.CTkButton(root, text="OK", command=check,width=130,height=40,corner_radius=12).pack(padx=5)

    root.bind("<Return>", lambda event: check())

    root.mainloop()

