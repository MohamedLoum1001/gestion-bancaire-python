# Importe le module json pour la manipulation de données au format JSON
import json
# Importe la classe datetime du module datetime pour gérer les horodatages des transactions
from datetime import datetime
# Importation de la fonction count du module itertools
from itertools import count

# Classe de base pour les utilisateurs avec gestion des ID
class Utilisateur:
    _id_user_counter = count(1)  # Variable de classe pour attribuer des IDs uniques
    _id_transaction_counter = count(1)  # Compteur global pour générer des IDs uniques pour les transactions

    # Initialisation de l'utilisateur avec un ID unique, nom, numéro de compte, solde et état du compte
    def __init__(self, nom, numero_compte, solde=0, compte_bloque=False):
        self._id = next(Utilisateur._id_user_counter)  # Attribution d'un ID unique à chaque utilisateur
        self.nom = nom
        self.numero_compte = numero_compte
        self._solde = solde
        self._historique_transactions = []
        self._compte_bloque = compte_bloque

    # Méthode pour bloquer le compte
    def bloquer_compte(self):
        self._compte_bloque = True

    # Méthode pour vérifier si le compte est bloqué
    def est_compte_bloque(self):
        return self._compte_bloque

    # Méthode pour consulter le solde du compte
    def consulter_solde(self):
        return self._solde

    # Méthode pour obtenir l'historique des transactions
    def obtenir_historique_transactions(self):
        return self._historique_transactions

    # Méthode interne pour ajouter une transaction à l'historique
    def _ajouter_a_historique(self, type_transaction, montant):
        horodatage = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        transaction = {"id_transaction": next(Utilisateur._id_transaction_counter), "horodatage": horodatage, "type": type_transaction, "montant": montant}
        self._historique_transactions.append(transaction)

# Classe dérivée pour les clients
class Client(Utilisateur):
    # Méthode pour effectuer un dépôt
    def effectuer_depot(self, montant):
        if not self.est_compte_bloque() and montant > 0:
            self._solde += montant
            self._ajouter_a_historique("Dépôt", montant)
        else:
            print("Opération de dépôt non autorisée.")

    # Méthode pour effectuer un retrait
    def effectuer_retrait(self, montant):
        if not self.est_compte_bloque() and 0 < montant <= self._solde:
            self._solde -= montant
            self._ajouter_a_historique("Retrait", montant)
        else:
            print("Opération de retrait non autorisée.")

    # Méthode pour effectuer un transfert
    def effectuer_transfert(self, utilisateur_cible, montant):
        if not self.est_compte_bloque() and 0 < montant <= self._solde:
            if not utilisateur_cible.est_compte_bloque():
                self._solde -= montant
                utilisateur_cible._solde += montant
                self._ajouter_a_historique(f"Transfert vers {utilisateur_cible.nom}", montant)
                utilisateur_cible._ajouter_a_historique(f"Transfert de {self.nom}", montant)
                print(f"Transfert de {montant} vers {utilisateur_cible.nom} (ID transaction: {self._historique_transactions[-1]['id_transaction']}) effectué avec succès.")
            else:
                print("Le destinataire du transfert est bloqué. Le transfert est impossible.")
        else:
            print("Solde insuffisant ou compte bloqué.")

# Classe dérivée pour les administrateurs
class Admin(Utilisateur):
    # Méthode pour créer un compte client
    def creer_compte(self):
        nom_client = input("Entrez le nom du client : ")
        numero_compte_client = input("Entrez le numéro de compte du client : ")

        while True:
            try:
                solde_initial = float(input("Entrez le solde initial : "))
                break
            except ValueError:
                print("Erreur : Veuillez entrer un montant valide (nombre entier ou à virgule flottante).")

        nouveau_client = Client(nom_client, numero_compte_client, solde_initial)
        return nouveau_client

    # Méthode pour bloquer le compte d'un utilisateur
    def bloquer_compte(self, utilisateur):
        utilisateur.bloquer_compte()

    # Méthode pour consulter l'historique des transactions d'un utilisateur
    def consulter_historique_transactions(self, utilisateur):
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
clients_charges = [Client(nom=donnees_client['nom'], numero_compte=donnees_client['numero_compte'], solde=donnees_client['_solde'], compte_bloque=donnees_client['_compte_bloque']) for donnees_client in donnees_chargees]

admin = Admin("Admin", "999999")

# Boucle principale qui s'exécute indéfiniment jusqu'à ce que l'utilisateur choisisse de quitter (choix "5").
while True:
    print("\n1. Créer un Compte")
    print("2. Effectuer une Transaction")
    print("3. Consulter l'Historique des Transactions")
    print("4. Bloquer un Compte")
    print("5. Sauvegarder et Quitter")

    choix = input("Entrez votre choix (1/2/3/4/5) : ")

    if choix == "1":
        nouveau_client = admin.creer_compte()
        if nouveau_client:
            clients_charges.append(nouveau_client)
            print(f"Nouveau compte créé pour {nouveau_client.nom} avec l'ID {nouveau_client._id}")

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
            if utilisateur.est_compte_bloque():
                print("Ce compte est bloqué. Les transactions ne sont pas autorisées.")
            else:
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
                        print("Le client ciblé est introuvable.")
                else:
                    print("Type de transaction invalide.")

                print(f"Solde de {utilisateur.nom} : {utilisateur.consulter_solde()}")
                print(f"Historique des transactions de {utilisateur.nom} : {utilisateur.obtenir_historique_transactions()}")

        else:
            print("Ce compte n'existe pas dans la base de données.")

    elif choix == "3":
        numero_compte = input("Entrez le numéro de compte pour consulter l'historique des transactions : ")
        utilisateur = next((c for c in clients_charges if c.numero_compte == numero_compte), None)

        if utilisateur:
            historique_transactions = admin.consulter_historique_transactions(utilisateur)
            print(f"{admin.nom} consulte l'historique des transactions de {utilisateur.nom} : {historique_transactions}")
        else:
            print("Utilisateur introuvable.")

    elif choix == "4":
        numero_compte_a_bloquer = input("Entrez le numéro de compte à bloquer : ")
        utilisateur_a_bloquer = next((c for c in clients_charges if c.numero_compte == numero_compte_a_bloquer), None)
        if utilisateur_a_bloquer:
            admin.bloquer_compte(utilisateur_a_bloquer)
            print(f"Compte de {utilisateur_a_bloquer.nom} bloqué.")
        else:
            print("Utilisateur introuvable.")

    elif choix == "5":
        donnees_a_sauvegarder = [client.__dict__ for client in clients_charges]
        sauvegarder_dans_fichier(donnees_a_sauvegarder, "donnees_bancaires.json")
        print("Données sauvegardées. Fin...")
        break

    else:
        print("Choix invalide. Veuillez entrer une option valide.")