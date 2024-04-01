from flask import Flask, render_template, request, jsonify, redirect, url_for
from tkinter import messagebox

app = Flask(__name__)

class FaitsUtilisateur:
    def __init__(self):
        self.faits = []

    def ajouter_fait(self, fait):
        self.faits.append(fait)

    def supprimer_fait(self, fait):
        self.faits.remove(fait)

    def vider(self):
        self.faits = []

class Expert:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class SystemeExpert:
    def __init__(self):
        self.base_de_regles = []
        self.faits_utilisateur = FaitsUtilisateur()
        self.expert = Expert("admin", "admin")
        self.charger_regles_depuis_fichier("base.txt")

    def authentifier_expert(self, username, password):
        return username == self.expert.username and password == self.expert.password

    def charger_regles_depuis_fichier(self, fichier):
        with open(fichier, 'r') as f:
            lignes = f.readlines()
        for ligne in lignes:
            if ":" in ligne:
                conditions, organe_en_panne = ligne.strip().split(":", 1)
                conditions = conditions.split(",")
                nouvelle_regle = Regle(conditions, organe_en_panne)
                self.base_de_regles.append(nouvelle_regle)
            else:
                print("Format de ligne incorrect dans le fichier base.txt:", ligne.strip())

    def ajouter_regle_expert(self, regle):
        self.base_de_regles.append(regle)
        regle_string = ",".join(regle.conditions) + ":" + regle.organe_en_panne
        with open("base.txt", 'a') as f:
            f.write(regle_string + "\n")

    def modifier_regle_expert(self, numero_regle, nouvelle_conditions, nouvel_organe):
        self.base_de_regles[numero_regle - 1].conditions = nouvelle_conditions
        self.base_de_regles[numero_regle - 1].organe_en_panne = nouvel_organe
        self.sauvegarder_regles_dans_fichier()

    def supprimer_regle_expert(self, numero_regle):
        del self.base_de_regles[numero_regle - 1]
        self.sauvegarder_regles_dans_fichier()

    def sauvegarder_regles_dans_fichier(self):
        with open("base.txt", 'w') as f:
            for regle in self.base_de_regles:
                regle_string = ",".join(regle.conditions) + ":" + regle.organe_en_panne
                f.write(regle_string + "\n")

    def vider_faits_utilisateur(self):
        self.faits_utilisateur.vider()

    def raisonner(self):
        organes_en_panne = set()
        for regle in self.base_de_regles:
            if regle.satisfait(self.faits_utilisateur.faits):
                organes_en_panne.add(regle.organe_en_panne)
        return organes_en_panne

class Regle:
    def __init__(self, conditions, organe_en_panne):
        self.conditions = conditions
        self.organe_en_panne = organe_en_panne

    def satisfait(self, faits_utilisateur):
        return any(set(self.conditions).issubset(set(fait)) for fait in faits_utilisateur)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if systeme_expert.authentifier_expert(username, password):
        return render_template('expert.html')
    else:
        return render_template('symptoms.html', symptomes=[", ".join(regle.conditions) for regle in systeme_expert.base_de_regles])

@app.route('/diagnose', methods=['POST'])
def diagnose():
    selected_indices = request.json['selected_indices']
    faits_utilisateur = [regle.conditions for i, regle in enumerate(systeme_expert.base_de_regles) if i in selected_indices]
    for fait_utilisateur in faits_utilisateur:
        systeme_expert.faits_utilisateur.ajouter_fait(fait_utilisateur)
    organes_en_panne = systeme_expert.raisonner()
    if organes_en_panne:
        result_text = f"Les organes potentiellement en panne sont : {', '.join(organes_en_panne)}"
    else:
        result_text = "Aucun organe en panne détecté."
    systeme_expert.vider_faits_utilisateur()
    return jsonify({'result': result_text})

@app.route('/add_rule', methods=['POST'])
def add_rule():
    conditions = request.form['conditions']
    organ_en_panne = request.form['organ_en_panne']
    systeme_expert.ajouter_regle_expert(Regle(conditions.split(","), organ_en_panne))
    return "Règle ajoutée avec succès."

@app.route('/modify_or_delete_rule', methods=['POST'])
def modify_or_delete_rule():
    numero_regle = int(request.form['rule_number'])
    if 'modify' in request.form:
        
        nouvelles_conditions = request.form['new_conditions']
        nouvel_organe = request.form['new_organ']
        systeme_expert.modifier_regle_expert(numero_regle, nouvelles_conditions.split(","), nouvel_organe)
        return "Règle modifiée avec succès. Entrez la nouvelle règle."
    elif 'delete' in request.form:
        
        systeme_expert.supprimer_regle_expert(numero_regle)
        return "Règle supprimée avec succès."
    else:
        return "Action non reconnue."


@app.route('/logout')
def logout():
    return redirect(url_for('index'))

if __name__ == "__main__":
    systeme_expert = SystemeExpert()
    app.run(debug=True)
