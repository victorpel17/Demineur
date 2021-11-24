"""
TODO: Ce fichier présente une ébauche d'interface pour le TP4. Vous pouvez le modifier à souhait.
N'oubliez pas de commenter le code!
"""
from tkinter import Tk, Frame, Button, messagebox, Toplevel, Label, Radiobutton, StringVar, Entry, filedialog
from tableau import Tableau
from bouton_case import BoutonCase


class InterfacePartie(Tk):
    """
    Cette classe est la fenêtre principale du jeu et fait le lien entre la fenêtre et le jeu.
    Attributes:
        compteur_tour (int): Nombre de tour qui a été fait
        dimension_rangee (int): Nombre de rangées du tableau
        dimension_colonne (int): Nombre de colonnes du tableau
        nombre_de_mines (int): Nombre de mines dans le tableau
        tableau_mines (Tableau) : Le jeu Démineur.
        label_tour (Label): Le label qui affiche le nombre de tours
        cadre (Frame): Le conteneur de l'interface qui contient les boutons.
        resultat (Label): Le label qui affiche le résultat de la partie.
        dictionnaire_boutons (dict): Dictionnaire de boutons dont les clés sont les coordonnées (x, y)
        """
    def __init__(self):
        """
        Crée une fenêtre pour jouer au Démineur.
        """
        super().__init__()
        self.compteur_tour = 0
        self.dimension_rangee = 8
        self.dimension_colonne = 8
        self.nombre_de_mines = 10

        # Nom de la fenêtre.
        self.title("Démineur")
        self.resizable(0, 0)

        self.tableau_mines = Tableau(self.dimension_rangee, self.dimension_colonne, self.nombre_de_mines)

        bouton_frame = Frame(self)
        bouton_frame.grid(pady=10)

        bouton_nouvelle_partie = Button(bouton_frame, text='Nouvelle partie', command=self.nouvelle_partie)
        bouton_nouvelle_partie["fg"] = "blue"
        bouton_nouvelle_partie.grid(row=0, column=0, padx=5)

        bouton_quitter = Button(bouton_frame, text="Quitter", command=self.quit, foreground = "red")
        bouton_quitter.grid(row=0, column=1, padx=5)

        bouton_param = Button(bouton_frame, text="Paramètres", command=self.fenetre_param)
        bouton_param.grid(row=0, column=2, padx=5)

        bouton_aide = Button(bouton_frame, text="Instructions", command=self.fenetre_aide)
        bouton_aide.grid(row=0, column=3, padx=5)

        bouton_sauvegarder = Button(bouton_frame, text="Sauvegarder la\npartie en cours", command=self.sauvegarder)
        bouton_sauvegarder.grid(row=0, column=4, padx=5)
        
        bouton_charger = Button(bouton_frame, text="Charger une partie\nprécédente", command=self.charger)
        bouton_charger.grid(row=0, column=5, padx=5)

        self.label_tour = Label(self, text=f'===> Tour #{self.compteur_tour} <===')
        self.label_tour.grid(row=1)

        self.cadre = Frame(self)
        self.cadre.grid(padx=10, pady=10, row=2)

        self.resultat = Label(self, text='\n')
        self.resultat.grid(row=3)

        self.dictionnaire_boutons = {}
        self.nouvelle_partie()
    

    def fenetre_param(self):
        """
        Instancie une fenêtre pour la saisie de paramètres.
        Returns: None
        """
        FenetreParam(self)

    def fenetre_aide(self):
        """
        Affiche les règles du jeu.
        Returns: None
        """
        messagebox.showinfo("Instructions",
                            "Les règles de jeu sont les suivantes : \n\n1.  Si le joueur choisit une case où une mine" +
                            " est cachée, la mine explose! La partie est terminée.\n\n2. Si le joueur choisit une case"+
                            " avec un nombre caché, la case est dévoilée et le nombre devient visible.\n\n" +
                            " 3. Si le joueur choisit une case vide (donc qui n’a ni mine ni nombre caché), il y a un" +
                            " effet en cascade qui fait le dévoilement de toutes les cases vides dans le voisinage" +
                            " jusqu’à ce que la limite du tableau soit atteinte ou qu’une case avec un numéro caché" +
                            " soit atteinte.\n\nL’objectif du jeu est d’identifier, par la logique, toutes les cases" +
                            " contenant des mines, sans en déclencher aucune.")

    def devoiler_case(self, event):
        """
        Dévoile une case du tableau lorsqu'on clique dessus. S'il y a un drapeau, on ne fait rien.
        Args:
            event: L'événement engendré par la souris.
        Returns: None
        """
        bouton = event.widget
        case = self.tableau_mines.obtenir_case(bouton.rangee_x, bouton.colonne_y)
        if bouton["text"] != chr(0x1f6a9) and bouton['state'] == 'normal':
            self.compteur_tour += 1
            self.label_tour['text'] = f'===> Tour #{self.compteur_tour} <==='
            if case.est_minee:
                self.afficher_solution()
                self.resultat['text'] = 'BOOM!\nMeilleure chance la prochaine fois...'
            else:
                self.tableau_mines.devoiler_case(bouton.rangee_x, bouton.colonne_y)

                if self.tableau_mines.nombre_cases_sans_mine_a_devoiler == 0:
                    self.resultat['text'] = 'Bien joué!'
                    self.afficher_solution()
                else:
                    self.afficher_tableau()

    def afficher_tableau(self):
        """
        Met à jour l'affichage du tableau.
        Returns: None
        """
        for coord, case in self.tableau_mines.dictionnaire_cases.items():
            if case.est_devoilee and self.dictionnaire_boutons[coord]['state'] == 'normal':
                self.dictionnaire_boutons[coord]['state'] = 'disable'
                if case.est_minee:
                    self.dictionnaire_boutons[coord]['text'] = chr(0x0001F4A3)
                    self.dictionnaire_boutons[coord].config(disabledforeground = "black")
                else:
                    self.dictionnaire_boutons[coord]['text'] = str(case.nombre_mines_voisines)
                    if self.dictionnaire_boutons[coord]["text"] == "1":
                        self.dictionnaire_boutons[coord].config(disabledforeground = "green")
                    if self.dictionnaire_boutons[coord]["text"] == "2":
                        self.dictionnaire_boutons[coord].config(disabledforeground = "blue")
                    if self.dictionnaire_boutons[coord]["text"] == "3":
                        self.dictionnaire_boutons[coord].config(disabledforeground = "orange")
                    if self.dictionnaire_boutons[coord]["text"] == "4":
                        self.dictionnaire_boutons[coord].config(disabledforeground = "red")
                    if self.dictionnaire_boutons[coord]["text"] == "5":
                        self.dictionnaire_boutons[coord].config(disabledforeground = "red")
                    if self.dictionnaire_boutons[coord]["text"] == "6":
                        self.dictionnaire_boutons[coord].config(disabledforeground = "red")
                        

    def afficher_solution(self):
        """
        Affiche la solution complète du tableau quand la partie est terminée.
        Returns: None
        """
        for coord, case in self.tableau_mines.dictionnaire_cases.items():
            if self.dictionnaire_boutons[coord]['state'] == 'normal':
                self.dictionnaire_boutons[coord]['state'] = 'disable'
                if case.est_minee:
                    self.dictionnaire_boutons[coord]['text'] = chr(0x0001F4A3)
                    self.dictionnaire_boutons[coord].config(disabledforeground = "black")
                else:
                    self.dictionnaire_boutons[coord]['text'] = str(case.nombre_mines_voisines)
                    if self.dictionnaire_boutons[coord]["text"] == "1":
                        self.dictionnaire_boutons[coord].config(disabledforeground = "green")
                    if self.dictionnaire_boutons[coord]["text"] == "2":
                        self.dictionnaire_boutons[coord].config(disabledforeground = "blue")
                    if self.dictionnaire_boutons[coord]["text"] == "3":
                        self.dictionnaire_boutons[coord].config(disabledforeground = "orange")
                    if self.dictionnaire_boutons[coord]["text"] == "4":
                        self.dictionnaire_boutons[coord].config(disabledforeground = "red")
                    if self.dictionnaire_boutons[coord]["text"] == "5":
                        self.dictionnaire_boutons[coord].config(disabledforeground = "red")
                    if self.dictionnaire_boutons[coord]["text"] == "6":
                        self.dictionnaire_boutons[coord].config(disabledforeground = "red")
                    
                    

    def quit(self):
        """
        Avant de quitter la fenêtre, on demande à l'utilisateur s'il veut vraiment quitter l'application.
        Returns: None
        """
        reponse = messagebox.askquestion('Quitter', "Êtes-vous sûr de vouloir quitter l'application?", icon='warning')
        if reponse == 'yes':
            super(InterfacePartie, self).quit()

    def drapeau(self, event):
        """
        Lorsqu'il y a un clique droit sur une case, on place un drapeau ou on enlève un drapeau.
        Args:
            event: L'événement engendré par la souris.
        Returns: None
        """
        bouton = event.widget
        if bouton["text"] == chr(0x1f6a9):
            bouton["text"] = " "
        elif bouton["text"] == " ":
            bouton["text"] = chr(0x1f6a9)

    def nouvelle_partie(self):
        """
        Crée un nouveau tableau et met à jour les variables pour recommencer une nouvelle partie.
        Returns: None
        """
        self.tableau_mines = Tableau(self.dimension_rangee, self.dimension_colonne, self.nombre_de_mines)
        self.resultat['text'] = '\n'
        self.compteur_tour = 0

        if len(self.dictionnaire_boutons) == self.dimension_rangee * self.dimension_colonne:
            for bouton in self.dictionnaire_boutons.values():
                bouton['text'] = " "
                bouton['state'] = "normal"

        else:
            self.dictionnaire_boutons.clear()
            self.clear_cadre()

            for i in range(self.tableau_mines.dimension_rangee):
                for j in range(self.tableau_mines.dimension_colonne):
                    bouton = BoutonCase(self.cadre, i + 1, j + 1)
                    bouton.grid(row=i, column=j)
                    bouton.bind('<Button-1>', self.devoiler_case)
                    bouton.bind('<Button-3>', self.drapeau)
                    self.dictionnaire_boutons[(i + 1, j + 1)] = bouton


    def clear_cadre(self):
        """
        Enlève tous les boutons de la fenêtre.
        Returns: None
        """
        for bouton in self.cadre.winfo_children():
            bouton.destroy()
            
    def sauvegarder(self):
        """
        Crée une sauvegarde de la partie en cours sous la forme d'un fichier texte dont le nom est au choix de l'utilisateur.
        Returns: None
        """
        fichier_de_sauvegarde = filedialog.asksaveasfile(parent = self, title = "Ouvrir le fichier", 
                                                         defaultextension = ".txt", filetypes = [("TXT", "*.txt")])
        chaine_de_sauvegarde = str(self.dimension_rangee)+"\n"+str(self.dimension_colonne)+"\n"+str(self.compteur_tour)+"\n"
        chaine_de_sauvegarde += str(self.nombre_de_mines) + "\n"
        for coord, case in self.tableau_mines.dictionnaire_cases.items():
            if case.est_devoilee:
                chaine_de_sauvegarde += str(case.nombre_mines_voisines) + "\n"
            if not case.est_devoilee and case.est_minee:
                chaine_de_sauvegarde += "M" + "?" + "\n"
            if not case.est_devoilee and not case.est_minee:
                chaine_de_sauvegarde += str(case.nombre_mines_voisines) + "?" + "\n"
        n = len(chaine_de_sauvegarde) - 1
        chaine_de_sauvegarde = chaine_de_sauvegarde[:n]
        fichier_de_sauvegarde.write(chaine_de_sauvegarde)
        fichier_de_sauvegarde.close()
        
        
    def charger(self):
        """
        Charge le fichier de sauvegarde sous forme de fichier teexte d'une partie antérieure préalablement enregistrée. 
        Returns: None
        """
        chargement = filedialog.askopenfilename(parent = self, title = "Ouvrir le fichier", defaultextension = ".txt",
                                   filetypes = [("TXT", "*.txt")])
        self.dictionnaire_boutons.clear()
        self.clear_cadre()
        fichier_de_chargement = open(chargement, "r")
        self.dimension_rangee = int(fichier_de_chargement.readline().rstrip("\n"))
        self.dimension_colonne = int(fichier_de_chargement.readline().rstrip("\n"))
        self.compteur_tour = int(fichier_de_chargement.readline().rstrip("\n"))
        self.nombre_de_mines = int(fichier_de_chargement.readline().rstrip("\n"))
        self.tableau_mines = Tableau(self.dimension_rangee,self.dimension_colonne, 0)
        self.resultat['text'] = '\n'
        for coord, case in self.tableau_mines.dictionnaire_cases.items():
            self.tableau_mines.dictionnaire_cases[coord].nombre_mines_voisines = fichier_de_chargement.readline().rstrip("\n")
            if "M" in self.tableau_mines.dictionnaire_cases[coord].nombre_mines_voisines:
                self.tableau_mines.dictionnaire_cases[coord].est_minee = True
                self.tableau_mines.dictionnaire_cases[coord].nombre_mines_voisines = 0
            else:
                if "?" in self.tableau_mines.dictionnaire_cases[coord].nombre_mines_voisines:
                    self.tableau_mines.dictionnaire_cases[coord].nombre_mines_voisines = int(self.tableau_mines
                                                                                             .dictionnaire_cases[coord]
                                                                                             .nombre_mines_voisines[:1])
                else:
                    self.tableau_mines.dictionnaire_cases[coord].est_devoilee = True
                    self.tableau_mines.dictionnaire_cases[coord].nombre_mines_voisines = int(self.tableau_mines
                                                                                             .dictionnaire_cases[coord]
                                                                                             .nombre_mines_voisines)
        fichier_de_chargement.close()

        for i in range(self.tableau_mines.dimension_rangee):
            for j in range(self.tableau_mines.dimension_colonne):
                bouton = BoutonCase(self.cadre, i + 1, j + 1)
                bouton.grid(row=i, column=j)
                bouton.bind('<Button-1>', self.devoiler_case)
                bouton.bind('<Button-3>', self.drapeau)
                self.dictionnaire_boutons[(i + 1, j + 1)] = bouton
        
        self.afficher_tableau()
        
                
                
        

        
        


