#!/bin/bash

# MSocietyTrace Launcher Script
# Version: 2.0

# Dark professional colors
RED='\033[0;31m'
LIGHTRED='\033[1;31m'
BLACK='\033[0;30m'
WHITE='\033[1;37m'
GRAY='\033[0;37m'
DARKGRAY='\033[1;30m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/venv"

# Print launcher banner with dark theme
echo -e "${RED}${BOLD}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${RED}${BOLD}║${NC} ${WHITE}${BOLD}MSocietyTrace - Social Tracking Tool${NC}                    ${RED}${BOLD}║${NC}"
echo -e "${RED}${BOLD}║${NC} ${GRAY}Version 2.0 - Professional Security Tool${NC}                      ${RED}${BOLD}║${NC}"
echo -e "${RED}${BOLD}╚══════════════════════════════════════════════════════════════╝${NC}"
echo

# Check if virtual environment exists
if [ ! -d "$VENV_DIR" ]; then
    echo -e "${BLACK}[!]${NC} ${WHITE}Virtual environment not found. Creating...${NC}"
    python3 -m venv "$VENV_DIR"
    if [ $? -eq 0 ]; then
        echo -e "${BLACK}[+]${NC} ${WHITE}Virtual environment created successfully${NC}"
    else
        echo -e "${RED}[!]${NC} ${WHITE}Failed to create virtual environment${NC}"
        exit 1
    fi
fi

# Activate virtual environment
echo -e "${BLACK}[+]${NC} ${WHITE}Activating virtual environment...${NC}"
source "$VENV_DIR/bin/activate"

# Check if dependencies are installed
echo -e "${BLACK}[+]${NC} ${WHITE}Checking dependencies...${NC}"
python -c "import flask" 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${BLACK}[!]${NC} ${WHITE}Dependencies not found. Installing...${NC}"
    pip install -r requirements.txt
    if [ $? -eq 0 ]; then
        echo -e "${BLACK}[+]${NC} ${WHITE}Dependencies installed successfully${NC}"
    else
        echo -e "${RED}[!]${NC} ${WHITE}Failed to install dependencies${NC}"
        exit 1
    fi
fi

# Check for required tools
echo -e "${BLACK}[+]${NC} ${WHITE}Checking required system tools...${NC}"

# Check for cloudflared
if ! command -v cloudflared &> /dev/null; then
    echo -e "${RED}[!]${NC} ${WHITE}cloudflared not found. Please install it:${NC}"
    echo -e "${GRAY}    wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb${NC}"
    echo -e "${GRAY}    sudo dpkg -i cloudflared-linux-amd64.deb${NC}"
    echo
    echo -e "${BLACK}[?]${NC} ${WHITE}Continue anyway? (y/N): ${NC}"
    read -r response
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        echo -e "${RED}[!]${NC} ${WHITE}Installation cancelled${NC}"
        exit 1
    fi
fi

# Check for SSH
if ! command -v ssh &> /dev/null; then
    echo -e "${RED}[!]${NC} ${WHITE}SSH not found. Please install OpenSSH client${NC}"
    echo -e "${GRAY}    sudo apt install openssh-client${NC}"
    exit 1
fi

echo -e "${BLACK}[+]${NC} ${WHITE}All checks passed!${NC}"
echo

# Launch the tool
echo -e "${RED}${BOLD}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${RED}${BOLD}║${NC} ${LIGHTRED}${BOLD}Launching MSocietyTrace...${NC}                                   ${RED}${BOLD}║${NC}"
echo -e "${RED}${BOLD}╚══════════════════════════════════════════════════════════════╝${NC}"
echo

python3 index.py

# Keep terminal open after tool exits
echo
echo -e "${BLACK}[+]${NC} ${WHITE}MSocietyTrace has stopped. Press Enter to exit...${NC}"
read
