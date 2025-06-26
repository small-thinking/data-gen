# Data-Gen

## Project Overview
Data-Gen is a modular toolkit for generating synthetic data tailored for LLM post-training and evaluation. The project is structured as a monorepo to support multiple components, including a core data generation module, a backend API, and a web client.

## Monorepo Structure
```
core/      # Core synthetic data generation logic (Python, uv-managed)
web/       # (future) Web client
backend/   # (future) Backend API
```

## Getting Started
- See `core/README.md` for details on the core module.
- Each component is managed independently.

## Local Development (Core Module)

1. Install [uv](https://github.com/astral-sh/uv):
   ```sh
   pip install uv
   ```
2. Create a virtual environment (recommended):
   ```sh
   uv venv .venv
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```sh
   uv pip install -e .
   ```
4. Run tests:
   ```sh
   uv pip install pytest  # if not already installed
   pytest
   ```

## Docker Usage

1. Build the Docker image:
   ```sh
   docker build -t data-gen .
   ```
2. Run the container:
   ```sh
   docker run -it data-gen
   ```

> **Note:** If you see an error about "No virtual environment found" when building Docker, ensure the Dockerfile uses `uv pip install --system ...` for global installs (already set up in this repo).

## Component Descriptions
- **core/**: Implements the main logic for generating synthetic data for LLM post-training. (First component to be implemented)
- **web/**: (Planned) Web-based user interface for data generation and management.
- **backend/**: (Planned) API backend for orchestration and integration.

## Contributing
- Contributions are welcome! Please see the contributing guidelines in each component folder.
