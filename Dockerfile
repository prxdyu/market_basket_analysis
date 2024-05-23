# Use the official Python image from the Docker Hub
FROM python:3.8-alpine

# Set the working directory
WORKDIR /install

# Copy the requirements file into the container
COPY requirements.txt .

# Install build dependencies and Python packages
RUN apk update && \
    apk add --no-cache \
        build-base \
        gfortran \
        openblas-dev \
        cmake \
        pkgconfig \
        musl-dev \
    && pip 
