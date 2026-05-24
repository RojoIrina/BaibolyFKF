# Baiboly FKF - Studio Control & Projection

Application desktop de projection biblique et de gestion de messages en direct pour la régie des services de culte. Interface d'administration double-écran développée en Python (CustomTkinter) et base de données relationnelle SQLite.

---

## Spécifications Techniques & Prérequis

* Langage : Python 3.x
* IHM : CustomTkinter (Thread principal asynchrone)
* Base de données : SQLite3 (Moteur de recherche insensible à la casse et aux espaces via l'opérateur LIKE)
* Arborescence requise :
  - MonProjetBible/
    |-- app.py (Script principal)
    |-- moteur_bible.db (Base SQLite contenant la table 'versets')

---

## Installation & Lancement

1. Accéder au répertoire du projet :
   cd chemin/vers/votre/projet

2. Installer la dépendance d'interface graphique :
   pip install customtkinter

3. Exécuter l'application :
   python app.py

---

## Guide d'Exploitation (Régie)

### 1. Recherche et Injection de Versets
Saisir la syntaxe dans le champ supérieur puis valider avec la touche Entrée ou le bouton AMPIDIRINA AO AMIN'NY PROGRAMME :
* Verset unique : Jaona 3:16 (ou 3 Jaona 1:4)
* Chapitre complet : Matio 5
* Plage de versets : Romana 8:1-10

### 2. Gestion de la Playlist (Panneau Latéral)
* ALOHA / MANARAKA : Commutation des versets actifs sur l'écran de projection.
* VIDER : Purge complète de la file d'attente.
* LANCER L'AUTO : Déclenchement du défilement minuté automatisé (géré par un thread indépendant pour éviter le gel de l'IHM).

### 3. Diffusion de Messages Directs (Annonces / Cantiques)
* Saisir le texte libre dans le champ Hafatra  en bas à gauche.
* Valider via Entrée pour centrer automatiquement le texte à l'écran et masquer temporairement les références bibliques actives.

---

## Compilation & Déploiement (.EXE Windows)

L'exécutable autonome regroupe l'interpréteur Python, les dépendances graphiques et la base de données sans installation requise sur le poste cible.

1. Installer l'outil de packaging :
   pip install pyinstaller

2. Exécuter la commande de compilation à la racine du projet :
   pyinstaller --noconfirm --onedir --windowed --add-data "moteur_bible.db;." app.py

### Instructions Obligatoires de Déploiement
* Le livrable est généré dans le répertoire dist/app/.
* Règle absolue : Ne jamais extraire le fichier app.exe de son dossier d'origine sous peine de rompre la liaison avec les bibliothèques système de l'interface graphique et la base de données.
* Pour l'exploitation, réaliser un clic droit sur app.exe -> Envoyer vers -> Bureau (créer un raccourci).
