import csv

# Définir les deux premières lignes
header = ["x", "y", "z", "qx", "qy", "qz", "qw", "vx", "vy", "vz", "vroll", "vpitch", "vyaw", "ax", "ay", "az", "aroll", "apitch", "ayaw"]
state = [
    0.554499, 0, 0.624502, 0.923898, -0.382638, 8.49627e-17, 2.05147e-16,
    -0, -0, -0, 0, 0, 0, -0.057735, -0.057735, -0.057735, 0.299, 0.190484, 0.299
]

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
