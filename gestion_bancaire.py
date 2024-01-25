# Importe le module json pour la manipulation de données au format JSON
import json
# Importe la classe datetime du module datetime pour gérer les horodatages des transactions
from datetime import datetime

# Classe représentant un utilisateur du système bancaire
class Utilisateur:
    def __init__(self, nom, numero_compte, solde=0):
        """
        Initialise un nouvel utilisateur avec un nom, un numéro de compte et un solde initial.
        """
        self.nom = nom
        self.numero_compte = numero_compte
        self._solde = solde
        self._historique_transactions = []

    def effectuer_depot(self, montant):
        """
        Effectue un dépôt dans le compte de l'utilisateur et enregistre la transaction.
        """
        try:
            # Vérifie si le montant du dépôt est supérieur à zéro
            if montant > 0:
                # Augmente le solde du compte de l'utilisateur du montant du dépôt
                self._solde += montant
                
                # Enregistre la transaction dans l'historique
                self._ajouter_a_historique("Dépôt", montant)
            else:
                raise ValueError("Le montant du dépôt doit être supérieur à zéro.")
        except ValueError as e:
            print(f"Erreur : {e}")

    def effectuer_retrait(self, montant):
        """
        Effectue un retrait du compte de l'utilisateur et enregistre la transaction.
        """
        try:
            # Vérifie si le montant du retrait est strictement positif et ne dépasse pas le solde
            if 0 < montant <= self._solde:
                # Diminue le solde du compte de l'utilisateur du montant du retrait
                self._solde -= montant
                
                # Enregistre la transaction dans l'historique
                self._ajouter_a_historique("Retrait", montant)
            else:
                raise ValueError("Montant de retrait invalide.")
        except ValueError as e:
            print(f"Erreur : {e}")

    def effectuer_transfert(self, utilisateur_cible, montant):
        """
        Transfère de l'argent vers un autre utilisateur et enregistre la transaction des deux utilisateurs.
        """
        try:
            # Vérifie si le montant du transfert est positif et ne dépasse pas le solde
            if 0 < montant <= self._solde:
                # Diminue le solde du compte de l'utilisateur émetteur
                self._solde -= montant
                
                # Augmente le solde du compte de l'utilisateur cible
                utilisateur_cible._solde += montant
                
                # Enregistre la transaction dans l'historique des deux utilisateurs
                self._ajouter_a_historique(f"Transfert vers {utilisateur_cible.nom}", montant)
                utilisateur_cible._ajouter_a_historique(f"Transfert de {self.nom}", montant)
            else:
                raise ValueError("Montant de transfert invalide.")
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
        # Obtient l'horodatage actuel au format "année-mois-jour heure:minute:seconde"
        horodatage = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Crée un dictionnaire représentant les détails de la transaction
        transaction = {"horodatage": horodatage, "type": type_transaction, "montant": montant}
        
        # Ajoute la transaction à l'historique du compte
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
            nom_client = input("Entrez le nom du client : ")
            numero_compte_client = input("Entrez le numéro de compte du client : ")
            solde_initial = float(input("Entrez le solde initial : "))
            nouveau_client = Utilisateur(nom_client, numero_compte_client, solde_initial)
            return nouveau_client
        except ValueError as e:
            print(f"Erreur : {e}")
            return None

    def bloquer_compte(self, utilisateur):
        """
        Bloque le compte d'un utilisateur (peut être étendu avec une logique supplémentaire).
        """
        # Implémenter une logique supplémentaire pour bloquer les comptes (non implémenté dans cet exemple)
        pass

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
clients_charges = [Utilisateur(nom=donnees_client['nom'], numero_compte=donnees_client['numero_compte'], solde=donnees_client['_solde']) for donnees_client in donnees_chargees]

# Création d'un administrateur
admin = Admin("Admin", "999999")

while True:
    print("\n1. Créer un Compte")
    print("2. Effectuer une Transaction")
    print("3. Consulter l'Historique des Transactions")
    print("4. Sauvegarder et Quitter")

    choix = input("Entrez votre choix (1/2/3/4) : ")

    if choix == "1":
        nouveau_client = admin.creer_compte()
        if nouveau_client:
            clients_charges.append(nouveau_client)
            print(f"Nouveau compte créé pour {nouveau_client.nom}")

    elif choix == "2":
        numero_compte = input("Entrez votre numéro de compte : ")
        montant = input("Entrez le montant de la transaction : ")

        try:
            montant = float(montant)
        except ValueError as e:
            print(f"Erreur : {e}")
            continue

        utilisateur = next((c for c in clients_charges if c.numero_compte == numero_compte), None)

        if utilisateur:
            type_transaction = input("Choisissez le type de transaction (depot/retrait/transfert) : ")

            if type_transaction == "depot":
                utilisateur.effectuer_depot(montant)
            elif type_transaction == "retrait":
                utilisateur.effectuer_retrait(montant)
            elif type_transaction == "transfert":
                numero_compte_cible = input("Entrez le numéro de compte de la cible : ")
                utilisateur_cible = next((c for c in clients_charges if c.numero_compte == numero_compte_cible), None)

                if utilisateur_cible:
                    utilisateur.effectuer_transfert(utilisateur_cible, montant)
                else:
                    print("Utilisateur cible introuvable.")
            else:
                print("Type de transaction invalide.")

            print(f"Solde de {utilisateur.nom} : {utilisateur.consulter_solde()}")
            print(f"Historique des transactions de {utilisateur.nom} : {utilisateur.obtenir_historique_transactions()}")

        else:
            print("Utilisateur introuvable.")

    elif choix == "3":
        numero_compte = input("Entrez le numéro de compte pour consulter l'historique des transactions : ")
        utilisateur = next((c for c in clients_charges if c.numero_compte == numero_compte), None)

        if utilisateur:
            historique_transactions = admin.consulter_historique_transactions(utilisateur)
            print(f"{admin.nom} consulte l'historique des transactions de {utilisateur.nom} : {historique_transactions}")
        else:
            print("Utilisateur introuvable.")

    elif choix == "4":
        donnees_a_sauvegarder = [client.__dict__ for client in clients_charges]
        sauvegarder_dans_fichier(donnees_a_sauvegarder, "donnees_bancaires.json")
        print("Données sauvegardées. Fin...")
        break

    else:
        print("Choix invalide. Veuillez entrer une option valide.")
