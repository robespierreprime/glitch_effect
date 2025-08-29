#!/usr/bin/env python3
"""
Setup script for the Glitch Effect Generator.
Creates virtual environment and installs dependencies.
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd):
    """Run a shell command and handle errors."""
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print(f"Output: {e.stdout}")
        print(f"Error: {e.stderr}")
        return False

def main():
    """Setup the project environment."""
    print("Setting up Glitch Effect Generator...")
    
    # Create directories if they don't exist
    Path("input").mkdir(exist_ok=True)
    Path("output").mkdir(exist_ok=True)
    print("Created input/ and output/ directories")
    
    # Check Python version
    python_cmd = "python3"
    if not run_command(f"{python_cmd} --version"):
        print("Python 3 not found. Please install Python 3.7+ first.")
        sys.exit(1)
    
    # Create virtual environment
    print("Creating virtual environment...")
    if not run_command(f"{python_cmd} -m venv venv"):
        print("Failed to create virtual environment")
        sys.exit(1)
    
    # Install dependencies
    print("Installing dependencies...")
    pip_cmd = "venv/bin/pip" if os.name != 'nt' else "venv\\Scripts\\pip"
    if not run_command(f"{pip_cmd} install -r requirements.txt"):
        print("Failed to install dependencies")
        sys.exit(1)
    
    print("Setup complete.")
    print("\nUsage:")
    print("  # Activate virtual environment")
    if os.name == 'nt':
        print("  venv\\Scripts\\activate")
    else:
        print("  source venv/bin/activate")
    print("\n  # Process single image")
    print("  python glitch_effect_improved.py input/image.jpg -o output/glitched.jpg")
    print("\n  # Process all images in input directory")
    print("  python glitch_effect_improved.py input/ -o output/")
    print("\nSee README.md for more examples and usage")

if __name__ == "__main__":
    main()