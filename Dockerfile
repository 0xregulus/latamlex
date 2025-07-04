# Dockerfile

FROM python:3.11-slim

# Set env vars
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Installs necessary system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Copies project files
COPY . .

# Installs dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Exposes Streamlit port
EXPOSE 8501

# Runs the app
CMD ["streamlit", "run", "app/interface.py", "--server.port=8501", "--server.address=0.0.0.0"]