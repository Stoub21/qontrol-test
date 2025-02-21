#!/bin/bash
set -e  # Arrête le script en cas d'erreur

# Cloner le dépôt
git clone https://gitlab.inria.fr/auctus-team/components/control/qontrol.git
cd qontrol

# Créer et entrer dans le répertoire de build
mkdir -p build
cd build

# Générer les fichiers de build avec CMake
cmake ..

# Compiler avec Make
make -j4

echo "Build terminé avec succès !"
