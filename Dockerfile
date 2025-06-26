# Use a slim Python base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libffi-dev \
    libssl-dev \
    poppler-utils \
    git \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . .

# Upgrade pip and install dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# (Optional) Validate spaCy model setup without failing the build
RUN python -m spacy validate || true

# Streamlit expects this for Cloud Run
ENV PORT=8080

# Expose the port (Cloud Run will use it)
EXPOSE 8080

# Start the app using Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
