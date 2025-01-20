#!/bin/bash

# Update package lists
echo "Updating package lists..."
sudo apt update && sudo apt upgrade -y

# Install essential packages
echo "Installing essential packages..."
sudo apt install -y docker.io docker-compose git python3-pip

# Add Docker to the system group
echo "Adding user to Docker group..."
sudo usermod -aG docker $USER

# Create useful aliases
echo "Creating aliases..."
echo 'alias ll="ls -la"' >> ~/.bashrc
echo 'alias ..="cd .."' >> ~/.bashrc

# Reload bash configuration
echo "Reloading bash configuration..."
source ~/.bashrc

# Print completion message
echo "Setup completed successfully!"