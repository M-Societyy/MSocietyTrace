#!/bin/bash

# MSocietyTrace Quick Launcher
# Fast execution without checks

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Activate virtual environment and run
source "$SCRIPT_DIR/venv/bin/activate" && python3 "$SCRIPT_DIR/index.py"
