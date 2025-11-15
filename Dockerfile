# ---------------------------
# Dockerfile for SysSentry
# ---------------------------

# Base image (Python with pip pre-installed)
FROM python:3.10

# Set working directory inside container
WORKDIR /app

# Copy everything into container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Streamlit port
EXPOSE 8501

# Default command when container starts
CMD ["streamlit", "run", "dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]

# Add health check for container
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8501/_stcore/health || exit 1
