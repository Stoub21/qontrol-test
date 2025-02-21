# Qontrol test

## Context

To apply to an [Inria offer](https://newsletter.gdr-robotique.org/?n=1cd560ec416116b25a1e0abba41ddd21) for the [Extender project of Orthopus](https://orthopus.com/fr/) I have to install and experiment the [qontrol tool](https://gitlab.inria.fr/auctus-team/components/control/qontrol).

specifically my task is to : 
- Install Qontrol
- Run any of the existing examples
- Modify it to make move a robot 
    - Start by a shift forward of 0.1 m along th x axis
    - Follow by a shift backward of 0.2 m along the z axis.
- Finaly I have to give back this report of my work throught git where I explain my choices and steps in english.


## Steps
### Installation
On the installation website it is specify that the tool is only compatible with Ubuntu 20.04 and 22.04. As I currently use Ubuntu 24.04 I will have to use [Docker](https://www.docker.com/) or a VM (I chose docke).

So I generate a [Dockerfile](Dockerfile) to generate a correct environment.

I never worked neither with [mujoco](https://mujoco.org/) and [pinocchio](https://stack-of-tasks.github.io/pinocchio/) so I had some documentation to check.

I can build my docker image with the command `docker build -t qontrol .`
And run it with the command `docker run -it --rm --gpus all -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -v .:/home  --device=/dev/dri:/dev/dri qontrol`

- I have GPU and it seems to be usefull for the simulation and mujoco so with the [Nvidia Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/index.html) I give access to the GPUs to the container (And I use a docker image with CUDA (**CUDA could be uncompatible due to your GPU**))
- To give the acces to the screen at the container I have to add X11 Forwarding option (-e ..., -v ... and --device option), but I also have to give the permition to do that before running the container with the command `xhost +`.

When the container is start I can lanch the simulation by moving to the paht `qontrol/build/examples` and by lanching the command :`./velocityQontrol panda`

### Understanding the Qontrol function

By reading the documentation and watching the code, it seems to be use to set some rules to the task of parameters reserse.

Each functions `velocityQontrol` `QontrolCustomConstraint` `QontrolCustomTask` `torqueQontrol` `Qontrol_qpmad` we need a path description for the end effector of the chosed robot (`panda` or `ur5`). The code will, for each line of the plan path, compare the position of the end effector to the target and use a corrector to have a target error. Finally the Qontrol function will use this output target to describe the motors command. The way as it use this output target is define in each examples of the documentation.

### Use

So to adapt the current work to a specific path I just have to generate the `trajectory.csv` file that containt the path planning.

Whe I read this file I saw that 19 parameters are ask for each point :
- 3 for the cartesian position
- 4 for the quaternion orientation
- 3 for the cartesian speed
- 3 for the euler angles speed
- 3 for the cartesian acceleration
- 3 for the euler angles acceleration

But position matrix (7 first parameters) is anought for `velocityQontrol`, `Qontrol_qpmad`, `QontrolCustomTask` and `QontrolCustomConstraint` and for `torqueQontrol` position and speed are anougth.

So I write a [python script](trajectory_gen.py) that generate a `trajectory.csv` file with only position setting based on number of point (equivalent to the time as each point is suppose to be execute every 1 ms) and a direction vector.

For a easier utilisation I also generate two script to update the trajectory path and to lanch the simulation.

For write the trajectory, it can be in the python code directly.

To replace the `trajectory.csv` file of a chosen robot you can lanch the command line `./update_trajectory.sh panda` (or `ur5`) and that will replace the trajectory file by the one generate by python.

To launch a simulation you can use the command `./launch_Qontrol.sh velocityQontrol ur5` (or any of the function with any robot). This command go to the `qontrol/build/examples` path (necessary to launch a function) and launch the desire function.

### Result

The trajectory currently generate by the python code is for respecting the task of start with a x shift of 0.1m and finish with a z shift of -0.2m.

## Further work

Even if I reach to follow my askek trajectory by the robot I have not fully understand the problematic and solution method describe by the Qontrol tool, so there is some point that could be interesting to go deeper in that way : 

- extract the robot states values to analyse them for each of control method
- add more task and/or constraint

## Biblio

- [QP Solver - *Wikipedia*](https://en.wikipedia.org/wiki/Quadratic_programming)
- [Hessian matrix - *Wikipedia*](https://en.wikipedia.org/wiki/Hessian_matrix)
- I have been help by chatGTP and Mistral LLM to write the code and improve my report. 