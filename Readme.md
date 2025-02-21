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

So I generate a [Dockerfile](Dockerfile) too generate a correct environment.

I never worked neither with [mujoco](https://mujoco.org/) and [pinocchio](https://stack-of-tasks.github.io/pinocchio/) so I had some documentation to check.

I can build my docker image with the command `docker build -t qontrol`
And run it with the command `docker run -it --rm --gpus all -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix --device=/dev/dri:/dev/dri qontrol`

I have GPU and it seems to be usefull for the simulation and mujoco so with the [Nvidia Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/index.html) I give access to the GPUs to the container (And I use a docker image with CUDA (**CUDA could be uncompatible due to your GPU**))

When the container is start I can lanch the simulation with the command :`./velocityQontrol panda` 

## 