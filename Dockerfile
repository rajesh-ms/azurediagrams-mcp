# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies including Graphviz
RUN apt-get update && apt-get install -y \
    graphviz \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY azure_diagram_server.py .
COPY docker_mcp_server.py .

# Expose port for the server
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run the Docker MCP server
CMD ["python", "docker_mcp_server.py"]
