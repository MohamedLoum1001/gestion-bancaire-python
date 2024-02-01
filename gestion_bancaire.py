# Importe le module json pour la manipulation de données au format JSON
import json
# Importe la classe datetime du module datetime pour gérer les horodatages des transactions
from datetime import datetime

# Classe représentant un utilisateur du système bancaire
class Utilisateur:
    def __init__(self, nom, numero_compte, solde=0, compte_bloque=False):
        """
        Initialise un nouvel utilisateur avec un nom, un numéro de compte, un solde initial et un état de compte bloqué.
        """
        self.nom = nom
        self.numero_compte = numero_compte
        self._solde = solde
        self._historique_transactions = []
        self._compte_bloque = compte_bloque

    def bloquer_compte(self):
        """
        Bloque le compte de l'utilisateur.
        """
        self._compte_bloque = True

    def est_compte_bloque(self):
        """
        Vérifie si le compte de l'utilisateur est bloqué.
        """
        return self._compte_bloque

    def effectuer_depot(self, montant):
        """
        Effectue un dépôt dans le compte de l'utilisateur et enregistre la transaction.
        """
        try:
            if not self.est_compte_bloque():
                if montant > 0:
                    self._solde += montant
                    self._ajouter_a_historique("Dépôt", montant)
                else:
                    raise ValueError("Le montant du dépôt doit être supérieur à zéro.")
            else:
                raise ValueError("Le compte est bloqué. Les dépôts ne sont pas autorisés.")
        except ValueError as e:
            print(f"Erreur : {e}")

    def effectuer_retrait(self, montant):
        """
        Effectue un retrait du compte de l'utilisateur et enregistre la transaction.
        """
        try:
            if not self.est_compte_bloque():
                if 0 < montant <= self._solde:
                    self._solde -= montant
                    self._ajouter_a_historique("Retrait", montant)
                else:
                    raise ValueError("Montant de retrait invalide.")
            else:
                raise ValueError("Le compte est bloqué. Les retraits ne sont pas autorisés.")
        except ValueError as e:
            print(f"Erreur : {e}")

    def effectuer_transfert(self, utilisateur_cible, montant):
        """
        Transfère de l'argent vers un autre utilisateur et enregistre la transaction des deux utilisateurs.
        """
        try:
            if not self.est_compte_bloque():
                if 0 < montant <= self._solde:
                    self._solde -= montant
                    utilisateur_cible._solde += montant
                    self._ajouter_a_historique(f"Transfert vers {utilisateur_cible.nom}", montant)
                    utilisateur_cible._ajouter_a_historique(f"Transfert de {self.nom}", montant)
                else:
                    raise ValueError("Montant de transfert invalide.")
            else:
                raise ValueError("Le compte est bloqué. Les transferts ne sont pas autorisés.")
        except ValueError as e:
            print(f"Erreur : {e}")

    def consulter_solde(self):
        """
        Retourne le solde actuel du compte.
        """
        return self._solde

    def obtenir_historique_transactions(self):
        """
        Retourne l'historique des transactions du compte.
        """
        return self._historique_transactions

    def _ajouter_a_historique(self, type_transaction, montant):
        """
        Ajoute une transaction à l'historique du compte avec le type de transaction et le montant.
        """
        horodatage = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        transaction = {"horodatage": horodatage, "type": type_transaction, "montant": montant}
        self._historique_transactions.append(transaction)

# Classe représentant un administrateur du système bancaire, héritant de la classe Utilisateur
class Admin(Utilisateur):
    def __init__(self, nom, numero_compte):
        """
        Initialise un nouvel administrateur avec un nom et un numéro de compte.
        """
        super().__init__(nom, numero_compte)

    def creer_compte(self):
        """
        Crée un nouveau compte client avec un nom, un numéro de compte et un solde initial.
        """
        try:
            if not self.est_compte_bloque():
                nom_client = input("Entrez le nom du client : ")
                numero_compte_client = input("Entrez le numéro de compte du client : ")
                solde_initial = float(input("Entrez le solde initial : "))
                nouveau_client = Utilisateur(nom_client, numero_compte_client, solde_initial)
                return nouveau_client
            else:
                raise ValueError("Le compte de ce client est bloqué. Les créations de compte ne sont pas autorisées.")
        except ValueError as e:
            print(f"Erreur : {e}")
            return None

    def bloquer_compte(self, utilisateur):
        """
        Bloque le compte d'un utilisateur.
        """
        utilisateur.bloquer_compte()

    def consulter_historique_transactions(self, utilisateur):
        """
        Retourne l'historique des transactions d'un utilisateur.
        """
        return utilisateur.obtenir_historique_transactions()

# Fonction pour sauvegarder les données dans un fichier JSON
def sauvegarder_dans_fichier(donnees, nom_fichier):
    try:
        with open(nom_fichier, 'w') as fichier:
            json.dump(donnees, fichier, default=lambda o: o.__dict__, indent=4)
    except Exception as e:
        print(f"Erreur lors de la sauvegarde dans le fichier : {e}")

# Fonction pour charger les données depuis un fichier JSON
def charger_depuis_fichier(nom_fichier):
    try:
        with open(nom_fichier, 'r') as fichier:
            donnees = json.load(fichier)
        return donnees
    except FileNotFoundError:
        return []
    except Exception as e:
        print(f"Erreur lors du chargement depuis le fichier : {e}")
        return []

