# Use CUDA runtime image as base
FROM nvidia/cuda:12.2.0-runtime-ubuntu22.04 AS builder

# Set working directory
WORKDIR /app

# install Python
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3.11-venv \
    python3.11-dev \
    python3-pip \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*


# ensure python3.11 is default
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1

COPY requirements.txt .

# install dependencies
RUN python3 -m pip install --user --no-cache-dir -r requirements.txt

# Final image
FROM nvidia/cuda:12.2.0-runtime-ubuntu22.04
WORKDIR /app

# Copy Python packages from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

COPY . .

CMD ["/bin/bash"]
