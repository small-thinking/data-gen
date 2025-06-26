FROM python:3.11-slim

# Install uv
RUN pip install uv

# Set workdir and copy project
WORKDIR /app
COPY . .

RUN uv pip install --system -r requirements.txt || true
RUN uv pip install --system .

# Default command (for development)
CMD ["bash"] 