#!/bin/bash
# ACEP ISO 27001 Quick Launcher
# Created by A Chaitanya Eshwar Prasad

cd "$(dirname "$0")"

echo "================================================"
echo "  Starting ACEP ISO 27001 Audit Assistant"
echo "  Created by A Chaitanya Eshwar Prasad"
echo "================================================"

# Check if virtual environment exists
if [ ! -d "acep_iso_venv" ]; then
    echo "ERROR: Virtual environment not found!"
    echo "Please run acep_iso_auto_setup.sh first"
    exit 1
fi

# Activate virtual environment
source acep_iso_venv/bin/activate

# Check dependencies
if ! python -c "import flask" 2>/dev/null; then
    echo "Installing missing dependencies..."
    pip install -r requirements.txt
fi

echo "Starting ACEP ISO 27001 Audit Assistant..."
echo "Access: http://localhost:5000"
echo "Login: admin / admin123"
echo "Press Ctrl+C to stop"
echo "================================================"

# Start application
python app.py
