from flask import Flask, request, redirect, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# ================== Connexion DB ==================
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="pfe"
)
cursor = db.cursor(dictionary=True)

# ================== TEMPLATE HTML ==================
def page_template(title, content):
    return f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <title>{title}</title>
        <style>
            body {{ font-family: Arial; background:#0f172a; color:white; padding:20px; }}
            h1 {{ color:#38bdf8; }}
            nav a {{ color:#38bdf8; text-decoration:none; margin-right:10px; }}
            table {{ width:100%; border-collapse: collapse; margin-top:20px; }}
            th, td {{ padding:10px; border:1px solid #94a3b8; text-align:left; }}
            input {{ padding:5px; margin-top:5px; margin-bottom:10px; border-radius:5px; border:none; }}
            button {{ padding:5px 10px; border:none; border-radius:5px; background:#38bdf8; color:#020617; cursor:pointer; }}
        </style>
    </head>
    <body>
        <h1>{title}</h1>
        <nav>
            <a href="/dashboard">Dashboard</a>
            <a href="/etudiants">Étudiants</a>
            <a href="/presences">Présences</a>
            <a href="/salles">Salles</a>
            <a href="/emploi">Emploi</a>
            <a href="/parametre">Paramètres</a>
        </nav>
        <hr>
        {content}
    </body>
    </html>
    """

# ================== ROUTES ==================
@app.route('/')
def home():
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    content = "<p>Bienvenue sur le Dashboard du système de présence.</p>"
    return page_template("Dashboard", content)

@app.route('/etudiants')
def etudiants():
    cursor.execute("SELECT * FROM etudiants")
    rows = cursor.fetchall()
    if not rows:
        table = "<p>Aucun étudiant trouvé.</p>"
    else:
        table = "<table><tr><th>ID</th><th>Nom</th><th>Filière</th><th>Année</th></tr>"
        for r in rows:
            table += f"<tr><td>{r['id']}</td><td>{r['nom']}</td><td>{r['filiere']}</td><td>{r['annee']}</td></tr>"
        table += "</table>"
    return page_template("Liste des Étudiants", table)

@app.route('/presences')
def presences():
    content = "<p>Page de gestion des présences (à compléter)</p>"
    return page_template("Présences", content)

@app.route('/salles')
def salles():
    cursor.execute("SELECT * FROM salles")
    rows = cursor.fetchall()
    if not rows:
        table = "<p>Aucune salle trouvée.</p>"
    else:
        table = "<table><tr><th>ID</th><th>Nom</th><th>PCs totaux</th><th>PCs utilisés</th><th>Statut</th></tr>"
        for r in rows:
            table += f"<tr><td>{r['id']}</td><td>{r['nom']}</td><td>{r['total_pcs']}</td><td>{r['pcs_utilises']}</td><td>{r['statut']}</td></tr>"
        table += "</table>"
    return page_template("Salles", table)

@app.route('/emploi')
def emploi():
    filiere = request.args.get('filiere','GI')
    annee = request.args.get('annee','2024')
    cursor.execute("SELECT * FROM emploi WHERE filiere=%s AND annee=%s", (filiere, annee))
    rows = cursor.fetchall()
    if not rows:
        table = "<p>Aucune séance trouvée pour cette filière/année.</p>"
    else:
        table = "<table><tr><th>Jour</th><th>Début</th><th>Fin</th><th>Module</th><th>Prof</th><th>Salle</th><th>Type</th></tr>"
        for r in rows:
            # Convertir TIME en string
            hdebut = r['heure_debut'].strftime("%H:%M") if r['heure_debut'] else ""
            hfin = r['heure_fin'].strftime("%H:%M") if r['heure_fin'] else ""
            table += f"<tr><td>{r['jour']}</td><td>{hdebut}</td><td>{hfin}</td><td>{r['module']}</td><td>{r['prof']}</td><td>{r['salle']}</td><td>{r['type_seance']}</td></tr>"
        table += "</table>"
    return page_template("Emploi du Temps", table)

@app.route('/parametre', methods=['GET','POST'])
def parametre():
    if request.method == 'POST':
        nom_app = request.form.get('nom_app')
        version = request.form.get('version')
        cursor.execute("UPDATE app_settings SET nom_app=%s, version=%s WHERE id=1", (nom_app, version))
        db.commit()
        return redirect('/parametre')
    cursor.execute("SELECT * FROM app_settings WHERE id=1")
    r = cursor.fetchone()
    if not r:
        r = {'nom_app':'ESTK Presence_System','version':'1.0'}
    content = f"""
    <form method='POST'>
        <label>Nom de l'application:</label><br>
        <input type='text' name='nom_app' value='{r['nom_app']}'><br>
        <label>Version:</label><br>
        <input type='text' name='version' value='{r['version']}'><br><br>
        <button type='submit'>Enregistrer</button>
    </form>
    """
    return page_template("Paramètres", content)

# ================== API JSON ==================
@app.route('/api/salles')
def api_salles():
    cursor.execute("SELECT * FROM salles")
    rows = cursor.fetchall()
    for r in rows:
        r['en_cours'] = r['pcs_utilises']>0
    return jsonify(rows)

@app.route('/api/emploi')
def api_emploi():
    filiere = request.args.get('filiere','GI')
    annee = request.args.get('annee','2024')
    cursor.execute("SELECT * FROM emploi WHERE filiere=%s AND annee=%s", (filiere, annee))
    rows = cursor.fetchall()
    for r in rows:
        r['heure_debut'] = r['heure_debut'].strftime("%H:%M") if r['heure_debut'] else ""
        r['heure_fin'] = r['heure_fin'].strftime("%H:%M") if r['heure_fin'] else ""
    return jsonify(rows)

@app.route('/api/etudiants')
def api_etudiants():
    cursor.execute("SELECT * FROM etudiants")
    return jsonify(cursor.fetchall())

# ================== RUN ==================
if __name__=="__main__":
    app.run(debug=True)