#!/bin/bash
# Launcher script for the Universal Repository Setup Wizard
# This script ensures Python and dependencies are available

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "🚀 Universal Repository Setup Wizard Launcher"
echo "=============================================="
echo ""

# Check for Python 3
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
elif command -v python &> /dev/null; then
    PYTHON_VERSION=$(python --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1)
    if [ "$PYTHON_VERSION" -ge 3 ]; then
        PYTHON_CMD=python
    else
        echo -e "${RED}❌ Error: Python 3.7 or higher is required${NC}"
        echo "Please install Python 3 from https://www.python.org/"
        exit 1
    fi
else
    echo -e "${RED}❌ Error: Python is not installed${NC}"
    echo "Please install Python 3 from https://www.python.org/"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | cut -d' ' -f2)
echo -e "${GREEN}✓${NC} Found Python $PYTHON_VERSION"

# Check for tkinter
if ! $PYTHON_CMD -c "import tkinter" 2>/dev/null; then
    echo -e "${YELLOW}⚠${NC}  Warning: tkinter not found"
    echo ""
    echo "Please install tkinter for your system:"
    echo "  Ubuntu/Debian: sudo apt-get install python3-tk"
    echo "  Fedora:        sudo dnf install python3-tkinter"
    echo "  Arch:          sudo pacman -S tk"
    echo ""
    exit 1
fi

echo -e "${GREEN}✓${NC} tkinter is available"

# Check for Git (optional)
if command -v git &> /dev/null; then
    GIT_VERSION=$(git --version | cut -d' ' -f3)
    echo -e "${GREEN}✓${NC} Git $GIT_VERSION is available"
else
    echo -e "${YELLOW}⚠${NC}  Git not found (needed for URL cloning)"
fi

echo ""
echo "Starting Setup Wizard..."
echo ""

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Launch the wizard
cd "$SCRIPT_DIR"
exec $PYTHON_CMD setup_wizard.py "$@"
