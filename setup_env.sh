#!/bin/zsh

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install the package in development mode
echo "Installing the package in development mode..."
pip install -e ".[dev]"

# Print success message
echo "Virtual environment setup complete!"
echo "To activate the environment, run: source .venv/bin/activate"