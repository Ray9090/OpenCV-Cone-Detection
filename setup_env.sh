#!/bin/bash

# Define the virtual environment directory
VENV_DIR="venv"

echo "===== Setup Environment Script for Ubuntu ====="

# Check for Python 3 installation
if ! command -v python3 &> /dev/null; then
    echo "Python3 is not installed. Installing Python3..."
    sudo apt update
    sudo apt install -y python3
    if [ $? -ne 0 ]; then
        echo "Failed to install Python3. Please install it manually and re-run this script."
        exit 1
    fi
else
    echo "Python3 is already installed."
fi

# Check for Python 3.10 version
PYTHON_VERSION=$(python3 --version | awk '{print $2}')
REQUIRED_VERSION="3.10"

if dpkg --compare-versions "$PYTHON_VERSION" lt "$REQUIRED_VERSION"; then
    echo "Python version is less than $REQUIRED_VERSION. Upgrading to Python $REQUIRED_VERSION..."
    sudo add-apt-repository -y ppa:deadsnakes/ppa
    sudo apt update
    sudo apt install -y python3.10 python3.10-venv python3.10-distutils
    if [ $? -ne 0 ]; then
        echo "Failed to install Python 3.10. Please install it manually and re-run this script."
        exit 1
    fi

    # Set Python 3.10 as the default python3 version
    sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1
    sudo update-alternatives --config python3 <<< 1
else
    echo "Python version is $PYTHON_VERSION, which meets the requirement."
fi

# Check for python3.10-venv package
if ! dpkg -l | grep -qw python3.10-venv; then
    echo "python3.10-venv is not installed. Installing python3.10-venv..."
    sudo apt install -y python3.10-venv
    if [ $? -ne 0 ]; then
        echo "Failed to install python3.10-venv. Please install it manually and re-run this script."
        exit 1
    fi
else
    echo "python3.10-venv is already installed."
fi

# Check if the virtual environment exists and is valid
if [ ! -d "$VENV_DIR" ] || [ ! -f "$VENV_DIR/bin/activate" ]; then
    echo "Creating virtual environment in $VENV_DIR using Python 3.10..."
    rm -rf $VENV_DIR  # Remove partially created venv if it exists
    python3.10 -m venv $VENV_DIR
    if [ $? -ne 0 ]; then
        echo "Failed to create virtual environment. Exiting..."
        exit 1
    fi
    echo "Virtual environment created."
else
    echo "Virtual environment already exists."
fi

# Activate the virtual environment
source $VENV_DIR/bin/activate
if [ $? -ne 0 ]; then
    echo "Failed to activate virtual environment. Exiting..."
    exit 1
fi

# Install dependencies from requirements.txt
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies from requirements.txt..."
    pip install --upgrade pip  # Ensure pip is up to date
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "Failed to install dependencies. Please check the requirements.txt file."
        deactivate
        exit 1
    fi
    echo "Dependencies installed successfully."
else
    echo "requirements.txt not found. Skipping dependency installation."
fi

# Deactivate the virtual environment
deactivate

echo "Setup complete! To use the virtual environment, activate it using:"
echo "    source $VENV_DIR/bin/activate"
