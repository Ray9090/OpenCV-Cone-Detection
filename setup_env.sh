#!/bin/bash

VENV_DIR="venv"

echo "===== Setup Environment Script for Ubuntu ====="

if ! command -v python3 &> /dev/null; then
    echo "Python3 is not installed. Installing Python3..."
    sudo apt update
    sudo apt install -y python3 python3-venv python3-pip
    if [ $? -ne 0 ]; then
        echo "Failed to install Python3. Please install it manually and re-run this script."
        exit 1
    fi
else
    echo "Python3 is already installed."
fi

if ! command -v pip3 &> /dev/null; then
    echo "pip3 is not installed. Installing pip3..."
    sudo apt install -y python3-pip
    if [ $? -ne 0 ]; then
        echo "Failed to install pip3. Please install it manually and re-run this script."
        exit 1
    fi
else
    echo "pip3 is already installed."
fi

if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment in $VENV_DIR..."
    python3 -m venv $VENV_DIR
    if [ $? -ne 0 ]; then
        echo "Failed to create virtual environment. Exiting..."
        exit 1
    fi
    echo "Virtual environment created."
else
    echo "Virtual environment already exists."
fi

source $VENV_DIR/bin/activate
if [ $? -ne 0 ]; then
    echo "Failed to activate virtual environment. Exiting..."
    exit 1
fi

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

deactivate

echo "Setup complete! To use the virtual environment, activate it using:"
echo "    source $VENV_DIR/bin/activate"
