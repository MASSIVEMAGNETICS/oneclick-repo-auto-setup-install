#!/usr/bin/env python3
"""
Universal Repository Setup Wizard
A production-ready GUI application for setting up repositories from various sources.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import sys
import subprocess
import shutil
import zipfile
import tempfile
import threading
import logging
import json
import shlex
import re
from pathlib import Path
from urllib.parse import urlparse, quote
from datetime import datetime


class SetupWizard:
    """Main application class for the Repository Setup Wizard."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Universal Repository Setup Wizard")
        self.root.geometry("800x600")
        self.root.minsize(700, 500)
        
        # Initialize variables
        self.source_type = tk.StringVar(value="folder")
        self.source_path = tk.StringVar()
        self.target_path = tk.StringVar(value=str(Path.home() / "repo_setups"))
        self.auto_install = tk.BooleanVar(value=True)
        self.use_venv = tk.BooleanVar(value=False)
        self.run_post_setup = tk.BooleanVar(value=False)
        self.add_ci_templates = tk.BooleanVar(value=False)
        self.enable_docker_build = tk.BooleanVar(value=False)
        self.enable_docker_run = tk.BooleanVar(value=False)
        self.run_post_setup_checks = tk.BooleanVar(value=False)
        self.ssh_key_path = tk.StringVar()
        self.oauth_token = tk.StringVar()
        self.git_credential_helper = tk.StringVar()
        self.is_processing = False
        
        # Setup logging
        self.setup_logging()
        
        # Create UI
        self.create_ui()
        
        # Center window
        self.center_window()
        
    def setup_logging(self):
        """Setup comprehensive logging system."""
        log_dir = Path.home() / ".repo_setup_wizard" / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        
        log_file = log_dir / f"setup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info("Setup Wizard initialized")
        
    def center_window(self):
        """Center the window on the screen."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def create_ui(self):
        """Create the main user interface."""
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # Title
        title_label = ttk.Label(
            main_frame, 
            text="Repository Setup Wizard",
            font=('Helvetica', 16, 'bold')
        )
        title_label.grid(row=0, column=0, pady=(0, 20))
        
        # Source selection section
        source_frame = ttk.LabelFrame(main_frame, text="1. Select Repository Source", padding="10")
        source_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        source_frame.columnconfigure(1, weight=1)
        
        # Radio buttons for source type
        ttk.Radiobutton(
            source_frame, 
            text="Local Folder", 
            variable=self.source_type,
            value="folder",
            command=self.on_source_type_change
        ).grid(row=0, column=0, sticky=tk.W, pady=5)
        
        ttk.Radiobutton(
            source_frame, 
            text="ZIP File", 
            variable=self.source_type,
            value="zip",
            command=self.on_source_type_change
        ).grid(row=0, column=1, sticky=tk.W, pady=5)
        
        ttk.Radiobutton(
            source_frame, 
            text="Git URL", 
            variable=self.source_type,
            value="url",
            command=self.on_source_type_change
        ).grid(row=0, column=2, sticky=tk.W, pady=5)
        
        # Source path/URL entry
        ttk.Label(source_frame, text="Source:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.source_entry = ttk.Entry(source_frame, textvariable=self.source_path)
        self.source_entry.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5, padx=(5, 5))
        
        self.browse_button = ttk.Button(source_frame, text="Browse...", command=self.browse_source)
        self.browse_button.grid(row=1, column=3, pady=5)
        
        # Target directory section
        target_frame = ttk.LabelFrame(main_frame, text="2. Select Target Directory", padding="10")
        target_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        target_frame.columnconfigure(1, weight=1)
        
        ttk.Label(target_frame, text="Target:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(target_frame, textvariable=self.target_path).grid(
            row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 5)
        )
        ttk.Button(target_frame, text="Browse...", command=self.browse_target).grid(
            row=0, column=2, pady=5
        )
        
        # Options section
        options_frame = ttk.LabelFrame(main_frame, text="3. Setup Options", padding="10")
        options_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Checkbutton(
            options_frame,
            text="Automatically install dependencies",
            variable=self.auto_install
        ).grid(row=0, column=0, sticky=tk.W, pady=5)
        
        ttk.Checkbutton(
            options_frame,
            text="Create Python .venv for isolated installs",
            variable=self.use_venv
        ).grid(row=1, column=0, sticky=tk.W, pady=5)
        
        ttk.Checkbutton(
            options_frame,
            text="Run post-setup script/recipe if present",
            variable=self.run_post_setup
        ).grid(row=2, column=0, sticky=tk.W, pady=5)
        
        ttk.Checkbutton(
            options_frame,
            text="Run quick post-setup checks",
            variable=self.run_post_setup_checks
        ).grid(row=3, column=0, sticky=tk.W, pady=5)
        
        ttk.Checkbutton(
            options_frame,
            text="Add CI workflow template (if missing)",
            variable=self.add_ci_templates
        ).grid(row=4, column=0, sticky=tk.W, pady=5)
        
        ttk.Checkbutton(
            options_frame,
            text="Build Docker image when Dockerfile is detected",
            variable=self.enable_docker_build
        ).grid(row=5, column=0, sticky=tk.W, pady=5)
        
        ttk.Checkbutton(
            options_frame,
            text="Run Docker image after build",
            variable=self.enable_docker_run
        ).grid(row=6, column=0, sticky=tk.W, pady=5)
        
        # Git authentication section
        auth_frame = ttk.LabelFrame(main_frame, text="4. Git Authentication (Optional)", padding="10")
        auth_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        auth_frame.columnconfigure(1, weight=1)
        
        ttk.Label(auth_frame, text="SSH Key:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(auth_frame, textvariable=self.ssh_key_path).grid(
            row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 5)
        )
        ttk.Button(auth_frame, text="Browse...", command=self.browse_ssh_key).grid(
            row=0, column=2, pady=5
        )
        
        ttk.Label(auth_frame, text="OAuth Token:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(auth_frame, textvariable=self.oauth_token, show="*").grid(
            row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 5)
        )
        
        ttk.Label(auth_frame, text="Credential Helper:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(auth_frame, textvariable=self.git_credential_helper).grid(
            row=2, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 5)
        )
        
        # Progress section
        progress_frame = ttk.LabelFrame(main_frame, text="Progress", padding="10")
        progress_frame.grid(row=5, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        progress_frame.columnconfigure(0, weight=1)
        progress_frame.rowconfigure(1, weight=1)
        main_frame.rowconfigure(5, weight=1)
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode='indeterminate')
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        self.log_text = scrolledtext.ScrolledText(
            progress_frame,
            height=10,
            wrap=tk.WORD,
            font=('Courier', 9)
        )
        self.log_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.log_text.config(state=tk.DISABLED)
        
        # Action buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=6, column=0, pady=(10, 0))
        
        self.start_button = ttk.Button(
            button_frame,
            text="Start Setup",
            command=self.start_setup,
            style='Accent.TButton'
        )
        self.start_button.grid(row=0, column=0, padx=5)
        
        ttk.Button(
            button_frame,
            text="Clear Log",
            command=self.clear_log
        ).grid(row=0, column=1, padx=5)
        
        ttk.Button(
            button_frame,
            text="Exit",
            command=self.exit_application
        ).grid(row=0, column=2, padx=5)
        
    def on_source_type_change(self):
        """Handle source type radio button changes."""
        source_type = self.source_type.get()
        if source_type == "url":
            self.browse_button.config(state=tk.DISABLED)
            self.source_entry.delete(0, tk.END)
            self.source_entry.insert(0, "https://")
        else:
            self.browse_button.config(state=tk.NORMAL)
            self.source_path.set("")
            
    def browse_source(self):
        """Open file/folder browser for source selection."""
        source_type = self.source_type.get()
        
        if source_type == "folder":
            path = filedialog.askdirectory(title="Select Repository Folder")
            if path:
                self.source_path.set(path)
        elif source_type == "zip":
            path = filedialog.askopenfilename(
                title="Select ZIP File",
                filetypes=[("ZIP files", "*.zip"), ("All files", "*.*")]
            )
            if path:
                self.source_path.set(path)
                
    def browse_target(self):
        """Open folder browser for target directory."""
        path = filedialog.askdirectory(title="Select Target Directory")
        if path:
            self.target_path.set(path)

    def browse_ssh_key(self):
        """Open file browser for SSH key selection."""
        path = filedialog.askopenfilename(
            title="Select SSH Private Key",
            filetypes=[("Private key", "*"), ("All files", "*.*")]
        )
        if path:
            self.ssh_key_path.set(path)
            
    def log_message(self, message, level="INFO"):
        """Add message to the log display."""
        self.log_text.config(state=tk.NORMAL)
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {level}: {message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        
        # Also log to file
        if level == "ERROR":
            self.logger.error(message)
        elif level == "WARNING":
            self.logger.warning(message)
        else:
            self.logger.info(message)
            
    def clear_log(self):
        """Clear the log display."""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
        
    def validate_inputs(self):
        """Validate user inputs before processing."""
        source_type = self.source_type.get()
        source = self.source_path.get().strip()
        target = self.target_path.get().strip()
        
        if not source:
            raise ValueError("Please specify a source location")
            
        if not target:
            raise ValueError("Please specify a target directory")
            
        if source_type == "folder":
            if not os.path.isdir(source):
                raise ValueError(f"Source folder does not exist: {source}")
        elif source_type == "zip":
            if not os.path.isfile(source):
                raise ValueError(f"ZIP file does not exist: {source}")
            if not zipfile.is_zipfile(source):
                raise ValueError(f"Invalid ZIP file: {source}")
        elif source_type == "url":
            if not source.startswith(("http://", "https://", "git@")):
                raise ValueError("Invalid Git URL format")

        ssh_key = self.ssh_key_path.get().strip()
        if ssh_key and not os.path.isfile(ssh_key):
            raise ValueError(f"SSH key file does not exist: {ssh_key}")
                
        return True
        
    def start_setup(self):
        """Start the setup process in a separate thread."""
        if self.is_processing:
            messagebox.showwarning("Processing", "Setup is already in progress")
            return
            
        try:
            self.validate_inputs()
        except ValueError as e:
            messagebox.showerror("Validation Error", str(e))
            return
            
        self.is_processing = True
        self.start_button.config(state=tk.DISABLED)
        self.progress_bar.start(10)
        self.clear_log()
        
        # Run setup in separate thread to keep UI responsive
        thread = threading.Thread(target=self.run_setup, daemon=True)
        thread.start()
        
    def run_setup(self):
        """Execute the setup process."""
        try:
            self.log_message("Starting repository setup...")
            
            source_type = self.source_type.get()
            source = self.source_path.get().strip()
            target = self.target_path.get().strip()
            
            # Create target directory
            target_dir = Path(target)
            target_dir.mkdir(parents=True, exist_ok=True)
            self.log_message(f"Target directory: {target_dir}")
            
            # Process based on source type
            if source_type == "folder":
                repo_path = self.setup_from_folder(source, target_dir)
            elif source_type == "zip":
                repo_path = self.setup_from_zip(source, target_dir)
            elif source_type == "url":
                repo_path = self.setup_from_url(source, target_dir)
            else:
                raise ValueError(f"Unknown source type: {source_type}")
                
            self.log_message(f"Repository extracted to: {repo_path}")
            
            # Auto-install dependencies if enabled
            if self.auto_install.get():
                self.install_dependencies(repo_path)

            if self.add_ci_templates.get():
                self.add_ci_template(repo_path)

            if self.run_post_setup.get():
                self.run_post_setup_steps(repo_path)

            if self.run_post_setup_checks.get():
                self.run_quick_checks(repo_path)

            if self.enable_docker_build.get() or self.enable_docker_run.get():
                self.handle_docker(repo_path)
                
            success_message = "Setup completed successfully!"
            self.log_message(success_message, "SUCCESS")
            self.root.after(0, lambda: messagebox.showinfo(
                "Success",
                f"Repository setup completed!\n\nLocation: {repo_path}"
            ))
            
        except Exception as e:
            error_msg = self.format_error_message(e)
            self.log_message(error_msg, "ERROR")
            self.logger.exception("Setup failed")
            self.root.after(0, lambda: messagebox.showerror("Error", error_msg))
            
        finally:
            self.is_processing = False
            self.root.after(0, self.finish_setup)
            
    def setup_from_folder(self, source, target_dir):
        """Setup repository from a local folder."""
        self.log_message(f"Copying from folder: {source}")
        
        source_path = Path(source)
        repo_name = source_path.name
        dest_path = target_dir / repo_name
        
        # Check if destination exists
        if dest_path.exists():
            counter = 1
            while (target_dir / f"{repo_name}_{counter}").exists():
                counter += 1
            dest_path = target_dir / f"{repo_name}_{counter}"
            
        # Copy directory
        shutil.copytree(source_path, dest_path, symlinks=True)
        self.log_message(f"Copied {self.count_files(dest_path)} files")
        
        return dest_path
        
    def setup_from_zip(self, source, target_dir):
        """Setup repository from a ZIP file."""
        self.log_message(f"Extracting ZIP file: {source}")
        
        zip_path = Path(source)
        repo_name = zip_path.stem
        dest_path = target_dir / repo_name
        
        # Check if destination exists
        if dest_path.exists():
            counter = 1
            while (target_dir / f"{repo_name}_{counter}").exists():
                counter += 1
            dest_path = target_dir / f"{repo_name}_{counter}"
            
        # Extract ZIP
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(dest_path)
            
        self.log_message(f"Extracted {self.count_files(dest_path)} files")
        
        # Handle single root folder in ZIP
        items = list(dest_path.iterdir())
        if len(items) == 1 and items[0].is_dir():
            temp_dir = dest_path.parent / f"temp_{repo_name}"
            items[0].rename(temp_dir)
            dest_path.rmdir()
            temp_dir.rename(dest_path)
            
        return dest_path
        
    def setup_from_url(self, url, target_dir):
        """Setup repository from a Git URL."""
        oauth_token = self.oauth_token.get().strip()
        self.log_message(f"Cloning from URL: {self.sanitize_url(url, oauth_token)}")
        
        # Check if git is available
        if not self.check_command("git"):
            raise RuntimeError("Git is not installed or not in PATH")
            
        # Extract repository name from URL
        parsed = urlparse(url)
        repo_name = Path(parsed.path).stem.replace('.git', '')
        
        if not repo_name and ":" in url:
            repo_name = Path(url.split(":")[-1]).stem.replace('.git', '')
        
        if not repo_name:
            repo_name = "repository"
            
        dest_path = target_dir / repo_name
        
        # Check if destination exists
        if dest_path.exists():
            counter = 1
            while (target_dir / f"{repo_name}_{counter}").exists():
                counter += 1
            dest_path = target_dir / f"{repo_name}_{counter}"
            
        # Clone repository
        env = os.environ.copy()
        ssh_key = self.ssh_key_path.get().strip()
        if ssh_key:
            env["GIT_SSH_COMMAND"] = f"ssh -i {ssh_key} -o IdentitiesOnly=yes"
            
        clone_url = url
        if oauth_token:
            if url.startswith(("http://", "https://")):
                clone_url = self.inject_oauth_token(url, oauth_token)
            else:
                self.log_message("OAuth token provided for non-HTTP URL; ignoring token", "WARNING")
        
        git_cmd = ["git"]
        credential_helper = self.git_credential_helper.get().strip()
        if credential_helper:
            git_cmd.extend(["-c", f"credential.helper={credential_helper}"])
        
        try:
            result = subprocess.run(
                git_cmd + ["clone", clone_url, str(dest_path)],
                capture_output=True,
                text=True,
                timeout=300,
                check=True,
                env=env
            )
            self.log_message("Clone completed successfully")
            if result.stdout:
                self.log_message(self.sanitize_text(result.stdout.strip()))
                
        except subprocess.TimeoutExpired:
            raise RuntimeError("Git clone timed out (5 minutes)")
        except subprocess.CalledProcessError as e:
            error_output = self.sanitize_text(e.stderr or "")
            raise RuntimeError(f"Git clone failed: {error_output or 'Unknown error'}")
            
        return dest_path
        
    def install_dependencies(self, repo_path):
        """Automatically detect and install dependencies."""
        self.log_message("Checking for dependencies...")
        
        repo_path = Path(repo_path)
        installed_any = False
        project_paths = self.detect_project_paths(repo_path)
        if len(project_paths) > 1:
            self.log_message(f"Detected monorepo with {len(project_paths)} projects")
        
        for project_path in project_paths:
            if project_path != repo_path:
                self.log_message(f"Installing dependencies in {project_path}")
            if self.install_dependencies_for_project(project_path):
                installed_any = True
                
        if not installed_any:
            self.log_message("No dependency files found or no package managers available")

    def detect_project_paths(self, repo_path):
        """Detect project roots for monorepos."""
        dependency_files = {
            "requirements.txt",
            "setup.py",
            "pyproject.toml",
            "Pipfile",
            "package.json",
            "Gemfile",
            "go.mod",
            "pom.xml",
            "build.gradle",
            "build.gradle.kts",
            "Cargo.toml",
        }
        skip_dirs = {
            ".git",
            ".hg",
            ".svn",
            "node_modules",
            ".venv",
            "venv",
            "__pycache__",
            "dist",
            "build",
            ".tox",
        }
        project_paths = set()
        repo_path = Path(repo_path)
        max_depth = 4
        
        for root, dirs, files in os.walk(repo_path):
            rel = Path(root).relative_to(repo_path)
            if len(rel.parts) > max_depth:
                dirs[:] = []
                continue
            dirs[:] = [d for d in dirs if d not in skip_dirs]
            if any(name in files for name in dependency_files):
                project_paths.add(Path(root))
                
        if not project_paths:
            project_paths.add(repo_path)
            
        return sorted(project_paths)
        
    def install_dependencies_for_project(self, project_path):
        """Install dependencies for a single project path."""
        installed_any = False
        project_path = Path(project_path)
        python_env = self.build_python_tool_env()
        
        requirements_file = project_path / "requirements.txt"
        pipfile = project_path / "Pipfile"
        pyproject = project_path / "pyproject.toml"
        setup_py = project_path / "setup.py"
        
        if pipfile.exists():
            self.log_message("Found Pipfile")
            if self.check_command("pipenv"):
                try:
                    self.run_command(["pipenv", "install"], cwd=project_path, env=python_env)
                    installed_any = True
                except Exception as e:
                    self.log_message(f"Failed to install Pipenv dependencies: {e}", "WARNING")
            else:
                self.log_message("pipenv is not available. Install with `pip install pipenv`.", "WARNING")
        
        if pyproject.exists() and self.is_poetry_project(pyproject):
            self.log_message("Found Poetry pyproject.toml")
            if self.check_command("poetry"):
                try:
                    self.run_command(["poetry", "install"], cwd=project_path, env=python_env)
                    installed_any = True
                except Exception as e:
                    self.log_message(f"Failed to install Poetry dependencies: {e}", "WARNING")
            else:
                self.log_message("poetry is not available. Install with `pip install poetry`.", "WARNING")
        
        if requirements_file.exists():
            self.log_message("Found requirements.txt")
            pip_cmd = self.resolve_pip_command(project_path)
            if pip_cmd:
                try:
                    self.run_command(
                        pip_cmd + ["install", "-r", "requirements.txt"],
                        cwd=project_path
                    )
                    installed_any = True
                except Exception as e:
                    self.log_message(f"Failed to install Python dependencies: {e}", "WARNING")
            else:
                self.log_message("pip is not available. Install Python/pip to continue.", "WARNING")
                
        elif setup_py.exists() or (pyproject.exists() and not self.is_poetry_project(pyproject)):
            self.log_message("Found Python project metadata")
            pip_cmd = self.resolve_pip_command(project_path)
            if pip_cmd:
                try:
                    self.run_command(pip_cmd + ["install", "."], cwd=project_path)
                    installed_any = True
                except Exception as e:
                    self.log_message(f"Failed to install Python package: {e}", "WARNING")
            else:
                self.log_message("pip is not available. Install Python/pip to continue.", "WARNING")
                    
        if (project_path / "package.json").exists():
            self.log_message("Found package.json")
            if self.check_command("npm"):
                try:
                    self.run_command(["npm", "install"], cwd=project_path)
                    installed_any = True
                except Exception as e:
                    self.log_message(f"Failed to install Node.js dependencies: {e}", "WARNING")
            else:
                self.log_message("npm is not available. Install Node.js to continue.", "WARNING")
                    
        if (project_path / "Gemfile").exists():
            self.log_message("Found Gemfile")
            if self.check_command("bundle"):
                try:
                    self.run_command(["bundle", "install"], cwd=project_path)
                    installed_any = True
                except Exception as e:
                    self.log_message(f"Failed to install Ruby dependencies: {e}", "WARNING")
            else:
                self.log_message("bundle is not available. Install Ruby bundler to continue.", "WARNING")
                    
        if (project_path / "go.mod").exists():
            self.log_message("Found go.mod")
            if self.check_command("go"):
                try:
                    self.run_command(["go", "mod", "download"], cwd=project_path)
                    installed_any = True
                except Exception as e:
                    self.log_message(f"Failed to install Go dependencies: {e}", "WARNING")
            else:
                self.log_message("go is not available. Install Go to continue.", "WARNING")
                    
        if (project_path / "Cargo.toml").exists():
            self.log_message("Found Cargo.toml")
            if self.check_command("cargo"):
                try:
                    self.run_command(["cargo", "fetch"], cwd=project_path)
                    installed_any = True
                except Exception as e:
                    self.log_message(f"Failed to fetch Cargo dependencies: {e}", "WARNING")
            else:
                self.log_message("cargo is not available. Install Rust to continue.", "WARNING")
                    
        if (project_path / "pom.xml").exists():
            self.log_message("Found pom.xml")
            if self.check_command("mvn"):
                try:
                    self.run_command(["mvn", "-q", "-DskipTests", "dependency:resolve"], cwd=project_path)
                    installed_any = True
                except Exception as e:
                    self.log_message(f"Failed to resolve Maven dependencies: {e}", "WARNING")
            else:
                self.log_message("mvn is not available. Install Maven to continue.", "WARNING")
                    
        if (project_path / "build.gradle").exists() or (project_path / "build.gradle.kts").exists():
            self.log_message("Found Gradle build file")
            gradle_cmd = self.get_gradle_command(project_path)
            if gradle_cmd:
                try:
                    self.run_command(gradle_cmd, cwd=project_path)
                    installed_any = True
                except Exception as e:
                    self.log_message(f"Failed to resolve Gradle dependencies: {e}", "WARNING")
            else:
                self.log_message("Gradle is not available. Install Gradle to continue.", "WARNING")
                
        return installed_any
        
    def build_python_tool_env(self):
        """Build environment variables for Python tooling."""
        env = os.environ.copy()
        if self.use_venv.get():
            env["PIPENV_VENV_IN_PROJECT"] = "1"
            env["POETRY_VIRTUALENVS_IN_PROJECT"] = "1"
        return env
        
    def is_poetry_project(self, pyproject_path):
        """Determine if pyproject.toml belongs to Poetry."""
        try:
            content = Path(pyproject_path).read_text(encoding="utf-8", errors="ignore")
        except OSError:
            return False
        return "[tool.poetry]" in content
        
    def resolve_pip_command(self, project_path):
        """Resolve the pip command, optionally using a venv."""
        if not self.check_command("pip") and not self.use_venv.get():
            return None
        
        if not self.use_venv.get():
            return ["pip"]
        
        try:
            venv_path = self.ensure_venv(project_path)
        except Exception as e:
            self.log_message(f"Failed to create virtual environment: {e}", "WARNING")
            return ["pip"] if self.check_command("pip") else None
        
        pip_path = self.get_venv_pip(venv_path)
        if pip_path.exists():
            return [str(pip_path)]
        
        return ["pip"] if self.check_command("pip") else None
        
    def ensure_venv(self, project_path):
        """Create a virtual environment if needed."""
        venv_path = Path(project_path) / ".venv"
        if not venv_path.exists():
            self.log_message(f"Creating virtual environment in {venv_path}")
            self.run_command([sys.executable, "-m", "venv", str(venv_path)], cwd=project_path)
        return venv_path
        
    def get_venv_pip(self, venv_path):
        """Get the pip path inside a virtual environment."""
        if os.name == "nt":
            return Path(venv_path) / "Scripts" / "pip.exe"
        return Path(venv_path) / "bin" / "pip"
        
    def get_gradle_command(self, project_path):
        """Return the Gradle command to run for dependency resolution."""
        gradlew = Path(project_path) / "gradlew"
        if gradlew.exists():
            return ["./gradlew", "--no-daemon", "dependencies"]
        gradlew_bat = Path(project_path) / "gradlew.bat"
        if gradlew_bat.exists():
            return ["gradlew.bat", "--no-daemon", "dependencies"]
        if self.check_command("gradle"):
            return ["gradle", "--no-daemon", "dependencies"]
        return None

    def add_ci_template(self, repo_path):
        """Add a minimal CI workflow template if none exists."""
        try:
            repo_path = Path(repo_path)
            workflow_dir = repo_path / ".github" / "workflows"
            workflow_dir.mkdir(parents=True, exist_ok=True)
            workflow_file = workflow_dir / "repo-setup-checks.yml"
            
            if workflow_file.exists():
                self.log_message("CI workflow template already exists")
                return
            
            template = """name: Repo Setup Checks
