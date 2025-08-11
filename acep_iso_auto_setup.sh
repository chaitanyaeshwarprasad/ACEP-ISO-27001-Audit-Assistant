#!/bin/bash
#############################################################################
# ACEP ISO 27001 Audit Assistant - Automated All-in-One Setup for Kali Linux
# Created by A Chaitanya Eshwar Prasad
# 
# This script automatically:
# - Detects and installs missing dependencies
# - Creates virtual environment
# - Handles all common errors automatically
# - Sets up and starts the application
#############################################################################

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Functions
log_info() { echo -e "${CYAN}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

print_banner() {
    echo -e "${BLUE}"
    echo "=================================================================="
    echo "    ACEP ISO 27001 AUDIT ASSISTANT - AUTO SETUP"
    echo "    Created by A Chaitanya Eshwar Prasad"
    echo "    Automated All-in-One Setup for Kali Linux"
    echo "=================================================================="
    echo -e "${NC}"
}

check_root() {
    if [[ $EUID -eq 0 ]]; then
        log_error "Do not run this script as root! Run as regular user."
        exit 1
    fi
}

update_system() {
    log_info "Updating system package lists..."
    if sudo apt update >/dev/null 2>&1; then
        log_success "System updated successfully"
    else
        log_warning "System update failed, continuing anyway..."
    fi
}

install_python_deps() {
    log_info "Checking and installing Python dependencies..."
    
    # Check if Python 3 is installed
    if ! command -v python3 &> /dev/null; then
        log_info "Installing Python 3..."
        sudo apt install -y python3
    fi
    
    # Check if pip is installed
    if ! command -v pip3 &> /dev/null; then
        log_info "Installing pip3..."
        sudo apt install -y python3-pip
    fi
    
    # Check if venv module is available
    if ! python3 -m venv --help >/dev/null 2>&1; then
        log_info "Installing python3-venv..."
        sudo apt install -y python3-venv
    fi
    
    # Install other useful tools
    log_info "Installing additional tools..."
    sudo apt install -y curl wget git >/dev/null 2>&1 || true
    
    log_success "Python dependencies installed"
}

handle_externally_managed() {
    log_info "Handling externally-managed-environment..."
    
    # Always use virtual environment to avoid externally-managed-environment error
    if [ -d "acep_iso_venv" ]; then
        log_warning "Virtual environment already exists, removing old one..."
        rm -rf acep_iso_venv
    fi
    
    log_info "Creating new virtual environment..."
    python3 -m venv acep_iso_venv
    
    if [ ! -f "acep_iso_venv/bin/activate" ]; then
        log_error "Failed to create virtual environment"
        exit 1
    fi
    
    log_success "Virtual environment created successfully"
}

install_requirements() {
    log_info "Activating virtual environment and installing requirements..."
    
    # Activate virtual environment
    source acep_iso_venv/bin/activate
    
    # Upgrade pip in virtual environment
    log_info "Upgrading pip..."
    pip install --upgrade pip >/dev/null 2>&1
    
    # Install requirements with error handling
    log_info "Installing Python packages..."
    if pip install -r requirements.txt >/dev/null 2>&1; then
        log_success "All Python packages installed successfully"
    else
        log_warning "Some packages failed, trying individual installation..."
        # Try installing each package individually
        while IFS= read -r package; do
            if [[ ! -z "$package" && ! "$package" =~ ^# ]]; then
                log_info "Installing $package..."
                pip install "$package" >/dev/null 2>&1 || log_warning "Failed to install $package"
            fi
        done < requirements.txt
    fi
    
    # Verify critical packages
    log_info "Verifying critical packages..."
    python -c "import flask, werkzeug, jinja2" 2>/dev/null || {
        log_error "Critical packages missing, trying alternative installation..."
        pip install flask werkzeug jinja2 >/dev/null 2>&1
    }
    
    log_success "Requirements installation completed"
}

fix_permissions() {
    log_info "Setting up permissions..."
    
    # Create necessary directories
    mkdir -p static/uploads database
    
    # Set proper permissions
    chmod 755 static/uploads
    chmod 755 database
    
    # Make scripts executable
    chmod +x *.sh 2>/dev/null || true
    
    log_success "Permissions configured"
}

test_application() {
    log_info "Testing application startup..."
    
    # Activate virtual environment
    source acep_iso_venv/bin/activate
    
    # Test import
    if ! python -c "import flask, werkzeug, jinja2, sqlite3" 2>/dev/null; then
        log_error "Required modules not available"
        return 1
    fi
    
    # Test database creation
    if python -c "
import sqlite3
import os
os.makedirs('database', exist_ok=True)
conn = sqlite3.connect('database/test.db')
conn.close()
os.remove('database/test.db')
" 2>/dev/null; then
        log_success "Database test passed"
    else
        log_error "Database test failed"
        return 1
    fi
    
    log_success "Application test completed successfully"
}

create_launcher() {
    log_info "Creating quick launcher..."
    
    cat > run_acep_iso.sh << 'EOF'
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
EOF

    chmod +x run_acep_iso.sh
    log_success "Quick launcher created: run_acep_iso.sh"
}

cleanup_windows_files() {
    log_info "Removing unnecessary Windows files..."
    
    # Remove Windows-specific files
    rm -f start_acep_iso.bat 2>/dev/null || true
    rm -f *.bat 2>/dev/null || true
    rm -f *.cmd 2>/dev/null || true
    
    log_success "Windows files cleaned up"
}

check_network() {
    log_info "Checking network connectivity..."
    if ping -c 1 8.8.8.8 >/dev/null 2>&1; then
        log_success "Network connectivity confirmed"
    else
        log_warning "No internet connection - using offline mode"
        return 1
    fi
}

main() {
    print_banner
    
    # Pre-flight checks
    check_root
    
    # System setup
    log_info "Starting automated setup process..."
    
    # Check network (optional)
    check_network || log_warning "Limited functionality without internet"
    
    # Update system
    update_system
    
    # Install dependencies
    install_python_deps
    
    # Handle virtual environment
    handle_externally_managed
    
    # Install requirements
    install_requirements
    
    # Fix permissions
    fix_permissions
    
    # Clean up Windows files
    cleanup_windows_files
    
    # Test application
    test_application
    
    # Create launcher
    create_launcher
    
    # Final success message
    echo
    log_success "ACEP ISO 27001 Audit Assistant setup completed successfully!"
    echo
    echo -e "${GREEN}=================================================================="
    echo "                    SETUP COMPLETE!"
    echo "=================================================================="
    echo
    echo "To start the application:"
    echo "  ${CYAN}./run_acep_iso.sh${NC}"
    echo
    echo "Or manually:"
    echo "  ${CYAN}source acep_iso_venv/bin/activate${NC}"
    echo "  ${CYAN}python app.py${NC}"
    echo
    echo "Access the application:"
    echo "  ${YELLOW}URL:${NC} http://localhost:5000"
    echo "  ${YELLOW}Username:${NC} admin"
    echo "  ${YELLOW}Password:${NC} admin123"
    echo
    echo "Created by: ${BLUE}A Chaitanya Eshwar Prasad${NC}"
    echo -e "==================================================================${NC}"
    echo
    
    # Ask if user wants to start immediately
    read -p "Start the application now? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        log_info "Starting ACEP ISO 27001 Audit Assistant..."
        ./run_acep_iso.sh
    else
        log_info "Setup complete. Run './run_acep_iso.sh' when ready."
    fi
}

# Trap errors and provide helpful messages
trap 'log_error "Setup failed at line $LINENO. Check the error above."; exit 1' ERR

# Run main function
main "$@"
