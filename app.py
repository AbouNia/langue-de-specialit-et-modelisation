from flask import Flask, render_template, request
import networkx as nx

app = Flask(__name__)

# Étape 1 : Créer un graphe de connaissances
G = nx.DiGraph()
relations = [
    ("Radiothérapie", "Techniques", "utilise des"),
    ("Radiothérapie", "Irradiation", "implique"),
    ("Radiothérapie", "Cancers", "cible les"),
    ("Techniques", "Modulation d’intensité", "comprend"),
    ("Techniques", "Radiothérapie stéréotaxique", "inclut"),
    ("Cancers", "Centres", "traités dans des"),
    ("Cancers", "Soins adaptés", "nécessitent des"),
    ("Centres", "Contrôle qualité", "assurent le"),
    ("Centres", "Recherche clinique", "sont impliqués dans la"),
    ("Recherche clinique", "Techniques", "évalue l’efficacité des"),
    ("Recherche clinique", "Soins", "vise à améliorer les"),
    ("Modulation d’intensité", "Radiothérapie", "utilisées dans la"),
    ("Radiothérapie stéréotaxique", "Radiothérapie", "utilisées dans la"),
    ("Modulation d’intensité", "Tissus sains", "permettent de minimiser"),
    ("Radiothérapie stéréotaxique", "Tissus sains", "permettent de minimiser"),
    ("Irradiation", "Radiothérapie", "est une forme de"),
    ("Soins adaptés", "Cancers", "sont nécessaires pour"),
    ("Contrôle qualité", "Centres", "est essentiel pour"),
    ("Soins", "Soins adaptés", "font partie des"),
    ("Tissus sains", "Modulation d’intensité", "aident à minimiser")
]

# Ajouter les relations au graphe
for source, target, label in relations:
    G.add_edge(source, target, label=label)

# Étape 2 : Route pour la page d'accueil
@app.route('/')
def index():
    return render_template("index.html", available_terms=list(G.nodes))

# Étape 3 : Route pour rechercher des informations
@app.route('/search', methods=['POST'])
def search():
    term = request.form['term']
    if term in G.nodes:
        neighbors = list(G[term])  # Obtenir les nœuds voisins
        if neighbors:
            relations = {neighbor: G[term][neighbor]['label'] for neighbor in neighbors}
            return render_template("result.html", term=term, relations=relations)
        else:
            return render_template("result.html", term=term, relations=None, error_message="Aucune relation associée pour ce terme.")
    else:
        return render_template("result.html", term=term, relations=None, error_message="Aucune information trouvée pour ce terme.")

# Démarrer l'application Flask
if __name__ == '__main__':
    app.run(debug=True)
