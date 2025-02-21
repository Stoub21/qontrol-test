#!/bin/bash
set -e  # Stop the script in error case

default_robot="panda"

robot=${1:-$default_robot}

case $robot in
    panda|ur5)
        ;;
    *)
        echo "Invalid robot: $robot"
        exit 1
        ;;
esac

python3 trajectory_gen.py $robot

mv trajectory.csv /qontrol/build/examples/resources/$robot/