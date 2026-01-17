#!/usr/bin/env python3
"""
Example: Programmatic Usage of Setup Wizard
For advanced users who want to integrate the wizard into their scripts
"""

import sys
import os
from pathlib import Path

# Add the parent directory to sys.path to import setup_wizard
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def example_folder_setup():
    """Example: Setup from a local folder."""
    print("Example 1: Setup from Local Folder")
    print("-" * 50)
    
    # Note: This is a conceptual example showing the wizard's capabilities
    # The actual GUI application should be run normally
    
    source = "/path/to/your/repository"
    target = str(Path.home() / "my_projects" / "new_repo")
    
    print(f"Source: {source}")
    print(f"Target: {target}")
    print("Action: Copy folder contents")
    print()


def example_zip_setup():
    """Example: Setup from a ZIP file."""
    print("Example 2: Setup from ZIP File")
    print("-" * 50)
    
    source = "/path/to/repository.zip"
    target = str(Path.home() / "my_projects" / "extracted_repo")
    
    print(f"Source: {source}")
    print(f"Target: {target}")
    print("Action: Extract ZIP and setup")
    print()


def example_url_setup():
    """Example: Setup from Git URL."""
    print("Example 3: Setup from Git URL")
    print("-" * 50)
    
    source = "https://github.com/user/repository.git"
    target = str(Path.home() / "my_projects" / "cloned_repo")
    
    print(f"Source: {source}")
    print(f"Target: {target}")
    print("Action: Clone repository")
    print()


def example_with_dependencies():
    """Example: Setup with automatic dependency installation."""
    print("Example 4: Setup with Auto Dependencies")
    print("-" * 50)
    
    source = "https://github.com/user/python-project.git"
    target = str(Path.home() / "my_projects" / "python_app")
    
    print(f"Source: {source}")
    print(f"Target: {target}")
    print("Auto-install: Yes")
    print("Dependencies: Will detect and install from requirements.txt")
    print()


def example_batch_setup():
    """Example: Batch setup of multiple repositories."""
    print("Example 5: Batch Setup")
    print("-" * 50)
    
    repositories = [
        {
            "source": "https://github.com/user/repo1.git",
            "target": "~/projects/repo1",
            "type": "url"
        },
        {
            "source": "/path/to/local/repo2",
            "target": "~/projects/repo2",
            "type": "folder"
        },
        {
            "source": "/path/to/archive.zip",
            "target": "~/projects/repo3",
            "type": "zip"
        }
    ]
    
    print("Batch setup plan:")
    for i, repo in enumerate(repositories, 1):
        print(f"  {i}. {repo['type'].upper()}: {repo['source']}")
        print(f"     → {repo['target']}")
    print()


def example_error_handling():
    """Example: Error handling scenarios."""
    print("Example 6: Error Handling")
    print("-" * 50)
    
    scenarios = [
        "Invalid source path → Shows error dialog",
        "Network timeout → Logs error and shows message",
        "Insufficient permissions → Clear error message",
        "Target already exists → Auto-rename with _1, _2, etc",
        "Git not installed → Warning with instructions",
        "Dependency install fails → Warning, continues setup"
    ]
    
    print("The wizard handles these scenarios gracefully:")
    for scenario in scenarios:
        print(f"  • {scenario}")
    print()


def main():
    """Run all examples."""
    print()
    print("=" * 70)
    print("Setup Wizard - Programmatic Usage Examples")
    print("=" * 70)
    print()
    print("Note: These are conceptual examples showing the wizard's capabilities.")
    print("To actually use the wizard, run: python3 setup_wizard.py")
    print()
    print("=" * 70)
    print()
    
    example_folder_setup()
    example_zip_setup()
    example_url_setup()
    example_with_dependencies()
    example_batch_setup()
    example_error_handling()
    
    print("=" * 70)
    print("Integration Tips:")
    print("-" * 70)
    print()
    print("1. Command Line Usage:")
    print("   python3 setup_wizard.py")
    print()
    print("2. From Scripts:")
    print("   Launch the GUI wizard from your automation scripts")
    print()
    print("3. Batch Operations:")
    print("   Run multiple wizard instances for parallel setups")
    print()
    print("4. Custom Workflows:")
    print("   Extend the wizard's classes for custom behavior")
    print()
    print("5. Monitoring:")
    print("   Check logs at ~/.repo_setup_wizard/logs/")
    print()
    print("=" * 70)
    print()
    print("For GUI usage, simply run:")
    print("  ./launch.sh (Linux/macOS)")
    print("  launch.bat (Windows)")
    print("  python3 setup_wizard.py (All platforms)")
    print()


if __name__ == "__main__":
    main()
