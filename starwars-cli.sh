#!/bin/bash
# Star Wars CLI launcher for Unix/Linux/macOS
# Ensures proper execution with correct Python interpreter

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check if python3 is available, fallback to python
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "Error: Python not found. Please install Python 3.8 or later."
    exit 1
fi

# Run the Python script with all passed arguments
"$PYTHON_CMD" "$SCRIPT_DIR/starwars-cli.py" "$@"
