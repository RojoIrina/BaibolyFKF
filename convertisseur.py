import sqlite3
import json
import os

def importer_baiboly_unique(chemin_json):
    chemin_json = os.path.abspath(chemin_json)
    
    if not os.path.exists(chemin_json):
        print(f"❌ Erreur : Le fichier '{chemin_json}' est introuvable.")
        return

    print("⚡ Connexion et initialisation de la base de données...")
    conn = sqlite3.connect('moteur_bible.db')
    cursor = conn.cursor()

    # Reconstruction propre de la table
    cursor.execute("DROP TABLE IF EXISTS versets")
    cursor.execute('''CREATE TABLE versets 
        (id INTEGER PRIMARY KEY AUTOINCREMENT, 
         livre TEXT, 
         chapitre INTEGER, 
         verset INTEGER, 
         texte_mg TEXT, 
         texte_fr TEXT, 
         texte_en TEXT)''')

    print(f"📖 Lecture du fichier unique : {os.path.basename(chemin_json)}...")
    with open(chemin_json, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except Exception as e:
            print(f"❌ Erreur lors de la lecture du JSON : {e}")
            conn.close()
            return

    # Extraction des livres
    liste_livres = data.get('books', [])
    compteur_versets = 0

    print("⏳ Extraction et insertion des textes sacrés...")
    for livre_obj in liste_livres:
        # On récupère le nom du livre (ex: "Genesisy") et on applique capitalize() par sécurité
        nom_livre = livre_obj.get('name', '').capitalize()
        
        # Parcours des chapitres du livre
        for chap_obj in livre_obj.get('chapters', []):
            num_chapitre = int(chap_obj.get('chapter'))
            
            # Parcours des versets du chapitre
            for verset_obj in chap_obj.get('verses', []):
                num_verset = int(verset_obj.get('verse'))
                texte_verset = verset_obj.get('text', '')

                # Insertion directe dans la base de données
                cursor.execute('''
                    INSERT INTO versets (livre, chapitre, verset, texte_mg) 
                    VALUES (?, ?, ?, ?)
                ''', (nom_livre, num_chapitre, num_verset, texte_verset))
                
                compteur_versets += 1
        
        print(f"✅ {nom_livre} importé.")

    # Validation et fermeture
    conn.commit()
    conn.close()
    print(f"\n🚀 TOUT EST RÉPARÉ ! {compteur_versets} versets ont été importés avec succès.")

# Lancement du traitement sur ton fichier unique
importer_baiboly_unique('./baiboly.json')