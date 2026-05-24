Markdown
# Baiboly FKF - Studio Control & Projection

Application desktop moderne de projection biblique et de gestion de messages en direct pour les services de culte, développée en Python (CustomTkinter) avec une base de données SQLite.

---

## 🛠️ Installation & Lancement

1. Placez-vous dans le dossier du projet :
   ```bash
   cd chemin/vers/le/projet
Installez la seule dépendance requise :

Bash
pip install customtkinter
Lancez l'application :

Bash
python app.py
⚠️ Important : Le fichier de la base de données moteur_bible.db doit obligatoirement se trouver dans le même dossier que app.py.

🚀 Utilisation Rapide
Recherche de versets : Saisissez la référence (ex: Jaona 3:16, Matio 5 ou Romana 8:1-10) dans le champ supérieur et appuyez sur Entrée.

Navigation : Utilisez les boutons Aloha (Précédent) et Manaraka (Suivant) à droite pour contrôler l'écran de projection.

Message direct (Annonces / Cantiques) : Écrivez votre texte dans la case en bas à gauche et appuyez sur Entrée pour l'afficher centré sur l'écran.

📦 Compilation en .EXE (Windows)
Pour créer l'exécutable autonome pour la régie, installez PyInstaller et lancez cette commande unique :

Bash
pip install pyinstaller
pyinstaller --noconfirm --onedir --windowed --add-data "moteur_bible.db;." app.py
