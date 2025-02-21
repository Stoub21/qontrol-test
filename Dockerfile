# Use a CUDA image with Ubuntu 22.04
FROM nvidia/cuda:12.2.0-devel-ubuntu22.04

# Install dependencies
RUN apt update && apt upgrade -y && \
    apt install -qqy \
    python3 python3-pip \
    build-essential wget curl lsb-release \
    libgl1-mesa-glx libglfw3 mesa-utils \
    x11-xserver-utils x11-apps libosmesa6-dev patchelf \
    cmake pkg-config git \
    libtinyxml2-dev libeigen3-dev \
    libxinerama-dev libxrandr-dev libxcursor-dev libxi-dev && \
    rm -rf /var/lib/apt/lists/*

# Configure the repo Robotpkg for Pinocchio
RUN mkdir -p /etc/apt/keyrings && \
    curl http://robotpkg.openrobots.org/packages/debian/robotpkg.asc \
    | tee /etc/apt/keyrings/robotpkg.asc && \
    echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/robotpkg.asc] http://robotpkg.openrobots.org/packages/debian/pub $(lsb_release -cs) robotpkg" \
    | tee /etc/apt/sources.list.d/robotpkg.list

# Update and install Pinocchio from Robotpkg
RUN apt update && \
    apt install -qqy robotpkg-py3*-pinocchio

# Initialisation for environment variables
ENV PATH="/opt/openrobots/bin:$PATH"
ENV PKG_CONFIG_PATH="/opt/openrobots/lib/pkgconfig:${PKG_CONFIG_PATH:-}"
ENV LD_LIBRARY_PATH="/opt/openrobots/lib:${LD_LIBRARY_PATH:-}"
ENV PYTHONPATH="/opt/openrobots/lib/python3.10/site-packages:${PYTHONPATH:-}"
ENV CMAKE_PREFIX_PATH="/opt/openrobots:${CMAKE_PREFIX_PATH:-}"

# Install Qontrol
RUN git clone https://gitlab.inria.fr/auctus-team/components/control/qontrol.git && \
    cd qontrol && \
    mkdir -p build && \
    cd build && \
    cmake .. && \
    make -j4

# Define the workspace
WORKDIR /home

# Default command
CMD ["/bin/bash"]
