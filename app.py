import customtkinter as ctk
import sqlite3
import time
import threading
import tkinter as tk
import os
import sys

# --- GESTION DU CHEMIN DE LA BASE DE DONNÉES COMPATIBLE .EXE ---
def resource_path(relative_path):
    """ Récupère le chemin absolu des ressources, compatible développement et .EXE """
    try:
        # Dossier temporaire créé par PyInstaller
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# --- CONFIGURATION DU THÈME COULEUR ---
ctk.set_appearance_mode("light")
COLOR_ACCENT = "#f43f5e"  # Rose Premium du Logo
COLOR_ORANGE = "#fb923c"  # Orange moderne du Logo
COLOR_TEXT = "#0f172a"    # Slate Dark (Texte principal des versets)

class FenetreProjection(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.title("FKF BIBLE - PROJECTION")
        self.geometry("1000x700")
        
        # Arrière-plan premium légèrement teinté pour le confort des yeux
        self.bg_color = "#fdfdfd" 
        self.configure(fg_color=self.bg_color)
        
        self.canvas = ctk.CTkCanvas(self, bg=self.bg_color, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        self.texte_actuel = "Jesosy Kristy"
        self.ref_actuelle = "Baiboly FKF"
        
        self.bind("<Configure>", self.on_resize)

    def on_resize(self, event):
        if not self.winfo_exists():
            return
        self.afficher(self.texte_actuel, self.ref_actuelle)

    def afficher(self, texte, ref):
        if not self.winfo_exists():
            return
            
        self.texte_actuel, self.ref_actuelle = texte, ref
        
        try:
            self.canvas.delete("all")
            w, h = self.winfo_width(), self.winfo_height()
            if w < 50 or h < 50: 
                return

            font_family = "Helvetica" 

            # 1. GESTION DE LA RÉFÉRENCE (Seulement si elle n'est pas vide)
            # Si c'est un message direct, le texte prend TOUT l'écran et se centre à 50% verticalement
            if ref.strip() == "":
                hauteur_centrage = h * 0.50
                limite_hauteur = h * 0.85
            else:
                hauteur_centrage = h * 0.42
                limite_hauteur = h * 0.75
                
                # Formatage de la référence en bas
                taille_ref = int(h * 0.06) 
                ref_text = " •  " + ref.upper() + "  • "
                
                # Ombre portée douce pour la référence
                self.canvas.create_text(w/2 + 1, h*0.88 + 1, text=ref_text, font=(font_family, taille_ref, "bold"), fill="#e2e8f0")
                self.canvas.create_text(w/2, h*0.88, text=ref_text, font=(font_family, taille_ref, "bold"), fill=COLOR_ACCENT)

            # 2. ALGORITHME RESPONSIVE AMÉLIORÉ
            taille_p = int(h * 0.45)
            while taille_p > 18:
                test_font = (font_family, taille_p, "bold")
                tmp = self.canvas.create_text(0, 0, text=texte, font=test_font, width=w*0.90)
                bbox = self.canvas.bbox(tmp)
                self.canvas.delete(tmp)
                
                if bbox and (bbox[3] - bbox[1]) <= limite_hauteur: 
                    break
                taille_p -= 2

            # 3. RENDU DU TEXTE AVEC OMBRE PORTÉE (Style ProPresenter)
            # Ombre décalée en gris ardoise très doux
            self.canvas.create_text(w/2 + 2, hauteur_centrage + 2, text=texte, 
                                     font=(font_family, taille_p, "bold"),
                                     fill="#cbd5e1", width=w*0.90, justify="center")

            # Texte principal
            self.canvas.create_text(w/2, hauteur_centrage, text=texte, 
                                     font=(font_family, taille_p, "bold"),
                                     fill=COLOR_TEXT, width=w*0.90, justify="center")
                                     
        except tk.TclError:
            pass

class LogicielBible(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Baiboly FKF - Studio Control")
        self.geometry("1200x900")
        self.configure(fg_color="#ffffff")
        
        self.playlist = []
        self.index = 0
        self.auto_mode = False
        self.projection = None
        
        # Liste officielle des livres pour le ComboBox
        self.books = [
            "Genesisy", "Eksodosy", "Levitikosy", "Nomery", "Deoteronomia", "Josoa", "Mpitsara", "Rota",
            "1 Samoela", "2 Samoela", "1 Mpanjaka", "2 Mpanjaka", "1 Tantara", "2 Tantara", "Ezra", "Nehemia",
            "Estera", "Joba", "Salamo", "Ohabolana", "Mpitoriteny", "Tononkiran'i Solomona", "Isaia", "Jeremia",
            "Fitomaniana", "Ezekiela", "Daniela", "Hosea", "Joela", "Amosa", "Obadia", "Jona", "Mika", "Nahoma",
            "Habakoka", "Zefania", "Hagay", "Zakaria", "Malakia", "Matio", "Marka", "Lioka", "Jaona", "Asan'ny Apostoly",
            "Romana", "1 Korintiana", "2 Korintiana", "Galatiana", "Efesianina", "Filipiana", "Kolosiana",
            "1 Tesaloniana", "2 Tesaloniana", "1 Timoty", "2 Timoty", "Titosy", "Filemona", "Hebreo", "Jakoba",
            "1 Petera", "2 Petera", "1 Jaona", "2 Jaona", "3 Jaona", "Joda", "Apokalypsy"
        ]

        self.setup_ui()
        self.after(500, self.ouvrir_p)

    def setup_ui(self):
        # En-tête
        nav = ctk.CTkFrame(self, height=80, fg_color="white", border_width=1, border_color="#f1f5f9", corner_radius=0)
        nav.pack(fill="x")
        ctk.CTkLabel(nav, text="Baiboly FKF", font=("Arial", 28, "bold"), text_color=COLOR_ORANGE).place(x=30, y=20)
        
        # Structure Principale
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.pack(expand=True, fill="both", padx=30, pady=20)

        # PANNEAU GAUCHE (Commandes)
        left = ctk.CTkFrame(main, fg_color="transparent")
        left.pack(side="left", fill="both", expand=True, padx=10)

        manuel = ctk.CTkFrame(left, fg_color="#fff1f2", corner_radius=15, border_width=1, border_color="#ffe4e6")
        manuel.pack(fill="x", pady=(0, 20))
        ctk.CTkLabel(manuel, text="📖 FOMBA FAMPIASANA (GUIDE RAPIDE)", font=("Arial", 13, "bold"), text_color=COLOR_ACCENT).pack(pady=5)
        guide = ("1. Hitady Verset tokana: Soraty 'Jaona 3:16'\n2. Toko manontolo: Soraty 'Jaona 1'\n3. Plage: Soraty 'Matio 5:1-12'\n4. Hafatra live: Soraty eo amin'ny boaty 'Hafatra'.")
        ctk.CTkLabel(manuel, text=guide, justify="left", font=("Arial", 12), text_color="#9f1239").pack(padx=15, pady=10)

        ctk.CTkLabel(left, text="SORATY NY VERSET NA TOKO", font=("Arial", 12, "bold")).pack(anchor="w")
        self.entry_search = ctk.CTkEntry(left, height=50, placeholder_text="Ex: 3 Jaona 1:4 na Jaona 3:16...")
        self.entry_search.pack(fill="x", pady=5)
        
        # Raccourci touche Entrée pour la recherche
        self.entry_search.bind("<Return>", lambda e: self.rechercher())
        
        btn_search = ctk.CTkButton(left, text="AMPIDIRINA AO AMIN'NY PROGRAMME", fg_color=COLOR_ORANGE, height=45, command=self.rechercher)
        btn_search.pack(fill="x", pady=(0, 15))

        self.book_list = ctk.CTkComboBox(left, values=self.books, height=35, fg_color="white", dropdown_fg_color="white", command=self.inject_book)
        self.book_list.pack(fill="x", pady=5)

        ctk.CTkLabel(left, text="HAFATRA SOSY / RECLAME / HIRA", font=("Arial", 11, "bold"), text_color="#64748b").pack(anchor="w", pady=(20, 0))
        self.entry_msg = ctk.CTkEntry(left, height=40)
        self.entry_msg.pack(fill="x", pady=5)
        
        # Raccourci touche Entrée pour le message en direct
        self.entry_msg.bind("<Return>", lambda e: self.proj_msg())
        
        btn_msg = ctk.CTkButton(left, text="PROJETER LE MESSAGE DIRECT", fg_color=COLOR_ACCENT, height=45, command=self.proj_msg)
        btn_msg.pack(fill="x")

        # PANNEAU DROIT (Playlist)
        right = ctk.CTkFrame(main, width=420, fg_color="white", border_width=1, border_color="#e2e8f0", corner_radius=20)
        right.pack(side="right", fill="both", padx=10)

        ctk.CTkLabel(right, text="FILAHARAN'NY VERSET", font=("Arial", 15, "bold")).pack(pady=15)
        
        self.playlist_view = ctk.CTkTextbox(right, height=320, fg_color="#f8fafc", font=("Arial", 13))
        self.playlist_view.pack(fill="both", padx=20, pady=5)

        nav_p = ctk.CTkFrame(right, fg_color="transparent")
        nav_p.pack(pady=10)
        ctk.CTkButton(nav_p, text="◀ ALOHA", command=self.prev_item).pack(side="left", padx=5)
        ctk.CTkButton(nav_p, text="MANARAKA ▶", command=self.next_item).pack(side="left", padx=5)
        ctk.CTkButton(nav_p, text="VIDER", fg_color="#ffe4e6", text_color="#b91c1c", command=self.vider).pack(side="left", padx=5)

        self.entry_time = ctk.CTkEntry(right, width=100)
        self.entry_time.insert(0, "10")
        self.entry_time.pack(pady=5)
        
        self.btn_auto = ctk.CTkButton(right, text="LANCER L'AUTO", height=55, fg_color="#10b981", command=self.toggle_auto)
        self.btn_auto.pack(fill="x", padx=20, pady=20)

    def inject_book(self, choice):
        self.entry_search.delete(0, "end")
        self.entry_search.insert(0, f"{choice} ")
        self.entry_search.focus()

    def ouvrir_p(self):
        if not self.projection or not self.projection.winfo_exists():
            self.projection = FenetreProjection()
        self.projection.deiconify()
        self.projection.afficher("Jesosy Kristy", "Baiboly FKF")

    def proj_msg(self):
        if not self.projection or not self.projection.winfo_exists():
            self.projection = FenetreProjection()
        self.projection.deiconify()
        # Envoi d'une référence vide pour enlever tout libellé inutile
        self.projection.afficher(self.entry_msg.get(), "")

    def rechercher(self):
        raw_input = self.entry_search.get().strip()
        if not raw_input: 
            return

        # Remplacement propre des délimiteurs
        saisie = raw_input.replace(':', ' ').replace('-', ' ').replace('_', ' ')
        parts = saisie.split()
        if not parts: 
            return

        try:
            # 1. RECHERCHE ULTRA-SOUPLE DU NOM DU LIVRE
            if parts[0].isdigit() and len(parts) > 1:
                chiffre = parts[0]
                nom_livre = parts[1]
                index_args = 2
                sql_like = f"%{chiffre}%{nom_livre}%"
            else:
                nom_livre = parts[0]
                index_args = 1
                sql_like = f"%{nom_livre}%"

            # 2. EXTRACTION DU CHAPITRE ET DES VERSETS
            chap = int(parts[index_args]) if len(parts) > index_args else 1
            
            if len(parts) > (index_args + 1):
                v_start = int(parts[index_args + 1])
                v_end = int(parts[index_args + 2]) if len(parts) > (index_args + 2) else v_start
            else:
                v_start = 1
                v_end = 300 

            # 3. RECHERCHE DANS LA BASE DE DONNÉES AVEC "LIKE" (Insensible au formatage de la DB)
            db_path = resource_path('moteur_bible.db')
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT livre, verset, texte_mg FROM versets 
                WHERE livre LIKE ? AND chapitre = ? AND verset BETWEEN ? AND ?
                ORDER BY verset ASC
            """, (sql_like, chap, v_start, v_end))
            res = cursor.fetchall()
            conn.close()

            # 4. INTÉGRATION DES RÉSULTATS
            if res:
                for row_livre, v, t in res:
                    # On affiche le nom exact du livre récupéré depuis la base de données
                    self.playlist.append({"txt": t, "ref": f"{row_livre} {chap}:{v}"})
                    self.playlist_view.insert("end", f"• {row_livre} {chap}:{v}\n")
                self.playlist_view.see("end")
                self.index = len(self.playlist) - len(res)
                self.maj_p()
                
            self.entry_search.delete(0, "end")
        except Exception: 
            pass

    def vider(self):
        self.playlist = []
        self.playlist_view.delete("1.0", "end")
        self.index = 0

    def maj_p(self):
        if not self.playlist: 
            return
        if not self.projection or not self.projection.winfo_exists():
            self.projection = FenetreProjection()
        item = self.playlist[self.index]
        self.projection.afficher(item["txt"], item["ref"])

    def next_item(self):
        if self.playlist:
            self.index = (self.index + 1) % len(self.playlist)
            self.maj_p()

    def prev_item(self):
        if self.playlist:
            self.index = (self.index - 1) % len(self.playlist)
            self.maj_p()

    def toggle_auto(self):
        if not self.playlist: 
            return
        self.auto_mode = not self.auto_mode
        if self.auto_mode:
            self.btn_auto.configure(text="STOP AUTO", fg_color=COLOR_ACCENT)
            threading.Thread(target=self.run_loop, daemon=True).start()
        else:
            self.btn_auto.configure(text="LANCER L'AUTO", fg_color="#10b981")

    def run_loop(self):
        while self.auto_mode:
            try:
                val = float(self.entry_time.get())
                t = val * 60 if val < 1 else val
            except Exception: 
                t = 10
            time.sleep(t)
            if self.auto_mode: 
                self.after(0, self.next_item)

if __name__ == "__main__":
    app = LogicielBible()
    app.mainloop()