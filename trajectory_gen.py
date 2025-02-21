import csv
import argparse

default_robot = "panda"

# Configurer l'analyseur d'arguments
parser = argparse.ArgumentParser(description="Générer une trajectoire pour un robot spécifique.")
parser.add_argument(
    "robot",
    nargs='?',  # L'argument est facultatif
    default=default_robot,
    choices=["panda", "ur5"],
    help="Le robot pour lequel générer la trajectoire. Choix : panda, ur5."
)

# Analyser les arguments
args = parser.parse_args()

# Définir les deux premières lignes
header = ["x", "y", "z", "qx", "qy", "qz", "qw", "vx", "vy", "vz", "vroll", "vpitch", "vyaw", "ax", "ay", "az", "aroll", "apitch", "ayaw"]
state_init_panda = [
    0.554499, 0, 0.624502, 0.923898, -0.382638, 8.49627e-17, 2.05147e-16,
    -0, -0, -0, 0, 0, 0, -0.057735, -0.057735, -0.057735, 0.299, 0.190484, 0.299
]

state_init_ur5 = [
    0.491999, 0.134, 0.488, -0.707107, 0.707107, -2.59735e-06, 5.19367e-12,
    -0, -0, -0, 0, 0, 0, -0.057735, -0.057735, -0.057735, 0.299, 0.190484, 0.299
]

if args.robot == "panda":
    state = state_init_panda
elif args.robot == "ur5":
    state = state_init_ur5

def add_path(writer,state,unit_v,N):
    for i in range(N):
        new_state = [a + b for a, b in zip(state, unit_v)]
        writer.writerow(new_state)
        state = new_state  # Mettre à jour la ligne initiale pour l'itération suivante
    
    return(state)

# Nombre de lignes supplémentaires à générer
num_additional_lines = 500

# Écrire dans un fichier CSV
with open('trajectory.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(header) 
    writer.writerow(state)

    forward = [0.0002, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    state = add_path(writer,state,forward,500)

    move_down = [0.0, 0, -0.0002, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    state = add_path(writer,state,move_down,1000)
    

print("Fichier CSV généré avec succès.")