# Chargement des données depuis le fichier
donnees_chargees = charger_depuis_fichier("donnees_bancaires.json")
# Création des instances d'utilisateurs à partir des données chargées
clients_charges = [Utilisateur(nom=donnees_client['nom'], numero_compte=donnees_client['numero_compte'], solde=donnees_client['_solde'], compte_bloque=donnees_client['_compte_bloque']) for donnees_client in donnees_chargees]

# Création d'un administrateur
admin = Admin("Admin", "999999")

# Boucle principale qui s'exécute indéfiniment jusqu'à ce que l'utilisateur choisisse de quitter (choix "5").
while True:
    # Affichage du menu principal.
    print("\n1. Créer un Compte")
    print("2. Effectuer une Transaction")
    print("3. Consulter l'Historique des Transactions")
    print("4. Bloquer un Compte")
    print("5. Sauvegarder et Quitter")

    # Demande à l'utilisateur de saisir son choix.
    choix = input("Entrez votre choix (1/2/3/4/5) : ")

    # Actions en fonction du choix de l'utilisateur.
    if choix == "1":
        # Création d'un nouveau compte en appelant la méthode "creer_compte()" de l'objet "admin".
        nouveau_client = admin.creer_compte()
        if nouveau_client:
            # Si la création du compte est réussie, ajout du nouveau client à la liste "clients_charges".
            clients_charges.append(nouveau_client)
            print(f"Nouveau compte créé pour {nouveau_client.nom}")

    elif choix == "2":
        # Demande des informations nécessaires pour effectuer une transaction.
        numero_compte = input("Entrez votre numéro de compte : ")
        montant = input("Entrez le montant de la transaction : ")

        try:
            montant = float(montant)
        except ValueError as e:
            print(f"Erreur : {e}")
            continue

        # Recherche de l'utilisateur correspondant au numéro de compte saisi.
        utilisateur = next((c for c in clients_charges if c.numero_compte == numero_compte), None)

        if utilisateur:
            # Si l'utilisateur est trouvé, vérification de l'état du compte.
            if utilisateur.est_compte_bloque():
                print("Ce compte est bloqué. Les transactions ne sont pas autorisées.")
            else:
                # Si le compte n'est pas bloqué, demande du type de transaction.
                type_transaction = input("Choisissez le type de transaction (depot/retrait/transfert) : ")

                if type_transaction == "depot":
                    # Exécution de la méthode "effectuer_depot()" de l'objet utilisateur.
                    utilisateur.effectuer_depot(montant)
                elif type_transaction == "retrait":
                    # Exécution de la méthode "effectuer_retrait()" de l'objet utilisateur.
                    utilisateur.effectuer_retrait(montant)
                elif type_transaction == "transfert":
                    # Pour le transfert, demande du numéro de compte de la cible et recherche de l'utilisateur correspondant.
                    numero_compte_cible = input("Entrez le numéro de compte de la cible : ")
                    # La fonction next() est utilisée pour récupérer le prochain élément d'un itérable
                    utilisateur_cible = next((c for c in clients_charges if c.numero_compte == numero_compte_cible), None)

                    if utilisateur_cible:
                        # Si la cible est trouvée, exécution de la méthode "effectuer_transfert()" de l'objet utilisateur.
                        utilisateur.effectuer_transfert(utilisateur_cible, montant)
                    else:
                        print("Utilisateur cible introuvable.")
                else:
                    print("Type de transaction invalide.")

                # Affichage du solde et de l'historique des transactions après la transaction.
                print(f"Solde de {utilisateur.nom} : {utilisateur.consulter_solde()}")
                print(f"Historique des transactions de {utilisateur.nom} : {utilisateur.obtenir_historique_transactions()}")

        else:
            print("Utilisateur introuvable.")

    elif choix == "3":
        # Consultation de l'historique des transactions pour un utilisateur spécifique.
        numero_compte = input("Entrez le numéro de compte pour consulter l'historique des transactions : ")
        utilisateur = next((c for c in clients_charges if c.numero_compte == numero_compte), None)

        if utilisateur:
            # Si l'utilisateur est trouvé, affichage de l'historique des transactions.
            historique_transactions = admin.consulter_historique_transactions(utilisateur)
            print(f"{admin.nom} consulte l'historique des transactions de {utilisateur.nom} : {historique_transactions}")
        else:
            print("Utilisateur introuvable.")

    elif choix == "4":
        # Bloquer un compte en appelant la méthode "bloquer_compte()" de l'objet "admin".
        numero_compte_a_bloquer = input("Entrez le numéro de compte à bloquer : ")
        utilisateur_a_bloquer = next((c for c in clients_charges if c.numero_compte == numero_compte_a_bloquer), None)
        if utilisateur_a_bloquer:
            admin.bloquer_compte(utilisateur_a_bloquer)
            print(f"Compte de {utilisateur_a_bloquer.nom} bloqué.")
        else:
            print("Utilisateur introuvable.")

    elif choix == "5":
        # Sauvegarde des données des clients dans un fichier JSON et sortie de la boucle.
        donnees_a_sauvegarder = [client.__dict__ for client in clients_charges]
        sauvegarder_dans_fichier(donnees_a_sauvegarder, "donnees_bancaires.json")
        print("Données sauvegardées. Fin...")
        break

    else:
        # Si le choix de l'utilisateur n'est pas valide, affichage d'un message d'erreur.
        print("Choix invalide. Veuillez entrer une option valide.")
