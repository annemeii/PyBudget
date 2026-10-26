import math
import json
import sys

type_revenu = "Revenu"
type_depense = "Dépense"


def calculer_solde(historique):
    solde = 0
    for transaction in historique:
      if transaction[0] == type_revenu:
        solde = solde + transaction[2]
      elif transaction[0] == type_depense:
        solde = solde - transaction[2]
    return solde 


def supprimer_transaction(historique):
  if not historique:
    print("Aucune transaction enregistrée.")
    return calculer_solde(historique)
  while True:
    try:
      choix = int(input("Quel transaction souhaitez vous supprimer? "))
      print(" ")
    except ValueError:
      print("Veuillez entrer un numéro valide.")
      continue
    if 1 <= choix <= len(historique):
      index = choix - 1
      break
    else:
     print("Cette transaction n'existe pas.")
  historique.pop(index)
  solde = calculer_solde(historique)
  sauvegarder_budget(historique, "pybudget.json")
  print("Transaction supprimée avec succès !")
  print(f"Nouveau solde : {solde:.2f} € ")
  return solde
 

def sauvegarder_budget(historique, nom_fichier):
  with open(nom_fichier, "w", encoding="utf-8") as fichier:
    json.dump(historique, fichier)
try:
    with open("pybudget.json", "r", encoding="utf-8") as fichier:
        historique = json.load(fichier)
except FileNotFoundError:
    historique = []
except json.JSONDecodeError:
    print("Erreur : le fichier JSON est vide ou invalide.")
    sys.exit()
if not isinstance(historique, list):
    print("Erreur : l'historique doit être une liste.")
    sys.exit()

for numero, transaction in enumerate(historique, start=1):
  if not isinstance(transaction,list):
    print(f"Erreur transaction n°{numero} : une transaction doit être une liste.")
    sys.exit()
  if len(transaction) != 3:
    print(f"Erreur transaction n°{numero} : une transaction doit contenir exactement 3 éléments.")
    sys.exit()
  if not isinstance(transaction[2], (float, int)) or isinstance(transaction[2], bool):
    print(f"Erreur transaction n°{numero} : le montant doit être un nombre.")
    sys.exit()
  if transaction[0] != type_revenu and transaction[0] != type_depense:
    print(f"Erreur transaction n°{numero} : le type doit être 'Revenu' ou 'Dépense'.")
    sys.exit()
  if not isinstance(transaction[1], str):
    print(f"Erreur transaction n°{numero} : la description doit être du texte.")
    sys.exit()
  if transaction[2] <= 0 or not math.isfinite(transaction[2]):
    print(f"Erreur transaction n°{numero} : le montant doit être strictement supérieur à 0.")
    sys.exit()

solde = calculer_solde(historique)
   

while True :
    print(" ")
    print("========= PYBUDGET =========")
    print(" ")
    print("1. Ajouter un revenu")
    print("2. Ajouter une dépense")
    print("3. Consulter mon solde")
    print("4. Voir mes transactions")
    print("5. Supprimer une transaction")
    print("6. Quitter")
    print(" ")
    while True:
      try:
        choix = int(input("Votre choix : "))
        print(" ")
        break
      except ValueError:
         print("Le choix saisi est invalide.")

    if choix == 1:
        description = input("Description : ")
        print(" ")
        while True :
           try:
              revenu = float(input("Montant : "))
              if revenu <= 0 or not math.isfinite(revenu):
                             print("Les revenus doivent être des nombres positifs et finis.")
              else:
                  break
           except ValueError:
              print("Veuillez entrer un montant numérique.") 
        historique.append([type_revenu, description, revenu])
        solde = calculer_solde(historique)
        sauvegarder_budget(historique , "pybudget.json")
        print(" ")
        print("✓ Revenu ajouté avec succès !")

    elif choix == 2:
        description = input("Description : ")
        print(" ")
        while True :
           try:
                depense = float(input("Montant : "))
                if depense <= 0 or not math.isfinite(depense):
                            print("Les dépenses doivent être des nombres positifs et finis.")
                elif solde < depense:
                            print("Vous n'avez pas assez d'argent pour cette dépense."  )          
                else:
                  break
           except ValueError:
                          print("Veuillez entrer un montant numérique.")
        historique.append([type_depense, description, depense])
        solde = calculer_solde(historique)
        sauvegarder_budget(historique , "pybudget.json")
        print(" ")
        print("✓ Dépense enregistrée !")

    elif choix == 3:
        print(f"Solde actuel : {solde:.2f} € ")
    elif choix == 4:
        print("========= HISTORIQUE =========")
        print(" ")
        if historique == []:
            print("Aucune transaction enregistrée.")
        else:
            for transaction in historique:
              if transaction[0] == type_revenu:
                print(f"+ {transaction[2]:.2f} € | {transaction[1]}")
              elif transaction[0] == type_depense:
                print(f"- {transaction[2]:.2f} € | {transaction[1]}")
        print(" ")
        print("=============================")  
    elif choix == 5:
        solde = supprimer_transaction(historique)      
    elif choix == 6:
        break
    else :
        print("Choix invalide.")