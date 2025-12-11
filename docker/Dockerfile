# Build OPENCV stage
FROM ubuntu:24.04 AS opencv_builder

# Install opencv
RUN apt update && apt install -y \
    build-essential \
    git \
    cmake \
    g++ \
    wget \
    unzip \
    python3 \
    python3-dev \
    python3-pip \
    python3-numpy \
    libgtk-3-dev \
    pkg-config \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libtbb-dev \
    libatlas-base-dev \
    gfortran \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opencv
RUN wget -O opencv.zip https://github.com/opencv/opencv/archive/4.x.zip \
    && unzip opencv.zip

# Grab extra modules (ximgproc lives here)
RUN wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/4.x.zip \
    && unzip opencv_contrib.zip

WORKDIR /opencv/build
RUN cmake \
    -D WITH_TBB=ON \
    -D ENABLE_FAST_MATH=1 \
    -D CMAKE_BUILD_TYPE=Release \
    -D PYTHON3_EXECUTABLE=/usr/bin/python3 \
    -D PYTHON3_INCLUDE_DIR=$(python3 -c "import sysconfig; print(sysconfig.get_path('include'))") \
    -D PYTHON3_PACKAGES_PATH=$(python3 -c "import sysconfig; print(sysconfig.get_path('platlib'))") \
    -D OPENCV_EXTRA_MODULES_PATH=/opencv/opencv_contrib-4.x/modules \
    -D BUILD_opencv_ximgproc=ON \
    -D BUILD_opencv_python_bindings_generator=ON \
    -D BUILD_opencv_python3=ON \
    -D BUILD_opencv_java=OFF \
    -D BUILD_opencv_js=OFF \
    -D BUILD_opencv_dnn_java=OFF \
    -D BUILD_opencv_world=OFF \
    -D BUILD_EXAMPLES=OFF \
    -D BUILD_TESTS=OFF \
    -D BUILD_PERF_TESTS=OFF \
    -D BUILD_DOCS=OFF \
    ../opencv-4.x \
    && cmake --build . --config Release -- -j"$(nproc)"

RUN cmake --install . --config Release

# Download mu-sid dataset stage
FROM ubuntu:24.04 AS mu_sid_dataset

RUN apt update && apt install -y \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /datasets/mus_sid/
RUN curl -L -o /datasets/mus_sid/musid.zip \
  https://www.kaggle.com/api/v1/datasets/download/umairatwork/manzoorumair-sea-image-dataset-musid
WORKDIR /datasets/mus_sid/
RUN unzip musid.zip && rm musid.zip

# # Download dataset stage
# FROM ubuntu:24.04 AS tmd_dataset

# RUN apt update && apt install -y \
#     python3-pip \
#     unzip \
#     && rm -rf /var/lib/apt/lists/*

# RUN pipx install gdown && pipx ensurepath

# RUN ["/bin/bash", "-c", "gdown --folder https://drive.google.com/drive/folders/1B0vmY051xV001RuzvJF31PYPeKKz0pol?usp=drive_link -O /datasets/tmd/"]

# build application/runtime stage
FROM ubuntu:24.04 AS build_application

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    g++ \
    vim \
    python3 \
    python3-pip \
    python3-numpy \
    python3-tk \
    libgtk-3-0 \
    libcanberra-gtk-module \
    libcanberra-gtk3-module \
    at-spi2-core \
    dbus-x11 \
    libgtk-3-dev \
    pkg-config \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libtbb-dev \
    libatlas-base-dev \
    gfortran \
    gdb \
    && rm -rf /var/lib/apt/lists/*

ENV NO_AT_BRIDGE=1

# Bring in OpenCV (installed under /usr/local in the builder)
COPY --from=opencv_builder /usr/local/ /usr/local/

# Bring in dataset
COPY --from=mu_sid_dataset /datasets/mus_sid/ /datasets/mus_sid/

WORKDIR /fast_detector
COPY FastHorizonAlg.py /fast_detector/
COPY main.py /fast_detector/
