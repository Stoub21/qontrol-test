#!/bin/bash
set -e  # Stop the script in error case

# define the default values
default_function="velocityQontrol"
default_robot="panda"

# read the input values
function_to_run=${1:-$default_function}
robot=${2:-$default_robot}

# Check the values compatibilities
case $function_to_run in
    velocityQontrol|QontrolCustomConstraint|QontrolCustomTask|torqueQontrol|Qontrol_qpmad)
        ;;
    *)
        echo "Invalid function: $function_to_run"
        exit 1
        ;;
esac

case $robot in
    panda|ur5)
        ;;
    *)
        echo "Invalid robot: $robot"
        exit 1
        ;;
esac

# Run the function
cd /qontrol/build/examples
./$function_to_run $robot
