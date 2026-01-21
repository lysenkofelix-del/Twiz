"""
Build script for creating Twix Launcher executable
Uses PyInstaller to create a standalone Windows executable
"""

import os
import sys
import subprocess
import shutil

def build_executable():
    """Build the launcher executable"""
    print("="*70)
    print("TWIX LAUNCHER - BUILD SCRIPT")
    print("="*70)
    print()

    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print("✓ PyInstaller is installed")
    except ImportError:
        print("✗ PyInstaller is not installed")
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✓ PyInstaller installed successfully")

    print()
    print("Building executable...")
    print()

    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--name=TwixLauncher",
        "--onefile",
        "--windowed",
        "--clean",
        # Add icon if available
        # "--icon=icon.ico",
        "launcher.py"
    ]

    # Additional options for cleaner build
    additional_options = [
        "--noconfirm",  # Don't ask for confirmation
        f"--distpath=dist",  # Output directory
        f"--workpath=build",  # Build directory
        f"--specpath=.",  # Spec file directory
    ]

    cmd.extend(additional_options)

    # Run PyInstaller
    try:
        print(f"Running: {' '.join(cmd)}")
        print()
        subprocess.check_call(cmd)
        print()
        print("="*70)
        print("✓ BUILD SUCCESSFUL!")
        print("="*70)
        print()
        print(f"Executable location: {os.path.abspath('dist/TwixLauncher.exe')}")
        print()
        print("You can now distribute the TwixLauncher.exe file.")
        print("The executable includes all dependencies and requires no installation.")
        print()

    except subprocess.CalledProcessError as e:
        print("="*70)
        print("✗ BUILD FAILED!")
        print("="*70)
        print(f"Error: {e}")
        sys.exit(1)

    except Exception as e:
        print("="*70)
        print("✗ BUILD FAILED!")
        print("="*70)
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    build_executable()