on:
  push:
  workflow_dispatch:

jobs:
  setup-checks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Repo summary
        run: |
          echo "Repository setup checks"
          ls -la
      - name: Python check
        if: hashFiles('requirements.txt', 'pyproject.toml', 'setup.py', 'Pipfile') != ''
        run: python3 --version
      - name: Node check
        if: hashFiles('package.json') != ''
        run: node --version
      - name: Go check
        if: hashFiles('go.mod') != ''
        run: go version
      - name: Rust check
        if: hashFiles('Cargo.toml') != ''
        run: cargo --version
      - name: Java check
        if: hashFiles('pom.xml', 'build.gradle', 'build.gradle.kts') != ''
        run: java -version
"""
            workflow_file.write_text(template, encoding="utf-8")
            self.log_message(f"Added CI workflow template: {workflow_file}")
        except Exception as e:
            self.log_message(f"Failed to add CI workflow template: {e}", "WARNING")
        
    def run_post_setup_steps(self, repo_path):
        """Run post-setup scripts or recipes if present."""
        repo_path = Path(repo_path)
        self.log_message("Checking for post-setup scripts or recipes...")
        scripts = [
            repo_path / ".repo_setup_wizard" / "post_setup.sh",
            repo_path / ".repo_setup_wizard" / "post_setup.py",
            repo_path / "post_setup.sh",
            repo_path / "post_setup.py",
        ]
        recipes = [
            repo_path / ".repo_setup_wizard.json",
            repo_path / ".repo_setup_wizard" / "recipe.json",
        ]
        ran_any = False
        
        for script in scripts:
            if script.exists():
                try:
                    ran_any = True
                    if script.suffix == ".sh":
                        if self.check_command("bash"):
                            self.run_command(["bash", str(script)], cwd=repo_path)
                        else:
                            self.log_message("bash is not available to run post_setup.sh", "WARNING")
                    elif script.suffix == ".py":
                        self.run_command([sys.executable, str(script)], cwd=repo_path)
                except Exception as e:
                    self.log_message(f"Post-setup script failed: {e}", "WARNING")
        
        for recipe in recipes:
            if recipe.exists():
                try:
                    ran_any = True
                    recipe_data = json.loads(recipe.read_text(encoding="utf-8"))
                    commands = recipe_data.get("commands", [])
                    working_dir = recipe_data.get("working_dir", ".")
                    recipe_cwd = repo_path / working_dir
                    for command in commands:
                        cmd_list = None
                        if isinstance(command, str):
                            cmd_list = shlex.split(command)
                        elif isinstance(command, list):
                            cmd_list = [str(part) for part in command]
                        if cmd_list:
                            self.run_command(cmd_list, cwd=recipe_cwd)
                except Exception as e:
                    self.log_message(f"Post-setup recipe failed: {e}", "WARNING")
        
        if not ran_any:
            self.log_message("No post-setup scripts or recipes found")
            
    def run_quick_checks(self, repo_path):
        """Run lightweight post-setup checks."""
        repo_path = Path(repo_path)
        self.log_message("Running quick post-setup checks...")
        if (repo_path / ".git").exists() and self.check_command("git"):
            try:
                self.run_command(["git", "status", "-sb"], cwd=repo_path)
            except Exception as e:
                self.log_message(f"Git status check failed: {e}", "WARNING")
        self.log_message("Post-setup checks completed")
        
    def handle_docker(self, repo_path):
        """Build and optionally run Docker images when Dockerfiles are detected."""
        repo_path = Path(repo_path)
        docker_contexts = self.find_docker_contexts(repo_path)
        if not docker_contexts:
            self.log_message("No Dockerfiles detected")
            return
        
        if not self.check_command("docker"):
            self.log_message("docker is not available. Install Docker to continue.", "WARNING")
            return
        
        for context in docker_contexts:
            tag_base = f"{repo_path.name}-{context.name}" if context != repo_path else repo_path.name
            tag = re.sub(r"[^0-9A-Za-z_.-]", "-", tag_base).lower()
            try:
                if self.enable_docker_build.get() or self.enable_docker_run.get():
                    self.log_message(f"Building Docker image for {context}")
                    self.run_command(["docker", "build", "-t", tag, str(context)], cwd=repo_path)
                if self.enable_docker_run.get():
                    self.log_message(f"Running Docker image {tag}")
                    self.run_command(["docker", "run", "--rm", tag], cwd=repo_path)
            except Exception as e:
                self.log_message(f"Docker operation failed: {e}", "WARNING")
        
    def find_docker_contexts(self, repo_path):
        """Find Dockerfile contexts within the repository."""
        docker_contexts = []
        skip_dirs = {".git", "node_modules", ".venv", "venv", "__pycache__", "dist", "build"}
        repo_path = Path(repo_path)
        max_depth = 4
        
        for root, dirs, files in os.walk(repo_path):
            rel = Path(root).relative_to(repo_path)
            if len(rel.parts) > max_depth:
                dirs[:] = []
                continue
            dirs[:] = [d for d in dirs if d not in skip_dirs]
            if "Dockerfile" in files:
                docker_contexts.append(Path(root))
                
        return docker_contexts
        
    def sanitize_url(self, url, oauth_token):
        """Sanitize URLs to avoid leaking tokens."""
        sanitized = url
        if oauth_token:
            sanitized = sanitized.replace(oauth_token, "***")
        parsed = urlparse(sanitized)
        if parsed.username:
            hostname = parsed.hostname or ""
            if parsed.port:
                hostname = f"{hostname}:{parsed.port}"
            sanitized = parsed._replace(netloc=hostname).geturl()
        return sanitized
        
    def inject_oauth_token(self, url, oauth_token):
        """Insert OAuth token into HTTPS URL."""
        parsed = urlparse(url)
        if parsed.username:
            return url
        encoded = quote(oauth_token, safe="")
        netloc = parsed.netloc
        return parsed._replace(netloc=f"{encoded}@{netloc}").geturl()
        
    def sanitize_text(self, text):
        """Sanitize output for secrets."""
        token = self.oauth_token.get().strip()
        if token:
            return text.replace(token, "***")
        return text
        
    def format_error_message(self, error):
        """Format errors with guided remediation steps."""
        raw_message = self.sanitize_text(str(error))
        message = f"Setup failed: {raw_message}"
        hints = []
        lower_msg = raw_message.lower()
        
        if "git is not installed" in lower_msg:
            hints.append("Install Git from https://git-scm.com/downloads")
        if "authentication" in lower_msg or "permission denied" in lower_msg or "could not read" in lower_msg:
            hints.append("Provide an OAuth token or SSH key in the Git Authentication section")
        if "pip" in lower_msg and "not available" in lower_msg:
            hints.append("Install Python and pip, then re-run setup")
        if "docker" in lower_msg and "not available" in lower_msg:
            hints.append("Install Docker Desktop or the Docker Engine")
        if "timeout" in lower_msg:
            hints.append("Check network connectivity and try again")
            
        if hints:
            message += "\n\nGuided remediation:\n" + "\n".join(f"- {hint}" for hint in hints)
            
        return message
            
    def check_command(self, command):
        """Check if a command is available in PATH."""
        return shutil.which(command) is not None
        
    def run_command(self, cmd, cwd=None, env=None):
        """Run a command and log output."""
        self.log_message(f"Running: {' '.join(cmd)}")
        
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=600,
            env=env
        )
        
        if result.stdout:
            for line in result.stdout.strip().split('\n'):
                if line.strip():
                    self.log_message(self.sanitize_text(line.strip()))
                    
        if result.returncode != 0:
            error_msg = result.stderr.strip() if result.stderr else f"Command failed with exit code {result.returncode}"
            raise RuntimeError(self.sanitize_text(error_msg))
            
    def count_files(self, path):
        """Count files in a directory recursively."""
        return sum(1 for _ in Path(path).rglob('*') if _.is_file())
        
    def finish_setup(self):
        """Cleanup after setup completes."""
        self.progress_bar.stop()
        self.start_button.config(state=tk.NORMAL)
        
    def exit_application(self):
        """Exit the application safely."""
        if self.is_processing:
            if not messagebox.askyesno(
                "Confirm Exit",
                "Setup is in progress. Are you sure you want to exit?"
            ):
                return
                
        self.logger.info("Application closed")
        self.root.quit()


def main():
    """Main entry point for the application."""
    try:
        root = tk.Tk()
        
        # Apply modern theme
        style = ttk.Style()
        available_themes = style.theme_names()
        
        # Use best available theme
        if 'clam' in available_themes:
            style.theme_use('clam')
        elif 'alt' in available_themes:
            style.theme_use('alt')
            
        # Configure accent button style
        style.configure(
            'Accent.TButton',
            font=('Helvetica', 10, 'bold')
        )
        
        app = SetupWizard(root)
        root.protocol("WM_DELETE_WINDOW", app.exit_application)
        root.mainloop()
        
    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"Fatal error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