class FenetreParam(Toplevel):
    """
    Fenêtre qui laisse l'utilisateur choisir les paramètres de jeu. La fenêtre va par-dessus une fenêtre de
    InterfacePartie.
    Attributes:
        racine (Tk): La fenêtre en dessous de la fenêtre de paramètres.
        mode (StringVar): Indique la difficulté qui a été choisie.
        rangee (StringVar): Valeur à l'intérieur de son Entry respectif.
        colonne (StringVar): Valeur à l'intérieur de son Entry respectif.
        mine (StringVar): Valeur à l'intérieur de son Entry respectif.
        entree_rangee (Entry): Zone de texte pour spécifier le nombre de rangées.
        entree_colonne (Entry): Zone de texte pour spécifier le nombre de colonnes.
        entree_mine (Entry): Zone de texte pour spécifier le nombre de mines.
        debutant (Radiobutton): Bouton qui pose les dimensions à 8 x 8 cases avec 10 mines.
        intermediaire (Radiobutton): Bouton qui pose les dimensions à 16 x 16 cases avec 40 mines.
        avancee (Radiobutton): Bouton qui pose les dimensions à 24 x 24 cases avec 99 mines.
        autre (Radiobutton): Bouton qui laisse l'utilisateur choisir les paramètres.
        """
    def __init__(self, racine):
        """
        Crée une fenêtre de paramètres. Rend la fenêtre de jeu inactive tant que la fenêtre de paramètre existe.
        Args:
            racine: La fenêtre de jeu.
        """
        super(FenetreParam, self).__init__(racine)
        self.racine = racine
        self.mode = StringVar()
        self.resizable(0, 0)
        self.title("Paramètres")
        self.grab_set()

        self.rangee = StringVar(value="8")
        self.colonne = StringVar(value="8")
        self.mine = StringVar(value="10")

        Label(self, text="Nombre de rangées : ").grid(pady=5, row=1, column=0)
        Label(self, text="Nombre de colonnes : ").grid(pady=5, row=2, column=0)
        Label(self, text="Nombre de mines : ").grid(pady=5, row=3, column=0)

        predicat = (self.register(self.filtre_touche))

        self.entree_rangee = Entry(self, textvariable=self.rangee, state="disable", validate="all",
                                   validatecommand=(predicat, '%P'))
        self.entree_colonne = Entry(self, textvariable=self.colonne, state="disable", validate="all",
                                    validatecommand=(predicat, '%P'))
        self.entree_mine = Entry(self, textvariable=self.mine, state="disable", validate="all",
                                 validatecommand=(predicat, '%P'))

        self.entree_rangee.grid(row=1, column=1)
        self.entree_colonne.grid(row=2, column=1)
        self.entree_mine.grid(row=3, column=1)

        Label(self, text="Difficulté : ").grid(row=0, column=0)

        self.debutant = Radiobutton(self, text="Débutant", value="8-8-10", variable=self.mode,
                                    command=self.set_mode_predefini)
        self.intermediaire = Radiobutton(self, text="Intermédiaire", value="16-16-40", variable=self.mode,
                                         command=self.set_mode_predefini)
        self.avancee = Radiobutton(self, text="Avancée", value="24-24-99", variable=self.mode,
                                   command=self.set_mode_predefini)
        self.autre = Radiobutton(self, text="Autre", value="0-0-0", variable=self.mode,
                                 command=self.set_mode_personalise)

        self.debutant.grid(row=0, column=1)
        self.intermediaire.grid(row=0, column=2)
        self.avancee.grid(row=0, column=3)
        self.autre.grid(row=0, column=4)

        self.debutant.select()

        Button(self, text="Confirmer", command=self.confirmer).grid(pady=10, row=4, column=0)
        Button(self, text="Annuler", command=self.destroy).grid(pady=10, row=4, column=1)

    def set_mode_predefini(self):
        """
        Pose les paramètres à un mode de jeu prédéfini et désactive les Entry.
        Returns: None
        """
        self.entree_rangee["state"] = "disable"
        self.entree_colonne["state"] = "disable"
        self.entree_mine["state"] = "disable"

        param = self.mode.get().split("-")
        self.rangee.set(param[0])
        self.colonne.set(param[1])
        self.mine.set(param[2])

    def set_mode_personalise(self):
        """
        Rend les Entry accessible à l'utilisateur.
        Returns: None
        """
        self.entree_rangee["state"] = "normal"
        self.entree_colonne["state"] = "normal"
        self.entree_mine["state"] = "normal"

    def filtre_touche(self, chaine):
        """
        Retourne vrai si et seulement si la chaîne de caractère est une chaîne vide ou c'est une chaîne de 3 chiffres.
        Returns:
            bool : True si et seulement si la chaîne de caractère est une chaîne vide ou c'est une chaîne de 3 chiffres.
        """
        return chaine.isdigit() and len(chaine) <= 2 or chaine == ""

    def confirmer(self):
        """
        Vérifie que les paramètres entrés sont valides. S'ils sont valides, alors on passe les paramètres à la fenêtre
        de jeu et on détruit la fenêtre de paramètres. Sinon, on affiche un message d'erreur.
        Returns: None
        """
        try:
            rangee = int(self.rangee.get())
            colonne = int(self.colonne.get())
            mine = int(self.mine.get())

            if rangee < 5 or rangee > 30 or colonne < 5 or colonne > 30 or mine < 5:
                raise ValueError

            self.racine.dimension_rangee = rangee
            self.racine.dimension_colonne = colonne
            self.racine.nombre_de_mines = mine
            self.racine.nouvelle_partie()
            self.destroy()
        except ValueError:
            messagebox.showerror("Erreur",
                                 "Les paramètres doivent tous être plus grands ou égals à 5 et les dimensions" +
                                 "doivent être inférieures ou égales à 30.")

        
        
        
        
        
        
        
        