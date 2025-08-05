# SymNet3 Dockerfile
FROM prost:latest AS builder

FROM ubuntu:24.04

RUN apt-get update && apt-get -y install locales
RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install tzdata

# install golang and python dependencies
RUN apt-get update && apt upgrade -y && apt-get install -y  \
    build-essential \
    curl \
    git \
    golang-go \
    libbz2-dev \
    libdb-dev \
    libffi-dev \
    libgdbm-dev \
    liblzma-dev \
    libncursesw5-dev \
    libnss3-dev \
    libreadline-dev \
    libsqlite3-dev \
    libssl-dev \
    libxml2-dev \
    libxmlsec1-dev \
    llvm \
    make \
    tk-dev \
    uuid-dev \
    wget \
    xz-utils \
    zlib1g-dev

# install asdf
RUN go install github.com/asdf-vm/asdf/cmd/asdf@v0.18.0

ENV ASDF_DATA_DIR="/root/.asdf"
ENV PATH="$PATH:/root/go/bin:${ASDF_DATA_DIR}/shims"

# install python
RUN asdf plugin add python
RUN asdf install python 3.12.4

# install uv
RUN asdf plugin add uv
RUN asdf install uv 0.7.21

# install java
RUN asdf plugin add java
RUN asdf install java openjdk-24.0.2

# install symnet3 dependencies
WORKDIR /workspace/symnet3

COPY ./requirements.txt /workspace/symnet3/requirements.txt
COPY ./uv.lock /workspace/symnet3/uv.lock
COPY ./.tool-versions /workspace/symnet3/.tool-versions
COPY ./pyproject.toml /workspace/symnet3/pyproject.toml

RUN uv sync

WORKDIR /workspace/prost
COPY --from=builder /workspace/prost/builds/release/rddl_parser/rddl-parser /workspace/prost/rddl-parser

WORKDIR /workspace/symnet3